import os
from pathlib import Path
from uuid import UUID, uuid4

_PATH_FILE_ID = f'{Path.home()}/.jaime-agent/id'


def setup_id_agent() -> UUID:

    if not os.path.exists(_PATH_FILE_ID):
        with open(_PATH_FILE_ID, 'w') as f:
            id = str(uuid4()).split('-')[4]
            f.write(id)

    return get_id_agent()


def get_id_agent() -> UUID:
    with open(_PATH_FILE_ID, 'r') as f:
        return f.read()
