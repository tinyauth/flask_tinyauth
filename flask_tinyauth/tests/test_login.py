import json
import unittest
from unittest import mock

from flask import Flask

from flask_tinyauth import authorize, login


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
        self.app.register_blueprint(login.login_blueprint)
        self.client = self.app.test_client()

        @self.app.route('/')
        def index():
            authorize.authorize_or_401('TestPermission', 'res_class', 'res_key')
            return 'INDEX'

        @self.app.route('/hi')
        def hi():
            authorize.authorize_or_login('TestPermission', 'res_class', 'res_key')
            return 'INDEX'

        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        self._ctx.pop()

    @mock.patch('flask_tinyauth.api.session')
    def test_login_post(self, session):
        session.post.return_value.json.return_value = {
            'token': '',
            'csrf': '',
        }

        response = self.client.post('/login', content_type='application/json', data=json.dumps({
            'username': 'root',
            'password': 'password',
        }))

        assert response.status_code == 200
        assert json.loads(response.get_data(as_text=True)) == {}

        assert session.post.call_args is not None
        assert session.post.call_args[0][0] == 'http://localhost/api/v1/services/test/get-token-for-login'
        request_kwargs = session.post.call_args[1]
        assert request_kwargs['auth'] == ('root', 'password')
        assert request_kwargs['headers']['Accept'] == 'application/json'
        assert request_kwargs['headers']['Content-Type'] == 'application/json'
        assert request_kwargs['json'] == {
            'csrf-strategy': 'cookie',
            'username': 'root',
            'password': 'password',
        }
