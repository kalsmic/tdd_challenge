import os
import unittest
from flask_migrate import upgrade

from app import (
    create_app,
    db,
)


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        This method is called once before any tests are run."""
        os.environ.get('TEST_DATABASE_URL')
        cls.app = create_app('config.TestingConfig')

        cls.app_context = cls.app.app_context()
        # push the app context to the app context stack
        cls.app_context.push()
        # upgrade the database to the latest version
        upgrade()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        This method is called once after all tests are run."""
        # drop all tables from the database
        db.drop_all()

        # delete the alembic_verison table
        db.engine.execute('DROP TABLE IF EXISTS "alembic_version"')
        # remove the app context from the app context stack
        cls.app_context.pop()

    def setUp(self) -> None:
        """
        This method is called before each test."""
        self.app = create_app('config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        """
        This method is called after each test."""
        # delete all records from the tables beginning with the ones without dependencies
        # (the ones that are not referenced by any other table)
        for table in reversed(db.metadata.sorted_tables):
            db.engine.execute(table.delete())

        db.session.commit()
        db.session.remove()

        self.app_context.pop()

    def test_hello_tdd(self):
        """
        Test the / route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, TDD!')
