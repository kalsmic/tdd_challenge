from model import User
from tests.test_base import TestBase


class TestUsers(TestBase):
    def test_get_users_returns_status_200_and_empty_list_if_no_users_exist(
            self):
        """
        Test the get users /users/ route.
        Should return an empty list"""
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) == 0)

    def test_get_users_returns_status_200_and_list_of_users_if_users_exist(
            self):
        """
        Test the get users /users/ route.
        Should return a list of users
        """
        # Create a user
        user = User(username='test')
        user.insert()
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) == 1)
        self.assertIsInstance(data[0], dict)
        self.assertTrue(data[0]['username'] == user.username)
        self.assertTrue(data[0]['id'] == user.id)
