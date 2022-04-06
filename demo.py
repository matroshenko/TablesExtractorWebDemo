import base64
import io

from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import SubmitField

from pdf2image import convert_from_bytes

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
        page_images = convert_from_bytes(
            pdf_data.read(), dpi=72, fmt='jpeg')
        assert len(page_images) == 1
        buffered = io.BytesIO()
        page_images[0].save(buffered, format="JPEG")
        image_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return render_template('upload.html', form=form, image_str=image_str)


if __name__ == '__main__':
    manager.run()