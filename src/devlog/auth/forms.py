from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired, Length


class BasicLoginForm(FlaskForm):
    name = StringField('Nazwa', validators=[InputRequired()])
    password = PasswordField('Hasło', validators=[InputRequired()])


class LoginForm(BasicLoginForm):
    code = StringField('Kod', validators=[InputRequired(), Length(6, 6)])
