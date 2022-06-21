"""
This module contains test for the get users endpoints
"""
from tests.test_base import BaseTestCase


class GetUsersTestCase(BaseTestCase):
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
        user = self.create_dummy_user()
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) == 1)
        self.assertIsInstance(data[0], dict)
        self.assertTrue(data[0]['username'] == user.username)
        self.assertTrue(data[0]['id'] == user.id)

    def test_get_user_by_id_with_invalid__user_id_returns_status_404_and_a_message(
            self):
        """
        Test the get user by id /users/<id> route.
        Should return a 404 if no user exists with that id
        """
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'User not found')

    def test_get_user_by_id_with_valid_user_id_returns_status_200_and_list_of_users(
            self):
        """
        Test the get user by id /users/<id> route.
        Should return a 404 if no user exists with that id
        """
        user = self.create_dummy_user()
        response = self.client.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], user.id)
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json['username'], user.username)
