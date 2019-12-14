from dataclasses import dataclass
from typing import ClassVar

from flask import Markup, render_template_string
from flask_babel import lazy_gettext as gettext
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField

from ..ext import db


class Renderable:

    def render(self) -> Markup:
        return Markup(render_template_string(self.template, obj=self))


@dataclass
class Link(Renderable):
    href: str
    text: str = 'click'

    template: ClassVar[str] = ''.join([
        '<a href="{{ obj.href }}" class="button">',
        '{{ obj.text }}',
        '</a>',
    ])


@dataclass
class Button(Renderable):
    type_: str = 'submit'
    class_: str = 'primary'
    icon: str = 'check'
    icon_type: str = 'fas'
    text: str = 'ok'

    template: ClassVar[str] = ''.join([
        '<button type="{{ obj.type_ }}" class="button is-{{ obj.class_ }}">',
        '<span class="icon">',
        '<i class="{{ obj.icon_type }} fa-{{ obj.icon }}"></i>',
        '</span>',
        '&nbsp;',
        '<span>{{ obj.text }}</span>',
        '</button>',
    ])


class DeleteForm(FlaskForm):
    delete_it = BooleanField(gettext('confirm'), default=False)

    buttons = [Button(text=gettext('confirm'), icon='trash-alt')]

    def confirm(self):
        if self.delete_it.data:
            return True
        return False


class BaseForm(FlaskForm):

    buttons = [
        Button(text=gettext('save')),
        Link(href='javascript:history.back()', text=gettext('go back')),
    ]


class ObjectForm(BaseForm):

    def save(self, obj, save=True):
        self.populate_obj(obj)
        db.session.add(obj)
        if save:
            db.session.commit()
        else:
            db.session.flush()
        return obj
