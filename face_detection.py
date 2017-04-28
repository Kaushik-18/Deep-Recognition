from flask import Flask, render_template, request, redirect, url_for
import os
import zipfile
import cv2, os
import numpy as np
from PIL import Image
from uniqueID import UniqueID
import face_checker
import fnmatch
from database import Database 
import pickle
import json

app = Flask(__name__)
# TODO config locations should be from seperate config files
app.config['UPLOAD_FOLDER'] = "/tmp/home/Database/"
app.config['ALLOWED_EXTENSIONS'] = ["png", 'jpg', 'jpeg']
app.config['ALLOWED_TRAIN_FILE_EXTENSIONS'] = ["zip"]

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.createLBPHFaceRecognizer()


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


def getListofImagesWithID():
    images = Database.readImagesWithID()    
    pp = json.loads(images)
    images = []
    labels = []
    for p in pp:
        images.append(pickle.loads(p["image"]))
        labels.append(p[ID])

    return (images,labels)


# TODO send JSON responses ; process files to check for face present
# TODO strategy for uploading multiple image files during registration
# handles user registration and file upload
@app.route('/uploader', methods=['POST'])
def uploader_file():

    if 'file' not in request.files:
        return 'No File Selected !'

    file = request.files['file']
    nbr = UniqueID.getUniqueID()
    imageData = []
    checks = face_checker.Face_Checker()

    if file and allowed_Training_file(file.filename):

        if checks.verify_faces_in_zipFile(file):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(nbr))
            os.makedirs(file_path , 0755)

            with zipfile.ZipFile(file) as zf:
                zf.extractall(os.path.join(file_path))     

            image_paths = []
            for root, dirnames, filenames in os.walk(file_path):
                for filename in fnmatch.filter(filenames, '*.jpg'):
                    image_paths.append(os.path.join(root, filename))   

            print image_paths


            for image_path in image_paths:            
                # Read the image and convert to grayscale
                image_pil = Image.open(image_path).convert('L')
                # Convert the image format into numpy array
                image = np.array(image_pil, 'uint8')           
                
                # Detect the face in the image
                faces = faceCascade.detectMultiScale(image)
                
                # If face is detected, append the face to images and the label to labels
                for (x, y, w, h) in faces:

                    imageData.append({"image": pickle.dumps(image[y: y + h, x: x + w]), "ID": nbr})    

            #print imageData
            Database.storeImagesWithID(imageData)            
            
            return 'File uploaded successfully !'
        else:
            return "Invalid File !"
    else:
        return "Invalid File ! Please upload image with only one person."
    return


@app.route('/uploader/MultipleData', methods=['POST'])
def uploaderMultipleData_file():

    path = request.form['DataPath']
    imageRepo_paths = [os.path.join(path, f) for f in os.listdir(path)]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []

    imageData = []
    for imageRepo_path in imageRepo_paths:
        image_paths = [os.path.join(imageRepo_path, f) for f in os.listdir(imageRepo_path)]

        # Get the label of the image
        nbr = UniqueID.getUniqueID()        

        for image_path in image_paths:            
            # Read the image and convert to grayscale
            image_pil = Image.open(image_path).convert('L')
            # Convert the image format into numpy array
            image = np.array(image_pil, 'uint8')           
             
            # Detect the face in the image
            faces = faceCascade.detectMultiScale(image)
            
            # If face is detected, append the face to images and the label to labels
            for (x, y, w, h) in faces:
                images.append(image[y: y + h, x: x + w])
                labels.append(nbr)

                imageData.append({"image": pickle.dumps(image[y: y + h, x: x + w]), "ID": nbr})
                
    # return the images list and labels list
    print imageData
    Database.storeImagesWithID(imageData)
    return "Done"
    

def allowed_Training_file(file_name):
    return "." in file_name and \
           file_name.rsplit(".", 1)[1] in app.config['ALLOWED_TRAIN_FILE_EXTENSIONS']

def allowed_file(file_name):
    return "." in file_name and \
           file_name.rsplit(".", 1)[1] in app.config['ALLOWED_EXTENSIONS']


if __name__ == '__main__':
    app.run()



