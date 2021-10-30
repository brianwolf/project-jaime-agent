import shutil
from os import walk
from pathlib import Path
from typing import Any, List
from uuid import UUID, uuid4

_TEMP_PATH = '/tmp'


def create() -> UUID:
    id = uuid4()
    Path(fullpath(id)).mkdir(parents=True, exist_ok=True)
    return id


def create_by_id(id: Any):
    Path(fullpath(id)).mkdir(parents=True, exist_ok=True)


def delete(id: Any):
    shutil.rmtree(fullpath(id))


def fullpath(id: Any) -> str:
    return f'{_TEMP_PATH}/{id}'


def get(id: Any) -> List[str]:
    result = []
    for (dirpath, _, _) in walk(fullpath(id)):
        result.extend(dirpath)

    return result
