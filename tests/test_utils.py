from datetime import date, datetime

import pytest
import pytz
from flask import url_for

from devlog.ext import cache
from devlog.utils.pagination import get_page
from devlog.utils.text import normalize_post_date
from devlog.utils.views import is_redirect_safe, next_redirect


def test_pagination_invalid_param(app):
    val = 'dummy'
    with app.test_request_context(f'/?p={val}'):
        page = get_page()
        assert page != val
        assert page == 1


class TestPostDateNormalization:

    TZ = pytz.timezone('Europe/Warsaw')

    @pytest.mark.parametrize('value', ['', None], ids=['empty-str', 'none'])
    def test_noop(self, value):
        assert normalize_post_date(value) == value

    def test_date(self, mocker):
        value = date(2020, 6, 12)
        now = datetime(2020, 6, 14, 20, 21, 44)
        mocker.patch(
            'devlog.utils.text._get_now', mocker.Mock(return_value=now)
        )
        rv = normalize_post_date(value)
        assert rv.time() == (now - self.TZ.utcoffset(now, is_dst=False)).time()
        assert rv.date() == value

    @pytest.mark.parametrize('value', [
        '2020-06-12T20:21:44+02:00',
        '2020-06-12 20:21:44 CET',
        'June 12, 2020 9:21:44 PM'
    ])
    def test_str_valid_datetime(self, value):
        rv = normalize_post_date(value)
        assert isinstance(rv, datetime)
        assert rv.utcoffset() is None

    def test_datetime_aware(self):
        now = datetime(2020, 6, 14, 20, 21, 44)
        value = self.TZ.localize(now, is_dst=False)
        rv = normalize_post_date(value)
        assert rv.utcoffset() is None


class TestCacheExtension:

    def test_backend_is_redis(self, app):
        if 'redis' not in self.cache_type.lower():
            pytest.skip('To be run only with Redis cache')
        assert len(cache.cache._write_client.keys('*')) == 0
        cache.set('prefix1:key1', 'a')
        cache.set('prefix2:key1', 'b')
        assert len(cache.cache._write_client.keys('*')) == 2
        assert cache.delete_prefixed('prefix1') == 1
        assert len(cache.cache._write_client.keys('prefix1')) == 0

    def test_backend_is_not_redis(self, app):
        if 'redis' in self.cache_type.lower():
            pytest.skip("Can't be run with Redis cache")
        cache.set('prefix1:key1', 'a')
        cache.set('prefix2:key1', 'b')
        assert cache.delete_prefixed('prefix1') is None


class TestSafeRedirect:

    LOCAL_HOST_URL = 'http://localhost:5000'

    @pytest.mark.parametrize('target', [
        '/some/where',
        f'{LOCAL_HOST_URL}/some/where/else'
    ], ids=['relative', 'absolute'])
    def test_safe(self, target, mocker):
        fake_request = mocker.Mock(host_url=self.LOCAL_HOST_URL)
        mocker.patch('devlog.utils.views.request', fake_request)
        assert is_redirect_safe(target)

    @pytest.mark.parametrize('params', [
        [LOCAL_HOST_URL, 'sftp://localhost:5000/some/where'],
        [LOCAL_HOST_URL, 'http://otherhost:5000/some/where'],
    ], ids=['scheme', 'netloc'])
    def test_not_safe(self, params, mocker):
        host_url, target = params
        fake_request = mocker.Mock(host_url=host_url)
        mocker.patch('devlog.utils.views.request', fake_request)
        assert is_redirect_safe(target) is False


@pytest.mark.usefixtures('app')
class TestNextRedirect:

    LOCAL_HOST_URL = 'http://localhost:5000'
    FALLBACK_ENDPOINT = 'auth.login'

    def test_only_fallback(self):
        assert next_redirect(self.FALLBACK_ENDPOINT) == url_for(self.FALLBACK_ENDPOINT)

    def test_all_valid(self, mocker):
        u1 = '/some/where'
        u2 = '/other/place'
        fake_request = mocker.Mock(args={'next': u1}, host_url=self.LOCAL_HOST_URL)
        fake_session = {'next': u2}
        mocker.patch('devlog.utils.views.request', fake_request)
        mocker.patch('devlog.utils.views.session', fake_session)
        assert next_redirect(self.FALLBACK_ENDPOINT) == u1

    def test_2nd_valid(self, mocker):
        u1 = 'ftp://localhost:5000/some/where'
        u2 = '/other/place'
        fake_request = mocker.Mock(args={'next': u1}, host_url=self.LOCAL_HOST_URL)
        fake_session = {'next': u2}
        mocker.patch('devlog.utils.views.request', fake_request)
        mocker.patch('devlog.utils.views.session', fake_session)
        assert next_redirect(self.FALLBACK_ENDPOINT) == u2

    def test_all_invalid(self, mocker):
        u1 = 'ftp://localhost:5000/some/where'
        u2 = 'http://othersite/other/place'
        fake_request = mocker.Mock(args={'next': u1}, host_url=self.LOCAL_HOST_URL)
        fake_session = {'next': u2}
        mocker.patch('devlog.utils.views.request', fake_request)
        mocker.patch('devlog.utils.views.session', fake_session)
        assert next_redirect(self.FALLBACK_ENDPOINT) == url_for(self.FALLBACK_ENDPOINT)
