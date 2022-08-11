import os
from pathlib import Path
import subprocess
from datetime import datetime

from logic.apps.filesystem.services import filesystem_service

_TEMP_REQUIREMENTS_FILE_PATH = '/tmp'
_LOGS_FILE_PATH = f'{Path.home()}/.jaime-agent/logs/app.log'


def update_requirements(content: str):

    requirements_temp_path = f'{_TEMP_REQUIREMENTS_FILE_PATH}/requirements_{datetime.now().timestamp()}.txt'

    filesystem_service.create_file(requirements_temp_path, content)

    os.system(f'pip3 install -r {requirements_temp_path} --upgrade pip')


def get_logs() -> str:
    return filesystem_service.get_file_content(_LOGS_FILE_PATH)
