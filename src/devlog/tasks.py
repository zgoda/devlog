import os
import re
from datetime import datetime

import markdown
import pytz
import sqlalchemy as sa
from dateutil.parser import isoparse

from .utils.text import slugify, stripping_markdown


METADATA_RE = re.compile(r'\A---(.|\n)*?---')


def import_post(file_name: str, blog_id: int):
    engine = sa.create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
    cn = engine.connect()
    try:
        with open(file_name) as fp:
            text = fp.read()
        md = markdown.Markdown(
            extensions=['meta', 'fenced_code', 'codehilite'], output_format='html'
        )
        html_text = md.convert(text)
        if not md.Meta or not md.Meta.get('title'):
            raise ValueError(
                f'Post file {file_name} does not provide post title in metadata'
            )
        blog_sql = sa.text(
            'select id, user_id from blog where id = :blog_id'
        ).bindparams(blog_id=blog_id)
        blog_rv = cn.execute(blog_sql)
        row = blog_rv.first()
        if row is None:
            raise ValueError(f'Blog ID {blog_id} not found')
        user_id = row[1]
        plain_content = METADATA_RE.sub('', text, count=1).strip()
        sm = stripping_markdown()
        plain_text = sm.convert(plain_content)
        summary = ' '.join(plain_text.split()[:10])
        title = ' '.join(md.Meta['title']).strip()
        title = title.replace("'", '')
        created_dt = None
        post_date = ' '.join(md.Meta.get('date', [])).strip()
        if post_date:
            created_dt = isoparse(post_date)
            if created_dt.tzinfo is None:
                tz = pytz.timezone(
                    os.environ.get('BABEL_DEFAULT_TIMEZONE', 'Europe/Warsaw')
                )
                created_dt = created_dt.astimezone(tz).astimezone(pytz.utc)
            else:
                created_dt = created_dt.astimezone(pytz.utc)
        is_draft = ' '.join(md.Meta.get('draft', [])).strip()
        is_draft = 'false' not in is_draft.lower()
        updated = datetime.utcnow()
        published = None
        if not is_draft:
            published = updated
        post_sql = sa.text(
            '''
            insert into post (
                blog_id, author_id, title, slug, text, text_html,
                created, updated, published, draft, summary
            ) values (
                :blog_id, :author_id, :title, :slug, :text, :text_html,
                :created, :updated, :published, :draft, :summary
            )'''
        ).bindparams(
            blog_id=blog_id, author_id=user_id, title=title, slug=slugify(title),
            text=plain_content, text_html=html_text, created=created_dt,
            updated=updated, published=published, draft=is_draft, summary=summary
        )
        cn.execute(post_sql)
    finally:
        cn.close()
