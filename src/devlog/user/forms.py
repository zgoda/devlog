from flask_babel import lazy_gettext as gettext
from wtforms import BooleanField, StringField, TextAreaField
from wtforms.validators import Email, Optional

from ..utils.forms import ObjectForm, SubmitButton


class UserForm(ObjectForm):
    name = StringField(gettext('name'))
    blurb = TextAreaField(gettext('blurb'))
    email = StringField(gettext('email'), validators=[Email(), Optional()])
    active = BooleanField(gettext('active'), default=True)
    public = BooleanField(gettext('public'), default=False)
    submit_button = StringField('', widget=SubmitButton(icon='check'))
