import time

import pytest
from flask import url_for

from devlog.ext import cache


@pytest.mark.usefixtures('client_class')
class TestAuthDecorator:

    @pytest.fixture(autouse=True)
    def _set_up(self):
        self.url = url_for('api.quip-collection')

    def test_anon(self):
        rv = self.client.get(self.url)
        assert rv.status_code == 401
        data = rv.get_json()
        assert 'message' in data
        assert 'authorization required' in data['message'].lower()

    @pytest.mark.parametrize('value', [
        'wrong', 'this is also wrong'
    ], ids=['not-enough', 'too-many'])
    def test_invalid_header(self, value):
        rv = self.client.get(self.url, headers={'Authorization': value})
        assert rv.status_code == 401
        data = rv.get_json()
        assert 'message' in data
        assert 'invalid authentication header' in data['message'].lower()

    def test_invalid_auth_type(self):
        rv = self.client.get(self.url, headers={'Authorization': 'Invalid token'})
        assert rv.status_code == 401
        data = rv.get_json()
        assert 'message' in data
        assert 'invalid authentication type' in data['message'].lower()

    def test_user_not_found(self, login, user_factory):
        user = user_factory(name='user_1')
        token = login(user.name, user.password)
        user.delete_instance()
        cache.clear()
        rv = self.client.get(self.url, headers={'Authorization': f'Basic {token}'})
        assert rv.status_code == 401
        data = rv.get_json()
        assert 'message' in data
        assert 'invalid token' in data['message'].lower()

    def test_token_tampered(self, login, user_factory):
        user = user_factory(name='user_1')
        token = login(user.name, user.password)[:-1]
        rv = self.client.get(self.url, headers={'Authorization': f'Basic {token}'})
        assert rv.status_code == 401
        data = rv.get_json()
        assert 'message' in data
        assert 'invalid token' in data['message'].lower()

    @pytest.mark.options(TOKEN_MAX_AGE=1)
    def test_token_expired(self, login, user_factory):
        user = user_factory(name='user_1')
        token = login(user.name, user.password)
        time.sleep(2)
        rv = self.client.get(self.url, headers={'Authorization': f'Basic {token}'})
        assert rv.status_code == 400
        data = rv.get_json()
        assert 'message' in data
        assert 'token expired' in data['message'].lower()
