import pytest
from flask import url_for

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestPostCreateView(DevlogTests):

    DATA_OK = {
        'title': 'Post No. 1',
        'text': 'Short introduction',
    }

    DATA_INCOMPLETE = {
        'text': 'Short introduction',
    }

    def url(self, blog):
        return url_for('post.create', blog_id=blog.id)

    def test_anon_get(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies')
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 302
        assert url_for('auth.select') in rv.headers['Location']

    def test_authenticated_get(self, blog_factory, user_factory):
        blog = blog_factory(name='Infernal Tendencies')
        user = user_factory(name='Ivory Tower')
        self.login(user.email)
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 404

    def test_owner_get(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower')
        blog = blog_factory(name='Infernal Tendencies', user=user)
        self.login(user.email)
        url = self.url(blog)
        rv = self.client.get(url)
        assert f'action="{url}"' in rv.text

    def test_anon_post_data_ok(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies')
        rv = self.client.post(self.url(blog), data=self.DATA_OK)
        assert rv.status_code == 302
        assert url_for('auth.select') in rv.headers['Location']

    def test_anon_post_data_incomplete(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies')
        rv = self.client.post(self.url(blog), data=self.DATA_INCOMPLETE)
        assert rv.status_code == 302
        assert url_for('auth.select') in rv.headers['Location']

    def test_authenticated_post_data_ok(self, blog_factory, user_factory):
        blog = blog_factory(name='Infernal Tendencies')
        user = user_factory(name='Ivory Tower')
        self.login(user.email)
        rv = self.client.post(self.url(blog), data=self.DATA_OK)
        assert rv.status_code == 404

    def test_authenticated_post_data_incomplete(self, blog_factory, user_factory):
        blog = blog_factory(name='Infernal Tendencies')
        user = user_factory(name='Ivory Tower')
        self.login(user.email)
        rv = self.client.post(self.url(blog), data=self.DATA_INCOMPLETE)
        assert rv.status_code == 404

    def test_owner_post_data_ok(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower')
        blog = blog_factory(name='Infernal Tendencies', user=user)
        self.login(user.email)
        rv = self.client.post(self.url(blog), data=self.DATA_OK)
        assert rv.status_code == 302
        assert url_for('blog.display', blog_id=blog.id) in rv.headers['Location']

    def test_owner_post_data_incomplete(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower')
        blog = blog_factory(name='Infernal Tendencies', user=user)
        self.login(user.email)
        rv = self.client.post(self.url(blog), data=self.DATA_INCOMPLETE)
        assert 'field is required' in rv.text


@pytest.mark.usefixtures('client_class')
class TestPostDisplayView(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self, user_factory):
        self.public_user = user_factory(name='Public User')
        self.nonpublic_user = user_factory(name='Nonpublic User', public=False)

    def url(self, post):
        return url_for('post.display', post_id=post.id)

    def test_anon_get_public(self, post_factory, blog_factory):
        blog = blog_factory(user=self.public_user, public=True)
        title = 'First post'
        post = post_factory(blog=blog, public=True, draft=False, title=title)
        url = self.url(post)
        rv = self.client.get(url)
        assert f'<h1>{title}</h1>' in rv.text

    def test_anon_get_public_draft(self, post_factory, blog_factory):
        blog = blog_factory(user=self.public_user, public=True)
        title = 'First post'
        post = post_factory(blog=blog, public=True, draft=True, title=title)
        url = self.url(post)
        rv = self.client.get(url)
        assert rv.status_code == 404

    def test_anon_get_nonpublic(self, post_factory, blog_factory):
        blog = blog_factory(user=self.public_user, public=True)
        title = 'First post'
        post = post_factory(blog=blog, public=False, draft=False, title=title)
        url = self.url(post)
        rv = self.client.get(url)
        assert rv.status_code == 404

    def test_anon_get_nonpublic_draft(self, post_factory, blog_factory):
        blog = blog_factory(user=self.public_user, public=True)
        title = 'First post'
        post = post_factory(blog=blog, public=False, draft=True, title=title)
        url = self.url(post)
        rv = self.client.get(url)
        assert rv.status_code == 404
