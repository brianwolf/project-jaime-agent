
from flask import Blueprint, request
from logic.apps.works.services import work_service

blue_print = Blueprint('works', __name__, url_prefix='/api/v1/works')


@blue_print.route('/<id>', methods=['POST'])
def exec(id: str):

    work_service.exec(id)

    return '', 201


@blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):

    work_service.delete(id)
    return '', 200
