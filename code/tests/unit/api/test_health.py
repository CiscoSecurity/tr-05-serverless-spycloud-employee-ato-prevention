from http import HTTPStatus

from pytest import fixture
from unittest import mock
from requests.exceptions import SSLError

from .utils import headers
from tests.unit.mock_for_tests import (
    WATCHLIST_RESPONSE_MOCK,
    EXPECTED_RESPONSE_404_ERROR,
    EXPECTED_RESPONSE_500_ERROR,
    EXPECTED_RESPONSE_401_ERROR,
    EXPECTED_RESPONSE_403_ERROR,
    EXPECTED_RESPONSE_SSL_ERROR,
    SPYCLOUD_401_RESPONSE,
    SPYCLOUD_403_RESPONSE,
    EXPECTED_AUTHORIZATION_HEADER_ERROR,
    EXPECTED_AUTHORIZATION_TYPE_ERROR,
    EXPECTED_JWT_STRUCTURE_ERROR,
    EXPECTED_JWT_PAYLOAD_STRUCTURE_ERROR,
)

from ..conftest import spycloud_api_response
from ..mock_for_tests import EXPECTED_RESPONSE_OF_JWKS_ENDPOINT


def routes():
    yield '/health'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


def test_health_call_success(route, client, valid_jwt, mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=WATCHLIST_RESPONSE_MOCK)
    )
    response = client.post(route, headers=headers(valid_jwt()))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'data': {'status': 'ok'}}


def test_health_call_auth_error(route, client, valid_jwt,
                                mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(
            status_code=HTTPStatus.UNAUTHORIZED,
            payload=SPYCLOUD_401_RESPONSE)
    )
    response = client.post(route, headers=headers(valid_jwt()))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_401_ERROR


def test_health_call_permission_error(route, client, valid_jwt,
                                      mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(
            status_code=HTTPStatus.FORBIDDEN,
            payload=SPYCLOUD_403_RESPONSE)
    )
    response = client.post(route, headers=headers(valid_jwt()))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_403_ERROR


def test_health_call_404(route, client, valid_jwt, mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(status_code=404)
    )
    response = client.post(route, headers=headers(valid_jwt()))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_404_ERROR


def test_health_call_500(route, client, valid_jwt, mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(status_code=500)
    )
    response = client.post(route, headers=headers(valid_jwt()))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_500_ERROR


def test_health_call_ssl_error(route, client, valid_jwt, mock_request):
    mock_exception = mock.MagicMock()
    mock_exception.reason.args.__getitem__().verify_message \
        = 'self signed certificate'
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        SSLError(mock_exception)
    )

    response = client.post(route, headers=headers(valid_jwt()))

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert data == EXPECTED_RESPONSE_SSL_ERROR


def test_health_call_auth_header_error(route, client, valid_jwt,
                                       mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=WATCHLIST_RESPONSE_MOCK)
    )

    response = client.post(route, headers={})

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert data == EXPECTED_AUTHORIZATION_HEADER_ERROR


def test_health_call_auth_type_error(route, client, valid_jwt,
                                     mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=WATCHLIST_RESPONSE_MOCK)
    )
    header = {
        'Authorization': 'Basic test_jwt'
    }

    response = client.post(route, headers=header)

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert data == EXPECTED_AUTHORIZATION_TYPE_ERROR


def test_health_call_jwt_structure_error(route, client, valid_jwt,
                                         mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=WATCHLIST_RESPONSE_MOCK)
    )
    header = {
        'Authorization': 'Bearer bad_jwt_token'
    }

    response = client.post(route, headers=header)

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert data == EXPECTED_JWT_STRUCTURE_ERROR


def test_health_call_payload_structure_error(route, client,
                                             valid_jwt,
                                             mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=WATCHLIST_RESPONSE_MOCK)
    )

    response = client.post(
        route,
        headers=headers(valid_jwt(wrong_structure=True))
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert data == EXPECTED_JWT_PAYLOAD_STRUCTURE_ERROR
