import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    MAIL_DEBUG = os.getenv('MAIL_DEBUG')
    MAIL_DEFAULT_SENDER_NAME = os.getenv('MAIL_DEFAULT_SENDER_NAME')
    MAIL_DEFAULT_SENDER_EMAIL = os.getenv('MAIL_DEFAULT_SENDER_EMAIL')
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
