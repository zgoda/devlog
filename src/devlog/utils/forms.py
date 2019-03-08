from flask_babel import lazy_gettext as gettext
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField
from wtforms.widgets import HTMLString, html_params

from ..ext import db


class DeleteForm(FlaskForm):
    delete_id = BooleanField(gettext('confirm'), default=False)


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

    def __init__(self, button_type='primary', icon_type='fas', icon='sticky-note'):
        self.icon_type = icon_type
        self.icon = icon
        self.button_type = button_type

    def __call__(self, field, **kwargs):
        icon_class = ' '.join([self.icon_type, f'fa-{self.icon}'])
        button_class = ' '.join(['btn', f'btn-{self.button_type}'])
        return HTMLString(
            '<button {params}><span {icon}></span>&nbsp;{text}</button>'.format(
                params=html_params(type='submit', class_=button_class),
                icon=html_params(class_=icon_class),
                text=gettext('save'),
            )
        )
