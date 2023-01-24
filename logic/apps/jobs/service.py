import os
import subprocess
import time
from multiprocessing import Process
from typing import Any, Dict, List

import requests

from logic.apps.admin.configs.variables import Vars, get_var
from logic.apps.filesystem import workingdir_service
from logic.apps.jaime.service import get_token
from logic.apps.jobs.model import StatusFinished
from logic.libs.logger import logger

_JOBS_RUNING: Dict[str, Process] = {}
_TIME_TO_REINTENT_SECONDS: int = 5


def exec(id: str):

    logger.log.info(f'Recibe job to process id -> {id}')

    base_path = workingdir_service.fullpath(id)

    runner_script = 'runner.pyc' if os.path.exists(
        f'{base_path}/runner.pyc') else 'runner.py'

    process = Process(target=_thread_exec, args=(id, runner_script))
    process.start()

    global _JOBS_RUNING
    _JOBS_RUNING[id] = process
    logger.log.info(f'Job started id -> {id}')


def _thread_exec(id: str, runner_script: str):

    base_path = workingdir_service.fullpath(id)

    cmd = f'cd {base_path} && python {runner_script}'

    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    status = StatusFinished.SUCCESS if process.returncode == 0 else StatusFinished.ERROR

    _notify_job_end(id, status)


def list_all_running() -> List[str]:
    return _JOBS_RUNING.keys()


def delete(id: str):
    global _JOBS_RUNING

    if id in _JOBS_RUNING:

        _JOBS_RUNING[id].kill()
        _JOBS_RUNING.pop(id)
        _kill_process()
        logger.log.info(f'Job running was killed id -> {id}')


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
                logger.log.warn(
                    f'Error Jaime status code -> {result.status_code}')
                time.sleep(_TIME_TO_REINTENT_SECONDS)
                continue

            keep_asking = False

        except Exception as e:
            logger.log.warn(e)
            time.sleep(_TIME_TO_REINTENT_SECONDS)

    logger.log.info(f'Finished Job id -> {id}')
