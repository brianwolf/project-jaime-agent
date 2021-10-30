"""
Variables
---------
1.0.0

Utiliza un archivo .env para crear un diccionario usado como variables del proyecto, 
en caso de que exista la variable de ambiente en el sistema utiliza esa, 
en caso de que no, usa la del archivo 
"""
import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from logic.libs.variables.src import config
from logic.libs.variables.src.file import make_vars_dict


@dataclass
class Config:
    """
    Objeto de configuracion
    """
    file_path: str
    hiden_vars: List[str]
    enum_vars: Enum


def setup(configs: List[Config]):
    """
    Configura la util, se debe usar antes de usar cualquier otro metodo

    - configs -> lista de objetos de configuracion
    """
    for cfg in configs:
        config.DICT_VARS.update(make_vars_dict(cfg.file_path))
        config.HIDEN_VARS.extend(cfg.hiden_vars)
        config.ENUMS_LIST.extend(cfg.enum_vars)


def get_var(var: Enum) -> str:
    """
    Obtiene el valor de la variable de entorno correspondiente, en caso de no obtenerla,
    la saca del diccionario de variables predefinidas
    """
    default_value = config.DICT_VARS.get(var.value)
    return os.environ.get(var.value, default_value)


def all_vars() -> Dict[str, str]:
    """
    Devuelve el mapa de variables con sus valores instanciados y filtrados por la lista de no mostrados
    """
    return {
        key.value: get_var(key)
        for key in config.ENUMS_LIST
        if key.value not in config.HIDEN_VARS
    }
