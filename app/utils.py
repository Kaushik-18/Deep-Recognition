from app import user_table
from app import images_worker
import random, string
import os
from flask import jsonify


def allowed_file(file_name, extensions):
    return "." in file_name and \
           file_name.rsplit(".", 1)[1] in extensions


def is_user_record_present(user_name):
    return user_table.find_one({"user_name": user_name})


def start_registration_process(user_name, uploaded_file):
    if not is_user_record_present(user_name):
        # images_worker.upload_encoder_task(user_name, upload_file=uploaded_file)
        os.makedirs('uploads', exist_ok=True)
        paths = os.path.join('uploads', create_random_file() + ".zip")
        uploaded_file.save(paths)
        images_worker.upload_encoder_task.delay(user_name, paths)
    else:
        return jsonify(status="failed", mesaage ="user already registered !")


def start_validation_process(user_name, validation_file):
    if not is_user_record_present(user_name):
        return jsonify(status="fail",error='user name not present in records')
    else:
        return images_worker.validation_task(user_name, validation_file)


def create_random_file():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(5))
