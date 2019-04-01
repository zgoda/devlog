from flask import url_for, escape

import pytest

from . import DevlogTests


@pytest.mark.usefixtures('app')
class UserViewsTests(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.ACCOUNT_URL = url_for('user.account')
        self.CONFIRM_URL = url_for('user.confirm_delete')
        self.DELETE_URL = url_for('user.delete')


@pytest.mark.usefixtures('client_class')
class TestAccountView(UserViewsTests):

    def test_user_account_anon_view(self):
        rv = self.client.get(self.ACCOUNT_URL)
        assert rv.status_code == 302
        assert url_for('auth.select') in rv.headers['Location']

    def test_user_account_authenticated_view(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(email=user.email)
        rv = self.client.get(self.ACCOUNT_URL)
        assert f'value="{user.name}"' in rv.text

    def test_user_account_anon_update(self):
        data = {'name': 'New Name'}
        rv = self.client.post(self.ACCOUNT_URL, data=data)
        assert rv.status_code == 302
        assert url_for('auth.select') in rv.headers['Location']

    def test_user_account_authenticated_update(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(email=user.email)
        new_name = 'Infernal Amendment'
        data = {'name': new_name}
        rv = self.client.post(self.ACCOUNT_URL, data=data, follow_redirects=True)
        assert f'Data for user {new_name} has been saved' in rv.text

    def test_user_account_authenticated_update_failure(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(email=user.email)
        new_email = 'invalid&email:com'
        data = {'email': new_email}
        rv = self.client.post(self.ACCOUNT_URL, data=data, follow_redirects=True)
        assert f'value="{escape(new_email)}"' in rv.text
        assert 'Invalid email address' in rv.text


@pytest.mark.usefixtures('client_class')
class TestDeleteViews(UserViewsTests):

    def test_user_confirm_delete_anon_view(self):
        rv = self.client.get(self.CONFIRM_URL)
        assert rv.status_code == 302
        assert url_for('auth.select') in rv.headers['Location']

    def test_user_confirm_delete_authenticated_view(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(email=user.email)
        rv = self.client.get(self.CONFIRM_URL, follow_redirects=True)
        assert f'action="{self.DELETE_URL}"' in rv.text

    def test_user_delete_anon(self):
        rv = self.client.post(
            self.DELETE_URL, data={'delete_it': True}
        )
        assert rv.status_code == 302
        assert url_for('auth.select') in rv.headers['Location']

    def test_user_delete_authenticated_confirm(self, user_factory):
        user_name = 'Ivory Tower'
        user = user_factory(name=user_name)
        self.login(email=user.email)
        rv = self.client.post(
            self.DELETE_URL, data={'delete_it': True}, follow_redirects=True
        )
        assert f'for user {user_name} deleted' in rv.text

    def test_user_delete_authenticated_no_confirm(self, user_factory):
        user_name = 'Ivory Tower'
        user = user_factory(name=user_name)
        self.login(email=user.email)
        rv = self.client.post(self.DELETE_URL, data={}, follow_redirects=True)
        assert f'action="{self.ACCOUNT_URL}"' in rv.text


@pytest.mark.usefixtures('client_class')
class TestProfileView(UserViewsTests):

    def url(self, user):
        return url_for('user.profile', user_id=user.id)

    def test_anon(self, user_factory):
        user = user_factory(name='Ivory Tower')
        rv = self.client.get(self.url(user))
        assert rv.status_code == 302
        assert url_for('auth.select') in rv.headers['Location']

    def test_authenticated_profile_accessible(self, user_factory):
        user = user_factory(name='Ivory Tower', public=True, active=True)
        actor = user_factory(name='Snowflake White')
        self.login(actor.email)
        rv = self.client.get(self.url(user))
        assert 'Profile page for Ivory Tower' in rv.text

    @pytest.mark.parametrize('public,active', [
            (False, True),
            (True, False),
            (False, False),
        ], ids=['private-active', 'public-inactive', 'private-inactive'],
    )
    def test_authenticated_profile_inaccessible(self, public, active, user_factory):
        user = user_factory(name='Ivory Tower', public=public, active=active)
        actor = user_factory(name='Snowflake White')
        self.login(actor.email)
        rv = self.client.get(self.url(user))
        assert rv.status_code == 404

    def test_owner_profile_accessible(self, user_factory):
        user = user_factory(name='Ivory Tower', public=True, active=True)
        self.login(user.email)
        rv = self.client.get(self.url(user))
        assert 'Profile page for Ivory Tower' in rv.text

    @pytest.mark.parametrize('public,active', [
            (False, True),
            (True, False),
            (False, False)
        ], ids=['private-active', 'public-inactive', 'private-inactive'],
    )
    def test_owner_profile_inaccessible(self, public, active, user_factory):
        user = user_factory(name='Ivory Tower', public=public, active=active)
        self.login(user.email)
        rv = self.client.get(self.url(user))
        assert rv.status_code == 200
        assert 'no one except you can see this page' in rv.text
