import pytest
from flask import url_for

from devlog.models import Quip


@pytest.mark.usefixtures('client_class')
class TestQuipCollection:

    @pytest.fixture(autouse=True)
    def _set_up(self):
        self.url = url_for('api.quip-collection')

    def test_get_anon(self):
        rv = self.client.get(self.url)
        assert rv.status_code == 401
        data = rv.get_json()
        assert 'authorization required' in data['message'].lower()

    def test_post_anon(self):
        rv = self.client.post(self.url, data={'data': 'dummy'})
        assert rv.status_code == 401
        data = rv.get_json()
        assert 'authorization required' in data['message'].lower()

    def test_get_empty(self, login, user_factory):
        user = user_factory()
        token = login(user.name, user.password)
        rv = self.client.get(self.url, headers={'Authorization': f'Basic {token}'})
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'quips' in data
        assert data['quips'] == []

    def test_get_nonempty(self, login, user_factory, quip_factory):
        user = user_factory()
        quip = quip_factory(author=user.name)
        token = login(user.name, user.password)
        rv = self.client.get(self.url, headers={'Authorization': f'Basic {token}'})
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'quips' in data
        assert len(data['quips']) == 1
        assert data['quips'][0]['text'] == quip.text
        assert data['quips'][0]['author'] == user.name

    def test_post_without_author(self, login, user_factory):
        user = user_factory()
        data = {'text': 'My *first* quip!'}
        token = login(user.name, user.password)
        rv = self.client.post(
            self.url, json=data, headers={'Authorization': f'Basic {token}'}
        )
        assert rv.status_code == 201
        quip = Quip.get(Quip.author == user.name)
        assert quip.text == data['text']
        assert '<em>first</em>' in quip.text_html

    def test_post_with_author(self, login, user_factory):
        author = 'johnny'
        user = user_factory()
        data = {'text': 'My *first* quip!', 'author': author}
        token = login(user.name, user.password)
        rv = self.client.post(
            self.url, json=data, headers={'Authorization': f'Basic {token}'}
        )
        assert rv.status_code == 201
        assert Quip.get_or_none(Quip.author == user.name) is None
        quip = Quip.get(Quip.author == author)
        assert quip.text == data['text']
        assert '<em>first</em>' in quip.text_html
