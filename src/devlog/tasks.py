import markdown2
from dateutil.parser import isoparse

from .app import make_app
from .models import Blog, Post, db

app = make_app()
app.app_context().push()


def import_post(file_name: str, blog_id: int):
    try:
        with open(file_name) as fp:
            text = fp.read()
        text_html = markdown2.markdown(
            text, safe_mode=True,
            extras={
                'html-classes': {'img': 'markdown-image'},
                'metadata': True
            }
        )
        if not text_html.metadata or not text_html.metadata.get('title'):
            raise ValueError(
                f'Post file {file_name} does not provide post title in metadata'
            )
        blog = Blog.query.get(blog_id)
        if blog is None:
            raise ValueError(f'Blog ID {blog_id} not found')
        post = Post(
            blog=blog, title=text_html.metadata['title'], text=text,
            text_html=text_html, text_markup_type='markdown',
            public=blog.effective_public,
        )
        post_date = text_html.metadata.get('date')
        if post_date:
            post_date = isoparse(post_date)
            post.created = post_date
        db.session.add(post)
        db.session.commit()
    except Exception:
        app.logger.exception('Unhandled exception in background task')
