from flask_babel import lazy_gettext as gettext
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, StringField
from wtforms.widgets import HTMLString, html_params

from ..ext import db


class SubmitButton:

    def __init__(self, button_type='primary', icon_type='fas', icon='sticky-note', text=None):
        self.icon_type = icon_type
        self.icon = icon
        self.button_type = button_type
        if text is None:
            text = gettext('save')
        self.text = text

    def __call__(self, field, **kwargs):
        icon_class = ' '.join([self.icon_type, f'fa-{self.icon}'])
        button_class = ' '.join(['btn', f'btn-{self.button_type}'])
        return HTMLString(
            '<button {params}><span {icon}></span>&nbsp;{text}</button>'.format(
                params=html_params(type='submit', class_=button_class),
                icon=html_params(class_=icon_class),
                text=self.text,
            )
        )


class DeleteForm(FlaskForm):
    delete_it = BooleanField(gettext('confirm'), default=False)
    submit_button = StringField('', widget=SubmitButton(icon='check', text=gettext('confirm')))

    def confirm(self):
        if self.delete_it.data:
            return True
        return False


class ObjectForm(FlaskForm):

    def save(self, obj, save=True):
        self.populate_obj(obj)
        db.session.add(obj)
        if save:
            db.session.commit()
        else:
            db.session.flush()
        return obj
