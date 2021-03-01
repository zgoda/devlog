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

    def test_get_empty(self, api_login, user_factory):
        user = user_factory()
        token = api_login(user.name, user.password)
        rv = self.client.get(self.url, headers={'Authorization': f'Basic {token}'})
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'quips' in data
        assert data['quips'] == []

    def test_get_nonempty(self, api_login, user_factory, quip_factory):
        user = user_factory()
        quip = quip_factory(author=user.name)
        token = api_login(user.name, user.password)
        rv = self.client.get(self.url, headers={'Authorization': f'Basic {token}'})
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'quips' in data
        assert len(data['quips']) == 1
        assert data['quips'][0]['text'] == quip.text
        assert data['quips'][0]['author'] == user.name

    def test_post_without_author(self, api_login, user_factory):
        user = user_factory()
        data = {'text': 'My *first* quip!'}
        token = api_login(user.name, user.password)
        rv = self.client.post(
            self.url, json=data, headers={'Authorization': f'Basic {token}'}
        )
        assert rv.status_code == 201
        quip = Quip.get(Quip.author == user.name)
        assert quip.text == data['text']
        assert '<em>first</em>' in quip.text_html

    def test_post_with_author(self, api_login, user_factory):
        author = 'johnny'
        user = user_factory()
        data = {'text': 'My *first* quip!', 'author': author}
        token = api_login(user.name, user.password)
        rv = self.client.post(
            self.url, json=data, headers={'Authorization': f'Basic {token}'}
        )
        assert rv.status_code == 201
        assert Quip.get_or_none(Quip.author == user.name) is None
        quip = Quip.get(Quip.author == author)
        assert quip.text == data['text']
        assert '<em>first</em>' in quip.text_html


@pytest.mark.usefixtures('client_class')
class TestQuipItem:

    def url(self, quip):
        return url_for('api.quip-item', quip_id=quip.pk)

    def test_get_anon(self, quip_factory):
        quip = quip_factory()
        url = self.url(quip)
        rv = self.client.get(url)
        assert rv.status_code == 401
        data = rv.get_json()
        assert 'authorization required' in data['message'].lower()

    def test_put_anon(self, quip_factory):
        quip = quip_factory()
        url = self.url(quip)
        data = {
            'text': 'New text',
        }
        rv = self.client.put(url, json=data)
        assert rv.status_code == 401
        data = rv.get_json()
        assert 'authorization required' in data['message'].lower()

    def test_get_ok(self, api_login, user_factory, quip_factory):
        user = user_factory()
        quip = quip_factory(author=user.name)
        url = self.url(quip)
        token = api_login(user.name, user.password)
        rv = self.client.get(url, headers={'Authorization': f'Basic {token}'})
        data = rv.get_json()['quip']
        assert rv.status_code == 200
        assert data['text'] == quip.text
        assert data['author'] == user.name

    def test_get_notfound(self, api_login, user_factory):
        user = user_factory()
        url = url_for('api.quip-item', quip_id=1)
        token = api_login(user.name, user.password)
        rv = self.client.get(url, headers={'Authorization': f'Basic {token}'})
        data = rv.get_json()
        assert rv.status_code == 404
        assert 'no such object' in data['message'].lower()

    def test_put_ok(self, api_login, user_factory, quip_factory):
        user = user_factory()
        text = 'My *first* quip!'
        quip = quip_factory(author=user.name, text=text)
        url = self.url(quip)
        new_text = 'My *very* first quip!'
        token = api_login(user.name, user.password)
        rv = self.client.put(
            url, json={'text': new_text}, headers={'Authorization': f'Basic {token}'}
        )
        data = rv.get_json()['quip']
        assert rv.status_code == 200
        assert data['text'] == new_text
        quip = Quip.get_by_id(quip.pk)
        assert quip.text == new_text

    def test_put_notfound(self, api_login, user_factory):
        user = user_factory()
        url = url_for('api.quip-item', quip_id=1)
        token = api_login(user.name, user.password)
        rv = self.client.put(
            url, json={'text': 'new text'}, headers={'Authorization': f'Basic {token}'}
        )
        data = rv.get_json()
        assert rv.status_code == 404
        assert 'no such object' in data['message'].lower()
