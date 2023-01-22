import subprocess
from datetime import datetime
from pathlib import Path

from logic.apps.filesystem import filesystem_service
from logic.libs.logger import logger

_TEMP_REQUIREMENTS_FILE_PATH = '/tmp'
_LOGS_FILE_PATH = f'{Path.home()}/.jaime-agent/logs/app.log'


def update_requirements(content: str):

    requirements_temp_path = f'{_TEMP_REQUIREMENTS_FILE_PATH}/requirements_{datetime.now().timestamp()}.txt'

    filesystem_service.create_file(requirements_temp_path, content)

    logger.log.info(f'Instalando dependencias de pip')
    subprocess.getoutput(f'pip install -r {requirements_temp_path}')
    logger.log.info(f'Dependencias instaladas')


def get_logs() -> str:
    return filesystem_service.get_file_content(_LOGS_FILE_PATH)
