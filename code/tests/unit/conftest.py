from tests.utils.crypto import generate_rsa_key_pair
import jwt

from app import app
from pytest import fixture
from http import HTTPStatus
from api.errors import AUTH_ERROR
from unittest.mock import MagicMock, patch


@fixture(scope="session")
def test_keys_and_token():
    private_pem, jwks, kid = generate_rsa_key_pair()
    wrong_private_pem, wrong_jwks, _ = generate_rsa_key_pair()

    return {
        "private_key": private_pem,
        "jwks": jwks,
        "kid": kid,
        "wrong_private_key": wrong_private_pem,
        "wrong_jwks": wrong_jwks,
    }


@fixture(scope='session')
def client(test_keys_and_token):
    app.rsa_private_key = test_keys_and_token["private_key"]

    app.testing = True

    with app.test_client() as client:
        yield client


@fixture(scope='session')
def valid_jwt(client):
    def _make_jwt(
            key='some_key',
            jwks_host='visibility.amp.cisco.com',
            aud='http://localhost',
            wrong_structure=False,
            wrong_jwks_host=False,
            kid=None,
            private_key=None
    ):
        payload = {
            'key': key,
            'jwks_host': jwks_host,
            'aud': aud,
        }

        if wrong_jwks_host:
            payload.pop('jwks_host')

        if wrong_structure:
            payload.pop('key')

        signing_key = private_key or app.rsa_private_key
        signing_kid = kid or "02B1174234C29F8EFB69911438F597FF3FFEE6B7"

        return jwt.encode(payload, signing_key, algorithm="RS256", headers={"kid": signing_kid})

    return _make_jwt


def spycloud_api_response(status_code=HTTPStatus.OK, payload=None):
    mock_response = MagicMock()

    mock_response.status_code = status_code
    mock_response.ok = status_code == HTTPStatus.OK

    mock_response.json = lambda: payload

    return mock_response


@fixture(scope='module')
def valid_json():
    return [{'type': 'email', 'value': 'admin@example.org'}]


@fixture(scope='function')
def mock_request():
    with patch('requests.get') as mock_request:
        yield mock_request


@fixture(scope='module')
def authorization_errors_expected_payload(route):
    def _make_payload_message(message):
        payload = {
            'errors': [
                {
                    'code': AUTH_ERROR,
                    'message': f'Authorization failed: {message}',
                    'type': 'fatal'
                }
            ]
        }
        return payload

    return _make_payload_message
