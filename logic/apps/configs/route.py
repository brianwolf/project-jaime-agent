from flask import Blueprint, request
from logic.apps.configs import service

blue_print = Blueprint('configs', __name__, url_prefix='/api/v1/configs')


@blue_print.route('/requirements', methods=['POST'])
def update_requirements():

    service.update_requirements(request.data.decode())

    return '', 200


@blue_print.route('/logs', methods=['GET'])
def get_logs():
    return service.get_logs(), 200
