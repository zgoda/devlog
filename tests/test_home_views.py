from flask import url_for

import pytest

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestMainPageAccountLinks(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.login_url = url_for('auth.login')
        self.logout_url = url_for('auth.logout')
        self.account_url = url_for('user.account')

    def test_anon_login_urls(self):
        r = self.client.get(url_for('home.index'))
        assert f'href="{self.login_url}"' in r.text
        assert f'href="{self.logout_url}"' not in r.text
        assert f'href="{self.account_url}"' not in r.text

    def test_authenticated_login_urls(self, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        self.login(user.email)
        r = self.client.get(url_for('home.index'))
        assert f'href="{self.login_url}"' not in r.text
        assert f'href="{self.logout_url}"' in r.text
        assert f'href="{self.account_url}"' in r.text
