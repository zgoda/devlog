import os

from flask.cli import FlaskGroup

from devlog import make_app
from devlog.models import db

_here = os.path.abspath(os.path.dirname(__file__))

os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_RUN_PORT'] = '5000'
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['AUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['DEVLOG_CONFIG_LOCAL'] = os.path.join(_here, 'secrets/config_local.py')
os.environ['DEVLOG_CONFIG_SECRETS'] = os.path.join(_here, 'secrets/secrets.py')
os.environ['DEVLOG_SQLITE_DB_PATH'] = os.path.join(_here, 'db.sqlite3')


def create_app(info):
    return make_app('dev')


cli = FlaskGroup(create_app=create_app)
cli.help = 'This is a management script for the Devlog application.'


@cli.command('initdb', short_help='Initialize missing database objects')
def initdb():
    db.create_all()


@cli.command('cleardb', short_help='Remove all database objects')
def cleardb():
    db.drop_all()


@cli.command('recreatedb', short_help='Recreate all database objects from scratch')
def recreatedb():
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    cli()
