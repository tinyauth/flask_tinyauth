import datetime

from flask import abort, request

from . import api


def authorize(permission, resource_class, resource='', ctx=None):
    context = {
        'SourceIp': request.remote_addr,
        'RequestDateTime': datetime.datetime.utcnow(),
    }
    context.update(ctx or {})

    authorized = api.call('authorize-by-token', {
        'permit': {
            permission: api.format_arn(resource_class, resource)
        },
        'headers': request.headers.to_wsgi_list(),
        'context': context,
    })

    if authorized['Authorized'] is not True:
        abort(401, authorized)

    return authorized
