from flask import session
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired, Length

from ..models import User
from ..utils.forms import Button

_REQ_VALIDATORS = [InputRequired()]
_OTP_VALIDATORS = [InputRequired(), Length(6, 6)]
_OTP_RENDER_KW = {'autocomplete': 'off'}


class LoginForm(FlaskForm):
    name = StringField('Nazwa użytkownika', validators=_REQ_VALIDATORS)
    password = PasswordField('Hasło', validators=_REQ_VALIDATORS)
    code = StringField('Kod OTP', validators=_OTP_VALIDATORS, render_kw=_OTP_RENDER_KW)

    buttons = [
        Button(text='zaloguj')
    ]

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
    name = StringField('Nazwa użytkownika', validators=_REQ_VALIDATORS)
    password = PasswordField('Hasło', validators=_REQ_VALIDATORS)

    buttons = [
        Button(text='zaloguj')
    ]

    def login(self) -> User:
        user = User.get_or_none(User.name == self.name.data)
        if user and user.check_password(self.password.data):
            session['user'] = user.name
            return user


class OTPCodeForm(FlaskForm):
    code1 = StringField(
        'Pierwszy kod OTP', validators=_OTP_VALIDATORS, render_kw=_OTP_RENDER_KW
    )
    code2 = StringField(
        'Drugi kod OTP', validators=_OTP_VALIDATORS, render_kw=_OTP_RENDER_KW
    )

    buttons = [
        Button(text='powiąż')
    ]

    def verify(self, user: User) -> bool:
        if user.verify_otp(self.code2.data):
            return True
        return False
