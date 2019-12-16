from flask import url_for

import pytest

from . import DevlogTests


@pytest.mark.usefixtures('app')
class UserViewsTests(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.ACCOUNT_URL = url_for('user.account')


@pytest.mark.usefixtures('client_class')
class TestAccountView(UserViewsTests):

    def test_user_account_anon_view(self):
        rv = self.client.get(self.ACCOUNT_URL)
        assert rv.status_code == 302
        assert url_for('auth.login') in rv.headers['Location']

    def test_user_account_authenticated_view(self, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        self.login(user.name)
        rv = self.client.get(self.ACCOUNT_URL)
        assert f'value="{user.name}"' in rv.text

    def test_user_account_anon_update(self):
        data = {'name': 'New Name'}
        rv = self.client.post(self.ACCOUNT_URL, data=data)
        assert rv.status_code == 302
        assert url_for('auth.login') in rv.headers['Location']

    def test_user_account_authenticated_update(self, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        self.login(user.name)
        new_name = 'Infernal Amendment'
        data = {'name': new_name}
        rv = self.client.post(self.ACCOUNT_URL, data=data, follow_redirects=True)
        assert f'user {user.name} details have been saved' in rv.text
