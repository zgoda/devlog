import pytest

from devlog.models import User
from devlog.ext import db

from . import DevlogTests


@pytest.mark.usefixtures("app")
class TestUserObject(DevlogTests):
    def test_defaults(self):
        user = User(email="test.email@example.com", name="Ivory Tower")
        db.session.add(user)
        db.session.commit()
        assert user.id is not None

    def test_blurb_markdown(self, user_factory):
        text = "**bold**\n > blockquote"
        user = user_factory(
            name="Ivory Tower", blurb=text, blurb_markup_type=User.SMP_MARKDOWN
        )
        assert "<strong>bold</strong>" in user.blurb_html
        assert "<blockquote>" in user.blurb_html

    def test_blurb_textile(self, user_factory):
        text = "*bold*\n\nbq. blockquote"
        user = user_factory(
            name="Ivory Tower", blurb=text, blurb_markup_type=User.SMP_TEXTTILE
        )
        assert "<strong>bold</strong>" in user.blurb_html
        assert "<blockquote>" in user.blurb_html

    def test_blurb_rst(self, user_factory):
        text = "**bold**\n\n    blockquote"
        user = user_factory(
            name="Ivory Tower", blurb=text, blurb_markup_type=User.SMP_RST
        )
        assert "<strong>bold</strong>" in user.blurb_html
        assert "<blockquote>" in user.blurb_html
