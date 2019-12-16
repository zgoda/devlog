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
        assert url_for('auth.login') in rv.headers['Location']

    def test_authenticated_get(self, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        self.login(user.name)
        rv = self.client.get(self.url)
        assert rv.status_code == 200
        assert f'action="{self.url}"' in rv.text

    def test_anon_post(self, user_factory):
        user = user_factory(name='Ivory Tower')
        data = {'user': user.id, 'name': 'Infernal Tendencies'}
        rv = self.client.post(self.url, data=data)
        assert rv.status_code == 302
        assert url_for('auth.login') in rv.headers['Location']

    def test_authenticated_post_ok(self, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog_name = 'Infernal Tendencies'
        data = {'user': user.id, 'name': blog_name}
        self.login(user.name)
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert f'{blog_name} has been created' in rv.text
        assert f'>{blog_name}</h1>' in rv.text

    def test_authenticated_post_fail(self, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        data = {'user': user.id}
        self.login(user.name)
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert f'field is required' in rv.text
        assert f'has been created' not in rv.text


@pytest.mark.usefixtures('client_class')
class TestBlogDisplayView(DevlogTests):

    def url(self, blog):
        return url_for('blog.display', blog_id=blog.id)

    def test_anon_get_active(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies')
        edit_url = url_for('blog.details', blog_id=blog.id)
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 200
        assert f'>{blog.name}</h1>' in rv.text
        assert f'href="{edit_url}"' not in rv.text

    def test_anon_get_inactive(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies', active=False)
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 404

    @pytest.mark.parametrize('active', [True, False], ids=['active', 'inactive'])
    def test_authenticated_get(self, user_factory, blog_factory, active):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='Infernal Tendencies', user=user, active=active)
        edit_url = url_for('blog.details', blog_id=blog.id)
        self.login(user.name)
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 200
        assert f'>{blog.name}</h1>' in rv.text
        assert f'href="{edit_url}"' in rv.text


@pytest.mark.usefixtures('client_class')
class TestBlogDetailsView(DevlogTests):

    def url(self, blog):
        return url_for('blog.details', blog_id=blog.id)

    def test_anon_get(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies')
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 302
        assert url_for('auth.login') in rv.headers['Location']

    def test_authenticated_get(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='Infernal Tendencies')
        self.login(user.name)
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 404

    def test_owner_get(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='Infernal Tendencies', user=user)
        url = self.url(blog)
        self.login(user.name)
        rv = self.client.get(url)
        assert f'action="{url}"' in rv.text

    def test_anon_post(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies')
        rv = self.client.post(self.url(blog), data={'name': 'New Order'})
        assert rv.status_code == 302
        assert url_for('auth.login') in rv.headers['Location']

    def test_authenticated_post(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='Infernal Tendencies')
        self.login(user.name)
        rv = self.client.post(self.url(blog), data={'name': 'New Order'})
        assert rv.status_code == 404

    def test_owner_ok(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='Infernal Tendencies', user=user)
        url = self.url(blog)
        self.login(user.name)
        new_name = 'New Order'
        rv = self.client.post(url, data={'name': new_name}, follow_redirects=True)
        assert f'{new_name} has been modified' in rv.text

    def test_owner_post_fail(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='Infernal Tendencies', user=user)
        url = self.url(blog)
        self.login(user.name)
        new_name = None
        rv = self.client.post(url, data={'name': new_name}, follow_redirects=True)
        assert 'field is required' in rv.text


@pytest.mark.usefixtures('client_class')
class TestBlogDeleteView(DevlogTests):

    def url(self, blog):
        return url_for('blog.delete', blog_id=blog.id)

    def test_anon_get(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies')
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 302
        assert url_for('auth.login') in rv.headers['Location']

    def test_authenticated_get(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='Infernal Tendencies')
        self.login(user.name)
        rv = self.client.get(self.url(blog))
        assert rv.status_code == 404

    def test_owner_get(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='infernal Tendencies', user=user)
        self.login(user.name)
        url = self.url(blog)
        rv = self.client.get(url)
        assert f'action="{url}"' in rv.text

    def test_anon_post(self, blog_factory):
        blog = blog_factory(name='Infernal Tendencies')
        rv = self.client.post(self.url(blog), data={'delete_it': True})
        assert rv.status_code == 302
        assert url_for('auth.login') in rv.headers['Location']

    def test_authenticated_post(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='Infernal Tendencies')
        self.login(user.name)
        rv = self.client.post(self.url(blog), data={'delete_it': True})
        assert rv.status_code == 404

    def test_owner_post(self, blog_factory, user_factory):
        user = user_factory(name='Ivory Tower', password=self.default_pw)
        blog = blog_factory(name='infernal Tendencies', user=user)
        self.login(user.name)
        url = self.url(blog)
        rv = self.client.post(url, data={'delete_it': True})
        assert rv.status_code == 302
        assert url_for('home.index') in rv.headers['Location']
