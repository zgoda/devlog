import collections

import markdown2
import textile
from docutils.core import publish_parts
from flask_babel import lazy_gettext as gettext
from flask_sqlalchemy.model import Model as BaseModel


class MappedModelMixin:

    __mapper_args__ = {
        'confirm_deleted_rows': False,
    }


MarkupFields = collections.namedtuple('MarkupFields', 'source,dest,processor')


class MarkupProcessingMixin:

    SMP_NONE = ''
    SMP_TEXTTILE = 'textile'
    SMP_RST = 'rst'
    SMP_MARKDOWN = 'markdown'

    SMP_CHOICES = (
        (SMP_NONE, gettext('None')),
        (SMP_MARKDOWN, 'Markdown'),
        (SMP_TEXTTILE, 'Textile'),
        (SMP_RST, 'reStructuredText'),
    )

    def markup_to_html(self, instr, processor):
        if processor == self.SMP_RST:
            config = {
                'input_encoding': 'unicode',
                'output_encoding': 'unicode',
            }
            parts = publish_parts(
                instr, writer_name='html5', settings_overrides=config,
            )
            return parts['fragment']
        elif processor == self.SMP_MARKDOWN:
            return markdown2.markdown(instr, safe_mode=True)
        elif processor == self.SMP_TEXTTILE:
            return textile.textile(instr, html_type='html5')
        return instr

    @classmethod
    def markup_fields(cls):
        raise NotImplementedError()

    @classmethod
    def process_markup(cls, mapper, connection, target):
        fields = cls.markup_fields()
        source = getattr(target, fields.source)
        processor = getattr(target, fields.processor)
        if source and processor:
            value = target.markup_to_html(source, processor)
            setattr(target, fields.dest, value)
        else:
            setattr(target, fields.dest, None)


class Model(BaseModel, MappedModelMixin):
    pass
