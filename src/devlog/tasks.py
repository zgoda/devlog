import markdown2
from dateutil.parser import isoparse
import re

from .app import make_app
from .models import Blog, Post, db

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
        post = Post(
            blog=blog, title=text_html.metadata['title'], text=plain_text,
            text_markup_type='markdown', public=blog.effective_public,
        )
        post_date = text_html.metadata.get('date')
        if post_date:
            post_date = isoparse(post_date)
            post.created = post_date
        db.session.add(post)
        db.session.commit()
    except Exception:
        app.logger.exception('Unhandled exception in background task')
