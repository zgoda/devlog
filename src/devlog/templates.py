from flask_babel import format_datetime
from wtforms.fields import HiddenField

from ._version import get_version
from .utils.app import Devlog
from .utils.pagination import url_for_other_page


def setup_globals(application: Devlog):
    application.jinja_env.globals.update({
        'format_datetime': format_datetime,
        'url_for_other_page': url_for_other_page,
        'version': get_version(),
        'is_hidden_field': lambda x: isinstance(x, HiddenField),
    })


def setup_template_extensions(application: Devlog):
    setup_globals(application)
