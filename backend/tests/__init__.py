import unittest

from gasprice import create_app


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SERVER_NAME'] = 'localhost'

        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        pass