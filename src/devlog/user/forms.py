from flask_babel import lazy_gettext as gettext
from wtforms.fields import BooleanField, SelectField, StringField, TextAreaField

from ..utils.forms import ObjectForm, input_required_validator
from ..utils.i18n import (
    DEFAULT_LANGUAGE, DEFAULT_TIMEZONE, SUPPORTED_LANGUAGE_CHOICES, TIMEZONE_CHOICES,
)


class UserForm(ObjectForm):
    name = StringField(gettext('name'), validators=[input_required_validator])
    blurb = TextAreaField(gettext('blurb'))
    default_language = SelectField(
        gettext('default language'), choices=SUPPORTED_LANGUAGE_CHOICES,
        default=DEFAULT_LANGUAGE,
    )
    timezone = SelectField(
        gettext('timezone'), choices=TIMEZONE_CHOICES, default=DEFAULT_TIMEZONE,
    )
    active = BooleanField(gettext('active'), default=True)
