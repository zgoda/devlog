from flask_babel import lazy_gettext as gettext
from wtforms import BooleanField, StringField, TextAreaField
from wtforms.validators import Email, Optional

from ..utils.forms import ObjectForm, SubmitButton


class UserForm(ObjectForm):
    name = StringField(gettext('name'))
    blurb = TextAreaField(gettext('blurb'))
    email = StringField(gettext('email'), validators=[Email(), Optional()])
    is_active = BooleanField(gettext('active'), default=True)
    submit_button = StringField('', widget=SubmitButton(icon='check'))

    def save(self, user):
        return super().save(user)
