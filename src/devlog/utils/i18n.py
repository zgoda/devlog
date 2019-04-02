import operator

import pytz
from babel import Locale
from babel.dates import get_timezone, get_timezone_location
from flask import session, request
from flask_babel import lazy_gettext as gettext
from flask_login import current_user

LANGUAGE_POLISH = 'pl'
LANGUAGE_ENGLISH = 'en'
SUPPORTED_LANGUAGES = [LANGUAGE_POLISH, LANGUAGE_ENGLISH]
SUPPORTED_LANGUAGE_CHOICES = (
    (LANGUAGE_POLISH, gettext('Polish')),
    (LANGUAGE_ENGLISH, gettext('English')),
)
DEFAULT_LANGUAGE = LANGUAGE_POLISH

TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]
DEFAULT_TIMEZONE = 'Europe/Warsaw'


def localized_timezone_choices(locale_name):
    if locale_name is None:
        return TIMEZONE_CHOICES
    locale = Locale.parse(locale_name)
    choices = []
    for tzname in pytz.common_timezones:
        tz = get_timezone(tzname)
        loc = get_timezone_location(tz, locale=locale)
        loc_name = f'{loc} ({tzname})'
        choices.append((tzname, loc_name))
    choices.sort(key=operator.itemgetter(-1))
    return choices


def get_user_language():
    lang = None
    if current_user.is_authenticated:
        lang = current_user.default_language
    if not lang:
        lang = session.get('lang')
    if lang is None:
        lang = request.accept_languages.best_match(SUPPORTED_LANGUAGES)
    return lang


def get_user_timezone():
    tzname = None
    if current_user.is_authenticated:
        tzname = current_user.timezone
    if not tzname:
        tzname = DEFAULT_TIMEZONE
    return tzname
