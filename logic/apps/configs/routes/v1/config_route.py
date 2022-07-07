from flask import Blueprint, request
from logic.apps.configs.services import config_service

blue_print = Blueprint('configs', __name__, url_prefix='/api/v1/configs')


@blue_print.route('/requirements', methods=['POST'])
def update_requirements():

    config_service.update_requirements(request.data.decode())

    return '', 200
