import ntpath
from io import BytesIO

from flask import Blueprint, jsonify, request, send_file
from logic.apps.filesystem.services import workingdir_service
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
    workingdir_service.delete(id)

    return '', 200


@blue_print.route('/<id>/workspace', methods=['GET'])
def download_workspace(id: str):

    zip_name = f'{id}.zip'
    zip_path = workingdir_service.download_zip(id)

    return send_file(BytesIO(open(zip_path, 'rb').read()),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=ntpath.basename(zip_name))
