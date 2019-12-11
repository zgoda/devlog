from typing import Optional

from flask_babel import lazy_gettext as gettext
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import (
    BooleanField, MultipleFileField, SelectField, StringField, TextAreaField,
)

from ..models import Blog
from ..utils.forms import Button, ObjectForm


class BlogForm(ObjectForm):
    name = StringField(gettext('name'), validators=[validators.InputRequired()])
    blurb = TextAreaField(gettext('blurb'))
    blurb_markup_type = SelectField(
        gettext('blurb markup processor'), choices=Blog.SMP_CHOICES,
        validators=[validators.Optional()], default=Blog.SMP_NONE,
    )
    active = BooleanField(gettext('active'), default=True)
    public = BooleanField(gettext('public'), default=True)
    default = BooleanField(gettext('default'), default=False)

    def save(self, obj: Optional[Blog] = None, save: bool = True) -> Blog:
        if obj is None:
            obj = Blog(user=current_user)
        return super().save(obj, save)


class PostImportForm(FlaskForm):
    files = MultipleFileField(gettext('files'))

    buttons = [
        Button(text=gettext('import'), icon='file-import')
    ]
