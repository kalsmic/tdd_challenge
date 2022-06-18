
from tests.test_base import TestBase


class TestUsers(TestBase):

    def test_hello_tdd(self):
        """
        Test the / route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, TDD!')
