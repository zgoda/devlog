from flask_sqlalchemy.model import Model


class MappedModelMixin:

    __mapper_args__ = {
        'confirm_deleted_rows': False,
    }


class Model(Model, MappedModelMixin):
    pass
