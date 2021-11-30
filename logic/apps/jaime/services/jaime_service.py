import subprocess
import time
from threading import Thread

import requests
from logic.apps.admin.config.variables import Vars, get_var
from logic.libs.logger.logger import logger
from logic.apps.admin.config import app

_THREAD_CONNECTION_JAIME_ACTIVE = True
_TIME_BETWEEN_REQUESTS_SECONDS = 5


def connect_with_jaime():

    global _THREAD_CONNECTION_JAIME_ACTIVE
    _THREAD_CONNECTION_JAIME_ACTIVE = True

    thread = Thread(target=_thread_func)
    thread.start()


def _thread_func():

    time.sleep(_TIME_BETWEEN_REQUESTS_SECONDS)

    connected_with_jaime = False

    while _THREAD_CONNECTION_JAIME_ACTIVE:

        if connected_with_jaime:
            try:
                url = get_var(Vars.JAIME_URL)
                requests.get(url, timeout=5, verify=False)

            except Exception:
                logger().error(
                    f'Se perdio la coneccion con Jaime -> reintentando en {_TIME_BETWEEN_REQUESTS_SECONDS} seg')
                connected_with_jaime = False

        else:
            try:
                url = get_var(Vars.JAIME_URL) + '/api/v1/agents/'
                host = subprocess.getoutput("awk 'END{print $1}' /etc/hosts") if get_var(
                    Vars.RUN_ON_DOCKER) else get_var(Vars.PYTHON_HOST)

                payload = {
                    'host': host,
                    'port': get_var(Vars.PYTHON_PORT),
                    'type': get_var(Vars.AGENT_TYPE).upper(),
                    'id': app.get_id_agent()
                }
                requests.post(url, json=payload, timeout=5, verify=False)
                connected_with_jaime = True

                logger().info(
                    f"Coneccion exitosa con Jaime -> URL: {get_var(Vars.JAIME_URL)}")

            except Exception:
                logger().error(
                    f'Error en coneccion con Jaime -> reintentando en {_TIME_BETWEEN_REQUESTS_SECONDS} seg')

        time.sleep(_TIME_BETWEEN_REQUESTS_SECONDS)


def disconnect_with_jaime():
    global _THREAD_CONNECTION_JAIME_ACTIVE
    _THREAD_CONNECTION_JAIME_ACTIVE = False
