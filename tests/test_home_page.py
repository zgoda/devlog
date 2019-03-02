from flask import url_for

import pytest

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestMainPage(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.url = url_for('home.index')

    def test_anon_login_url(self):
        r = self.client.get(self.url)
        page = r.data.decode('utf-8')
        login_url = url_for('auth.select')
        assert login_url in page
