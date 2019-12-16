import click
from dotenv import find_dotenv, load_dotenv
from flask.cli import FlaskGroup

from . import make_app
from .ext import db
from .models import User


def create_app(info):
    return make_app('dev')


cli = FlaskGroup(create_app=create_app)
cli.help = 'This is a management script for the Devlog application.'


@cli.group(name='db', help='database management commands')
def db_ops():
    pass


@db_ops.command('init', short_help='initialize missing database objects')
def initdb():
    db.create_all()


@db_ops.command('clear', short_help='remove all database objects')
def cleardb():
    db.drop_all()


@db_ops.command('recreate', short_help='recreate all database objects from scratch')
def recreatedb():
    db.drop_all()
    db.create_all()


@cli.group(name='user', help='user account management commands')
def user_ops():
    pass


@user_ops.command(name='create')
@click.argument('name')
@click.password_option('-p', '--password', help='account password', required=True)
@click.option('-l', '--language', default='pl', help='user language [default: pl]')
@click.option(
    '-z', '--timezone', default='Europe/Warsaw',
    help='user time zone [default: Europe/Warsaw]',
)
def user_create(name, password, language, timezone):
    if User.get_by_name(name) is not None:
        raise click.ClickException(f'user {name} is already registered')
    user = User(name=name, default_language=language, timezone=timezone)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f'user {name} has been created')


def main():
    load_dotenv(find_dotenv())
    cli()
