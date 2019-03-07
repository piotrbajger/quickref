from unittest import TestCase

from quickref import create_app


class TestStatic(TestCase):
    """Tests static functionality"""
    def setUp(self):
        app = create_app(test=True)
        self.client = app.test_client()

    def test_home(self):
        re = self.client.get('/')
        self.assertEqual(re.status_code, 200)

        re = self.client.get('/index')
        self.assertEqual(re.status_code, 200)

    def test_login(self):
        re = self.client.get('/login')
        self.assertEqual(re.status_code, 200)

    def test_logout(self):
        re = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(re.status_code, 200)
