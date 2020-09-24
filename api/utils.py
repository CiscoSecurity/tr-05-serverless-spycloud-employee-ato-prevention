import json
import time
from typing import Optional
from http import HTTPStatus

from authlib.jose import jwt
from authlib.jose.errors import JoseError
from flask import request, current_app, jsonify, g
from requests.exceptions import SSLError

from api.errors import (
    SpycloudInternalServerError,
    SpycloudInvalidCredentialsError,
    SpycloudNotFoundError,
    SpycloudUnexpectedResponseError,
    SpycloudForbidenError,
    BadRequestError,
    SpycloudTooManyRequestsError,
    SpycloudCatalogError,
    SpycloudForbiddenError,
    SpycloudSSLError
)


def url_for(endpoint) -> Optional[str]:

    return current_app.config['SPYCLOUD_API_URL'].format(
        endpoint=endpoint,
    )


def get_jwt():
    """
    Parse the incoming request's Authorization Bearer JWT for some credentials.
    Validate its signature against the application's secret key.

    Note. This function is just an example of how one can read and check
    anything before passing to an API endpoint, and thus it may be modified in
    any way, replaced by another function, or even removed from the module.
    """

    try:
        scheme, token = request.headers['Authorization'].split()
        assert scheme.lower() == 'bearer'
        return jwt.decode(token, current_app.config['SECRET_KEY'])
    except (KeyError, ValueError, AssertionError, JoseError):
        return {}


def get_json(schema):
    """
    Parse the incoming request's data as JSON.
    Validate it against the specified schema.

    Note. This function is just an example of how one can read and check
    anything before passing to an API endpoint, and thus it may be modified in
    any way, replaced by another function, or even removed from the module.
    """

    data = request.get_json(force=True, silent=True, cache=False)

    error = schema.validate(data) or None

    if error:
        raise BadRequestError(
            f'Invalid JSON payload received. {json.dumps(error)}.'
        )

    return data


def jsonify_data(data, errors=None):
    data = {
        'data': data
    }
    if errors:
        data.update({
            'errors': errors
        })
    return jsonify(data)


def format_docs(docs):
    return {'count': len(docs), 'docs': docs}


def get_catalog_error(error_message):
    return SpycloudCatalogError(error_message).json


def jsonify_errors(error):
    data = {
        'errors': [error],
        'data': {}
    }

    if g.get('sightings'):
        data['data'].update({'sightings': format_docs(g.sightings)})

    if g.get('indicators'):
        data['data'].update({'indicators': format_docs(g.indicators)})

    if not data['data']:
        data.pop('data')
    return jsonify(data)


def get_response_data(response):

    expected_response_errors = {
        HTTPStatus.UNAUTHORIZED: SpycloudInvalidCredentialsError,
        HTTPStatus.FORBIDDEN: SpycloudForbidenError,
        HTTPStatus.NOT_FOUND: SpycloudNotFoundError,
        HTTPStatus.INTERNAL_SERVER_ERROR: SpycloudInternalServerError,
        HTTPStatus.TOO_MANY_REQUESTS: SpycloudTooManyRequestsError
    }

    if response.ok:
        return response.json()

    else:
        if response.status_code in expected_response_errors:
            raise expected_response_errors[response.status_code]
        elif response.status_code == HTTPStatus.BAD_REQUEST:
            raise SpycloudForbiddenError(response)
        else:
            raise SpycloudUnexpectedResponseError(response)


def catch_ssl_errors(func):
    def wraps(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SSLError as error:
            raise SpycloudSSLError(error)
    return wraps


def add_delay(func):
    """
    Check request duration and make delay
    if it's faster than spycloud rate limit
    """
    def wraps(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        pause_time = current_app.config['SPYCLOUD_REQUEST_DURATION'] - (
                    time.time() - start)
        if pause_time > 0:
            time.sleep(pause_time)
        return result
    return wraps
