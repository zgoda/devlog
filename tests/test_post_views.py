import pytest
from flask import url_for

from . import DevlogTests


@pytest.mark.usefixtures("client_class")
class TestPostCreateView(DevlogTests):
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.data_ok = {"title": "Post No. 1", "text": "Short introduction"}
        self.data_incomplete = {"text": "Short introduction"}

    def url(self, blog):
        return url_for("post.create", blog_id=blog.id)

    def test_anon_get(self, blog_factory):
        blog = blog_factory(name="Infernal Tendencies")
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 302
        assert url_for("auth.select") in rv.headers["Location"]

    def test_authenticated_get(self, blog_factory, user_factory):
        blog = blog_factory(name="Infernal Tendencies")
        user = user_factory(name="Ivory Tower")
        self.login(user.email)
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 404

    def test_owner_get(self, blog_factory, user_factory):
        user = user_factory(name="Ivory Tower")
        blog = blog_factory(name="Infernal Tendencies", user=user)
        self.login(user.email)
        url = self.url(blog)
        rv = self.client.get(url)
        assert f'action="{url}"' in rv.text

    def test_anon_post_data_ok(self, blog_factory):
        blog = blog_factory(name="Infernal Tendencies")
        rv = self.client.post(self.url(blog), data=self.data_ok)
        assert rv.status_code == 302
        assert url_for("auth.select") in rv.headers["Location"]

    def test_anon_post_data_incomplete(self, blog_factory):
        blog = blog_factory(name="Infernal Tendencies")
        rv = self.client.post(self.url(blog), data=self.data_incomplete)
        assert rv.status_code == 302
        assert url_for("auth.select") in rv.headers["Location"]

    def test_authenticated_post_data_ok(self, blog_factory, user_factory):
        blog = blog_factory(name="Infernal Tendencies")
        user = user_factory(name="Ivory Tower")
        self.login(user.email)
        rv = self.client.post(self.url(blog), data=self.data_ok)
        assert rv.status_code == 404

    def test_authenticated_post_data_incomplete(self, blog_factory, user_factory):
        blog = blog_factory(name="Infernal Tendencies")
        user = user_factory(name="Ivory Tower")
        self.login(user.email)
        rv = self.client.post(self.url(blog), data=self.data_incomplete)
        assert rv.status_code == 404

    def test_owner_post_data_ok(self, blog_factory, user_factory):
        user = user_factory(name="Ivory Tower")
        blog = blog_factory(name="Infernal Tendencies", user=user)
        self.login(user.email)
        rv = self.client.post(self.url(blog), data=self.data_ok)
        assert rv.status_code == 302
        assert url_for("blog.display", blog_id=blog.id) in rv.headers["Location"]

    def test_owner_post_data_incomplete(self, blog_factory, user_factory):
        user = user_factory(name="Ivory Tower")
        blog = blog_factory(name="Infernal Tendencies", user=user)
        self.login(user.email)
        rv = self.client.post(self.url(blog), data=self.data_incomplete)
        assert "field is required" in rv.text
