from unittest import TestCase

from quickref import create_app
from quickref.extensions import db
from quickref.models.user import User


class TestLogin(TestCase):
    """Tests static functionality"""
    def setUp(self):
        self.app = create_app(test=True)
        test_user = User(username='test', email='test@example.com')
        test_user.set_password('testpass')

        with self.app.app_context():
            db.create_all()
            db.session.add(test_user)
            db.session.commit()

        self.client = self.app.test_client()

    def test_login_valid(self):
        """Test that login with valid details actually logs in"""
        re = self.client.post(
            '/login',
            data={
                'username': 'test',
                'password': 'testpass',
            },
            follow_redirects=True
        )

        self.assertEqual(re.status_code, 200)

        self.assertTrue('Welcome test!' in str(re.data))
        self.assertTrue('<title>Home</title>' in str(re.data))

    def test_login_valid_redirect(self):
        """Test that login correctly uses the 'next' parameter"""
        re = self.client.post(
            '/login',
            data={
                'username': 'test',
                'password': 'testpass',
            },
            query_string={
                'next': '/refs'
            },
            follow_redirects=True
        )

        self.assertEqual(re.status_code, 200)
        self.assertTrue('Refs' in str(re.data))

    def test_login_invalid(self):
        """Test that login with invalid details does not log in"""
        re = self.client.post(
            '/login',
            data={
                'username': 'test',
                'password': 'invalid_pass',
            },
            follow_redirects=True
        )

        self.assertEqual(re.status_code, 200)

        self.assertTrue('Invalid username or password' in str(re.data))

    def test_login_required(self):
        """Test that a pages requiring login is inaccessible"""
        re = self.client.get('/refs')

        self.assertEqual(re.status_code, 302)

    def test_login_required_redirect(self):
        """Test that user is redirected to the login view"""
        re = self.client.get('/refs', follow_redirects=True)

        self.assertEqual(re.status_code, 200)
        self.assertTrue("Please log in to access this page." in str(re.data))
