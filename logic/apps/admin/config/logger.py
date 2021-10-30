from pathlib import Path

from logic.libs.logger.logger import Config, setup
from logic.libs.variables.variables import get_var

from .variables import Vars


def setup_loggers():
    setup([
        Config(
            name='app',
            path=f'{Path.home()}/.jaime-agent/logs',
            level=get_var(Vars.LOGS_LEVEL),
            file_backup_count=int(get_var(Vars.LOGS_BACKUPS))
        )
    ])
