from datetime import datetime

import markdown

from ..models import Post, Tag, TaggedPost, db
from .text import (
    DEFAULT_MD_EXTENSIONS, METADATA_RE, normalize_post_date, post_summary, slugify,
)


def post_from_markdown(text: str) -> Post:
    md = markdown.Markdown(extensions=DEFAULT_MD_EXTENSIONS, output_format='html')
    html = md.convert(text)
    if not md.Meta or not md.Meta.get('title'):
        raise ValueError('Metadata not provided in source')
    plain_content = METADATA_RE.sub('', text, count=1).strip()
    summary = post_summary(plain_content)
    title = md.Meta['title'].strip().replace("'", '')
    created_dt = updated = datetime.utcnow()
    post_date = md.Meta.get('date')
    if post_date:
        created_dt = normalize_post_date(post_date)
    author = md.Meta.get('author', '').strip()
    is_draft = md.Meta.get('draft', False)
    published = None
    if not is_draft:
        published = updated
    post_tags = md.Meta.get('tags', [])
    with db.atomic():
        post = Post.create(
            author=author, created=created_dt, updated=updated,
            published=published, title=title, slug=slugify(title),
            text=plain_content, text_html=html, summary=summary,
            c_year=created_dt.year, c_month=created_dt.month, c_day=created_dt.day,
        )
        for tag_s in post_tags:
            tag, _ = Tag.get_or_create(
                name=tag_s, defaults={'slug': slugify(tag_s)}
            )
            TaggedPost.create(post=post, tag=tag)
    return post
