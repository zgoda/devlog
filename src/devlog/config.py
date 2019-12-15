import os

DEBUG = False
TESTING = False
SECRET_KEY = 'not so secret'
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
WTF_CSRF_ENABLED = CSRF_ENABLED
CSRF_SESSION_KEY = 'not so secret'
MAX_CONTENT_LENGTH = 1024 * 1024  # 1 MB max upload size
REDIS_URL = os.environ['REDIS_URL']

# flatpages
FLATPAGES_EXTENSION = '.html.md'
FLATPAGES_MARKDOWN_EXTENSIONS = []

# babel
BABEL_DEFAULT_LOCALE = 'pl'
BABEL_DEFAULT_TIMEZONE = 'Europe/Warsaw'

# file uploads
ALLOWED_UPLOAD_EXTENSIONS = ('.md', '.gfm', '.markdown')
UPLOAD_DIR_NAME = 'uploads'

# emails
CONFIRMATION_TOKEN_MAX_AGE = 86400  # 24 hours
__mailgun_domain = os.environ['MAILGUN_DOMAIN']
__mailgun_api_key = os.environ['MAILGUN_API_KEY']
MAILGUN_API_BASE_URL = f'https://api.eu.mailgun.net/v3/{__mailgun_domain}'
MAILGUN_MESSAGES_URL = f'{MAILGUN_API_BASE_URL}/messages'
MAILGUN_AUTH = ('api', __mailgun_api_key)
MAIL_FROM = f'Devlog <devlog@{__mailgun_domain}>'
