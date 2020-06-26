import fcntl
import os
import re
import stat
import sys
from datetime import date, datetime

import markdown
import pytz
from dotenv import find_dotenv, load_dotenv

from .app import make_app
from .models import Post, Tag, TaggedPost, db
from .utils.text import CenterBlockExtension, rich_summary, slugify, stripping_markdown

load_dotenv(find_dotenv())

app = make_app(os.environ.get('ENV'))
os.makedirs(app.instance_path, exist_ok=True)

METADATA_RE = re.compile(r'\A---.*?---', re.S | re.MULTILINE)

MD_EXTENSIONS = [
    'full_yaml_metadata', 'fenced_code', 'codehilite', CenterBlockExtension()
]
MD = markdown.Markdown(extensions=MD_EXTENSIONS, output_format='html')
SM = stripping_markdown()


def import_posts():
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
        html_text = MD.convert(text)
        if not MD.Meta or not MD.Meta.get('title'):
            app.logger.warning(
                f'Post file {file_name} does not provide post title in metadata'
            )
            continue
        plain_content = METADATA_RE.sub('', text, count=1).strip()
        plain_text = SM.convert(plain_content)
        summary_end_pos = plain_text.find('<!-- more -->')
        if summary_end_pos > -1:
            summary = rich_summary(plain_content)
        else:
            summary = markdown.markdown(
                ' '.join(plain_text.split()[:50]), extensions=MD_EXTENSIONS,
                output_format='html',
            )
        title = MD.Meta['title'].strip().replace("'", '')
        created_dt = updated = datetime.utcnow()
        post_date = MD.Meta.get('date')
        author = MD.Meta.get('author', '').strip()
        if post_date:
            if isinstance(post_date, date):
                post_date = datetime.utcnow().replace(
                    year=post_date.year, month=post_date.month, day=post_date.day
                )
            if post_date.tzinfo is None:
                tz = pytz.timezone(
                    os.environ.get('BABEL_DEFAULT_TIMEZONE', 'Europe/Warsaw')
                )
                post_date = post_date.astimezone(tz).astimezone(pytz.utc)
            else:
                post_date = post_date.astimezone(pytz.utc)
            created_dt = post_date.replace(tzinfo=None)
        is_draft = MD.Meta.get('draft', False)
        published = None
        if not is_draft:
            published = updated
        post_tags = MD.Meta.get('tags', [])
        with db.atomic():
            MD.reset()
            post = Post.create(
                author=author, created=created_dt, updated=updated,
                published=published, title=title, slug=slugify(title),
                text=plain_content, text_html=html_text, summary=summary,
                c_year=created_dt.year, c_month=created_dt.month, c_day=created_dt.day,
            )
            for tag_s in post_tags:
                tag, _ = Tag.get_or_create(
                    name=tag_s, defaults={'slug': slugify(tag_s)}
                )
                TaggedPost.create(post=post, tag=tag)
            os.remove(file_path)
    os.close(lf_fd)
    os.remove(lf)
