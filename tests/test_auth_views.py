import pytest
from flask import url_for

from devlog.models import User

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestAuthViews(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.register_url = url_for('auth.register')
        self.logout_url = url_for('auth.logout')

    def test_register_anon_get(self):
        rv = self.client.get(self.register_url)
        assert 'sign out' not in rv.text
        assert 'sign in' in rv.text
        assert f'action="{self.register_url}"' in rv.text

    def test_register_authenticated_get(self, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        self.login(user.email)
        rv = self.client.get(self.register_url)
        assert 'sign out' not in rv.text
        assert 'sign in' in rv.text
        assert f'action="{self.register_url}"' in rv.text

    def test_register_anon_post(self):
        email = 'dummy@test.info'
        password = 'pass'
        data = {'email': email, 'password1': password, 'password2': password}
        rv = self.client.post(self.register_url, data=data, follow_redirects=True)
        assert f'account for {email} has been registered' in rv.text
        assert 'sign out' in rv.text
        assert 'sign in' not in rv.text
        user_obj = User.get_by_email(email)
        assert user_obj.check_password(password)

    def test_register_authenticated_post(self, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        self.login(user.email)
        email = 'dummy@test.info'
        password = 'pass'
        data = {'email': email, 'password1': password, 'password2': password}
        rv = self.client.post(self.register_url, data=data, follow_redirects=True)
        assert f'account for {email} has been registered' in rv.text
        assert 'sign out' in rv.text
        assert 'sign in' not in rv.text
        user_obj = User.get_by_email(email)
        assert user_obj.check_password(password)

    def test_logout(self, user_factory):
        url = url_for('home.index')
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        self.login(user.email)
        rv = self.client.get(url)
        assert 'sign out' in rv.text
        assert 'sign in' not in rv.text
        self.client.get(self.logout_url, follow_redirects=True)
        rv = self.client.get(url)
        assert 'sign out' not in rv.text
        assert 'sign in' in rv.text
