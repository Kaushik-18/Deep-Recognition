import cv2, os, zipfile
import numpy as np
from database import Database
import numpy as np
import fnmatch
from PIL import Image
import pickle, json

class OpenCVObject:
    
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    UPLOAD_FOLDER = "/tmp/home/Database/"

    # For face recognition we will the the LBPH Face Recognizer 
    recognizer = cv2.createLBPHFaceRecognizer()

    @staticmethod
    def detectMultiScale(image):
        faces = OpenCVObject.faceCascade.detectMultiScale(image)
        return faces

    @staticmethod
    def performTraining(images, labels):
        OpenCVObject.recognizer.train(images, np.array(labels))
    
    @staticmethod
    def predictFace(predict_image):
        
        faces = OpenCVObject.faceCascade.detectMultiScale(predict_image)
        for (x, y, w, h) in faces:
            nbr_predicted, conf = OpenCVObject.recognizer.predict(predict_image[y: y + h, x: x + w])
            return nbr_predicted, conf


    @staticmethod
    def uploadPhotos(file, nbr):
        imageData = []
        file_path = os.path.join(OpenCVObject.UPLOAD_FOLDER, str(nbr))
        os.makedirs(file_path)

        with zipfile.ZipFile(file) as zf:
            zf.extractall(os.path.join(file_path))     

        image_paths = []
        for root, dirnames, filenames in os.walk(file_path):
            for filename in fnmatch.filter(filenames, '*.jpg'):
                image_paths.append(os.path.join(root, filename))

        for image_path in image_paths:            
            # Read the image and convert to grayscale
            image_pil = Image.open(image_path).convert('L')
            # Convert the image format into numpy array
            image = np.array(image_pil, 'uint8')           
            
            # Detect the face in the image
            faces = OpenCVObject.faceCascade.detectMultiScale(image)
            
            # If face is detected, append the face to images and the label to labels
            for (x, y, w, h) in faces:

                imageData.append({"image": pickle.dumps(image[y: y + h, x: x + w]), "ID": nbr})    

        #print imageData
        Database.storeImagesWithID(imageData)

    @staticmethod
    def uploadRegistrationInfo(request, nbr):
        Database.storeRegistrationInfo(request, nbr)