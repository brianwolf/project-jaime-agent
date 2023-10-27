import importlib
import os
import shutil
import subprocess
import sys
import time
from multiprocessing import Process
from typing import Dict, List

import requests

from logic.apps.admin.configs.variables import Vars, get_var
from logic.apps.filesystem import workingdir_service
from logic.apps.jaime.service import get_token
from logic.apps.jobs.model import StatusFinished
from logic.libs.logger.logger import log

_JOBS_RUNING: Dict[str, Process] = {}
_TIME_TO_REINTENT_SECONDS: int = 5
_RESOURCE_FOLDER_PATH: str = 'logic/apps/resources/'


def exec(id: str):

    log.info(f'Recibing job to process id -> {id}')

    process = Process(target=_thread_exec, args=[id])

    global _JOBS_RUNING
    _JOBS_RUNING[id] = process

    log.info(f'Job starting with id -> {id}')

    process.start()


def _thread_exec(id: str):

    workingdir_path = workingdir_service.fullpath(id)

    runner_script = _prepare_files_to_run(id)

    cmd = f'cd {workingdir_path} && python {runner_script}'

    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    status = StatusFinished.SUCCESS if process.returncode == 0 else StatusFinished.ERROR

    _notify_job_end(id, status)
    _clean_files_to_run(id)


def list_all_running() -> List[str]:
    return _JOBS_RUNING.keys()


def delete(id: str):

    global _JOBS_RUNING
    if id in _JOBS_RUNING:

        _JOBS_RUNING[id].kill()
        _JOBS_RUNING.pop(id)
        _kill_process()
        log.info(f'Job running was killed id -> {id}')

    _clean_files_to_run(id)


def _kill_process():
    processes = subprocess.run(
        ['pgrep', 'python'], capture_output=True, text=True).stdout.split('\n')
    pid = processes[len(processes)-2]
    subprocess.run(['kill', '-9', pid], capture_output=True, text=True)


def _notify_job_end(id: str, status: StatusFinished):

    keep_asking = True
    while keep_asking:
        try:
            url = get_var(Vars.JAIME_URL) + f'/api/v1/jobs/{id}/finish'
            body = {"status": status.value}

            token = get_token()
            headers = {'Authorization': f'Bearer {token}'}

            result = requests.patch(
                url, json=body, timeout=5, verify=False, headers=headers)

            if result.status_code != 200:
                log.warn(
                    f'Error Jaime status code -> {result.status_code}')
                time.sleep(_TIME_TO_REINTENT_SECONDS)
                continue

            keep_asking = False

        except Exception as e:
            log.warn(e)
            time.sleep(_TIME_TO_REINTENT_SECONDS)


def _prepare_files_to_run(id: str) -> str:

    runner_script = 'runner.pyc' if os.path.exists(
        f'{_RESOURCE_FOLDER_PATH}/runner.pyc') else 'runner.py'

    tools_script = 'tools.pyc' if os.path.exists(
        f'{_RESOURCE_FOLDER_PATH}/tools.pyc') else 'tools.py'

    workingdir_path = workingdir_service.fullpath(id)

    shutil.copy(f'{_RESOURCE_FOLDER_PATH}/{runner_script}', workingdir_path)
    shutil.copy(f'{_RESOURCE_FOLDER_PATH}/{tools_script}', workingdir_path)

    return runner_script


def _clean_files_to_run(id: str):

    list_files = [
        'runner.py', 'runner.pyc', 'tools.py', 'tools.pyc', 'module.py', 'params.yaml'
    ]

    workingdir_path = workingdir_service.fullpath(id)

    for f in list_files:
        if os.path.exists(f'{workingdir_path}/{f}'):
            os.remove(f'{workingdir_path}/{f}')
