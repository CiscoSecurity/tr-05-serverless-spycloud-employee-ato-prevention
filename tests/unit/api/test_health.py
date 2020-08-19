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
    EXPECTED_RESPONSE_SSL_ERROR
)


def routes():
    yield '/health'


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
        payload = WATCHLIST_RESPONSE_MOCK

    else:
        mock_response.status_code = status_error

    mock_response.json = lambda: payload

    return mock_response


def test_health_call_success(route, client, valid_jwt, spycloud_api_request):
    spycloud_api_request.return_value = spycloud_api_response(ok=True)
    response = client.post(route, headers=headers(valid_jwt))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'data': {'status': 'ok'}}


def test_health_call_auth_error(route, client, valid_jwt,
                                spycloud_api_request):
    spycloud_api_request.return_value = spycloud_api_response(ok=False,
                                                              status_error=401)
    response = client.post(route, headers=headers(valid_jwt))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_401_ERROR


def test_health_call_permission_error(route, client, valid_jwt,
                                      spycloud_api_request):
    spycloud_api_request.return_value = spycloud_api_response(ok=False,
                                                              status_error=403)
    response = client.post(route, headers=headers(valid_jwt))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_403_ERROR


def test_health_call_404(route, client, valid_jwt, spycloud_api_request):
    spycloud_api_request.return_value = spycloud_api_response(ok=False,
                                                              status_error=404)
    response = client.post(route, headers=headers(valid_jwt))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_404_ERROR


def test_health_call_500(route, client, valid_jwt, spycloud_api_request):
    spycloud_api_request.return_value = spycloud_api_response(ok=False,
                                                              status_error=500)
    response = client.post(route, headers=headers(valid_jwt))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == EXPECTED_RESPONSE_500_ERROR


def test_enrich_call_ssl_error(route, client, valid_jwt, spycloud_api_request):
    mock_exception = mock.MagicMock()
    mock_exception.reason.args.__getitem__().verify_message \
        = 'self signed certificate'
    spycloud_api_request.side_effect = SSLError(mock_exception)

    response = client.post(route, headers=headers(valid_jwt))

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert data == EXPECTED_RESPONSE_SSL_ERROR
