from flask import url_for, escape

import pytest

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestUserViews(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.profile_url = url_for('user.profile')

    def test_user_profile_anon_view(self):
        rv = self.client.get(self.profile_url)
        assert rv.status_code == 302

    def test_user_profile_authenticated_view(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(email=user.email)
        rv = self.client.get(self.profile_url)
        page = rv.data.decode('utf-8')
        assert 'value="{}"'.format(user.name) in page

    def test_user_profile_anon_update(self):
        data = {'name': 'New Name'}
        rv = self.client.post(self.profile_url, data=data)
        assert rv.status_code == 302

    def test_user_profile_authenticated_update(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(email=user.email)
        new_name = 'Infernal Amendment'
        data = {'name': new_name}
        rv = self.client.post(self.profile_url, data=data, follow_redirects=True)
        page = rv.data.decode('utf-8')
        assert 'value="{}"'.format(new_name) in page

    def test_user_profile_authenticated_update_failure(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(email=user.email)
        new_email = 'invalid&email:com'
        data = {'email': new_email}
        rv = self.client.post(self.profile_url, data=data, follow_redirects=True)
        page = rv.data.decode('utf-8')
        assert 'value="{}"'.format(escape(new_email)) in page
        assert 'Invalid email address' in page
