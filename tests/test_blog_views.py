from flask import url_for

import pytest

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestBlogCreateView(DevlogTests):

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.url = url_for('blog.create')

    def test_anon_get(self):
        rv = self.client.get(self.url)
        assert rv.status_code == 302
        assert url_for('auth.select') in rv.headers['Location']

    def test_authenticated_get(self, user_factory):
        user = user_factory(name='Ivory Tower')
        self.login(user.email)
        rv = self.client.get(self.url)
        assert rv.status_code == 200
        assert f'action="{self.url}"' in rv.text

    def test_anon_post(self, user_factory):
        user = user_factory(name='Ivory Tower')
        data = {
            'user': user.id,
            'name': 'Infernal Tendencies',
        }
        rv = self.client.post(self.url, data=data)
        assert rv.status_code == 302
        assert url_for('auth.select') in rv.headers['Location']

    def test_authenticated_post_ok(self, user_factory):
        user = user_factory(name='Ivory Tower')
        blog_name = 'Infernal Tendencies'
        data = {
            'user': user.id,
            'name': blog_name,
        }
        self.login(user.email)
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert f'{blog_name} has been created' in rv.text
        assert f'<h1>{blog_name}</h1>' in rv.text

    def test_authenticated_post_fail(self, user_factory):
        user = user_factory(name='Ivory Tower')
        data = {
            'user': user.id,
        }
        self.login(user.email)
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert f'field is required' in rv.text
        assert f'has been created' not in rv.text


@pytest.mark.usefixtures('client_class')
class TestBlogDetailsView(DevlogTests):

    def url(self, blog):
        return url_for('blog.display', blog_id=blog.id)

    def test_anon_get_public(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies')
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 200
        assert f'<h1>{blog.name}</h1>' in rv.text

    def test_anon_get_private(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies', public=False)
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 404

    def test_anon_get_inactive(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies', active=False)
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 404
