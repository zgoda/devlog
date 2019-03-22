import collections

import markdown2
import textile
from docutils.core import publish_parts
from flask_babel import lazy_gettext as gettext
from flask_sqlalchemy.model import Model as BaseModel

from .text import slugify


class MappedModelMixin:

    __mapper_args__ = {"confirm_deleted_rows": False}


MarkupField = collections.namedtuple("MarkupField", "source,dest,processor")
SlugField = collections.namedtuple("SlugField", "source,dest")


class TextProcessingMixin:

    SMP_NONE = ""
    SMP_TEXTTILE = "textile"
    SMP_RST = "rst"
    SMP_MARKDOWN = "markdown"

    SMP_CHOICES = (
        (SMP_NONE, gettext("None")),
        (SMP_MARKDOWN, "Markdown"),
        (SMP_TEXTTILE, "Textile"),
        (SMP_RST, "reStructuredText"),
    )

    def markup_to_html(self, instr, processor):
        if processor == self.SMP_RST:
            config = {"input_encoding": "unicode", "output_encoding": "unicode"}
            parts = publish_parts(instr, writer_name="html5", settings_overrides=config)
            return parts["fragment"]
        elif processor == self.SMP_MARKDOWN:
            return markdown2.markdown(instr, safe_mode=True)
        elif processor == self.SMP_TEXTTILE:
            return textile.textile(instr, html_type="html5")
        return instr

    @classmethod
    def markup_fields(cls):
        return []

    @classmethod
    def slug_fields(cls):
        return []

    @classmethod
    def pre_save(cls, mapper, connection, target):
        mkp_fields = cls.markup_fields()
        for field in mkp_fields:
            source = getattr(target, field.source, None)
            processor = getattr(target, field.processor, None)
            if source and processor:
                value = target.markup_to_html(source, processor)
                setattr(target, field.dest, value)
            else:
                setattr(target, field.dest, None)
        sg_fields = cls.slug_fields()
        for field in sg_fields:
            source = getattr(target, field.source, None)
            if source:
                value = slugify(source)
                setattr(target, field.dest, value)


class Model(BaseModel, MappedModelMixin):
    pass
