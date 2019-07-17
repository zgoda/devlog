import attr
from flask import Markup, render_template_string
from flask_babel import lazy_gettext as gettext
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField

from ..ext import db


class Renderable:

    def render(self):
        return Markup(render_template_string(self.template, obj=self))


@attr.s  # noqa: H601
class Link(Renderable):
    href = attr.ib()
    text = attr.ib(default='click')

    template = ''.join([
        '<a href="{{ obj.href }}" class="button">',
        '{{ obj.text }}',
        '</a>',
    ])


@attr.s  # noqa: H601
class Button(Renderable):
    type_ = attr.ib(default='submit')
    class_ = attr.ib(default='primary')
    icon = attr.ib(default='check')
    icon_type = attr.ib(default='fas')
    text = attr.ib('ok')

    template = ''.join([
        '<button type="{{ obj.type_ }}" class="button is-{{ obj.class_ }}">',
        '<span class="icon">',
        '<i class="{{ obj.icon_type }} fa-{{ obj.icon }}"></i>',
        '</span>',
        '&nbsp;',
        '<span>{{ obj.text }}</span>',
        '</button>',
    ])


class DeleteForm(FlaskForm):  # noqa: H601
    delete_it = BooleanField(gettext('confirm'), default=False)

    buttons = [Button(text=gettext('confirm'), icon='trash-alt')]

    def confirm(self):
        if self.delete_it.data:
            return True
        return False


class ObjectForm(FlaskForm):  # noqa: H601

    buttons = [
        Button(text=gettext('save')),
        Link(href='javascript:history.back()', text=gettext('go back')),
    ]

    def save(self, obj, save=True):
        self.populate_obj(obj)
        db.session.add(obj)
        if save:
            db.session.commit()
        else:
            db.session.flush()
        return obj
