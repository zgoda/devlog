from factory.alchemy import SQLAlchemyModelFactory

from devlog.ext import db
from devlog.models import Blog


class BlogFactory(SQLAlchemyModelFactory):

    active = True
    public = True
    default = False

    class Meta:
        model = Blog
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
