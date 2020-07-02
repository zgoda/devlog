import fcntl
import os
import stat
import sys
from datetime import datetime

import markdown
from dotenv import find_dotenv, load_dotenv

from .app import make_app
from .models import Post, Tag, TaggedPost, db
from .utils.text import (
    DEFAULT_MD_EXTENSIONS, METADATA_RE, normalize_post_date, post_summary, slugify,
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
