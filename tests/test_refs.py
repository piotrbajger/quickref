from unittest import TestCase

from flask_login import login_user

from quickref import create_app
from quickref.extensions import db
from quickref.models.ref import Ref
from quickref.models.user import User


class TestLogin(TestCase):
    """Tests login functionality"""
    def setUp(self):
        self.app = create_app(test=True)
        self.test_user = User(username='lars', email='lars@example.com')
        self.test_user.set_password('testpass')

        self.test_ref1 = Ref(
            entry_type='article',
            title='Test Article',
            author='Test McTestface and T. Testovich',
            year=1905,
            month=5,
            journal="International Journal of Testing",
            pages="12-99",
            owner=self.test_user
        )
        self.test_ref2 = Ref(
            entry_type='book',
            title='Test Book',
            author='Test McTestface',
            year=1995,
            editor="Test Editor",
            owner=self.test_user
        )
        self.test_ref3 = Ref(
            entry_type='book',
            title='Test Book',
            author='Test McTestface',
            year=1995,
            editor="Test Editor",
        )
        with self.app.app_context():
            db.create_all()
            db.session.add(self.test_user)
            db.session.add(self.test_ref1)
            db.session.add(self.test_ref2)
            db.session.add(self.test_ref3)
            db.session.commit()

        self.client = self.app.test_client()

    def _login(self, username, password):
        return self.client.post('/login',
                                data={
                                    'username': username,
                                    'password': password
                                })

    def test_login_required_refs(self):
        """Test that user is redirected to the login view"""
        re = self.client.get('/refs', follow_redirects=True)

        self.assertEqual(re.status_code, 200)
        self.assertTrue("Please log in to access this page." in str(re.data))
        self.assertTrue('<title>Login</title>' in str(re.data))

    def test_refs_logged_in(self):
        """Test that all refs are displayed for a logged-in user."""
        self._login('lars', 'testpass')
        re = self.client.get('/refs')

        self.assertEqual(re.status_code, 200)
        self.assertTrue('<title>Refs</title>' in str(re.data))
        row_count = (str(re.data)).count('<tr')
        self.assertEqual(row_count, 2 + 1)