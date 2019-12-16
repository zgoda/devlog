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
        assert url_for('auth.login') in rv.headers['Location']

    def test_authenticated_get(self, blog_factory, user_factory):
        blog = blog_factory(name='Infernal Tendencies')
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        self.login(user.name)
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 404

    def test_owner_get(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='Infernal Tendencies', user=user)
        self.login(user.name)
        url = self.url(blog)
        rv = self.client.get(url)
        assert f'action="{url}"' in rv.text

    def test_anon_post_data_ok(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies')
        rv = self.client.post(self.url(blog), data=self.DATA_OK)
        assert rv.status_code == 302
        assert url_for('auth.login') in rv.headers['Location']

    def test_anon_post_data_incomplete(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies')
        rv = self.client.post(self.url(blog), data=self.DATA_INCOMPLETE)
        assert rv.status_code == 302
        assert url_for('auth.login') in rv.headers['Location']

    def test_authenticated_post_data_ok(self, blog_factory, user_factory):
        blog = blog_factory(name='Infernal Tendencies')
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        self.login(user.name)
        rv = self.client.post(self.url(blog), data=self.DATA_OK)
        assert rv.status_code == 404

    def test_authenticated_post_data_incomplete(self, blog_factory, user_factory):
        blog = blog_factory(name='Infernal Tendencies')
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        self.login(user.name)
        rv = self.client.post(self.url(blog), data=self.DATA_INCOMPLETE)
        assert rv.status_code == 404

    def test_owner_post_data_ok(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='Infernal Tendencies', user=user)
        self.login(user.name)
        rv = self.client.post(self.url(blog), data=self.DATA_OK)
        assert rv.status_code == 302
        assert url_for('blog.display', blog_id=blog.id) in rv.headers['Location']

    def test_owner_post_data_incomplete(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='Infernal Tendencies', user=user)
        self.login(user.name)
        rv = self.client.post(self.url(blog), data=self.DATA_INCOMPLETE)
        assert 'field is required' in rv.text


@pytest.mark.usefixtures('client_class')
class TestPostDisplayView(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self, user_factory):
        self.user = user_factory(name='Public User', password=self.default_pw)

    def url(self, post):
        return url_for('post.display', post_id=post.id)

    def test_anon_get_public(self, post_factory, blog_factory):
        blog = blog_factory(user=self.user)
        title = 'First post'
        post = post_factory(blog=blog, draft=False, title=title)
        url = self.url(post)
        rv = self.client.get(url)
        assert f'>{title}</h1>' in rv.text

    def test_anon_get_no_access(self, post_factory, blog_factory):
        blog = blog_factory(user=self.user)
        title = 'First post'
        post = post_factory(blog=blog, draft=True, title=title)
        url = self.url(post)
        rv = self.client.get(url)
        assert rv.status_code == 404

    def test_authenticated_get_public(self, post_factory, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(user=self.user)
        title = 'First post'
        post = post_factory(blog=blog, draft=False, title=title)
        self.login(user.name)
        url = self.url(post)
        rv = self.client.get(url)
        assert f'>{title}</h1>' in rv.text

    def test_authenticated_get_no_access(
                self, post_factory, blog_factory, user_factory
            ):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(user=self.user)
        title = 'First post'
        post = post_factory(blog=blog, draft=True, title=title)
        self.login(user.name)
        url = self.url(post)
        rv = self.client.get(url)
        assert rv.status_code == 404

    @pytest.mark.parametrize('draft', [False, True], ids=['active', 'draft'])
    def test_owner_get(self, draft, post_factory, blog_factory):
        blog = blog_factory(user=self.user)
        title = 'First post'
        post = post_factory(blog=blog, draft=draft, title=title)
        self.login(self.user.name)
        url = self.url(post)
        rv = self.client.get(url)
        assert f'>{title}</h1>' in rv.text

    @pytest.mark.parametrize('draft', [False, True], ids=['active', 'draft'])
    def test_anon_post_no_access(self, draft, post_factory, blog_factory):
        blog = blog_factory(user=self.user)
        title = 'First post'
        post = post_factory(blog=blog, draft=draft, title=title)
        url = self.url(post)
        data = {
            'title': 'New name',
        }
        rv = self.client.post(url, data=data)
        assert rv.status_code == 404

    @pytest.mark.parametrize('draft', [False, True], ids=['active', 'draft'])
    def test_authenticated_post_no_access(
                self, draft, post_factory, blog_factory, user_factory
            ):
        blog = blog_factory(user=self.user)
        title = 'First post'
        post = post_factory(blog=blog, draft=draft, title=title)
        user = user_factory(name='Ivory Tower')
        url = self.url(post)
        self.login(user.name)
        data = {
            'title': 'New name',
        }
        rv = self.client.post(url, data=data)
        assert rv.status_code == 404

    @pytest.mark.parametrize('draft', [False, True], ids=['active', 'draft'])
    def test_owner_post_ok(self, draft, post_factory, blog_factory):
        blog = blog_factory(user=self.user)
        title = 'First post'
        post = post_factory(blog=blog, draft=draft, title=title)
        url = self.url(post)
        self.login(self.user.name)
        new_title = 'New name'
        data = {
            'title': new_title,
            'text': 'this is text'
        }
        rv = self.client.post(url, data=data, follow_redirects=True)
        assert 'post has been saved' in rv.text
        assert f'value="{new_title}"' in rv.text

    @pytest.mark.parametrize('draft', [False, True], ids=['active', 'draft'])
    def test_owner_post_fail(self, draft, post_factory, blog_factory):
        blog = blog_factory(user=self.user)
        title = 'First post'
        post = post_factory(blog=blog, draft=draft, title=title)
        url = self.url(post)
        self.login(self.user.name)
        new_title = None
        data = {
            'title': new_title,
        }
        rv = self.client.post(url, data=data, follow_redirects=True)
        assert 'post has been saved' not in rv.text
        assert 'field is required' in rv.text
