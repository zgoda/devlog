import os

import pytest
from flask.wrappers import Response
from pytest_factoryboy import register
from werkzeug.utils import cached_property

from devlog import make_app
from devlog.assets import all_css
from devlog.models import MODELS, db

from .factories import (
    LinkFactory, PostFactory, TagFactory, TaggedPostFactory, UserFactory,
)

register(TagFactory)
register(PostFactory)
register(TaggedPostFactory)
register(LinkFactory)
register(UserFactory)


class TestResponse(Response):

    @cached_property
    def text(self):
        if self.mimetype.startswith('text'):
            return self.data.decode(self.charset)
        return self.data


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['pl_PL']


def fake_gen_password_hash(password):
    return password


def fake_check_password_hash(stored, password):
    return stored == password


@pytest.fixture()
def app(mocker):
    mocker.patch('devlog.models.generate_password_hash', fake_gen_password_hash)
    mocker.patch('devlog.models.check_password_hash', fake_check_password_hash)
    os.environ['FLASK_ENV'] = 'test'
    app = make_app(env='test')
    with app.app_context():
        all_css.build()
    app.response_class = TestResponse
    with app.app_context():
        db.create_tables(MODELS)
        yield app
        db.drop_tables(MODELS)
