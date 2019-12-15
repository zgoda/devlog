import os

DEBUG = False
TESTING = False
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
WTF_CSRF_ENABLED = CSRF_ENABLED
MAX_CONTENT_LENGTH = 1024 * 1024  # 1 MB max upload size
REDIS_URL = os.environ.get('REDIS_URL')

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
__mailgun_domain = os.environ.get('MAILGUN_DOMAIN')
__mailgun_api_key = os.environ.get('MAILGUN_API_KEY')
MAILGUN_API_BASE_URL = f'https://api.eu.mailgun.net/v3/{__mailgun_domain}'
MAILGUN_MESSAGES_URL = f'{MAILGUN_API_BASE_URL}/messages'
MAILGUN_AUTH = ('api', __mailgun_api_key)
MAIL_FROM = f'Devlog <devlog@{__mailgun_domain}>'
