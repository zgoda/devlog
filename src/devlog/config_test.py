from uuid import uuid4

TESTING = True
BABEL_DEFAULT_LOCALE = 'en_US'
CSRF_ENABLED = False
WTF_CSRF_ENABLED = CSRF_ENABLED
LOGIN_DISABLED = False
SQLALCHEMY_DATABASE_URI = 'sqlite://'
REDIS_URL = 'redis://'
SECRET_KEY = str(uuid4())
SENTRY_PUBKEY = str(uuid4())
SENTRY_PROJECT = str(uuid4())
MAILGUN_API_KEY = str(uuid4())
MAILGUN_DOMAIN = str(uuid4())

EMAIL_CONFIRMATION_SALT = str(uuid4())
