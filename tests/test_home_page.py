from flask import url_for

import pytest

from . import DevlogTests


@pytest.mark.usefixtures("client_class")
class TestMainPage(DevlogTests):

    def test_anon_login_url(self):
        r = self.client.get(url_for("home.index"))
        assert url_for("auth.select") in r.text
