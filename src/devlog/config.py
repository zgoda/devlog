import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TESTING = False
SECRET_KEY = 'not so secret'
SQLALCHEMY_DATABASE_URI = 'sqlite://'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
WTF_CSRF_ENABLED = CSRF_ENABLED
CSRF_SESSION_KEY = 'not so secret'
MAX_CONTENT_LENGTH = 1024 * 1024  # 1 MB max upload size

# flatpages
FLATPAGES_EXTENSION = '.html.md'
FLATPAGES_MARKDOWN_EXTENSIONS = []

# babel
BABEL_DEFAULT_LOCALE = 'pl'
BABEL_DEFAULT_TIMEZONE = 'Europe/Warsaw'

# file uploads
ALLOWED_UPLOAD_EXTENSIONS = ['.md', '.gfm', '.markdown']
