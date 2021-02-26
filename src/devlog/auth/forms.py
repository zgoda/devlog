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


class PartialLoginForm(FlaskForm):
    name = StringField('Nazwa użytkownika', validators=[InputRequired()])
    password = PasswordField('Hasło', validators=[InputRequired()])

    def login(self) -> bool:
        user = User.get_or_none(User.name == self.name.data)
        if user is None:
            return False
        if user.check_password(self.password.data):
            session['user'] = user.name
            return True
        return False


class OTPCodeForm(FlaskForm):
    code1 = StringField(
        'Kod OTP 1', validators=[InputRequired(), Length(6, 6)],
        render_kw={'autocomplete': 'off'}
    )
    code2 = StringField(
        'Kod OTP 2', validators=[InputRequired(), Length(6, 6)],
        render_kw={'autocomplete': 'off'}
    )

    def verify(self, user: User) -> bool:
        if user.verify_otp(self.code2.data):
            return True
        return False
