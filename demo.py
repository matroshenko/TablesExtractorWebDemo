import base64
import io

from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import SubmitField

import fitz

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


@app.route('/', methods=['GET', 'POST'])
def upload():
    image_str = None
    form = UploadForm()
    if form.validate_on_submit():
        pdf_data = form.pdf_file.data
        document = fitz.open(stream=pdf_data.read(), filetype='pdf')
        page_data = document[0].get_pixmap(dpi=72).pil_tobytes(format='JPEG')
        image_str = base64.b64encode(page_data).decode('utf-8')

    return render_template('upload.html', form=form, image_str=image_str)


if __name__ == '__main__':
    manager.run()