import datetime
import os
from urllib.parse import urljoin, urlparse

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
)
from flask_restful import reqparse

from . import api

CURRENT_JS_HASH = 'b9228724'

login_blueprint = Blueprint('frontend', __name__, static_folder=None)

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, location='json', required=True)
user_parser.add_argument('password', type=str, location='json', required=True)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@login_blueprint.route('/login/static/<path:path>')
def login_static(path):
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), 'static'),
        path,
    )


@login_blueprint.route('/logout')
def logout():
    response = redirect('/login')

    if 'tinysess' in request.cookies:
        response.set_cookie('tinysess', '', expires=0)

    if 'tinycsrf' in request.cookies:
        response.set_cookie('tinycsrf', '', expires=0)

    return response


@login_blueprint.route('/login')
def login():
    return render_template(
       'frontend/login.html',
       js_hash='login/main.{CURRENT_JS_HASH}.js',
      )


@login_blueprint.route('/login', methods=["POST"])
def login_post():
    req = user_parser.parse_args()

    tokens = api.call('get-token-for-login', {
        'username': req['username'],
        'password': req['password'],
        'csrf-strategy': 'cookie',
    })

    # FIXME: This should be in lockstep with the JWT token we get back in tokens['token']
    expires = datetime.datetime.utcnow() + datetime.timedelta(hours=8)

    response = jsonify({})
    response.set_cookie('tinysess', tokens['token'], httponly=True, secure=True, expires=expires)
    response.set_cookie('tinycsrf', tokens['csrf'], httponly=False, secure=True, expires=expires)

    return response
