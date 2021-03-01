import os
from typing import List
from xml.etree import ElementTree as etree  # noqa: DUO107,N813

import click
from defusedxml.ElementTree import parse
from dotenv import find_dotenv, load_dotenv
from flask import current_app
from flask.cli import FlaskGroup

from . import make_app
from .api.utils import get_user
from .ext import cache
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
    click.echo('\n'.join(sorted(MIGRATIONS.keys())))


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
    cache.delete_memoized(get_user)
    click.echo(f'User {name} created')


@cli.group(name='generate')
def generate_grp():
    pass


@generate_grp.command(
    name='icons',
    help='Generate Jinja2 include file for SVG icons from specified icon set',
)
@click.argument('iconset')
@click.argument('names', nargs=-1)
def gen_icons(iconset: str, names: List[str]):
    _default_icons = [
        'check',
    ]
    if names[0] == 'default':
        names = _default_icons
    target = os.path.join(
        current_app.root_path, current_app.template_folder, 'includes'
    )
    os.makedirs(target, exist_ok=True)
    target = os.path.join(target, 'icons.html')
    if os.path.isfile(target) and len(names) < len(_default_icons):
        if not click.confirm(
            'You are about to overwrite existing icon includes with smaller set '
            'than default, you sure want to do this?'
        ):
            return
    ns = 'http://www.w3.org/2000/svg'
    directory = os.path.join(current_app.static_folder, 'vendor', iconset)
    includes = []
    for name in names:
        fname = f'{name}.svg'
        file_path = os.path.join(directory, fname)
        tree = parse(file_path, forbid_dtd=True)
        root = tree.getroot()
        elems = root.findall('*')
        for el in elems:
            _, _, el.tag = el.tag.rpartition('}')
        symbol = etree.Element('symbol', attrib=root.attrib)
        symbol.attrib['id'] = name
        del symbol.attrib['class']
        symbol.attrib['width'] = symbol.attrib['height'] = '100%'
        symbol.extend(elems)
        includes.append(symbol)
    root = etree.Element('svg', attrib={'display': 'none', 'xmlns': ns})
    root.extend(includes)
    with open(target, 'w') as fp:
        fp.write(etree.tostring(root, encoding='unicode', short_empty_elements=False))


def main():
    load_dotenv(find_dotenv())
    cli()
