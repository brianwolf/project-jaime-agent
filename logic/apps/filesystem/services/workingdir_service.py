import shutil
import zipfile
from os import walk
from pathlib import Path
from typing import Any, List
from uuid import UUID, uuid4

from logic.apps.zip.service import zip_service

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


def download_zip(id: str) -> str:

    zip_result_path = _TEMP_PATH + f'/{id}.zip'
    path = fullpath(id)

    zip_service.create(zip_result_path, path)

    return zip_result_path
