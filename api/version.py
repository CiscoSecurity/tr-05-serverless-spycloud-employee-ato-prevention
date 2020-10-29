from flask import Blueprint, current_app, jsonify

version_api = Blueprint('version', __name__)


@version_api.route('/version', methods=['POST'])
def version():
    return jsonify({'version': current_app.config['VERSION']})
