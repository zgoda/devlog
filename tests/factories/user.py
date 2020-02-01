import factory
from factory.alchemy import SQLAlchemyModelFactory

from devlog.ext import db
from devlog.models import User
from werkzeug.security import generate_password_hash


class UserFactory(SQLAlchemyModelFactory):

    name = factory.Faker('name')
    password = factory.Faker('password')
    default_language = 'en'
    timezone = 'Europe/London'

    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'flush'

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        kwargs['password'] = generate_password_hash(kwargs['password'])
        return kwargs
