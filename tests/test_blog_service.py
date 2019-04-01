import pytest

from devlog.blog.service import get_recent

from . import DevlogTests


@pytest.mark.usefixtures('app')
class TestBlogService(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self, user_factory):
        self.public_user = user_factory()
        self.hidden_user = user_factory(public=False)

    def test_get_recent_public_only(self, blog_factory):
        blog_factory(user=self.public_user)
        blog_factory(user=self.public_user, public=False)
        blog_factory(user=self.hidden_user)
        blog_factory(user=self.hidden_user, public=False)
        blogs = get_recent().all()
        assert len(blogs) == 2

    def test_get_recent_public_only_extra_user(self, blog_factory):
        blog_factory(user=self.public_user)
        blog_factory(user=self.public_user, public=False)
        blog_factory(user=self.hidden_user)
        blog_factory(user=self.hidden_user, public=False)
        blogs = get_recent(extra_user=self.public_user).all()
        assert len(blogs) == 3

    def test_get_recent_all(self, blog_factory):
        blog_factory(user=self.public_user)
        blog_factory(user=self.public_user, public=False)
        blog_factory(user=self.hidden_user)
        blog_factory(user=self.hidden_user, public=False)
        blogs = get_recent(public_only=False).all()
        assert len(blogs) == 4

    def test_get_recent_limit(self, blog_factory):
        limit = 3
        blog_factory(user=self.public_user)
        blog_factory(user=self.public_user, public=False)
        blog_factory(user=self.hidden_user)
        blog_factory(user=self.hidden_user, public=False)
        blogs = get_recent(public_only=False, limit=limit).all()
        assert len(blogs) == limit
