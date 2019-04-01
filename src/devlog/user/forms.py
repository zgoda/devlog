from flask_babel import lazy_gettext as gettext
from wtforms import BooleanField, SelectField, StringField, TextAreaField
from wtforms.validators import Optional
from wtforms_components import Email

from ..models import User
from ..utils.forms import ObjectForm


class UserForm(ObjectForm):
    name = StringField(gettext('name'))
    blurb = TextAreaField(gettext('blurb'))
    blurb_markup_type = SelectField(
        gettext('blurb markup processor'),
        choices=User.SMP_CHOICES,
        validators=[Optional()],
        default=User.SMP_NONE,
    )
    email = StringField(gettext('email'), validators=[Email(), Optional()])
    active = BooleanField(gettext('active'), default=True)
    public = BooleanField(gettext('public'), default=False)
