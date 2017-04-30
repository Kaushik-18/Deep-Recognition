from app import celery, facechecker, user_table
import zipfile
import json


@celery.task
def upload_encoder_task(uploader_name, upload_file):
    if user_table.find_one({"user_name": uploader_name}) is None:
        tmp_zip = zipfile.ZipFile(upload_file)
        complete_array = []
        for filename in tmp_zip.namelist():
            temp_file = tmp_zip.open(filename)
            enc_array = facechecker.FaceChecker.create_face_encodings(img_file=temp_file)
            complete_array.append(enc_array)

        cp = json.dump(complete_array)
        user_entry = {"user_name": uploader_name,
                      "image_data": cp}
        user_table.insert_one(user_entry)


@celery.task
def validation_task(uploader_name, validation_image_file):
    if user_table.find_one({"user_name": uploader_name}, filter=None) is None:
        pass
