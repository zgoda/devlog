from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as gettext
from wtforms.widgets import HTMLString, html_params

from ..ext import db


class ObjectForm(FlaskForm):

    def save(self, obj, save=True):
        self.populate_obj(obj)
        db.session.add(obj)
        if save:
            db.session.commit()
        else:
            db.session.flush()
        return obj


class SubmitButton:

    def __init__(self, icon_type='fas', icon=None):
        self.icon_type = icon_type
        self.icon = icon

    def __call__(self, field, **kwargs):
        icon_class = ' '.join([self.icon_type, 'fa-%s' % self.icon])
        return HTMLString(
            '<button {params}><span {icon}></span>&nbsp;{text}</button>'.format(
                params=html_params(type='submit', class_='btn btn-primary'),
                icon=html_params(class_=icon_class),
                text=gettext('save'),
            )
        )
