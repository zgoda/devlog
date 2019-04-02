import pytest

from devlog.post.service import get_recent

from . import DevlogTests


@pytest.mark.usefixtures('app')
class TestPostService(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self, user_factory):
        self.user_1 = user_factory(name='Ivory Tower')
        self.user_2 = user_factory(name='Tom Jones')

    def test_get_recent_public_only(self, blog_factory, post_factory):
        blog_1 = blog_factory(user=self.user_1, public=True)
        blog_2 = blog_factory(user=self.user_2, public=True)
        post_factory(blog=blog_1, draft=False)
        post_factory(blog=blog_1, draft=False, public=False)
        post_factory(blog=blog_2, draft=False)
        post_factory(blog=blog_2, draft=False, public=False)
        posts = get_recent().all()
        assert len(posts) == 2

    def test_get_recent_public_only_extra_user(self, blog_factory, post_factory):
        blog_1 = blog_factory(user=self.user_1, public=True)
        blog_2 = blog_factory(user=self.user_2, public=True)
        post_factory(blog=blog_1, draft=False)
        post_factory(blog=blog_1, draft=False, public=False)
        post_factory(blog=blog_2, draft=False)
        post_factory(blog=blog_2, draft=False, public=False)
        posts = get_recent(extra_user=blog_1.user).all()
        assert len(posts) == 3

    def test_get_recent_all(self, blog_factory, post_factory):
        blog_1 = blog_factory(user=self.user_1, public=True)
        blog_2 = blog_factory(user=self.user_2, public=True)
        post_factory(blog=blog_1, draft=False)
        post_factory(blog=blog_1, draft=False, public=False)
        post_factory(blog=blog_2, draft=False)
        post_factory(blog=blog_2, draft=False, public=False)
        posts = get_recent(public_only=False).all()
        assert len(posts) == 4

    def test_get_recent_drafts(self, blog_factory, post_factory):
        blog_1 = blog_factory(user=self.user_1, public=True)
        blog_2 = blog_factory(user=self.user_2, public=True)
        post_factory(blog=blog_1, draft=False)
        post_factory(blog=blog_1, draft=False, public=False)
        post_factory(blog=blog_1, draft=True)
        post_factory(blog=blog_2, draft=False)
        post_factory(blog=blog_2, draft=False, public=False)
        posts = get_recent(public_only=False, drafts=True).all()
        assert len(posts) == 5

    def test_get_recent_limit(self, blog_factory, post_factory):
        limit = 3
        blog_1 = blog_factory(user=self.user_1, public=True)
        blog_2 = blog_factory(user=self.user_2, public=True)
        post_factory(blog=blog_1, draft=False)
        post_factory(blog=blog_1, draft=False, public=False)
        post_factory(blog=blog_2, draft=False)
        post_factory(blog=blog_2, draft=False, public=False)
        posts = get_recent(public_only=False, limit=limit).all()
        assert len(posts) == limit
