from pymongo import MongoClient
from json import dumps
import json
import pickle


class Database:
    client = MongoClient("mongodb://127.0.0.1:27017/faceDetection")
    db = client.get_default_database()

    @staticmethod
    def storeUniqueID(id):
        bulk = Database.db.General_Entry.update(
            {"Key": "UniqueKey"},
            {"$set": {"id": id}},
            upsert=True
        )

    @staticmethod
    def getUniqueID():
        try:
            d = Database.db.General_Entry.find({"Key": "UniqueKey"}, {"_id": 0})
            id = dumps(list(d))
            p = json.loads(id)
            return p[0]["id"]
        except:
            return 0

    @staticmethod
    def storeImagesWithID(images):
        bulk = Database.db.Image_With_ID.insert_many(images)
        return Database.db.Image_With_ID.count()

    @staticmethod
    def getListofImagesWithID():
        d = Database.db.Image_With_ID.find({}, {"_id": 0})
        images = dumps(list(d))
        pp = json.loads(images)
        images = []
        labels = []
        for p in pp:
            images.append(pickle.loads(p["image"]))
            labels.append(p["ID"])
        print
        images
        print
        labels
        return (images, labels)

    @staticmethod
    def storeRegistrationInfo(request, nbr):

        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        phone = request.form['phone']

        info = {"ID": nbr, "name": name, "age": age, "city": city, "state": state, "zip": zip, "phone": phone}

        Database.db.RegistrationInfo.update(
            {"ID": nbr},
            {"$set": info},
            upsert=True
        )

    @staticmethod
    def getRegistrationInfo(nbr):
        data = Database.db.RegistrationInfo.find(
            {"ID": nbr}, {"_id": 0})
        return dumps(list(data))
