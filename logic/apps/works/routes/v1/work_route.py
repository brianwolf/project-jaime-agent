import yaml
from flask import Blueprint, jsonify, request
from logic.apps.works.services import work_service

blue_print = Blueprint('works', __name__, url_prefix='/api/v1/works')


@blue_print.route('/', methods=['POST'])
def exec():

    id = request.form['id']
    files_dict = {
        k: v.read()
        for k, v in request.files.items()
    }

    work_service.start(id, files_dict)

    return '', 201


@blue_print.route('/<id>/logs', methods=['GET'])
def logs(id: str):

    result = work_service.get_logs(id)

    return result, 200
