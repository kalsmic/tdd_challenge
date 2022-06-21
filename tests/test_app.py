"""This module contains test for the application's basic functionality."""

from tests.test_base import BaseTestCase


class AppTestCase(BaseTestCase):

    def test_hello_tdd(self):
        """
        Test the / route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, TDD!')

    def test_user_model_repr_result(self):
        """
        Test the User model's __repr__ method."""
        user = self.create_dummy_user()
        self.assertEqual(
            repr(user),
            f"User('{user.id} {user.username}')"
        )
