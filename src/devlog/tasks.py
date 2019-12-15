import re
from typing import List, Optional

import markdown2
from dateutil.parser import isoparse

from .app import make_app
from .models import Blog, Post, db
from .utils import email

app = make_app()
app.app_context().push()


METADATA_RE = re.compile(r'\A---(.|\n)*?---')


def import_post(file_name: str, blog_id: int):
    try:
        with open(file_name) as fp:
            text = fp.read()
        text_html = markdown2.markdown(
            text, safe_mode=True, extras=['metadata']
        )
        if not text_html.metadata or not text_html.metadata.get('title'):
            raise ValueError(
                f'Post file {file_name} does not provide post title in metadata'
            )
        blog = Blog.query.get(blog_id)
        if blog is None:
            raise ValueError(f'Blog ID {blog_id} not found')
        plain_text = METADATA_RE.sub('', text, count=1).strip()
        title = text_html.metadata['title']
        title = title.replace("'", '')
        created_dt = None
        post_date = text_html.metadata.get('date')
        if post_date:
            created_dt = isoparse(post_date)
        post = Post(
            blog=blog, title=title, text=plain_text, text_markup_type='markdown',
            public=blog.effective_public, created=created_dt,
        )
        db.session.add(post)
        db.session.commit()
    except Exception:
        app.logger.exception(
            f'Unhandled exception when importing post file {file_name}'
        )


def send_email(
            recipients: List[str], subject: str, html_body: str,
            text_body: Optional[str] = None,
        ):
    try:
        email.send_email(recipients, subject, html_body, text_body)
    except Exception:
        app.logger.exception(
            f'Unhandled exception when sending email {subject} to {recipients}',
        )
