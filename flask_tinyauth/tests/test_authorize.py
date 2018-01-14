import unittest
from unittest import mock

from flask import Flask

from flask_tinyauth import authorize


class TestAuthorize(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.debug = True
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = True
        self.app.config['TINYAUTH_SERVICE'] = 'test'
        self.app.config['TINYAUTH_ENDPOINT'] = 'http://localhost/'
        self.app.config['TINYAUTH_ACCESS_KEY_ID'] = 'root'
        self.app.config['TINYAUTH_SECRET_ACCESS_KEY'] = 'password'
        self.client = self.app.test_client()

        @self.app.route('/')
        def index():
            authorize.authorize_or_401('TestPermission', 'res_class', 'res_type')
            return 'INDEX'

        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        self._ctx.pop()

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_401(self, session):
        session.post.return_value.json.return_value = {
            'Authorized': True,
        }
        self.client.get('/')
