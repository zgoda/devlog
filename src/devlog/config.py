import os

DEBUG = False
TESTING = False
DB_NAME = os.environ.get('DB_NAME')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY')
SESSION_COOKIE_HTTPONLY = True

POST_INCOMING_DIR = os.environ.get('POST_INCOMING_DIR', 'incoming')
REDIS_URL = os.environ.get('REDIS_URL')

# babel
BABEL_DEFAULT_TIMEZONE = 'Europe/Warsaw'
