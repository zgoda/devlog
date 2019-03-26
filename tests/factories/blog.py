import factory
from factory.alchemy import SQLAlchemyModelFactory

from devlog.ext import db
from devlog.models import Blog

from .user import UserFactory


class BlogFactory(SQLAlchemyModelFactory):

    name = factory.Faker("name")
    user = factory.SubFactory(UserFactory)
    active = True
    public = True
    default = False

    class Meta:
        model = Blog
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"
