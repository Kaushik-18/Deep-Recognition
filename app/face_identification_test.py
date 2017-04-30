import face_recognition

client_image = face_recognition.load_image_file("/home/sunil/Pictures/b.jpg")
test_image = face_recognition.load_image_file("/home/sunil/Pictures/g1.jpg")
client_face_loc = face_recognition.face_locations(client_image)
test_face_loc = face_recognition.face_locations(test_image)

print("found {} face(s) in client photograph.".format(len(client_face_loc)))
print("found {} face(s) in test photograph.".format(len(test_face_loc)))


# assuming that there is only one face in each image

client_image_encoding = face_recognition.face_encodings(client_image)[0]
test_image_encoding = face_recognition.face_encodings(test_image)[0]

result = face_recognition.compare_faces([client_image_encoding],test_image_encoding)

print("Does this face match ? ",result)
