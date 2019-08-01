from flask_babel import lazy_gettext as gettext
from flask_login import current_user
from wtforms.fields import BooleanField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Optional

from ..models import Blog
from ..utils.forms import ObjectForm


class BlogForm(ObjectForm):
    name = StringField(gettext('name'), validators=[DataRequired()])
    blurb = TextAreaField(gettext('blurb'))
    blurb_markup_type = SelectField(
        gettext('blurb markup processor'), choices=Blog.SMP_CHOICES,
        validators=[Optional()], default=Blog.SMP_NONE,
    )
    active = BooleanField(gettext('active'), default=True)
    public = BooleanField(gettext('public'), default=True)
    default = BooleanField(gettext('default'), default=False)

    def save(self, obj=None, save=True):
        if obj is None:
            obj = Blog(user=current_user)
        return super().save(obj, save)
