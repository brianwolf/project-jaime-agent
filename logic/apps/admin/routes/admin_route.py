import ntpath
import os
from io import BytesIO

from flask import Blueprint, jsonify, send_file
from logic.apps.admin.config.variables import Vars
from logic.libs.variables.variables import all_vars, get_var
from logic.apps.admin.config import app

blue_print = Blueprint('admin', __name__, url_prefix='/')


@blue_print.route('/vars')
def get_vars():
    return jsonify(all_vars())


@blue_print.route('')
def alive():
    version = get_var(Vars.VERSION)
    return jsonify(version=version)


@blue_print.route('/postman')
def get_postman():
    postman_files = sorted([
        f for f in os.listdir(os.getcwd())
        if str(f).endswith('.postman_collection.json')
    ], reverse=True)

    collection_dir = next(iter(postman_files), None)

    return send_file(BytesIO(open(collection_dir, 'rb').read()),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=ntpath.basename(collection_dir))


@blue_print.route('/alive')
def alive_jaime():
    return jsonify(id=app.get_id_agent())
