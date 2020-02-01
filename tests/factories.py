import factory
from factory.alchemy import SQLAlchemyModelFactory
from werkzeug.security import generate_password_hash

from devlog.ext import db
from devlog.models import Blog, Post, User


class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'flush'


class UserFactory(BaseFactory):

    name = factory.Faker('name')
    password = factory.Faker('password')
    default_language = 'en'
    timezone = 'Europe/London'

    class Meta:
        model = User

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        kwargs['password'] = generate_password_hash(kwargs['password'])
        return kwargs


class BlogFactory(BaseFactory):

    name = factory.Faker('name')
    user = factory.SubFactory(UserFactory)
    active = True
    default = False

    class Meta:
        model = Blog


class PostFactory(BaseFactory):

    blog = factory.SubFactory(BlogFactory)
    author = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    text = factory.Faker('text')
    draft = True
    pinned = False

    class Meta:
        model = Post
