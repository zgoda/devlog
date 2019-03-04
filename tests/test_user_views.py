from flask import url_for

import pytest

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestUserViews(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.profile_url = url_for('user.profile')

    def test_user_profile_anon(self):
        rv = self.client.get(self.profile_url)
        assert rv.status_code == 302

    def test_user_profile_authenticated(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(email=user.email)
        rv = self.client.get(self.profile_url)
        page = rv.data.decode('utf-8')
        assert 'value="{}"'.format(user.name) in page
