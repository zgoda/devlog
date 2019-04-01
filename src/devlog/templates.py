from flask_babel import format_date

from .utils.pagination import url_for_other_page


def setup_filters(application):
    pass  # no filters yet


def setup_globals(application):
    application.jinja_env.globals.update(
        {'format_date': format_date, 'url_for_other_page': url_for_other_page}
    )


def setup_template_extensions(application):
    setup_filters(application)
    setup_globals(application)
