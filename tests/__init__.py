from urllib.parse import urlencode


class DevlogTests:

    def login(self, email, name=None):
        params = {
            'email': email
        }
        if name:
            params['name'] = name
        params = urlencode(params)
        return self.client.get(
            f'/auth/local/login?{params}', follow_redirects=True,
        )

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)
