class DevlogTests:

    default_pw = 'pass'

    def login(self, name, password=None):
        params = {
            'name': name,
            'password': password or self.default_pw,
        }
        return self.client.post('/auth/login', data=params, follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)
