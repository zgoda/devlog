import pytest
from pytest_factoryboy import register

from devlog import make_app
from devlog.ext import db

from .factories import UserFactory

register(UserFactory)


@pytest.fixture
def app():
    app = make_app('test')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
