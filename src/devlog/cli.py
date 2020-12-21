import click
from dotenv import find_dotenv, load_dotenv
from flask.cli import FlaskGroup

from . import make_app
from .migrations import MIGRATIONS, run_migration
from .models import Post, Tag, TaggedPost, User, db
from .utils import security


def create_app(info):
    return make_app('dev')


cli = FlaskGroup(create_app=create_app)
cli.help = 'This is a management script for the Devlog application.'


@cli.group(name='db', help='database management commands')
def db_ops():
    pass


@db_ops.command(name='init', help='initialize missing database objects')
def db_init():
    db.create_tables([User, Post, Tag, TaggedPost])


@db_ops.command(name='clear', help='remove all database objects')
def db_clear():
    db.drop_tables([TaggedPost, Tag, Post, User])


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


@user_ops.command(name='create', help='create user account')
@click.argument('name')
@click.password_option('-p', '--password', required=True, help='set user password')
@click.option('-d', '--display-name', help='set user display (screen) name')
def user_create(name, display_name, password):
    u = User(name=name)
    if not display_name:
        display_name = name
    u.display_name = display_name
    u.password = security.generate_password_hash(password)
    private_key = security.generate_private_key()
    u.private_key = security.serialize_private_key(private_key)
    public_key = security.generate_public_key(private_key)
    u.public_key = security.serialize_public_key(public_key)
    u.actor_id = f'https://devlog.zgodowie.org/{name}'
    u.save()


def main():
    load_dotenv(find_dotenv())
    cli()
