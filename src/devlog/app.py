import os
from logging.config import dictConfig

from flask import Flask, render_template, request, send_from_directory, session
from flask_babel import gettext as _
from werkzeug.utils import ImportStringError

from .auth import auth_bp
from .blog import blog_bp
from .ext import babel, bootstrap, csrf, db, login_manager, oauth, pages
from .home import home_bp
from .post import post_bp
from .templates import setup_template_extensions
from .user import user_bp
from .utils.text import SUPPORTED_LANGUAGES


def make_app(env=None):
    if os.environ.get('FLASK_ENV', '') != 'development':
        configure_logging()
    app = Flask(__name__.split('.')[0])
    configure_app(app, env)
    configure_extensions(app, env)
    with app.app_context():
        configure_hooks(app, env)
        configure_blueprints(app, env)
        configure_error_handlers(app)
        setup_template_extensions(app)
    return app


def configure_app(app, env):
    app.config.from_object('devlog.config')
    if env is not None:
        try:
            app.config.from_object(f'devlog.config_{env}')
        except ImportStringError:
            app.logger.info(f'no environment config for {env}')
    config_local = os.environ.get('DEVLOG_CONFIG_LOCAL')
    if config_local:
        app.logger.info(f'local configuration loaded from {config_local}')
        app.config.from_envvar('DEVLOG_CONFIG_LOCAL')
    config_secrets = os.environ.get('DEVLOG_CONFIG_SECRETS')
    if config_secrets:
        app.logger.info(f'secrets loaded from {config_secrets}')
        app.config.from_envvar('DEVLOG_CONFIG_SECRETS')
    if app.debug:
        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(
                os.path.join(app.root_path, 'static'),
                'favicon.ico',
                mimetype='image/vnd.microsoft.icon',
            )


def configure_hooks(app, env):
    pass


def configure_blueprints(app, env):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(post_bp, url_prefix='/post')


def configure_extensions(app, env):
    db.init_app(app)
    csrf.init_app(app)
    oauth.init_app(app)
    bootstrap.init_app(app)
    pages.init_app(app)
    pages.get('foo')  # preload all static pages
    login_manager.init_app(app)
    login_manager.login_view = 'auth.select'
    login_manager.login_message = _('Please log in to access this page')
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def get_user(userid):
        from .models import User
        return User.query.get(userid)

    if not app.testing:
        @babel.localeselector
        def get_locale():
            lang = session.get('lang')
            if lang is None:
                lang = request.accept_languages.best_match(SUPPORTED_LANGUAGES)
            return lang

    babel.init_app(app)


def configure_logging():
    dictConfig(
        {
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
            'root': {'level': 'INFO', 'handlers': ['wsgi']},
        }
    )


def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/403.jinja'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.jinja'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.jinja'), 500
