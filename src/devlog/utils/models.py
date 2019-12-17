import collections

import markdown
from flask_sqlalchemy.model import Model as BaseModel

from .text import slugify


class MappedModelMixin:

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }


MarkupField = collections.namedtuple('MarkupField', 'source,dest')
SlugField = collections.namedtuple('SlugField', 'source,dest')


class TextProcessingMixin:

    @staticmethod
    def markup_to_html(instr: str) -> str:
        return markdown.markdown(
            instr, extensions=['fenced_code', 'codehilite'], output_format='html'
        )

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
            if source:
                value = target.markup_to_html(source)
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
