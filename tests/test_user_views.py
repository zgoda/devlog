from flask import url_for, escape

import pytest

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestUserViews(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.profile_url = url_for('user.profile')
        self.confirm_url = url_for('user.confirm_delete')
        self.delete_url = url_for('user.delete')

    def test_user_profile_anon_view(self):
        rv = self.client.get(self.profile_url)
        assert rv.status_code == 302

    def test_user_profile_authenticated_view(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(email=user.email)
        rv = self.client.get(self.profile_url)
        page = rv.data.decode('utf-8')
        assert f'value="{user.name}"' in page

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
        assert f'value="{new_name}"' in page

    def test_user_profile_authenticated_update_failure(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(email=user.email)
        new_email = 'invalid&email:com'
        data = {'email': new_email}
        rv = self.client.post(self.profile_url, data=data, follow_redirects=True)
        page = rv.data.decode('utf-8')
        assert f'value="{escape(new_email)}"' in page
        assert 'Invalid email address' in page

    def test_user_confirm_delete_anon_view(self):
        rv = self.client.get(self.confirm_url)
        assert rv.status_code == 302

    def test_user_confirm_delete_authenticated_view(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(email=user.email)
        rv = self.client.get(self.confirm_url, follow_redirects=True)
        page = rv.data.decode('utf-8')
        assert f'action="{self.delete_url}"' in page

    def test_user_delete_anon(self):
        rv = self.client.post(
            self.delete_url, data=dict(delete_it=True), follow_redirects=True,
        )
        page = rv.data.decode('utf-8')
        assert 'elect login provider' in page

    def test_user_delete_authenticated_confirm(self, user_factory):
        user_name = 'Ivory Tower'
        user = user_factory(name=user_name)
        self.login(email=user.email)
        rv = self.client.post(
            self.delete_url, data=dict(delete_it=True), follow_redirects=True,
        )
        page = rv.data.decode('utf-8')
        assert f'for user {user_name} deleted' in page

    def test_user_delete_authenticated_no_confirm(self, user_factory):
        user_name = 'Ivory Tower'
        user = user_factory(name=user_name)
        self.login(email=user.email)
        rv = self.client.post(
            self.delete_url, data={}, follow_redirects=True,
        )
        page = rv.data.decode('utf-8')
        assert f'action="{self.profile_url}"' in page
