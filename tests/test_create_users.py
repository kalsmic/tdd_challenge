"""This module contains the unit tests for the create users endpoint."""

import json

from model import User
from tests.test_base import BaseTestCase


class CreateUsersTestCase(BaseTestCase):
    """
    Test functions that create users"""

    def test_create_user_without_json_data_returns_400(self):
        """
        Should return 400 if the request data is not JSON
        """
        response = self.client.post(
            '/users/',
            data='username',
            # content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()['message'],
            'Invalid request data')

    def test_create_user_with_no_request_data_returns_400(self):
        """
        Should return 400 if the request data is empty
        """
        response = self.client.post(
            '/users/',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()['message'],
            'Invalid request data')

    def test_create_user_with_invalid_username_returns_400(self):
        """
        Should return 400 if the username is invalid
        """
        response = self.client.post(
            '/users/',
            data=json.dumps({
                'username': '',
                'password': 'password'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()['message'],
            'Invalid request data')

    def test_create_user_with_duplicate_username_returns_409(self):
        """
        Should return 409 if username already exists
        """
        user = self.create_dummy_user("udacian")
        response = self.client.post(
            '/users/',
            data=json.dumps({
                'username': 'udacian',
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json['message'],
            f'Username {user.username} already exists')

    def test_create_user_with_valid_username_returns_201(self):
        """
        Should return 201 if the username is valid
        """
        response = self.client.post(
            '/users/',
            data=json.dumps({
                'username': 'udacians',
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.json, dict)
        user = response.json
        self.assertEqual(user['username'], 'udacians')
        self.assertIn('id', user)
        self.assertIsNotNone(user['id'])
        new_user_in_db = User.query.get(user['id'])
        self.assertIsNotNone(new_user_in_db)
        self.assertEqual(user["id"], new_user_in_db.id)
        self.assertEqual(user["username"], new_user_in_db.username)
