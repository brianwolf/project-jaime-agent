import subprocess
from datetime import datetime

from logic.apps.admin.configs.logger import get_logs_path
from logic.apps.filesystem import filesystem_service
from logic.libs.logger import logger

_TEMP_REQUIREMENTS_FILE_PATH = '/tmp'


def update_requirements(content: str):

    requirements_temp_path = f'{_TEMP_REQUIREMENTS_FILE_PATH}/requirements_{datetime.now().timestamp()}.txt'

    filesystem_service.create_file(requirements_temp_path, content)

    logger.log.info(f'Installing pip dependencies')
    subprocess.getoutput(f'pip install -r {requirements_temp_path}')
    logger.log.info(f'Dependencies are installed')


def get_logs() -> str:
    return filesystem_service.get_file_content(get_logs_path())
