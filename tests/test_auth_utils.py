from flask import url_for

import pytest

from devlog.models import User
from devlog.auth.utils import login_success


@pytest.mark.usefixtures('app')
class TestLoginSuccess:

    def test_existing(self, user_factory):
        email = 'ivory@tower.com'
        orig_name = 'Ivory Tower'
        token = 'token1'
        user_id = 'user_1'
        service = 'service_1'
        user_factory(
            name=orig_name, email=email, oauth_service=service,
            remote_user_id=user_id,
        )
        name = 'Infernal Rifleman'
        ret = login_success(email, token, user_id, service, name=name)
        assert ret.status_code == 302
        assert url_for('home.index') in ret.headers['Location']
        user = User.get_by_email(email)
        assert user.name == name

    def test_nonexisting(self):
        email = 'ivory@tower.com'
        name = 'Ivory Tower'
        token = 'token1'
        user_id = 'user_1'
        service = 'service_1'
        ret = login_success(email, token, user_id, service, name=name)
        assert ret.status_code == 302
        assert url_for('home.index') in ret.headers['Location']
        user = User.get_by_email(email)
        assert user.name == name
