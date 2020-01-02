from typing import Optional

from flask_babel import lazy_gettext as gettext
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired

from ..models import User
from ..utils.forms import BaseForm, Button


class LoginForm(BaseForm):
    name = StringField(gettext('name'), validators=[InputRequired()])
    password = PasswordField(gettext('password'), validators=[InputRequired()])

    buttons = [
        Button(text=gettext('sign in'), icon='sign-in-alt'),
    ]

    def login(self) -> Optional[User]:
        user = User.get_by_name(self.name.data)
        if user is not None and user.check_password(self.password.data):
            return user
