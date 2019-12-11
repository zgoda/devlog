from flask_babel import lazy_gettext as gettext
from wtforms import validators
from wtforms.fields import BooleanField, SelectField, StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms_components.validators import Email

from ..models import User
from ..utils.forms import ObjectForm
from ..utils.i18n import (
    DEFAULT_LANGUAGE, DEFAULT_TIMEZONE, SUPPORTED_LANGUAGE_CHOICES, TIMEZONE_CHOICES,
)


class UserForm(ObjectForm):
    name = StringField(gettext('name'), validators=[validators.InputRequired()])
    blurb = TextAreaField(gettext('blurb'))
    blurb_markup_type = SelectField(
        gettext('blurb markup processor'),
        choices=User.SMP_CHOICES,
        validators=[validators.Optional()],
        default=User.SMP_NONE,
    )
    email = EmailField(gettext('email'), validators=[Email(), validators.Optional()])
    default_language = SelectField(
        gettext('default language'), choices=SUPPORTED_LANGUAGE_CHOICES,
        default=DEFAULT_LANGUAGE,
    )
    timezone = SelectField(
        gettext('timezone'), choices=TIMEZONE_CHOICES, default=DEFAULT_TIMEZONE,
    )
    active = BooleanField(gettext('active'), default=True)
    public = BooleanField(gettext('public'), default=False)

    def validate(self) -> bool:
        if not super().validate():
            return False
        result = True
        if self.active.data and not self.email.data:
            self.email.errors.append(
                gettext('user can not be activated without email'),
            )
            result = False
        return result
