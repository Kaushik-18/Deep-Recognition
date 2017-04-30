class Config:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    ALLOWED_EXTENSIONS = ["png", 'jpg', 'jpeg']
    ALLOWED_TRAIN_FILE_EXTENSIONS = ["zip"]
    MONGO_DB_URL = 'localhost:27017'
    UPLOAD_FOLDER = "/tmp/home/Database/"


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
