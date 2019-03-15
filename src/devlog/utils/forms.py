import attr
from flask import render_template_string
from flask_babel import lazy_gettext as gettext
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField

from ..ext import db


class Clickable:

    def render(self):
        return render_template_string(self.template, obj=self)


@attr.s
class Button(Clickable):
    type_ = attr.ib(default='submit')
    class_ = attr.ib(default='primary')
    icon = attr.ib(default='check')
    icon_type = attr.ib(default='fas')
    text = attr.ib('ok')
    link = attr.ib(default=False)

    template = '''
<button type="{{ obj.type_ }}" class="btn btn-{{ obj.class_ }}">
    <i class="{{ obj.icon_type }} fa-{{ obj.icon }}"></i>
    &nbsp;
    {{ obj.text }}
</button>'''.strip()


class DeleteForm(FlaskForm):
    delete_it = BooleanField(gettext('confirm'), default=False)

    buttons = [Button(text=gettext('confirm'))]

    def confirm(self):
        if self.delete_it.data:
            return True
        return False


class ObjectForm(FlaskForm):

    buttons = [Button(text=gettext('save'))]

    def save(self, obj, save=True):
        self.populate_obj(obj)
        db.session.add(obj)
        if save:
            db.session.commit()
        else:
            db.session.flush()
        return obj
