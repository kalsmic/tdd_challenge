from model import User
from tests.test_base import BaseTestCase


class DeleteTestCase(BaseTestCase):
    def test_delete_user_with_invalid_user_id_returns_404(self):
        """
        Should return 404 if no user exists with that id
        """
        response = self.client.delete('/users/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'User not found')

    def test_delete_user_with_valid_user_id_returns_200_and_message(self):
        """
        Should return 200 and message if user is deleted
        """
        user = self.create_dummy_user()
        user_id = user.id
        response = self.client.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], f'User with id {user.id} deleted')
        self.assertIsNone(User.query.get(user_id))
