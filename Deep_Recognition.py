from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from celery import Celery
import face_checker
import zipfile

app = Flask(__name__)
# TODO config locations should be from seperate config files
app.config['UPLOAD_FOLDER'] = "/tmp/home/Database/"
app.config['ALLOWED_EXTENSIONS'] = ["png", 'jpg', 'jpeg']
app.config['ALLOWED_TRAIN_FILE_EXTENSIONS'] = ["zip"]

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/validate_user')
def validate_user_form():
    return render_template('validate_user.html')


@app.route('/validator', methods=['POST'])
def validate_user():
    if 'file' not in request.files:
        return 'No File Selected !'

    file = request.files['file']
    user_name = request.form['user_name']
    if file and allowed_file(file.filename):
        checks = face_checker.Face_Checker()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user_name, user_name + "jpg")
        if os.path.exists(file_path):
            return str(checks.decode_compare_face(file_to_validate=file, user_path=file_path))
        else:
            return "User does not exist !"


@app.route('/register_user')
def user_registration():
    return render_template('register_user.html')

# TODO send JSON responses ; process files to check for face present
# TODO strategy for uploading multiple image files during registration
# handles user registration and file upload
@app.route('/uploader', methods=['POST'])
def uploader_file():
    if 'file' not in request.files:
        return 'No File Selected !'

    file = request.files['file']
    uploader_name = request.form['user_name']
    checks = face_checker.Face_Checker()
    if file and allowed_Training_file(file.filename):

        if checks.verify_faces_in_zipFile(file):

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploader_name)
            os.makedirs(file_path , 0755)

            with zipfile.ZipFile(file) as zf:
                zf.extractall(os.path.join(file_path))            

            return 'File uploaded successfully !'
        else:
            return "Invalid File !"
    else:
        return "Invalid File ! Please upload image with only one person."

def allowed_Training_file(file_name):
    return "." in file_name and \
           file_name.rsplit(".", 1)[1] in app.config['ALLOWED_TRAIN_FILE_EXTENSIONS']

def allowed_file(file_name):
    return "." in file_name and \
           file_name.rsplit(".", 1)[1] in app.config['ALLOWED_EXTENSIONS']


if __name__ == '__main__':
    app.run()
