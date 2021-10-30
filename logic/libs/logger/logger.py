"""
Logger
-------
1.0.0

Crea logs de la aplicacion
"""
import logging
from dataclasses import dataclass
from typing import Dict, List

from logic.libs.logger.src.file import make_logger

import logic.libs.logger.src.config as config


@dataclass
class Config():
    """
    Objeto de configuracion
    """
    name: str = 'app'
    path: str = '/tmp/logs'
    level: str = 'INFO'
    file_backup_count: int = 3


def setup(configs: List[Config]):
    """
    Configura las opciones PREDEFINIDAS del logger para el proyecto, en caso del handler, 
    el que viene rota los logs con un archivo por dia hasta hasta un maximo de 7 archivos.
    """
    for con in configs:
        config._LOGGERS[con.name] = make_logger(con)


def logger(name: str = 'app') -> logging.Logger:
    """
    Devuelve un objeto logger por un nombre, en caso de que no exista lo crea.\n
    En caso de pasarle un fileHandler el path del mismo debe existir 
    """
    return config._LOGGERS[name]
