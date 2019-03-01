import pytest

from devlog.models import User
from devlog.ext import db

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestUserObject(DevlogTests):

    def test_defaults(self):
        user = User(email='test.email@example.com')
        db.session.add(user)
        db.session.commit()
        assert user.id is not None
