import logging
import os
import tempfile
from typing import Optional

import sentry_sdk
from flask import render_template
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.utils import ImportStringError

from ._version import get_version
from .ext import babel, pages
from .models import db
from .templates import setup_template_extensions
from .utils.app import Devlog


def make_app(env: Optional[str] = None) -> Devlog:
    flask_environment = os.environ.get('FLASK_ENV', '')
    if flask_environment == 'production':
        sentry_pubkey = os.environ.get('SENTRY_PUBKEY')
        sentry_project = os.environ.get('SENTRY_PROJECT')
        if all([sentry_pubkey, sentry_project]):
            version = get_version()
            sentry_sdk.init(
                dsn=f'https://{sentry_pubkey}@sentry.io/{sentry_project}',
                release=f'devlog@{version}',
                integrations=[FlaskIntegration()],
            )
    extra = {}
    instance_path = os.environ.get('INSTANCE_PATH')
    if instance_path is not None:
        extra['instance_path'] = instance_path
    app = Devlog(__name__.split('.')[0], **extra)
    configure_app(app, env)
    with app.app_context():
        configure_logging_handler(app)
        configure_database(app)
        configure_hooks(app)
        configure_extensions(app)
        configure_blueprint(app)
        configure_error_handlers(app)
        setup_template_extensions(app)
    return app


def configure_app(app: Devlog, env: Optional[str]):
    app.config.from_object('devlog.config')
    if env is not None:
        try:
            app.config.from_object(f'devlog.config_{env}')
        except ImportStringError:
            app.logger.info(f'no environment config for {env}')


def configure_database(app: Devlog):
    if app.testing:
        tmp_dir = tempfile.mkdtemp()
        db_name = os.path.join(tmp_dir, 'db.sqlite3')
    else:
        db_name = os.getenv('DB_NAME')
    kw = {
        'pragmas': {
            'journal_mode': 'wal',
            'cache_size': -1 * 64000,
            'foreign_keys': 1,
            'ignore_check_constraints': 0,
        }
    }
    if db_name is None:
        db_name = ':memory:'
        kw = {}
    db.init(db_name, **kw)


def configure_hooks(app: Devlog):

    @app.before_request
    def db_connect():
        db.connect(reuse_if_open=True)

    @app.teardown_request
    def db_close(exc):
        if not db.is_closed():
            db.close()


def configure_extensions(app: Devlog):
    babel.init_app(app)
    pages.init_app(app)


def configure_blueprint(app: Devlog):
    from .views import bp
    app.register_blueprint(bp)


def configure_logging_handler(app: Devlog):
    if app.debug or app.testing:
        return
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def configure_error_handlers(app: Devlog):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html'), 500
