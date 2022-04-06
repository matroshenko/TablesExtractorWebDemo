import base64
import io
import xml.etree.ElementTree as ET

from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import SubmitField

import fitz

from tables_extractor.tables_extractor import TablesExtractor
from tables_extractor.page_objects_creator import PageObjectsCreator
from tables_extractor.table_to_html_exporter import TableToHTMLExporter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)


class UploadForm(FlaskForm):
    pdf_file = FileField('Pdf file', [FileRequired(), FileAllowed(['pdf'], 'Only pdf files are allowed.')])
    submit = SubmitField('Upload')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


def process_file_data(data):
    page_objects_list = PageObjectsCreator().create_from_bytes(data)
    result = []
    for page_objects in page_objects_list:
        page_image = page_objects.page_image
        page_data = io.BytesIO()
        page_image.save(page_data, format='JPEG')
        page_image_str = base64.b64encode(page_data.getvalue()).decode('utf-8')

        tables_extractor = TablesExtractor(page_objects)
        tables = tables_extractor.extract()
        root = ET.Element('div')
        for table in tables:
            exporter = TableToHTMLExporter(table.cells, css_class="table table-striped")
            root.append(exporter.export())
        tables_str = ET.tostring(root, encoding='unicode', method='html')
        
        result.append((page_image_str, tables_str))
    
    return result


@app.route('/', methods=['GET', 'POST'])
def upload():
    processing_result_data = None
    form = UploadForm()
    if form.validate_on_submit():
        pdf_data = form.pdf_file.data
        processing_result_data = process_file_data(pdf_data.read())

    return render_template('upload.html', form=form, processing_result_data=processing_result_data)


if __name__ == '__main__':
    manager.run()