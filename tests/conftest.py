import os

import pytest
from flask.wrappers import Response
from pytest_factoryboy import register
from werkzeug.utils import cached_property

from devlog import make_app
from devlog.assets import all_css
from devlog.models import Post, Tag, TaggedPost, User, db

from .factories import PostFactory, TagFactory, TaggedPostFactory, UserFactory

register(UserFactory)
register(TagFactory)
register(PostFactory)
register(TaggedPostFactory)


def fake_gen_password_hash(password: str) -> str:
    return password


class TestResponse(Response):

    @cached_property
    def text(self):
        if self.mimetype.startswith('text'):
            return self.data.decode(self.charset)
        return self.data


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['pl_PL']


@pytest.fixture()
def app(mocker):
    mocker.patch('devlog.utils.security.generate_password_hash', fake_gen_password_hash)
    os.environ['FLASK_ENV'] = 'test'
    app = make_app(env='test')
    with app.app_context():
        all_css.build()
    app.response_class = TestResponse
    models = [Post, Tag, TaggedPost, User]
    with app.app_context():
        db.create_tables(models)
        yield app
        db.drop_tables(models)
