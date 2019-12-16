import pytest

from devlog.models import User
from devlog.ext import db

from . import DevlogTests


@pytest.mark.usefixtures('app')
class TestUserObject(DevlogTests):

    def test_defaults(self):
        user = User(name='Ivory Tower')
        user.set_password(self.default_pw)
        db.session.add(user)
        db.session.commit()
        assert user.id is not None

    def test_blurb_markdown(self, user_factory):
        text = '**bold**\n > blockquote'
        user = user_factory(
            name='Ivory Tower', blurb=text,
        )
        assert '<strong>bold</strong>' in user.blurb_html
        assert '<blockquote>' in user.blurb_html
