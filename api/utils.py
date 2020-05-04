from typing import Optional
import json
from http import HTTPStatus

from authlib.jose import jwt
from authlib.jose.errors import JoseError
from flask import request, current_app, jsonify

from api.errors import (
    SpycloudInternalServerError,
    SpycloudInvalidCredentialsError,
    SpycloudNotFoundError,
    SpycloudUnexpectedResponseError,
    BadRequestError
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


def jsonify_data(data):
    return jsonify({'data': data})


def jsonify_errors(error):
    return jsonify({'errors': [error]})


def get_response_data(response):

    if response.ok:
        return response.json()

    else:
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise SpycloudInvalidCredentialsError()

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise SpycloudNotFoundError()

        if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise SpycloudInternalServerError()

        else:
            raise SpycloudUnexpectedResponseError(response)
