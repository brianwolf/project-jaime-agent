from logic.apps.admin.configs.variables import Vars, get_var
from logic.libs.logger.logger import Config, setup


def get_logs_path() -> str:
    return f'{get_var(Vars.JAIME_AGENT_HOME_PATH)}/logs/app.log'


def setup_loggers():
    setup(
        Config(
            path=get_logs_path(),
            level=get_var(Vars.LOGS_LEVEL),
            file_backup_count=int(get_var(Vars.LOGS_BACKUPS))
        )
    )
