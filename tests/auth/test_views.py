import pytest
from flask import url_for


@pytest.mark.usefixtures('client_class')
class TestAuthViews:

    @pytest.fixture(autouse=True)
    def _set_up(self):
        self.url = url_for('auth.login')

    def test_no_user(self):
        data = {'name': 'username', 'password': 'password', 'code': '123456'}
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert 'Nieprawidłowe dane logowania' in rv.text
