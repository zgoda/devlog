from typing import Optional

from flask_babel import lazy_gettext
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, MultipleFileField, StringField, TextAreaField

from ..models import Blog
from ..utils.forms import Button, ObjectForm, input_required_validator


class BlogForm(ObjectForm):
    name = StringField(lazy_gettext('name'), validators=[input_required_validator])
    blurb = TextAreaField(lazy_gettext('blurb'))
    active = BooleanField(lazy_gettext('active'), default=True)
    default = BooleanField(lazy_gettext('default'), default=False)

    def save(self, obj: Optional[Blog] = None, save: bool = True) -> Blog:
        if obj is None:
            obj = Blog(user=current_user)
        return super().save(obj, save)


class PostImportForm(FlaskForm):
    files = MultipleFileField(lazy_gettext('files'))

    buttons = [
        Button(text=lazy_gettext('import'), icon='file-import')
    ]
