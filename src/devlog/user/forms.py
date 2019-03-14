from flask_babel import lazy_gettext as gettext
from wtforms import BooleanField, SelectField, StringField, TextAreaField
from wtforms.validators import Email, Optional

from ..models import User
from ..utils.forms import ObjectForm, SubmitButton


class UserForm(ObjectForm):
    name = StringField(gettext('name'))
    blurb = TextAreaField(gettext('blurb'))
    blurb_markup_type = SelectField(
        gettext('blurb markup processor'), choices=User.SMP_CHOICES,
    )
    email = StringField(gettext('email'), validators=[Email(), Optional()])
    active = BooleanField(gettext('active'), default=True)
    public = BooleanField(gettext('public'), default=False)
    submit_button = StringField('', widget=SubmitButton(icon='check'))
