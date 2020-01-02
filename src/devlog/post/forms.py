from datetime import datetime
from typing import Optional

from flask_babel import lazy_gettext as gettext
from wtforms import validators
from wtforms.fields import BooleanField, StringField, TextAreaField

from ..ext import db
from ..models import Blog, Post
from ..utils.forms import ObjectForm


class PostForm(ObjectForm):
    title = StringField(gettext('title'), validators=[validators.InputRequired()])
    text = TextAreaField(gettext('text'), validators=[validators.InputRequired()])
    mood = StringField(gettext('mood'))
    draft = BooleanField(gettext('draft'), default=True)
    pinned = BooleanField(gettext('pinned'), default=False)

    def save(self, blog: Blog, obj: Optional[Post] = None, save: bool = True) -> Post:
        if obj is None:
            obj = Post(blog=blog)
        post = super().save(obj, save=False)
        db.session.add(post)
        blog.updated = datetime.utcnow()
        db.session.add(blog)
        db.session.commit()
        return post
