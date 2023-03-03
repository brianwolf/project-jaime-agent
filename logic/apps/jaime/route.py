import time

from flask import Blueprint, jsonify, request

from logic.apps.jaime import service

blue_print = Blueprint('jaime', __name__, url_prefix='/api/v1/jaime')


@blue_print.route('/', methods=['DELETE'])
def delete():

    service.disconnect_with_jaime()
    time.sleep(1)
    service.connect_with_jaime()

    return '', 200


@blue_print.route('/clusters/test', methods=['POST'])
def cluster_test():

    s = request.json
    result = service.test_cluster(s['url'], s['token'], s['type'])
    return jsonify(result.__dict__), 200
