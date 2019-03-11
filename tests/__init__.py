class DevlogTests:

    def login(self, email):
        return self.client.get(
            f'/auth/local/login?email={email}', follow_redirects=True,
        )

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)
