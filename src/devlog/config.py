import os

DEBUG = False
TESTING = False
DB_NAME = os.environ.get('DB_NAME')
SECRET_KEY = os.environ.get('SECRET_KEY')
SESSION_COOKIE_HTTPONLY = True

POST_INCOMING_DIR = os.environ.get('POST_INCOMING_DIR', 'incoming')

# babel
BABEL_DEFAULT_LOCALE = 'pl_PL'
BABEL_DEFAULT_TIMEZONE = 'Europe/Warsaw'

# flatpages
FLATPAGES_EXTENSION = ['.html.md']
FLATPAGES_MARKDOWN_EXTENSIONS = []
