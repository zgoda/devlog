import factory
from factory.alchemy import SQLAlchemyModelFactory

from devlog.ext import db
from devlog.models import Post

from .blog import BlogFactory


class PostFactory(SQLAlchemyModelFactory):

    blog = factory.SubFactory(BlogFactory)
    title = factory.Faker('sentence')
    text = factory.Faker('text')
    draft = True
    pinned = False

    class Meta:
        model = Post
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'flush'
