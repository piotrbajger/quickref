from unittest import TestCase

from quickref import create_app


class TestStatic(TestCase):
    """Tests static functionality"""
    def setUp(self):
        app = create_app(test=True)
        self.client = app.test_client()

    def test_home(self):
        """Test static home view (take me /, country road)."""
        re = self.client.get('/')
        self.assertEqual(re.status_code, 200)
        self.assertTrue("<title>Home</title>" in re.data.decode())

        re = self.client.get('/index')
        self.assertEqual(re.status_code, 200)
        self.assertTrue("<title>Home</title>" in re.data.decode())

    def test_login(self):
        """Test static login view."""
        re = self.client.get('/login')
        self.assertEqual(re.status_code, 200)
        self.assertTrue("<title>Login</title>" in re.data.decode())

    def test_logout(self):
        """Test static logout view (redirect)."""
        re = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(re.status_code, 200)
        self.assertTrue("<title>Home</title>" in re.data.decode())
