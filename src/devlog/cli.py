import json
import os
import sys
from datetime import datetime

import click
from dotenv import find_dotenv, load_dotenv
from flask.cli import FlaskGroup

from . import make_app
from .ext import db
from .models import Blog, Post, User


def create_app(info):
    return make_app('dev')


cli = FlaskGroup(create_app=create_app)
cli.help = 'This is a management script for the Devlog application.'


@cli.group(name='db', help='database management commands')
def db_ops():
    pass


@db_ops.command(name='init', short_help='initialize missing database objects')
def db_init():
    db.create_all()


@db_ops.command(name='clear', short_help='remove all database objects')
def db_clear():
    db.drop_all()


@db_ops.command(
    name='recreate', short_help='recreate all database objects from scratch'
)
def db_recreate():
    db.drop_all()
    db.create_all()


@db_ops.command(name='export', help='export application data')
@click.option('-o', '--output-dir', help='where to write result [default: .]')
def db_export(output_dir):

    def dump(data, directory: str, datatype: str):
        if data:
            fn = os.path.join(directory, f'{datatype}.json')
            with open(fn, mode='w') as fp:
                json.dump(data, fp)
            click.echo(f'{datatype} data written to {fn}')

    if output_dir is None:
        output_dir = os.getcwd()
    output_dir = os.path.abspath(os.path.normpath(output_dir))
    click.echo('exporting users data')
    data = []
    for user in User.query:
        data.append({
            'name': user.name,
            'blurb': user.blurb,
            'password': user.password,
            'default_language': user.default_language,
            'timezone': user.timezone,
            'active': user.active
        })
    dump(data, output_dir, 'users')
    click.echo('exporting blog data')
    data = []
    for blog in Blog.query:
        blog_data = {
            'user': blog.user.name,
            'created': blog.created.timestamp(),
            'name': blog.name,
            'blurb': blog.blurb,
            'default': blog.default,
            'language': blog.language,
            'active': blog.active,
        }
        if blog.updated:
            blog_data['updated'] = blog.updated.timestamp()
        else:
            blog_data['updated'] = None
        data.append(blog_data)
    dump(data, output_dir, 'blog')
    click.echo('exporting posts')
    data = []
    for post in Post.query:
        post_data = {
            'blog': post.blog.name,
            'author': post.author.name,
            'created': post.created.timestamp(),
            'title': post.title,
            'text': post.text,
            'summary': post.summary,
            'mood': post.mood,
            'draft': post.draft,
            'pinned': post.pinned,
            'language': post.language,
        }
        if post.updated:
            post_data['updated'] = post.updated.timestamp()
        else:
            post_data['updated'] = None
        if post.published:
            post_data['published'] = post.published.timestamp()
        else:
            post_data['published'] = None
        data.append(post_data)
    dump(data, output_dir, 'post')
    click.echo('export complete')


@db_ops.command(name='import', help='import application data')
@click.option('-i', '--input-dir', help='location of input data [default: .]')
def db_import(input_dir):
    db.create_all()
    if input_dir is None:
        input_dir = os.getcwd()
    input_dir = os.path.abspath(os.path.normpath(input_dir))
    click.echo('importing users')
    users_fn = os.path.join(input_dir, 'users.json')
    if not os.path.isfile(users_fn):
        click.echo('WARNING: users data not found')
    else:
        with open(users_fn) as fp:
            data = json.load(fp)
            for record in data:
                user = User(**record)
                db.session.add(user)
        db.session.flush()
    click.echo('importing blogs')
    blogs_fn = os.path.join(input_dir, 'blog.json')
    if not os.path.isfile(blogs_fn):
        click.echo('WARNING: blogs data not found')
    else:
        with open(blogs_fn) as fp:
            data = json.load(fp)
            for record in data:
                username = record['user']
                user = User.get_by_name(username)
                if user is None:
                    click.echo(f'WARNING: user {username} does not exist')
                    continue
                record['user'] = user
                record['created'] = datetime.fromtimestamp(record['created'])
                if record['updated'] is not None:
                    record['updated'] = datetime.fromtimestamp(record['updated'])
                blog = Blog(**record)
                db.session.add(blog)
        db.session.flush()
    click.echo('importing posts')
    post_fn = os.path.join(input_dir, 'post.json')
    if not os.path.isfile(post_fn):
        click.echo('WARNING: posts data not found')
    else:
        with open(post_fn) as fp:
            data = json.load(fp)
            for record in data:
                username = record['author']
                user = User.get_by_name(username)
                if user is None:
                    click.echo(f'WARNING: user {username} does not exist')
                    continue
                blogname = record['blog']
                blog = Blog.get_by_name(user, blogname)
                if blog is None:
                    click.echo(f'WARNING: blog {blogname} does not exist')
                    continue
                record['author'] = user
                record['blog'] = blog
                record['created'] = datetime.fromtimestamp(record['created'])
                if record['updated']:
                    record['updated'] = datetime.fromtimestamp(record['updated'])
                if record['published']:
                    record['published'] = datetime.fromtimestamp(record['published'])
                post = Post(**record)
                db.session.add(post)
    db.session.commit()
    click.echo('import complete')


@cli.group(name='user', help='user account management commands')
def user_ops():
    pass


@user_ops.command(name='create', help='create new user account')
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


@user_ops.command(name='delete')
@click.argument('name')
@click.option(
    '-s', '--substitute', required=True, help='substitute user as owner of blogs',
)
def user_delete(name, substitute):
    user = User.get_by_name(name)
    if user is None:
        raise click.ClickException(f'user {name} not found')
    if User.query.count() == 1:
        raise click.ClickException('there has to be at least one user')
    sub = User.get_by_name(substitute)
    if sub is None:
        raise click.ClickException(f'substitute user {substitute} not found')
    if not click.confirm(
        f'Do you really want to delete account for {name} '
        f'and move all content to {substitute}?'
    ):
        click.echo('operation aborted, no changes made to site')
        sys.exit(0)
    for blog in Blog.query.filter_by(user=user):
        blog.user = sub
        db.session.add(blog)
    for post in Post.query.filter_by(author=user):
        post.author = sub
        db.session.add(post)
    db.session.delete(user)
    db.session.commit()
    click.echo(f'user {name} has been deleted, all content moved to user {substitute}')


def main():
    load_dotenv(find_dotenv())
    cli()
