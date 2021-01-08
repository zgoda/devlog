import pytest
from flask import url_for


@pytest.mark.usefixtures('client_class')
class TestLogin:

    @pytest.fixture(autouse=True)
    def _set_up(self):
        self.url = url_for('api.login')

    def test_no_account(self):
        data = {'name': 'user1', 'password': 'pass'}
        rv = self.client.post(self.url, data=data)
        assert rv.status_code == 404
        data = rv.get_json()
        assert 'no such account' in data['message'].lower()

    def test_wrong_password(self, user_factory):
        user = user_factory(password='pass1')
        data = {'name': user.name, 'password': 'pass2'}
        rv = self.client.post(self.url, data=data)
        assert rv.status_code == 404
        data = rv.get_json()
        assert 'no such account' in data['message'].lower()

    def test_ok(self, user_factory):
        user = user_factory()
        data = {'name': user.name, 'password': user.password}
        rv = self.client.post(self.url, data=data)
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'token' in data
