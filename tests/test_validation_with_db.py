"""
This module contains tests that test validation which are not related to the database.
"""
from helpers.validation import is_username_in_db
from tests.test_base import BaseTestCase


class ValidationWithDbTestCase(BaseTestCase):
    """
    Test functions that validate functions that involve data validation from the database"""

    def test_validate_username_exists_returns_none_if_username_does_not_exist(
            self):
        """
        Should return None if the username does not exist
        """
        self.assertIsNone(is_username_in_db('username'))

    def test_validate_username_exists_returns_user_object_if_username_exists(
            self):
        """
        Should return User object if the username exists
        """
        user = self.create_dummy_user('username')
        user_object = is_username_in_db('username')
        self.assertEqual(user_object.username, 'username')
        self.assertEqual(user_object.id, user.id)
