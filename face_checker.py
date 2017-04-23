# create face encodings of uploaded images when we register a new user and save the results
# we could take up to 3 images

import face_recognition
import zipfile
import Deep_Recognition
import os


class Face_Checker:
    # TODO this is only a testing method ; need to add bettter and more methods

    def decode_compare_face(self, file_to_validate, user_path):
        client_image = face_recognition.load_image_file(os.path.join(user_path, "1.jpg"))
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
