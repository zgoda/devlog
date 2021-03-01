import os

import fakeredis
import pytest
import responses
from flask.wrappers import Response
from pytest_factoryboy import register
from werkzeug.utils import cached_property

from devlog import config_test, make_app
from devlog.assets import all_css
from devlog.models import MODELS, db

from .factories import (
    LinkFactory, PostFactory, QuipFactory, TagFactory, TaggedPostFactory, UserFactory,
)

register(TagFactory)
register(PostFactory)
register(TaggedPostFactory)
register(LinkFactory)
register(UserFactory)
register(QuipFactory)


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
def api_login(client):
    def _login(name: str, password: str):
        rv = client.post('/api/v1/login', data={'name': name, 'password': password})
        data = rv.get_json()
        return data['token']
    return _login


@pytest.fixture()
def login(client):
    def _login(name: str, password: str):
        return client.post(
            '/auth/login', data={'name': name, 'password': password},
            follow_redirects=True,
        )
    return _login


@pytest.fixture()
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def fake_gen_password_hash(password):
    return password


def fake_check_password_hash(stored, password):
    return stored == password


def _app_fixture(env, mocker):
    mocker.patch('devlog.models.generate_password_hash', fake_gen_password_hash)
    mocker.patch('devlog.models.check_password_hash', fake_check_password_hash)
    os.environ['FLASK_ENV'] = 'test'
    app = make_app(env=env)
    with app.app_context():
        all_css.build()
    app.response_class = TestResponse
    return app


@pytest.fixture(params=['null', 'redis'], ids=['null-cache', 'redis-cache'])
def app(request, mocker):
    mocker.patch('devlog.models.generate_password_hash', fake_gen_password_hash)
    mocker.patch('devlog.models.check_password_hash', fake_check_password_hash)
    os.environ['FLASK_ENV'] = 'test'
    cache_type = request.param
    if request.cls:
        request.cls.cache_type = cache_type
    config_test.CACHE_TYPE = cache_type
    config_test.CACHE_REDIS_HOST = fakeredis.FakeStrictRedis()
    app = make_app(env='test')
    with app.app_context():
        all_css.build()
    app.response_class = TestResponse
    with app.app_context():
        db.create_tables(MODELS)
        yield app
        db.drop_tables(MODELS)
