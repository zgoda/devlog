from flask import url_for
import pytest


@pytest.mark.usefixtures('client_class')
@pytest.mark.skip('Not yet')
class TestUserProfile:

    def test_not_found(self):
        url = url_for('ap.userprofile', name='alice')
        rv = self.client.get(url)
        assert rv.status_code == 404

    def test_ok(self, user_factory):
        user_name = 'alice'
        host = 'wonderland.org'
        summary = 'Some summary text'
        user = user_factory(
            name=user_name, actor_id=f'https://{host}/user/{user_name}', summary=summary
        )
        url = url_for('ap.userprofile', name=user_name)
        rv = self.client.get(url)
        assert user.display_name in rv.text
        assert summary in rv.text
