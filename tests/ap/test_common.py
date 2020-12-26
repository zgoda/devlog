import json

import pytest
from flask import url_for


@pytest.mark.usefixtures('client_class')
class TestWebfinger:

    def test_no_user_spec(self):
        url = url_for('ap.webfinger')
        rv = self.client.get(url)
        assert rv.status_code == 400
        data = json.loads(rv.text)
        assert 'error' in data
        assert data['error'] == 'malformed request'

    def test_user_not_found(self):
        url = url_for('ap.webfinger', resource='acct:alice@wonderland.org')
        rv = self.client.get(url)
        assert rv.status_code == 404
        data = json.loads(rv.text)
        assert 'error' in data
        assert data['error'] == 'no such resource'

    def test_user_inactive(self, user_factory):
        user_name = 'alice'
        host = 'wonderland.org'
        user_factory(
            name=user_name, actor_id=f'https://{host}/user/{user_name}', is_active=False
        )
        res = f'acct:{user_name}@{host}'
        url = url_for('ap.webfinger', resource=res)
        rv = self.client.get(url)
        assert rv.status_code == 404
        data = json.loads(rv.text)
        assert 'error' in data
        assert data['error'] == 'no such resource'

    def test_unknown_resource_type(self):
        url = url_for('ap.webfinger', resource='email:alice@wonderland.org')
        rv = self.client.get(url)
        assert rv.status_code == 404
        data = json.loads(rv.text)
        assert 'error' in data
        assert data['error'] == 'no such resource'

    def test_ok(self, user_factory):
        user_name = 'alice'
        host = 'wonderland.org'
        user_factory(
            name=user_name, actor_id=f'https://{host}/user/{user_name}'
        )
        res = f'acct:{user_name}@{host}'
        url = url_for('ap.webfinger', resource=res)
        rv = self.client.get(url)
        assert rv.headers['Content-Type'] == 'application/jrd+json'
        assert rv.status_code == 200
        data = json.loads(rv.text)
        assert 'error' not in data
        assert data['subject'] == res
        assert 'links' in data
        assert len(data['links']) == 2


def test_nodeinfo(client):
    url = url_for('ap.nodeinfo')
    rv = client.get(url)
    assert rv.status_code == 200
    assert rv.headers['Content-Type'] == 'application/json; profile=http://nodeinfo.diaspora.software/ns/schema/2.0#'  # noqa: E501
