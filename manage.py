import os

from flask.cli import FlaskGroup

os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_RUN_PORT'] = '5000'
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['AUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


def create_app(info):
    from devlog import make_app
    return make_app('dev')


cli = FlaskGroup(create_app=create_app)
cli.help = 'This is a management script for the Devlog application.'


@cli.command('initdb', short_help='Initialize missing database objects')
def initdb():
    from devlog.models import db
    db.create_all()


@cli.command('cleardb', short_help='Remove all database objects')
def cleardb():
    from devlog.models import db
    db.drop_all()


@cli.command('recreatedb', short_help='Recreate all database objects from scratch')
def recreatedb():
    from devlog.models import db
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    cli()
