from pymongo import MongoClient
from json import dumps

class Database:

    client = MongoClient("mongodb://127.0.0.1:27017/faceDetection")
    db = client.get_default_database()

    @staticmethod
    def storeImagesWithID(images):
        bulk = Database.db.Image_With_ID.insert_many(images)
        return Database.db.Image_With_ID.count()
        
    @staticmethod
    def readImagesWithID():
        d = Database.db.Image_With_ID.find({},{"_id":0})
        return dumps(list(d))
        