"""
This module contains the unit tests for the validation module.
"""

import unittest

from helpers.validation import USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH, validate_username


class TestValidation(unittest.TestCase):
    """
    Test functions that validate user inputs"""

    def test_validate_username_with_spaces_returns_false(self):
        """
        Should return False if the username contains spaces
        """
        self.assertFalse(validate_username('username with spaces'))

    def test_validate_username_with_special_characters_returns_false(self):
        """
        Should return False if the username contains special characters
        """
        self.assertFalse(validate_username('u$#@!_'))

    def test_validate_username_with_empty_string_returns_false(self):
        """
        Should return False if the username is an empty string
        """
        self.assertFalse(validate_username(''))

    def test_validate_username_with_none_returns_false(self):
        """
        Should return False if the username is None
        """
        self.assertFalse(validate_username(None))

    def test_validate_username_with_empty_list_returns_false(self):
        """
        Should return False if the username is an empty list
        """
        self.assertFalse(validate_username([]))

    def test_validate_username_with_list_returns_false(self):
        """
        Should return False if the username is a list
        """
        self.assertFalse(validate_username(['username']))

    def test_validate_username_with_int_returns_false(self):
        """
        Should return False if the username is an int
        """
        self.assertFalse(validate_username(1))

    def test_validate_username_with_length_greater_than_max_length_returns_false(
            self):
        """
        Should return False if the username is greater than MAX LENGTH characters
        """
        self.assertFalse(validate_username('ab' * USERNAME_MAX_LENGTH))

    def test_validate_username_with_length_less_than_min_length_returns_false(
            self):
        """
        Should return False if the username is less than MIN LENGTH characters
        """
        self.assertFalse(validate_username('a' * (USERNAME_MIN_LENGTH - 1)))

    def test_validate_username_with_valid_syntax_returns_true(self):
        """
        Should return True if the username contains valid syntax
        """
        self.assertTrue(validate_username('username'))
