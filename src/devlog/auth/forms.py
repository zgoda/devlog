from flask import session
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired, Length

from ..models import User


class LoginForm(FlaskForm):
    name = StringField('Nazwa użytkownika', validators=[InputRequired()])
    password = PasswordField('Hasło', validators=[InputRequired()])
    code = StringField('Kod OTP', validators=[InputRequired(), Length(6, 6)])

    def login(self) -> bool:
        user = User.get_or_none(User.name == self.name.data)
        if user is None:
            return False
        if user.verify_secrets(self.password.data, self.code.data):
            login_user(user)
            session.permanent = True
            return True
        return False
