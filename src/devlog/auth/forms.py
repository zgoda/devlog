from typing import Optional

from flask_babel import lazy_gettext as gettext
from wtforms.fields import PasswordField, StringField
from wtforms.validators import EqualTo, InputRequired
from wtforms_components.fields import EmailField

from ..ext import db
from ..models import User
from ..utils.forms import BaseForm


class RegisterForm(BaseForm):
    email = EmailField(gettext('email'), validators=[InputRequired()])
    name = StringField(gettext('user name'))
    password1 = PasswordField(gettext('password'), validators=[InputRequired()])
    password2 = PasswordField(
        gettext('repeat password'),
        validators=[
            InputRequired(),
            EqualTo('password1', message=gettext('both password fields must match')),
        ]
    )

    def save(self) -> User:
        user = User(name=self.name.data, email=self.email.data)
        user.set_password(self.password1.data)
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(BaseForm):
    email = EmailField(gettext('email'), validators=[InputRequired()])
    password = PasswordField(gettext('password'), validators=[InputRequired()])

    def login(self) -> Optional[User]:
        user = User.get_by_email(self.email.data)
        if user is not None and user.check_password(self.password.data):
            return user
