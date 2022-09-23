import os
import shutil
import subprocess
from multiprocessing import Process
from typing import Any, Dict, List

import requests
from logic.apps.admin.config.variables import Vars, get_var
from logic.apps.filesystem.services import workingdir_service
from logic.apps.works.models.work_model import StatusFinished
from logic.libs.logger.logger import logger

_NAME_FILE_LOGS = 'logs.log'

_FOLDER_MODULES = 'logic/apps/repo_modules_default'

_WORKS_RUNING: Dict[str, Process] = {}


def start(id: str, files_bytes_dict: Dict[str, bytes]):

    logger().info(f'Generando workingdir -> proceso: {id}')
    workingdir_service.create_by_id(id)

    base_path = workingdir_service.fullpath(id)

    for file_name in os.listdir(_FOLDER_MODULES):

        logger().info(f'Generando archivo -> {file_name}')
        shutil.copy(f'{_FOLDER_MODULES}/{file_name}', base_path)

    for file_name, file_bytes in files_bytes_dict.items():

        logger().info(f'Generando archivo -> {file_name}')
        with open(f'{base_path}/{file_name}', 'w') as f:
            f.write(file_bytes.decode())

    process = Process(target=_exec, args=(id,))
    process.start()

    global _WORKS_RUNING
    _WORKS_RUNING[id] = process


def _exec(id: str):

    base_path = workingdir_service.fullpath(id)

    name_file_runner_final = 'runner.pyc' if os.path.exists(
        os.path.join(base_path, 'runner.pyc')) else 'runner.py'

    cmd = f'cd {base_path} && python {name_file_runner_final}'

    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    status = StatusFinished.SUCCESS if process.returncode == 0 else StatusFinished.ERROR

    _notify_work_end(id, status)


def list_all_running() -> List[str]:
    return _WORKS_RUNING.keys()


def delete(id: str):
    global _WORKS_RUNING

    if id in _WORKS_RUNING:
        _WORKS_RUNING[id].kill()
        _WORKS_RUNING.pop(id)


def _notify_work_end(id: str, status: StatusFinished):

    url = get_var(Vars.JAIME_URL) + f'/api/v1/works/{id}/finish'
    body = {"status": status.value}

    requests.patch(url, json=body, timeout=5, verify=False)
