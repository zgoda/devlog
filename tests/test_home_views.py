from datetime import datetime

import pytest
from flask import url_for

from devlog.utils.text import slugify

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
        self.login(user.name)
        r = self.client.get(url_for('home.index'))
        assert f'href="{self.login_url}"' not in r.text
        assert f'href="{self.logout_url}"' in r.text
        assert f'href="{self.account_url}"' in r.text


@pytest.mark.usefixtures('client_class')
class TestViewSinglePost(DevlogTests):

    def test_ok(self, post_factory):
        title = 'test post 1'
        slug = slugify(title)
        y, m, d = 2020, 2, 2
        created = datetime(y, m, d)
        post_factory(title=title, created=created, draft=False)
        url = url_for('home.post', y=y, m=m, d=d, slug=slug)
        rv = self.client.get(url)
        assert rv.status_code == 200
        assert f'<h1>{title}</h1>' in rv.text

    def test_fail(self):
        title = 'test post 1'
        slug = slugify(title)
        y, m, d = 2020, 2, 2
        url = url_for('home.post', y=y, m=m, d=d, slug=slug)
        rv = self.client.get(url)
        assert rv.status_code == 404
