import pytest
from flask import url_for

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestAuthViews(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.logout_url = url_for('auth.logout')

    def test_logout(self, user_factory):
        url = url_for('home.index')
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        self.login(user.name)
        rv = self.client.get(url)
        assert 'sign out' in rv.text
        assert 'sign in' not in rv.text
        self.client.get(self.logout_url, follow_redirects=True)
        rv = self.client.get(url)
        assert 'sign out' not in rv.text
        assert 'sign in' in rv.text
