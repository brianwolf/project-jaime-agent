import logging
import os
from logging.handlers import TimedRotatingFileHandler


def make_logger(config) -> logging.Logger:
    """
    Devuelve un objeto logger por un nombre, en caso de que no exista lo crea
    """
    if not os.path.exists(config.path):
        os.makedirs(config.path, exist_ok=True)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    fh = TimedRotatingFileHandler(
        f'{config.path}/{config.name}.log',
        when="d",
        interval=1,
        backupCount=config.file_backup_count)
    fh.setLevel(config.level)
    fh.setFormatter(formatter)

    sh = logging.StreamHandler()
    sh.setLevel(config.level)
    sh.setFormatter(formatter)

    logger = logging.getLogger(config.name)
    logger.setLevel(config.level)
    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger
