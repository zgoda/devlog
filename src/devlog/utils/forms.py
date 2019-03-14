import attr
from flask_babel import lazy_gettext as gettext
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField

from ..ext import db


@attr.s
class Button:
    type_ = attr.ib(default='submit')
    class_ = attr.ib(default='primary')
    icon = attr.ib(default='check')
    icon_type = attr.ib(default='fas')
    text = attr.ib('ok')
    link = attr.ib(default=False)


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
