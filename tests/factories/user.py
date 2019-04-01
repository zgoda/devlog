import factory
from factory.alchemy import SQLAlchemyModelFactory

from devlog.ext import db
from devlog.models import User


class UserFactory(SQLAlchemyModelFactory):

    name = factory.Faker('name')
    email = factory.Faker('email')
    public = True
    default_language = 'en'
    timezone = 'Europe/London'

    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
