from app import celery, facechecker, user_table
import zipfile
import pickle
from bson.binary import Binary
from sklearn import svm, ensemble
import os
from collections import Counter


@celery.task
def upload_encoder_task(uploader_name, upload_file):
    tmp_zip = zipfile.ZipFile(upload_file)
    complete_array = []
    for filename in tmp_zip.namelist():
        temp_file = tmp_zip.open(filename)
        enc_array = facechecker.FaceChecker.create_face_encodings(img_file=temp_file)
        complete_array.append(enc_array.tolist())

    cp = Binary(pickle.dumps(complete_array, protocol=2))
    user_entry = {"user_name": uploader_name,
                  "image_data": cp}
    user_table.insert_one(user_entry)
    os.remove(upload_file)


def validation_task(uploader_name, validation_image_file):
    validation_encoding = facechecker.FaceChecker.create_face_encodings(validation_image_file)
    if len(validation_encoding) == 0:
        return 'fail', 'invalid image for validation !'
    user_entry = user_table.find_one({"user_name": uploader_name})
    if user_entry is not None:
        encodings = user_entry['image_data']
        encoding_array = pickle.loads(encodings)

        checks_array = [facechecker.FaceChecker.compare_faces(validation_encoding, encoding) for encoding in
                        encoding_array]

        checkval = Counter(checks_array).most_common(1)[0][0]
        if checkval:
            return 'success', "Image match !"
        else:
            return 'fail', "Image does not match records !"

            #
            # # using one shot svm
            # svm_classifier = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
            # svm_classifier.fit(X=encoding_array)
            # prediction = svm_classifier.predict(validation_encoding)
            # distance = svm_classifier.decision_function(validation_encoding)
            # print(distance, prediction[0])
            # if prediction[0] == 1:
            #     return 'success', "Image match !"
            # else:
            #     return 'fail', "Image does not match records !"
