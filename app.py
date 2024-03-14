#!env/bin/python
import os
import sys

from flask.app import Flask

from logic.apps.admin.configs.app import setup_id_agent
from logic.apps.admin.configs.logger import setup_loggers
from logic.apps.admin.configs.rest import setup_rest
from logic.apps.admin.configs.variables import Vars, setup_vars
from logic.apps.jaime.service import connect_with_jaime
from logic.libs.logger import logger
from logic.libs.variables.variables import get_var

# pyinstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

setup_vars()
setup_loggers()

app = Flask(__name__)
setup_rest(app)

id_agent = setup_id_agent()
logger.log.info(f'Agent ID -> {id_agent}')
connect_with_jaime()

with open('logic/resources/banner.txt', 'r') as f:
    # logger.log.info(f.read())
    print(f.read())


if __name__ == "__main__":
    flask_host = get_var(Vars.PYTHON_HOST)
    flask_port = int(get_var(Vars.PYTHON_PORT))

    app.run(host=flask_host, port=flask_port, debug=False)
