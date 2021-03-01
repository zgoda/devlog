import pytest
from flask import url_for


@pytest.mark.usefixtures('client_class')
class TestLoginView:

    @pytest.fixture(autouse=True)
    def _set_up(self):
        self.url = url_for('auth.login')

    def test_login_ok(self, user_factory, mocker):
        name = 'user1'
        password = 'password1'
        mocker.patch('devlog.models.check_otp', mocker.Mock(return_value=True))
        user_factory(name=name, password=password)
        data = {'name': name, 'password': password, 'code': '123456'}
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert 'Użytkownik zalogowany' in rv.text

    def test_invalid_credentials(self):
        data = {'name': 'username', 'password': 'password', 'code': '123456'}
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert 'Nieprawidłowe dane logowania' in rv.text

    def test_invalid_code(self, user_factory, mocker):
        name = 'user1'
        password = 'password1'
        mocker.patch('devlog.models.check_otp', mocker.Mock(return_value=False))
        user_factory(name=name, password=password)
        data = {'name': name, 'password': password, 'code': '123456'}
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert 'Nieprawidłowe dane logowania' in rv.text

    def test_missing_code(self, user_factory):
        name = 'user1'
        password = 'password1'
        user_factory(name=name, password=password)
        data = {'name': name, 'password': password}
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert '<p class="validation-error">' in rv.text
        assert 'To pole jest wymagane' in rv.text


@pytest.mark.usefixtures('client_class')
class TestMFABeginView:

    @pytest.fixture(autouse=True)
    def _set_up(self):
        self.url = url_for('auth.mfa-begin')

    def test_login_ok(self, user_factory):
        name = 'user1'
        password = 'password1'
        user_factory(name=name, password=password)
        data = {'name': name, 'password': password}
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert 'Prawidłowe dane logowania' in rv.text

    def test_login_failure(self, user_factory):
        name = 'user1'
        password = 'password1'
        user_factory(name=name, password=f'x{password}x')
        data = {'name': name, 'password': password}
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert 'Nieprawidłowe dane logowania' in rv.text

    def test_login_form_invalid(self, user_factory):
        name = 'user1'
        password = 'password1'
        user_factory(name=name, password=password)
        data = {'name': name}
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert '<p class="validation-error">' in rv.text
        assert 'To pole jest wymagane' in rv.text


@pytest.mark.usefixtures('client_class')
class TestMFAPairView:

    @pytest.fixture(autouse=True)
    def _set_up(self):
        self.url = url_for('auth.mfa-qrcode')

    def test_code_ok(self, user_factory, mocker):
        name = 'user1'
        user_factory(name=name)
        mocker.patch('devlog.models.check_otp', mocker.Mock(return_value=True))
        with self.client.session_transaction() as sess:
            sess['user'] = name
        data = {'code1': '123456', 'code2': '234567'}
        rv = self.client.post(self.url, data=data, follow_redirects=True)
        assert 'Użytkownik zalogowany' in rv.text

    def test_user_from_space_get(self):
        redirect_url = url_for('auth.login')
        rv = self.client.get(self.url, follow_redirects=False)
        assert redirect_url in rv.headers['Location']
        assert rv.status_code == 302

    def test_user_from_space_post(self):
        redirect_url = url_for('auth.login')
        data = {'code1': '123456', 'code2': '234567'}
        rv = self.client.get(self.url, data=data, follow_redirects=False)
        assert redirect_url in rv.headers['Location']
        assert rv.status_code == 302

    def test_unknown_user_get(self):
        redirect_url = url_for('auth.login')
        with self.client.session_transaction() as sess:
            sess['user'] = 'user1'
        rv = self.client.get(self.url, follow_redirects=False)
        assert redirect_url in rv.headers['Location']
        assert rv.status_code == 302

    def test_unknown_user_post(self):
        redirect_url = url_for('auth.login')
        data = {'code1': '123456', 'code2': '234567'}
        with self.client.session_transaction() as sess:
            sess['user'] = 'user1'
        rv = self.client.get(self.url, data=data, follow_redirects=False)
        assert redirect_url in rv.headers['Location']
        assert rv.status_code == 302
