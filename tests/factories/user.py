import factory
from factory.alchemy import SQLAlchemyModelFactory

from devlog.ext import db
from devlog.models import User


class UserFactory(SQLAlchemyModelFactory):

    email = factory.Faker('email')
    public = True

    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
