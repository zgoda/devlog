import re

import markdown
import pytz
from dateutil.parser import isoparse

from .app import make_app
from .models import Blog, Post, db

app = make_app()
app.app_context().push()


METADATA_RE = re.compile(r'\A---(.|\n)*?---')


def import_post(file_name: str, blog_id: int):
    try:
        with open(file_name) as fp:
            text = fp.read()
        md = markdown.Markdown(extensions=['meta'])
        md.convert(text)
        if not md.Meta or not md.Meta.get('title'):
            raise ValueError(
                f'Post file {file_name} does not provide post title in metadata'
            )
        blog = Blog.query.get(blog_id)
        if blog is None:
            raise ValueError(f'Blog ID {blog_id} not found')
        plain_text = METADATA_RE.sub('', text, count=1).strip()
        title = ' '.join(md.Meta['title']).strip()
        title = title.replace("'", '')
        created_dt = None
        post_date = ' '.join(md.Meta.get('date', [])).strip()
        if post_date:
            created_dt = isoparse(post_date)
            if created_dt.tzinfo is None:
                tz = pytz.timezone(app.config['BABEL_DEFAULT_TIMEZONE'])
                created_dt = created_dt.astimezone(tz).astimezone(pytz.utc)
            else:
                created_dt = created_dt.astimezone(pytz.utc)
        is_draft = ' '.join(md.Meta.get('draft', [])).strip()
        is_draft = 'false' not in is_draft.lower()
        post = Post(
            blog=blog, title=title, text=plain_text, created=created_dt, draft=is_draft
        )
        db.session.add(post)
        db.session.commit()
    except Exception:
        app.logger.exception(
            f'Unhandled exception when importing post file {file_name}'
        )
