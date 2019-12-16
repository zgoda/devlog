import os

DEBUG = False
TESTING = False
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY')
CSRF_ENABLED = True
WTF_CSRF_ENABLED = CSRF_ENABLED
MAX_CONTENT_LENGTH = 1024 * 1024  # 1 MB max upload size
REDIS_URL = os.environ.get('REDIS_URL')

# babel
BABEL_DEFAULT_LOCALE = 'pl'
BABEL_DEFAULT_TIMEZONE = 'Europe/Warsaw'

# file uploads
ALLOWED_UPLOAD_EXTENSIONS = ('.md', '.gfm', '.markdown')
UPLOAD_DIR_NAME = 'uploads'

# sentry
SENTRY_PUBKEY = os.environ.get('SENTRY_PUBKEY')
SENTRY_PROJECT = os.environ.get('SENTRY_PROJECT')
