import os

import sentry_sdk
from sentry_sdk.integrations.rq import RqIntegration

if os.environ.get('FLASK_ENV', '').lower() == 'production':
    sentry_pubkey = os.environ.get('SENTRY_PUBKEY')
    sentry_project = os.environ.get('SENTRY_PROJECT')
    sentry_sdk.init(
        dsn=f'https://{sentry_pubkey}@sentry.io/{sentry_project}',
        integrations=[RqIntegration()],
    )
