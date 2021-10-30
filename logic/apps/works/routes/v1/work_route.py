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


@blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):

    work_service.delete(id)
    return '', 200


@blue_print.route('/', methods=['GET'])
def get():

    result = work_service.list_all()
    return jsonify(result), 200


def _is_yaml(text: str) -> bool:
    try:
        yaml.load(request.data, Loader=yaml.FullLoader)
        return True

    except Exception:
        return False
