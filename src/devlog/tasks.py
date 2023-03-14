import os
import sys
from datetime import datetime

import requests
from dotenv import find_dotenv, load_dotenv
from flask import url_for
from markdown import markdown

from .app import make_app
from .ext import cache, pages
from .models import Link, Post, Tag, TaggedPost, db
from .utils.platform import single_instance_mutex
from .utils.text import LinkProcessor, PostProcessor, slugify
from .utils.web import (
    PageDef, URLSet, URLSetConfig, generate_sitemap, save_sitemap_file,
)

load_dotenv(find_dotenv())

app = make_app(os.environ.get('ENV'))
os.makedirs(app.instance_path, exist_ok=True)


def import_posts() -> None:  # pragma: nocover
    with single_instance_mutex(app.instance_path, 'postimport'):
        incoming_dir = app.config['POST_INCOMING_DIR']
        if not os.path.isabs(incoming_dir):
            incoming_dir = os.path.abspath(
                os.path.join(app.instance_path, incoming_dir)
            )
        os.makedirs(incoming_dir, exist_ok=True)
        files_imported = 0
        for file_name in os.listdir(incoming_dir):
            if not file_name.endswith('.md'):
                continue
            file_path = os.path.join(incoming_dir, file_name)
            with open(file_path) as fp:
                text = fp.read()
            post_from_markdown(text)
            os.remove(file_path)
            files_imported += 1
        if files_imported:
            sitemap_generator()


def post_from_markdown(text: str) -> None:
    pp = PostProcessor(text)
    meta = pp.process_meta()
    search_crit = (
        (Post.slug == meta.slug) &
        (Post.c_year == meta.c_year) &
        (Post.c_month == meta.c_month) &
        (Post.c_day == meta.c_day)
    )
    post = Post.get_or_none(search_crit)
    kw = pp.as_dict(meta, pp.published(post is None, meta), post is not None)
    with db.atomic():
        if post is None:
            post = Post.create(**kw)
        else:
            Post.update(**kw).where(search_crit).execute()
            TaggedPost.delete().where(TaggedPost.post == post).execute()
        for tag_s in pp.tags:
            tag_slug = slugify(tag_s)
            tag, _ = Tag.get_or_create(
                name=tag_s, defaults={'slug': tag_slug}
            )
            TaggedPost.create(post=post, tag=tag)


def import_links() -> None:  # pragma: nocover
    with single_instance_mutex(app.instance_path, 'linkimport'):
        incoming_dir = app.config['LINK_INCOMING_DIR']
        if not os.path.isabs(incoming_dir):
            incoming_dir = os.path.abspath(
                os.path.join(app.instance_path, incoming_dir)
            )
        os.makedirs(incoming_dir, exist_ok=True)
        processed = 0
        for file_name in os.listdir(incoming_dir):
            if not file_name.endswith('.md'):
                continue
            file_path = os.path.join(incoming_dir, file_name)
            with open(file_path) as fp:
                text = fp.read()
            link_from_markdown(text)
            os.remove(file_path)
            processed += 1
        if processed:
            with app.app_context():
                cache.delete_prefixed('links')


def link_from_markdown(text: str) -> None:
    lp = LinkProcessor(text)
    kw = {
        'section': lp.meta['category'],
        'text': lp.text,
        'text_html': markdown(lp.text, **lp.MD_KWARGS)[len('<p>'):-len('</p>')],
    }
    Link.create(**kw)


def sitemap_generator() -> None:
    sitemap_filename = 'sitemap.xml'
    server_name = os.environ.get('WHERE_AM_I')
    if not server_name:
        app.logger.error('scheme://host part not known, can not generate sitemap')
        sys.exit(1)
    app.config['SERVER_NAME'] = server_name
    with app.app_context():
        posts = URLSet(config=URLSetConfig(changefreq='weekly'), pagedefs=[])
        for post in Post.select().where(Post.published.is_null(False)).iterator():
            page_def = PageDef(
                url_for(
                    'main.post',
                    slug=post.slug, y=post.c_year, m=post.c_month, d=post.c_day,
                    _external=True,
                ),
                post.updated.isoformat()
            )
            posts.pagedefs.append(page_def)
        collection_config = URLSetConfig(changefreq='daily', priority='0.8')
        collections = URLSet(config=collection_config, pagedefs=[])
        for tag in Tag.select():
            last_post = (
                TaggedPost
                .select(TaggedPost, Post)
                .join(Post)
                .where(TaggedPost.tag == tag)
                .order_by(Post.updated.desc())
                .first()
            )
            page_def = PageDef(
                url_for('main.tag', slug=tag.slug, _external=True),
                last_post.post.updated.isoformat(),
            )
            collections.pagedefs.append(page_def)
        last_post = Post.select().order_by(Post.created.desc()).first()
        if last_post:
            last_post_updated = last_post.updated.isoformat()
        else:
            last_post_updated = datetime.utcnow().isoformat()
        collections.pagedefs.append(
            PageDef(
                url_for('main.index', _external=True), last_post_updated,
            )
        )
        misc = URLSet(
            config=URLSetConfig(changefreq='monthly', priority='0.3'), pagedefs=[]
        )
        for path in ['o', 'kontakt']:
            page = pages.get(path)
            last_mod = \
                page.meta.get('updated') or page.meta.get('published')  # type: ignore
            page_def = PageDef(
                url_for('main.page', path=path), last_mod.isoformat()
            )
            misc.pagedefs.append(page_def)
        urlsets = [misc, posts, collections]
        sitemap = generate_sitemap(*urlsets)
        save_sitemap_file(
            os.path.join(app.static_folder, sitemap_filename), sitemap  # type: ignore
        )
        sitemap_url = os.path.join(server_name, sitemap_filename)
        requests.get('http://www.google.com/ping', params={'sitemap': sitemap_url})
