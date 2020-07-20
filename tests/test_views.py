from datetime import datetime

import pytest
from flask import url_for

from devlog.utils.text import slugify


def test_index_no_posts(client):
    url = url_for('main.index')
    rv = client.get(url)
    assert rv.status_code == 200
    assert 'żadnych postów' in rv.text


def test_index_one_post(client, post_factory):
    d = datetime.utcnow()
    post = post_factory(created=d, published=d)
    url = url_for('main.index')
    rv = client.get(url)
    assert rv.status_code == 200
    assert f'<h3>{post.title}</h3>' in rv.text


def test_index_many_posts(client, post_factory):
    d = datetime.utcnow()
    post_factory.create_batch(6, created=d, published=d)
    url = url_for('main.index')
    rv = client.get(url)
    assert rv.status_code == 200
    assert rv.text.count('<h3>') == 5


def test_flatpages(client):
    pages = ['o', 'kontakt']
    for page in pages:
        url = url_for('main.page', path=page)
        rv = client.get(url)
        assert rv.status_code == 200


@pytest.mark.usefixtures('client_class')
class TestBlogHomeView:

    @pytest.fixture(autouse=True)
    def _set_up(self):
        self.url = url_for('main.blog')

    def test_no_posts(self):
        rv = self.client.get(self.url)
        assert rv.status_code == 200
        assert 'żadnych postów' in rv.text

    def test_one_post(self, post_factory):
        d = datetime.utcnow()
        post = post_factory(created=d, published=d)
        rv = self.client.get(self.url)
        assert rv.status_code == 200
        assert f'<h3>{post.title}</h3>' in rv.text

    def test_many_pages(self, post_factory):
        post_num = 24
        d = datetime.utcnow()
        post_factory.create_batch(post_num, created=d, published=d)
        rv = self.client.get(self.url)
        assert rv.status_code == 200
        assert '>Poprzednia (' not in rv.text
        assert '>Następna (2 / 3)' in rv.text


@pytest.mark.usefixtures('client_class')
class TestPostView:

    def test_ok(self, post_factory):
        title = 'test post 1'
        slug = slugify(title)
        y, m, d = 2020, 2, 2
        created = datetime(y, m, d)
        post_factory(title=title, created=created, published=created)
        url = url_for('main.post', y=y, m=m, d=d, slug=slug)
        rv = self.client.get(url)
        assert rv.status_code == 200
        assert f'<h2>{title}</h2>' in rv.text

    def test_fail(self):
        title = 'test post 1'
        slug = slugify(title)
        y, m, d = 2020, 2, 2
        url = url_for('main.post', y=y, m=m, d=d, slug=slug)
        rv = self.client.get(url)
        assert rv.status_code == 404


@pytest.mark.usefixtures('client_class')
class TestTagView:

    def test_ok(self, post_factory, tag_factory, tagged_post_factory):
        name = 'etykieta 1'
        tag = tag_factory(name=name)
        dt = datetime(2020, 2, 2)
        post = post_factory(created=dt, published=dt)
        tagged_post_factory.create(tag=tag, post=post)
        url = url_for('main.tag', slug=tag.slug)
        rv = self.client.get(url)
        assert rv.status_code == 200
        assert f'<h3>{post.title}</h3>' in rv.text

    def test_fail(self):
        url = url_for('main.tag', slug=slugify('etykieta 1'))
        rv = self.client.get(url)
        assert rv.status_code == 404
