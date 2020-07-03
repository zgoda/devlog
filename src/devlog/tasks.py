import fcntl
import os
import stat
import sys
from datetime import datetime

import markdown
from dotenv import find_dotenv, load_dotenv
from flask import url_for

from .app import make_app
from .models import Post, Tag, TaggedPost, db
from .utils.text import (
    DEFAULT_MD_EXTENSIONS, METADATA_RE, normalize_post_date, post_summary, slugify,
)
from .utils.web import (
    PageDef, URLSet, URLSetConfig, generate_sitemap, save_sitemap_file,
)

load_dotenv(find_dotenv())

app = make_app(os.environ.get('ENV'))
os.makedirs(app.instance_path, exist_ok=True)


def import_posts():  # pragma: nocover
    lf = os.path.join(app.instance_path, 'postimport.lock')
    lf_flags = os.O_WRONLY | os.O_CREAT
    lf_mode = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
    lf_fd = os.open(lf, lf_flags, lf_mode)
    try:
        fcntl.lockf(lf_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        sys.exit('Only one instance of post import can be running')
    incoming_dir = app.config['POST_INCOMING_DIR']
    if not os.path.isabs(incoming_dir):
        incoming_dir = os.path.join(app.instance_path, incoming_dir)
        os.makedirs(incoming_dir, exist_ok=True)
    for file_name in os.listdir(incoming_dir):
        if not file_name.endswith('.md'):
            continue
        file_path = os.path.join(incoming_dir, file_name)
        with open(file_path) as fp:
            text = fp.read()
        action_from_markdown(text)
        os.remove(file_path)
    os.close(lf_fd)
    os.remove(lf)


def action_from_markdown(text: str) -> Post:
    md = markdown.Markdown(extensions=DEFAULT_MD_EXTENSIONS, output_format='html')
    html = md.convert(text)
    if not md.Meta or not md.Meta.get('title'):
        raise ValueError('Metadata not provided in source')
    plain_content = METADATA_RE.sub('', text, count=1).strip()
    summary = post_summary(plain_content)
    title = md.Meta['title'].strip().replace("'", '')
    created_dt = published = updated = datetime.utcnow()
    post_date = md.Meta.get('date')
    if post_date:
        created_dt = normalize_post_date(post_date)
    slug = slugify(title)
    c_year, c_month, c_day = created_dt.year, created_dt.month, created_dt.day
    search_crit = (
        (Post.slug == slug) &
        (Post.c_year == c_year) &
        (Post.c_month == c_month) &
        (Post.c_day == c_day)
    )
    post = Post.get_or_none(search_crit)
    author = md.Meta.get('author', '').strip()
    if md.Meta.get('draft', False):
        published = None
    post_tags = md.Meta.get('tags', [])
    kw = dict(
        author=author, created=created_dt, updated=updated,
        published=published, title=title, slug=slug,
        text=plain_content, text_html=html, summary=summary,
        c_year=c_year, c_month=c_month, c_day=c_day,
    )
    with db.atomic():
        if post is None:
            post = Post.create(**kw)
        else:
            kw.pop('created')
            Post.update(**kw).where(search_crit).execute()
            TaggedPost.delete().where(TaggedPost.post == post).execute()
        for tag_s in post_tags:
            tag, _ = Tag.get_or_create(
                name=tag_s, defaults={'slug': slugify(tag_s)}
            )
            TaggedPost.create(post=post, tag=tag)


def sitemap_generator():
    server_name = os.environ.get('WHERE_AM_I')
    if server_name is None:
        app.logger.error('scheme://host part not known, can not generate sitemap')
        sys.exit(1)
    with app.app_context():
        app.config['SERVER_NAME'] = server_name
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
                url_for('main.index', _external=True), last_post_updated
            )
        )
        misc = URLSet(
            config=URLSetConfig(changefreq='monthly', priority='0.3'), pagedefs=[]
        )
        urlsets = [misc, posts, collections]
        sitemap = generate_sitemap(*urlsets)
        save_sitemap_file(os.path.join(app.static_folder, 'sitemap.xml'), sitemap)
