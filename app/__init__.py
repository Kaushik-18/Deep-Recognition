from flask import Flask
from celery import Celery
from config import config, Config
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object(config["default"])
celery = Celery(__name__)
celery.conf.update(app.config)
mongo_client = MongoClient(app.config['MONGO_DB_URL'])
db = mongo_client.FaceDB
user_table = db.UserDataTable

from app import routes
