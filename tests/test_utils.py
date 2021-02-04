from datetime import date, datetime

import pytest
import pytz

from devlog.ext import cache
from devlog.utils.pagination import get_page
from devlog.utils.text import normalize_post_date


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
        if self.cache_type != 'redis':
            pytest.skip('To be run only with Redis cache')
        assert len(cache.cache._write_client.keys('*')) == 0
        cache.set('prefix1:key1', 'a')
        cache.set('prefix2:key1', 'b')
        assert len(cache.cache._write_client.keys('*')) == 2
        assert cache.delete_prefixed('prefix1') == 1
        assert len(cache.cache._write_client.keys('prefix1')) == 0

    def test_backend_is_not_redis(self, app):
        if self.cache_type == 'redis':
            pytest.skip("Can't be run with Redis cache")
        cache.set('prefix1:key1', 'a')
        cache.set('prefix2:key1', 'b')
        assert cache.delete_prefixed('prefix1') is None
