import os

DEBUG = False
TESTING = False
DB_NAME = os.getenv('DB_NAME')
SECRET_KEY = os.getenv('SECRET_KEY')

POST_INCOMING_DIR = os.getenv('POST_INCOMING_DIR', 'incoming')
LINK_INCOMING_DIR = os.getenv('LINK_INCOMING_DIR', 'newlinks')

# babel
BABEL_DEFAULT_LOCALE = 'pl_PL'
BABEL_DEFAULT_TIMEZONE = 'Europe/Warsaw'

# flatpages
FLATPAGES_EXTENSION = ['.html.md']
FLATPAGES_MARKDOWN_EXTENSIONS = []

# caching
CACHE_TYPE = os.getenv('CACHE_TYPE', 'flask_caching.backends.RedisCache')
CACHE_DEFAULT_TIMEOUT = 6 * 60 * 60  # 6 hours
CACHE_KEY_PREFIX = 'dvlg:'
CACHE_NO_NULL_WARNING = True
