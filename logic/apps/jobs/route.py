
from flask import Blueprint, request

from logic.apps.jobs import service

blue_print = Blueprint('jobs', __name__, url_prefix='/api/v1/jobs')


@blue_print.route('/<id>', methods=['POST'])
def exec(id: str):

    service.exec(id)

    return '', 201


@blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):

    service.delete(id)
    return '', 200
