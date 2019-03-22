from devlog.utils.pagination import url_for_other_page

from . import DevlogTests


class TestUtilsPagination(DevlogTests):
    def test_url_for_other_page(self, mocker):
        fake_url_for = mocker.Mock()
        mocker.patch("devlog.utils.pagination.url_for", fake_url_for)
        fake_request = mocker.MagicMock(view_args={})
        mocker.patch("devlog.utils.pagination.request", fake_request)
        page = 1
        url_for_other_page(page)
        fake_url_for.assert_called_once_with(mocker.ANY, p=page)
