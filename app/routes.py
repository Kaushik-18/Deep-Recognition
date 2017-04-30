from flask import render_template, request, jsonify
from app import app
from app import facechecker
from app import images_worker


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
        pass
    else:
        return


@app.route('/register_user')
def user_registration():
    return render_template('register_user.html')


# handles user registration and file upload
@app.route('/uploader', methods=['POST'])
def uploader_file():
    if 'file' not in request.files:
        return 'No File Selected !'

    file = request.files['file']
    uploader_name = request.form['user_name']
    if file and allowed_file(file.filename, app.config['ALLOWED_TRAIN_FILE_EXTENSIONS']):
        images_worker.upload_encoder_task(uploader_name,file)

    else:
        return "Invalid File ! Please upload image with only one person."


def allowed_file(file_name, extensions):
    return "." in file_name and \
           file_name.rsplit(".", 1)[1] in extensions
