import os
import subprocess
from datetime import datetime

from logic.apps.filesystem.services import filesystem_service

_TEMP_REQUIREMENTS_FILE_PATH = '/tmp'


def update_requirements(content: str):

    requirements_temp_path = f'{_TEMP_REQUIREMENTS_FILE_PATH}/requirements_{datetime.now().timestamp()}.txt'

    filesystem_service.create_file(requirements_temp_path, content)

    os.system(f'pip3 install -r {requirements_temp_path} --upgrade pip')
