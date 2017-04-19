from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from celery import Celery

app = Flask(__name__)


@app.route('/register_user')
def user_registration():
    return render_template('register_user.html')


@app.route('/validate_user')
def validate_user():
    return ''


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run()
