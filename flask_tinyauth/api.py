import requests
from flask import current_app

from . import exceptions

session = requests.Session()


def get_arn_base():
    return ':'.join((
        'arn',
        current_app.config.get('TINYAUTH_PARTITION', 'tinyauth'),
        current_app.config['TINYAUTH_SERVICE'],
        current_app.config.get('TINYAUTH_REGION', 'default'),
        ''
    ))


def format_arn(resource_class, resource=''):
    return ':'.join((
        get_arn_base(),
        '/'.join((resource_class, resource))
    ))


def call(api, request):
    endpoint = current_app.config['TINYAUTH_ENDPOINT']
    service = current_app.config['TINYAUTH_SERVICE']

    try:
        response = session.post(
            f'{endpoint}api/v1/services/{service}/{api}',
            auth=(
                current_app.config['TINYAUTH_ACCESS_KEY_ID'],
                current_app.config['TINYAUTH_SECRET_ACCESS_KEY'],
            ),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            json=request,
        ).json()
    except requests.exceptions.ConnectionError as e:
        raise exceptions.ConnectionError()

    return response
