import pytest
from flask import url_for


@pytest.mark.usefixtures('client_class')
class TestQuipCollection:

    @pytest.fixture(autouse=True)
    def _set_up(self):
        self.url = url_for('api.quip-collection')

    def test_get_anon(self):
        rv = self.client.get(self.url)
        assert rv.status_code == 401
        data = rv.get_json()
        assert 'authorization required' in data['message'].lower()

    def test_post_anon(self):
        rv = self.client.post(self.url, data={'data': 'dummy'})
        assert rv.status_code == 401
        data = rv.get_json()
        assert 'authorization required' in data['message'].lower()

    def test_get_empty(self, login, user_factory):
        user = user_factory()
        token = login(user.name, user.password)
        rv = self.client.get(self.url, headers={'Authorization': f'Basic {token}'})
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'quips' in data
        assert bool(data['quips']) is False
