import pytest

from . import DevlogTests


@pytest.mark.usefixtures('client_class')
class TestUserViews(DevlogTests):

    def test_user_profile(self):
        pass
