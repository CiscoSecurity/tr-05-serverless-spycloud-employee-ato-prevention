import requests
from flask import Blueprint, current_app

from api.utils import (
    get_jwt,
    jsonify_data,
    url_for,
    get_response_data,
    catch_ssl_errors
)

health_api = Blueprint('health', __name__)


@catch_ssl_errors
def check_spycloud_health():
    url = url_for('watchlist/example.org')

    headers = {
        **current_app.config['SPYCLOUD_BASE_HEADERS'],
        'X-API-Key': get_jwt()
    }

    response = requests.get(url, headers=headers)

    return get_response_data(response)


@health_api.route('/health', methods=['POST'])
def health():
    check_spycloud_health()
    return jsonify_data({'status': 'ok'})
