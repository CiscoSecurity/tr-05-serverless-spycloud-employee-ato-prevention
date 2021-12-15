import jwt
import json
import time
import requests

from json.decoder import JSONDecodeError
from typing import Optional
from http import HTTPStatus
from flask import request, current_app, jsonify, g
from requests.exceptions import (
    ConnectionError,
    InvalidURL,
    SSLError,
    HTTPError,
    InvalidHeader,
)
from jwt import InvalidSignatureError, InvalidAudienceError, DecodeError

from api.errors import (
    SpycloudInternalServerError,
    SpycloudNotFoundError,
    SpycloudUnexpectedResponseError,
    BadRequestError,
    SpycloudTooManyRequestsError,
    SpycloudCatalogError,
    SpycloudSSLError,
    AuthorizationError
)


NO_AUTH_HEADER = 'Authorization header is missing'
WRONG_AUTH_TYPE = 'Wrong authorization type'
WRONG_PAYLOAD_STRUCTURE = 'Wrong JWT payload structure'
WRONG_JWT_STRUCTURE = 'Wrong JWT structure'
WRONG_AUDIENCE = 'Wrong configuration-token-audience'
KID_NOT_FOUND = 'kid from JWT header not found in API response'
WRONG_KEY = ('Failed to decode JWT with provided key. '
             'Make sure domain in custom_jwks_host '
             'corresponds to your SecureX instance region.')
JWK_HOST_MISSING = ('jwks_host is missing in JWT payload. Make sure '
                    'custom_jwks_host field is present in module_type')
WRONG_JWKS_HOST = ('Wrong jwks_host in JWT payload. Make sure domain follows '
                   'the visibility.<region>.cisco.com structure')
UNAUTHORIZED = 'Unauthorized'


def url_for(endpoint) -> Optional[str]:

    return current_app.config['SPYCLOUD_API_URL'].format(
        endpoint=endpoint,
    )


def set_ctr_entities_limit(payload):
    try:
        ctr_entities_limit = int(payload['CTR_ENTITIES_LIMIT'])
        assert ctr_entities_limit > 0
    except (KeyError, ValueError, AssertionError):
        ctr_entities_limit = current_app.config['CTR_DEFAULT_ENTITIES_LIMIT']
    current_app.config['CTR_ENTITIES_LIMIT'] = ctr_entities_limit


def get_public_key(jwks_host, token):
    expected_errors = (
        ConnectionError,
        InvalidURL,
        JSONDecodeError,
        HTTPError,
    )
    try:
        response = requests.get(f"https://{jwks_host}/.well-known/jwks")
        response.raise_for_status()
        jwks = response.json()

        public_keys = {}
        for jwk in jwks['keys']:
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(
                json.dumps(jwk)
            )
        kid = jwt.get_unverified_header(token)['kid']
        return public_keys.get(kid)

    except expected_errors:
        raise AuthorizationError(WRONG_JWKS_HOST)


def get_jwt():
    """
    Get authorization token and validate its signature against the public key
    from /.well-known/jwks endpoint
    """

    expected_errors = {
        KeyError: WRONG_PAYLOAD_STRUCTURE,
        AssertionError: JWK_HOST_MISSING,
        InvalidSignatureError: WRONG_KEY,
        DecodeError: WRONG_JWT_STRUCTURE,
        InvalidAudienceError: WRONG_AUDIENCE,
        TypeError: KID_NOT_FOUND
    }

    token = get_auth_token()
    try:
        jwks_payload = jwt.decode(token, options={'verify_signature': False})
        assert 'jwks_host' in jwks_payload
        jwks_host = jwks_payload.get('jwks_host')
        key = get_public_key(jwks_host, token)
        aud = request.url_root
        payload = jwt.decode(
            token, key=key, algorithms=['RS256'], audience=[aud.rstrip('/')]
        )
        set_ctr_entities_limit(payload)
        return payload['key']
    except tuple(expected_errors) as error:
        message = expected_errors[error.__class__]
        raise AuthorizationError(message)


def get_auth_token():
    """
    Parse the incoming request's Authorization header and Validate it.
    """

    expected_errors = {
        KeyError: NO_AUTH_HEADER,
        AssertionError: WRONG_AUTH_TYPE
    }

    try:
        scheme, token = request.headers['Authorization'].split()
        assert scheme.lower() == 'bearer'
        return token
    except tuple(expected_errors) as error:
        raise AuthorizationError(expected_errors[error.__class__])


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
        HTTPStatus.NOT_FOUND: SpycloudNotFoundError,
        HTTPStatus.INTERNAL_SERVER_ERROR: SpycloudInternalServerError,
        HTTPStatus.TOO_MANY_REQUESTS: SpycloudTooManyRequestsError
    }

    if response.ok:
        return response.json()

    else:
        if response.status_code in expected_response_errors:
            raise expected_response_errors[response.status_code]
        elif response.status_code == HTTPStatus.UNAUTHORIZED or \
                response.status_code == HTTPStatus.FORBIDDEN:
            raise AuthorizationError(response.json()['message'])
        elif response.status_code == HTTPStatus.BAD_REQUEST:
            return {}
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
    Measures execution time of a function and makes delay
    if it's faster than time limit
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


def catch_auth_errors(func):
    def wraps(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (UnicodeEncodeError, InvalidHeader):
            raise AuthorizationError(UNAUTHORIZED)
    return wraps
