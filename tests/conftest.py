import os

import pytest
from flask.wrappers import Response
from pytest_factoryboy import register
from werkzeug.utils import cached_property

from devlog import make_app
from devlog.models import db, Post, Tag, TaggedPost

from .factories import PostFactory, TagFactory, TaggedPostFactory

register(TagFactory)
register(PostFactory)
register(TaggedPostFactory)


class TestResponse(Response):

    @cached_property
    def text(self):
        if self.mimetype.startswith('text'):
            return self.data.decode(self.charset)
        return self.data


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['pl_PL']


@pytest.fixture
def app(tmp_path):
    os.environ['FLASK_ENV'] = 'test'
    app = make_app(env='test')
    app.static_folder = str(tmp_path)
    app.response_class = TestResponse
    models = [Post, Tag, TaggedPost]
    with app.app_context():
        db.create_tables(models)
        yield app
        db.drop_tables(models)
