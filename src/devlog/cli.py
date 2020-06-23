from dotenv import find_dotenv, load_dotenv
from flask.cli import FlaskGroup

from . import make_app
from .models import Post, Tag, TaggedPost, db


def create_app(info):
    return make_app('dev')


cli = FlaskGroup(create_app=create_app)
cli.help = 'This is a management script for the Devlog application.'


@cli.group(name='db', help='database management commands')
def db_ops():
    pass


@db_ops.command(name='init', short_help='initialize missing database objects')
def db_init():
    db.create_tables([Post, Tag, TaggedPost])


@db_ops.command(name='clear', short_help='remove all database objects')
def db_clear():
    db.drop_tables([TaggedPost, Tag, Post])


@db_ops.command(
    name='recreate', short_help='recreate all database objects from scratch'
)
def db_recreate():
    db.drop_all()
    db.create_all()


def main():
    load_dotenv(find_dotenv())
    cli()
