from enum import Enum

from logic.libs.variables.variables import Config, setup, get_var


class Vars(Enum):
    VERSION = 'VERSION'
    PYTHON_HOST = 'PYTHON_HOST'
    PYTHON_PORT = 'PYTHON_PORT'
    LOGS_LEVEL = 'LOGS_LEVEL'
    LOGS_BACKUPS = 'LOGS_BACKUPS'
    AGENT_TYPE = 'AGENT_TYPE'
    JAIME_URL = 'JAIME_URL'
    JAIME_AGENT_HOME_PATH = 'JAIME_AGENT_HOME_PATH'
    WORKINGDIR_PATH = 'WORKINGDIR_PATH'
    STORAGE_PATH = 'STORAGE_PATH'


def setup_vars():
    setup(
        Config(
            file_path='logic/resources/variables.yaml',
            hiden_vars=[]
        )
    )
