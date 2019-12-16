from typing import Optional

from flask_babel import lazy_gettext as gettext
from wtforms.fields import PasswordField
from wtforms.validators import InputRequired
from wtforms_components.fields import EmailField

from ..models import User
from ..utils.forms import BaseForm


class LoginForm(BaseForm):
    name = EmailField(gettext('name'), validators=[InputRequired()])
    password = PasswordField(gettext('password'), validators=[InputRequired()])

    def login(self) -> Optional[User]:
        user = User.get_by_name(self.name.data)
        if user is not None and user.check_password(self.password.data):
            return user
