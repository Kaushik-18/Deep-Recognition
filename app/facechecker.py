# create face encodings of uploaded images when we register a new user and save the results
# we could take up to 3 images

import face_recognition
from app import user_table


class FaceChecker:
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

    # generate and save face encoding for given image .
    @staticmethod
    def create_face_encodings(img_file):
        image_array = face_recognition.load_image_file(img_file)
        client_face_loc = face_recognition.face_locations(image_array)
        if len(client_face_loc) == 1:
            image_encoding = face_recognition.face_encodings(image_array)[0]
            return image_encoding
        else:
            return []

    @staticmethod
    def compare_faces(test_image_encodings, user_encodings):
        result = face_recognition.compare_faces([user_encodings], test_image_encodings)
        return result[0]

    def verify_faces_in_zipFile(self, img_zipFile):
        # TODO extact files from zip and confirmthat all are pics of same person.
        return True
