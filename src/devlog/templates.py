from flask_babel import format_date, get_locale
from wtforms.fields import HiddenField

from ._version import get_version
from .utils.pagination import url_for_other_page


def setup_filters(application):
    pass  # no filters yet


def setup_globals(application):
    application.jinja_env.globals.update({
        'format_date': format_date,
        'get_locale': get_locale,
        'url_for_other_page': url_for_other_page,
        'version': get_version(),
        'is_hidden_field': lambda x: isinstance(x, HiddenField),
    })


def setup_template_extensions(application):
    setup_filters(application)
    setup_globals(application)
