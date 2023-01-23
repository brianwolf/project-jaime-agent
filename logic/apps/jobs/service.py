import os
import subprocess
from multiprocessing import Process
from typing import Any, Dict, List

import requests

from logic.apps.admin.configs.variables import Vars, get_var
from logic.apps.filesystem import workingdir_service
from logic.apps.jobs.model import StatusFinished
from logic.libs.logger import logger

_WORKS_RUNING: Dict[str, Process] = {}


def exec(id: str):

    logger.log.info(f'Recibiendo proceso para ejecutar -> {id}')

    base_path = workingdir_service.fullpath(id)

    runner_script = 'runner.pyc' if os.path.exists(
        f'{base_path}/runner.pyc') else 'runner.py'

    process = Process(target=_thread_exec, args=(id, runner_script))
    process.start()

    global _WORKS_RUNING
    _WORKS_RUNING[id] = process


def _thread_exec(id: str, runner_script: str):

    base_path = workingdir_service.fullpath(id)

    cmd = f'cd {base_path} && python {runner_script}'

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

    url = get_var(Vars.JAIME_URL) + f'/api/v1/jobs/{id}/finish'
    body = {"status": status.value}

    token = os.getenv('JAIME_TOKEN')
    print(token)
    headers = {'Authorization': f'Bearer {token}'}

    result = requests.patch(url, json=body, timeout=5,
                            verify=False, headers=headers)
    if result.status_code != 200:
        raise Exception(f'Error Jaime status code -> {result.status_code}')

    logger.log.info(f'Proceso terminado -> {id}')
