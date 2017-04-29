from flask import Flask, render_template, request, redirect, url_for
import os, zipfile, cv2
import numpy as np
from PIL import Image
from uniqueID import UniqueID
import fnmatch, face_checker
from database import Database 
import pickle, json
from openCVObject import OpenCVObject

app = Flask(__name__)

# TODO config locations should be from seperate config files

app.config['ALLOWED_EXTENSIONS'] = ["png", 'jpg', 'jpeg']
app.config['ALLOWED_TRAIN_FILE_EXTENSIONS'] = ["zip"]


@app.route('/validate_user')
def validate_user_form():
    return render_template('validate_user.html')


@app.route('/validator', methods=['POST'])
def validate_user():
    if 'file' not in request.files:
        return 'No File Selected !'

    file = request.files['file']
    predict_image_pil = Image.open(file).convert('L')
    predict_image = np.array(predict_image_pil, 'uint8')
    nbr_predicted, conf = OpenCVObject.predictFace(predict_image)
    return Database.getRegistrationInfo(nbr_predicted)
    

@app.route('/train_model', methods=['POST'])
def train_model():
    images,labels = Database.getListofImagesWithID()
    OpenCVObject.performTraining(images,labels)
    return "Done"

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
    nbr = UniqueID.getUniqueID()
    
    checks = face_checker.Face_Checker()

    if file and allowed_Training_file(file.filename):

        if checks.verify_faces_in_zipFile(file):
            OpenCVObject.uploadPhotos(file, nbr)
        else:
            return "Invalid File !"
    else:
        return "Invalid File ! Please upload image with only one person."

    OpenCVObject.uploadRegistrationInfo(request, nbr)
    return "Done"


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
            faces = OpenCVObject.faceCascade.detectMultiScale(image)
            
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



