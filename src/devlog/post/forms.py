from flask_babel import lazy_gettext as gettext
from wtforms.fields import SelectField, StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional

from ..models import Post
from ..utils.forms import ObjectForm


class PostForm(ObjectForm):
    title = StringField(gettext("title"), validators=[DataRequired()])
    text = TextAreaField(gettext("text"))
    text_markup_type = SelectField(
        gettext("blurb markup processor"),
        choices=Post.SMP_CHOICES,
        validators=[Optional()],
        default=Post.SMP_NONE,
    )
    mood = StringField(gettext("mood"))
    public = BooleanField(gettext("public"), default=True)
    draft = BooleanField(gettext("draft"), default=True)
    pinned = BooleanField(gettext("pinned"), default=False)
