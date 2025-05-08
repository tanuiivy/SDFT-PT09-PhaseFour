from flask import Blueprint, jsonify, request
from server.services.soldier_services import fetch_a_soldier, fetch_all_soldiers

zeraki_api = Blueprint('api', __name__)

@zeraki_api.route('/soldiers', methods=['GET'])
def soldiers_list():
    data, status_code = fetch_all_soldiers()
    return jsonify(data), status_code

@zeraki_api.route('/soldiers/<int:id>', methods=['GET'])
def soldier_detail(id):
    data, status_code = fetch_a_soldier(id)
    return jsonify(data), status_code
