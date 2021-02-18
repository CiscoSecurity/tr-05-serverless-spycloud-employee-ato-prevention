from unittest import mock
from .utils import headers
from pytest import fixture
from http import HTTPStatus
from requests.exceptions import SSLError

from tests.unit.mock_for_tests import (
    BREACH_EMAIL_RESPONSE_MOCK,
    EXPECTED_SUCCESS_RESPONSE,
    EXPECTED_RESPONSE_401_ERROR,
    EXPECTED_RESPONSE_403_ERROR,
    EXPECTED_RESPONSE_500_ERROR,
    EXPECTED_RESPONSE_404_ERROR,
    CATALOG_17494_RESPONSE_MOCK,
    CATALOG_17551_RESPONSE_MOCK,
    CATALOG_PASS_RESPONSE_MOCK,
    EXPECTED_SUCCESS_RESPONSE_WITHOUT_1_CATALOG,
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
    yield '/observe/observables'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='module')
def invalid_json():
    return [{'type': 'unknown', 'value': ''}]


def test_enrich_call_with_invalid_json_failure(route, client, valid_jwt,
                                               invalid_json):
    response = client.post(
        route, headers=headers(valid_jwt()), json=invalid_json
    )

    expected_payload = {
        'errors': [
            {
                'code': 'invalid argument',
                'message': mock.ANY,
                'type': 'fatal',
            }
        ]
    }

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == expected_payload


@fixture(scope='module')
def valid_json():
    return [{'type': 'email', 'value': 'admin@example.org'}]


@fixture(scope='module')
def valid_json_multiple():
    return [
        {'type': 'email', 'value': 'admin@example.org'},
        {'type': 'email', 'value': 'second@example.org'},
    ]


def test_enrich_call_success(route, client, valid_jwt, valid_json,
                             mock_request):

    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=BREACH_EMAIL_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17551_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17494_RESPONSE_MOCK),
    )

    response = client.post(
        route, headers=headers(valid_jwt()), json=valid_json
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert data['data']['sightings']['docs'][0].pop('id')
    assert data['data']['sightings']['docs'][1].pop('id')

    assert data['data']['indicators']['docs'][0].pop('id')
    assert data['data']['indicators']['docs'][1].pop('id')

    assert data == EXPECTED_SUCCESS_RESPONSE


def test_enrich_call_success_without_catalog(route, client, valid_jwt,
                                             valid_json, mock_request):

    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=BREACH_EMAIL_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17551_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_PASS_RESPONSE_MOCK),
    )

    response = client.post(
        route, headers=headers(valid_jwt()), json=valid_json
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert data['data']['sightings']['docs'][0].pop('id')
    assert data['data']['sightings']['docs'][1].pop('id')

    assert data['data']['indicators']['docs'][0].pop('id')

    assert data == EXPECTED_SUCCESS_RESPONSE_WITHOUT_1_CATALOG


def test_enrich_call_auth_error(route, client, valid_jwt, valid_json,
                                mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(status_code=HTTPStatus.UNAUTHORIZED,
                              payload=SPYCLOUD_401_RESPONSE)
    )
    response = client.post(
        route, headers=headers(valid_jwt()),  json=valid_json
    )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_401_ERROR


def test_enrich_call_permission_error(route, client, valid_jwt, valid_json,
                                      mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(status_code=HTTPStatus.FORBIDDEN,
                              payload=SPYCLOUD_403_RESPONSE)
    )
    response = client.post(
        route, headers=headers(valid_jwt()), json=valid_json
    )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_403_ERROR


def test_enrich_call_404(route, client, valid_jwt, valid_json,
                         mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(status_code=404)
    )
    response = client.post(
        route, headers=headers(valid_jwt()), json=valid_json
    )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_404_ERROR


def test_enrich_call_500(route, client, valid_jwt, valid_json,
                         mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(status_code=500)
    )
    response = client.post(
        route, headers=headers(valid_jwt()), json=valid_json
    )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_500_ERROR


def test_enrich_call_ssl_error(route, client, valid_jwt, valid_json,
                               mock_request):
    mock_exception = mock.MagicMock()
    mock_exception.reason.args.__getitem__().verify_message \
        = 'self signed certificate'
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        SSLError(mock_exception)
    )

    response = client.post(
        route, headers=headers(valid_jwt()), json=valid_json
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert data == EXPECTED_RESPONSE_SSL_ERROR


def test_enrich_error_with_data(route, client, valid_jwt, valid_json_multiple,
                                mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=BREACH_EMAIL_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17551_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17494_RESPONSE_MOCK),
        spycloud_api_response(status_code=HTTPStatus.FORBIDDEN,
                              payload=SPYCLOUD_403_RESPONSE)
    )
    response = client.post(
        route, headers=headers(valid_jwt()), json=valid_json_multiple
    )
    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert data['data']['sightings']['docs'][0].pop('id')
    assert data['data']['sightings']['docs'][1].pop('id')

    assert data['data']['indicators']['docs'][0].pop('id')
    assert data['data']['indicators']['docs'][1].pop('id')

    expected_response = {}
    expected_response.update(EXPECTED_SUCCESS_RESPONSE)
    expected_response.update(EXPECTED_RESPONSE_403_ERROR)

    assert data == expected_response


def test_enrich_call_auth_header_error(route, client, valid_jwt, valid_json,
                                       mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=BREACH_EMAIL_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17551_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17494_RESPONSE_MOCK),
    )

    response = client.post(route, headers={}, json=valid_json)

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert data == EXPECTED_AUTHORIZATION_HEADER_ERROR


def test_enrich_call_auth_type_error(route, client, valid_jwt, valid_json,
                                     mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=BREACH_EMAIL_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17551_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17494_RESPONSE_MOCK),
    )
    header = {
        'Authorization': 'Basic test_jwt'
    }

    response = client.post(route, headers=header, json=valid_json)

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert data == EXPECTED_AUTHORIZATION_TYPE_ERROR


def test_enrich_call_jwt_structure_error(route, client, valid_jwt, valid_json,
                                         mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=BREACH_EMAIL_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17551_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17494_RESPONSE_MOCK),
    )
    header = {
        'Authorization': 'Bearer bad_jwt_token'
    }

    response = client.post(route, headers=header, json=valid_json)

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert data == EXPECTED_JWT_STRUCTURE_ERROR


def test_enrich_call_payload_structure_error(route, client,
                                             valid_jwt,
                                             valid_json, mock_request):
    mock_request.side_effect = (
        spycloud_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT),
        spycloud_api_response(payload=BREACH_EMAIL_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17551_RESPONSE_MOCK),
        spycloud_api_response(payload=CATALOG_17494_RESPONSE_MOCK),
    )

    response = client.post(
        route,
        headers=headers(valid_jwt(wrong_structure=True)),
        json=valid_json
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert data == EXPECTED_JWT_PAYLOAD_STRUCTURE_ERROR
