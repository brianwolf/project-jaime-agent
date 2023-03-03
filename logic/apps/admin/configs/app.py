import os
from uuid import UUID, uuid4

from logic.apps.admin.configs.variables import Vars, get_var


def get_path_file_id() -> str:
    return f'{get_var(Vars.JAIME_AGENT_HOME_PATH)}/id'


def setup_id_agent() -> UUID:

    if not os.path.exists(get_path_file_id()):
        with open(get_path_file_id(), 'w') as f:
            id = str(uuid4()).split('-')[4]
            f.write(id)

    return get_id_agent()


def get_id_agent() -> UUID:
    with open(get_path_file_id(), 'r') as f:
        return f.read()
