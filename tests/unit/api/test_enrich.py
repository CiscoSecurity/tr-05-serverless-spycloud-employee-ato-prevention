from pytest import fixture
from unittest import mock
from http import HTTPStatus

from .utils import headers
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
    EXPECTED_SUCCESS_RESPONSE_WITHOUT_1_CATALOG
)


def routes():
    yield '/observe/observables'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='function')
def spycloud_api_request():
    with mock.patch('requests.get') as mock_request:
        yield mock_request


def spycloud_api_response(*, ok, status_error=None, payload=None):
    mock_response = mock.MagicMock()

    mock_response.ok = ok

    if ok:
        if not payload:
            payload = BREACH_EMAIL_RESPONSE_MOCK

    else:
        mock_response.status_code = status_error
        mock_response.text = str(payload)

    mock_response.json = lambda: payload

    return mock_response


@fixture(scope='module')
def invalid_json():
    return [{'type': 'unknown', 'value': ''}]


def test_enrich_call_with_invalid_json_failure(route, client, valid_jwt,
                                               invalid_json):
    response = client.post(
        route, headers=headers(valid_jwt), json=invalid_json
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
                             spycloud_api_request):

    spycloud_api_request.side_effect = (
        spycloud_api_response(ok=True),
        spycloud_api_response(ok=True, payload=CATALOG_17551_RESPONSE_MOCK),
        spycloud_api_response(ok=True, payload=CATALOG_17494_RESPONSE_MOCK),
    )

    response = client.post(
        route, headers=headers(valid_jwt), json=valid_json
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert data['data']['sightings']['docs'][0].pop('id')
    assert data['data']['sightings']['docs'][1].pop('id')

    assert data['data']['indicators']['docs'][0].pop('id')
    assert data['data']['indicators']['docs'][1].pop('id')

    assert data == EXPECTED_SUCCESS_RESPONSE


def test_enrich_call_success_without_catalog(route, client, valid_jwt,
                                             valid_json, spycloud_api_request):

    spycloud_api_request.side_effect = (
        spycloud_api_response(ok=True),
        spycloud_api_response(ok=True, payload=CATALOG_17551_RESPONSE_MOCK),
        spycloud_api_response(ok=True, payload=CATALOG_PASS_RESPONSE_MOCK),
    )

    response = client.post(
        route, headers=headers(valid_jwt), json=valid_json
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert data['data']['sightings']['docs'][0].pop('id')
    assert data['data']['sightings']['docs'][1].pop('id')

    assert data['data']['indicators']['docs'][0].pop('id')

    assert data == EXPECTED_SUCCESS_RESPONSE_WITHOUT_1_CATALOG



def test_enrich_call_auth_error(route, client, valid_jwt, valid_json,
                                spycloud_api_request):
    spycloud_api_request.return_value = spycloud_api_response(ok=False,
                                                              status_error=401)
    response = client.post(
        route, headers=headers(valid_jwt),  json=valid_json
    )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_401_ERROR


def test_enrich_call_permission_error(route, client, valid_jwt, valid_json,
                                      spycloud_api_request):
    spycloud_api_request.return_value = spycloud_api_response(ok=False,
                                                              status_error=403)
    response = client.post(
        route, headers=headers(valid_jwt), json=valid_json
    )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_403_ERROR


def test_enrich_call_404(route, client, valid_jwt, valid_json,
                         spycloud_api_request):
    spycloud_api_request.return_value = spycloud_api_response(ok=False,
                                                              status_error=404)
    response = client.post(
        route, headers=headers(valid_jwt), json=valid_json
    )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_404_ERROR


def test_enrich_call_500(route, client, valid_jwt, valid_json,
                         spycloud_api_request):
    spycloud_api_request.return_value = spycloud_api_response(ok=False,
                                                              status_error=500)
    response = client.post(
        route, headers=headers(valid_jwt), json=valid_json
    )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_500_ERROR


def test_enrich_error_with_data(route, client, valid_jwt, valid_json_multiple,
                                spycloud_api_request):
    spycloud_api_request.side_effect = (
        spycloud_api_response(ok=True),
        spycloud_api_response(ok=True, payload=CATALOG_17551_RESPONSE_MOCK),
        spycloud_api_response(ok=True, payload=CATALOG_17494_RESPONSE_MOCK),
        spycloud_api_response(ok=False, status_error=401)
    )
    response = client.post(
        route, headers=headers(valid_jwt), json=valid_json_multiple
    )
    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert data['data']['sightings']['docs'][0].pop('id')
    assert data['data']['sightings']['docs'][1].pop('id')

    assert data['data']['indicators']['docs'][0].pop('id')
    assert data['data']['indicators']['docs'][1].pop('id')

    expected_response = {}
    expected_response.update(EXPECTED_SUCCESS_RESPONSE)
    expected_response.update(EXPECTED_RESPONSE_401_ERROR)

    assert data == expected_response
