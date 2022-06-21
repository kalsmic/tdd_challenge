"""
This module contains tests for the update users endpoint."""
import json

from tests.test_base import BaseTestCase


class UpdateUserTestCase(BaseTestCase):
    """
    Test functions that update users"""

    def test_update_user_without_invalid_username_returns_status_400_and_message(self):
        """
        Should return 400 if the request data is not JSON
        """
        user = self.create_dummy_user()
        response = self.client.put(
            f'/users/{user.id}',
            data='usern ame',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()['message'],
            'Invalid request data')

    def test_update_user_with_invalid_user_id_returns_status_404_and_message(self):
        """
        Should return 404 if the user id is invalid
        """
        response = self.client.put(
            '/users/1',
            data=json.dumps({
                'username': 'username'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()['message'],
            'User not found')

    def test_update_user_with_duplicate_username_returns_status_409_and_message(self):
        """
        Should return 409 if the username is a duplicate if username already assigned to another user
        """
        user = self.create_dummy_user()
        user2 = self.create_dummy_user("John")
        response = self.client.put(
            f'/users/{user.id}',
            data=json.dumps({
                'username': f'{user2.username}'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.get_json()['message'],
            f'Username {user2.username} already exists')

    def test_update_user_with_the_same_username_returns_satus_204(self):
        """
        Should return 204 if the username is the same as the current username in the database
        """
        user = self.create_dummy_user(username="John")
        response = self.client.put(
            f'/users/{user.id}',
            data=json.dumps({
                'username': 'John'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.get_json())

    def test_update_user_with_invalid_username_and_valid_user_id_returns_status_400_and_message(self):
        """
        Should return 400 if the username is invalid
        """
        user = self.create_dummy_user()
        response = self.client.put(
            f'/users/{user.id}',
            data=json.dumps({
                'username': 'usern ame'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()['message'],
            'Invalid request data')

    def test_update_user_with_valid_and_unique_username_returns_satus_200_and_message(self):
        """
        Should return 200 if the username is valid and unique"""
        user = self.create_dummy_user(username="John")
        new_username = 'Jimmy'
        response = self.client.put(
            f'/users/{user.id}',
            data=json.dumps({
                'username': new_username
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertIn('user', data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'User Updated Successfully')
        self.assertIsInstance(data['user'], dict)
        self.assertIn('username', data['user'])
        self.assertIn('id', data['user'])
        self.assertEqual(data['user']['username'], new_username)
        self.assertEqual(user.username, new_username)
