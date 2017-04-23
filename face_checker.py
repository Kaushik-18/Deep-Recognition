# create face encodings of uploaded images when we register a new user and save the results
# we could take up to 3 images

import face_recognition
import zipfile
import Deep_Recognition
import os


class Face_Checker:
    # TODO this is only a testing method ; need to add better and more methods

    def decode_compare_face(self, file_to_validate, user_path):
        client_image = face_recognition.load_image_file(user_path)
        test_image = face_recognition.load_image_file(file_to_validate)
        client_face_loc = face_recognition.face_locations(client_image)
        test_face_loc = face_recognition.face_locations(test_image)

        if (len(client_face_loc) != 1):
            return "Invalid   image  in records !"

        if (len(test_face_loc) != 1):
            return "Invalid image for testing !"

        # assuming that there is only one face in each image
        client_image_encoding = face_recognition.face_encodings(client_image)[0]
        test_image_encoding = face_recognition.face_encodings(test_image)[0]
        result = face_recognition.compare_faces([client_image_encoding], test_image_encoding)
        return result[0]

    # check if image has only one face .. reject  image otherwise
    def verify_faces(self, img_file):
        uploaded_image_array = face_recognition.load_image_file(img_file)
        if (len(face_recognition.face_locations(uploaded_image_array)) != 1):
            return False
        else:
            return True

    # generate and save face encoding for given image .
    # Note : function assumes image has already been checked

    def create_face_encodings(self, img_file):
        image_array = face_recognition.load_image_file(img_file)
        image_encoding = face_recognition.face_encodings(image_array)[0]
        return image_encoding

    # TODO save file to database ..maybe MongoDB ?
    def save_face_encoding(self, encoding_array, user_name):
        pass

    def compare_faces(self, test_image_encodings, user_encodings):
        result = face_recognition.compare_faces([user_encodings], test_image_encodings)
        return result[0]
