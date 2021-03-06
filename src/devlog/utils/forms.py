from dataclasses import dataclass
from typing import ClassVar

from flask import Markup, render_template_string


class Renderable:

    def render(self):
        return Markup(render_template_string(self.template, obj=self))


@dataclass
class Button(Renderable):
    type_: str = 'submit'
    class_: str = 'primary'
    icon: str = 'check'
    text: str = 'ok'

    template: ClassVar[str] = (
        '<button type="{{ obj.type_ }}" class="button-{{ obj.class_ }}">'
        '<span class="icon">'
        '<svg><use xlink:href="#{{ obj.icon }}"></svg>'
        '</span>'
        '&nbsp;'
        '<span>{{ obj.text }}</span>'
        '</button>'
    )
