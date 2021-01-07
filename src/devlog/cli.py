import click
from dotenv import find_dotenv, load_dotenv
from flask.cli import FlaskGroup

from . import make_app
from .migrations import MIGRATIONS, run_migration
from .models import MODELS, User, db


def create_app(info):
    return make_app('dev')


cli = FlaskGroup(create_app=create_app)
cli.help = 'This is a management script for the Devlog application.'


@cli.group(name='db', help='database management commands')
def db_ops():
    pass


@db_ops.command(name='init', help='initialize missing database objects')
def db_init():
    db.create_tables(MODELS)


@db_ops.command(name='clear', help='remove all database objects')
def db_clear():
    db.drop_tables(MODELS)


@db_ops.command(
    name='recreate', help='recreate all database objects from scratch'
)
def db_recreate():
    db.drop_all()
    db.create_all()


@db_ops.command(name='migrate', help='run schema migration script')
@click.argument('name')
def db_migrate(name):
    run_migration(name)


@db_ops.command(name='migrations', help='list available migrations')
def db_list_migrations():
    click.echo('\n'.join(MIGRATIONS.keys()))


@cli.group(name='user', help='user account management')
def user_ops():
    pass


@user_ops.command(name='create', help='create new user account')
@click.argument('name')
@click.password_option('-p', '--password', help='set password', required=True)
def user_create(name: str, password: str) -> None:
    u = User(name=name)
    u.set_password(password)
    u.save()
    click.echo(f'User {name} created')


def main():
    load_dotenv(find_dotenv())
    cli()
