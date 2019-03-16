import pytest
from flask.wrappers import Response
from pytest_factoryboy import register
from werkzeug.utils import cached_property

from devlog import make_app
from devlog.ext import db

from .factories import BlogFactory, UserFactory

register(UserFactory)
register(BlogFactory)


class TestResponse(Response):

    @cached_property
    def text(self):
        if self.mimetype.startswith('text'):
            return self.data.decode(self.charset)
        return self.data


@pytest.fixture
def app():
    app = make_app(env='test')
    app.response_class = TestResponse
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
