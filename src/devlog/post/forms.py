from typing import Optional

from flask_babel import lazy_gettext as gettext
from wtforms import validators
from wtforms.fields import BooleanField, SelectField, StringField, TextAreaField

from ..models import Blog, Post
from ..utils.forms import ObjectForm


class PostForm(ObjectForm):
    title = StringField(gettext('title'), validators=[validators.InputRequired()])
    text = TextAreaField(gettext('text'))
    text_markup_type = SelectField(
        gettext('blurb markup processor'),
        choices=Post.SMP_CHOICES,
        validators=[validators.Optional()],
        default=Post.SMP_NONE,
    )
    mood = StringField(gettext('mood'))
    public = BooleanField(gettext('public'), default=True)
    draft = BooleanField(gettext('draft'), default=True)
    pinned = BooleanField(gettext('pinned'), default=False)

    def save(self, blog: Blog, obj: Optional[Post] = None, save: bool = True) -> Post:
        if obj is None:
            obj = Post(blog=blog)
        return super().save(obj, save)
