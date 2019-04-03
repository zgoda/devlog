import pytest
from flask import url_for

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestAuthViews(DevlogTests):

    def test_logout_view(self, user_factory):
        url = url_for('home.index')
        user = user_factory(name='Ivory Tower')
        self.login(user.email)
        rv = self.client.get(url)
        assert 'sign out' in rv.text
        assert 'sign in' not in rv.text
        self.logout()
        rv = self.client.get(url)
        assert 'sign out' not in rv.text
        assert 'sign in' in rv.text

    def test_select_view(self):
        rv = self.client.get(url_for('auth.select'))
        assert 'Select login provider' in rv.text
