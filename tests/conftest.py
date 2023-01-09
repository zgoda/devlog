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
    LinkFactory, PostFactory, TagFactory, TaggedPostFactory,
)

register(TagFactory)
register(PostFactory)
register(TaggedPostFactory)
register(LinkFactory)


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
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def _app_fixture():
    app = make_app(env='test')
    app.testing = True
    with app.app_context():
        all_css.build()
    app.response_class = TestResponse
    return app


@pytest.fixture(
    params=['flask_caching.backends.NullCache', 'flask_caching.backends.RedisCache'],
    ids=['null-cache', 'redis-cache'],
)
def app(request):
    cache_type = request.param
    if request.cls:
        request.cls.cache_type = cache_type
    config_test.CACHE_TYPE = cache_type
    config_test.CACHE_REDIS_HOST = fakeredis.FakeStrictRedis()
    app = make_app(env='test')
    app.testing = True
    with app.app_context():
        all_css.build()
    app.response_class = TestResponse
    with app.app_context():
        db.create_tables(MODELS)
        yield app
        db.drop_tables(MODELS)
