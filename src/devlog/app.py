import os
from logging.config import dictConfig
from typing import Optional

import rq
import sentry_sdk
from fakeredis import FakeStrictRedis
from flask import render_template
from flask_babel import gettext as _
from redis import Redis
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.utils import ImportStringError

from ._version import get_version
from .auth import auth_bp
from .blog import blog_bp
from .ext import babel, csrf, db, login_manager
from .home import home_bp
from .post import post_bp
from .templates import setup_template_extensions
from .user import user_bp
from .utils.app import Devlog
from .utils.i18n import get_user_language, get_user_timezone


def make_app(env: Optional[str] = None) -> Devlog:
    flask_environment = os.environ.get('FLASK_ENV', '')
    if flask_environment == 'production':
        configure_logging()
        sentry_pubkey = os.environ.get('SENTRY_PUBKEY')
        sentry_project = os.environ.get('SENTRY_PROJECT')
        if all([sentry_pubkey, sentry_project]):
            version = get_version()
            sentry_sdk.init(
                dsn=f'https://{sentry_pubkey}@sentry.io/{sentry_project}',
                release=f'devlog@{version}',
                integrations=[FlaskIntegration()],
            )
    app = Devlog()
    configure_app(app, env)
    configure_rq(app, env)
    configure_extensions(app, env)
    with app.app_context():
        configure_blueprints(app, env)
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
    uploads_dir = os.path.join(app.instance_path, app.config['UPLOAD_DIR_NAME'])
    os.makedirs(uploads_dir, exist_ok=True)


def configure_rq(app: Devlog, env: Optional[str]):
    redis_conn_cls = Redis
    run_async = True
    if app.testing:
        redis_conn_cls = FakeStrictRedis
        run_async = False
    app.redis = redis_conn_cls.from_url(app.config['REDIS_URL'])
    app.queues = {
        'import': rq.Queue('devlog-import', is_async=run_async, connection=app.redis),
        'mail': rq.Queue('devlog-mail', is_async=run_async, connection=app.redis),
    }


def configure_blueprints(app: Devlog, env: Optional[str]):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(post_bp, url_prefix='/post')


def configure_extensions(app: Devlog, env: Optional[str]):
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = _('Please log in to access this page')
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def get_user(userid):
        from .models import User
        return User.query.get(userid)

    if not app.testing:
        @babel.localeselector
        def get_locale():
            return get_user_language()

        @babel.timezoneselector
        def get_timezone():
            return get_user_timezone()

    babel.init_app(app)


def configure_logging():
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi'],
        },
    })


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
