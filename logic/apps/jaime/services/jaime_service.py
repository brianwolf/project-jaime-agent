import subprocess
import time
from threading import Thread

import requests
from logic.apps.admin.config.variables import Vars, get_var
from logic.libs.logger.logger import logger

_THREAD_CONNECTION_JAIME_ACTIVE = True


def connect_with_jaime():

    thread = Thread(target=_thread_func)
    thread.start()


def _thread_func():

    connect_with_jaime = False
    status_code = 0

    while _THREAD_CONNECTION_JAIME_ACTIVE:

        if connect_with_jaime:
            try:
                url = get_var(Vars.JAIME_URL)
                requests.get(url, timeout=5)
            except Exception:
                logger().error(f'Se perdio la coneccion con Jaime -> reintentando en 5 seg')
                connect_with_jaime = False
        else:
            try:
                url = get_var(Vars.JAIME_URL) + '/api/v1/agents/'
                payload = {
                    'host': subprocess.getoutput('hostname -I').split(" ")[0],
                    # 'host': subprocess.getoutput("awk 'END{print $1}' /etc/hosts"),
                    'port': get_var(Vars.PYTHON_PORT),
                    'type': get_var(Vars.AGENT_TYPE).upper(),
                }
                requests.post(url, json=payload, timeout=5)
                connect_with_jaime = True
                logger().info(
                    f"Coneccion exitosa con Jaime -> URL: {get_var(Vars.JAIME_URL)}")
            except Exception:
                logger().error(f'Error en coneccion con Jaime -> reintentando en 5 seg')

        time.sleep(5)
