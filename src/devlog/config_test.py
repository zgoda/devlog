from uuid import uuid4

__uuid = str(uuid4())

TESTING = True
BABEL_DEFAULT_LOCALE = 'en_US'
CSRF_ENABLED = False
WTF_CSRF_ENABLED = CSRF_ENABLED
LOGIN_DISABLED = False
SQLALCHEMY_DATABASE_URI = 'sqlite://'
REDIS_URL = 'redis://'
SECRET_KEY = __uuid
SENTRY_PUBKEY = __uuid
SENTRY_PROJECT = __uuid
