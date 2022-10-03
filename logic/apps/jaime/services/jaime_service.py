import os
import socket
import subprocess
import time
from threading import Thread
from typing import Dict

import requests
from logic.apps.admin.config import app
from logic.apps.admin.config.variables import Vars, get_var
from logic.libs.logger.logger import logger

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
                url = get_var(Vars.JAIME_URL) + '/api/v1/login/refresh'
                token = os.getenv('JAIME_TOKEN')
                headers = {'Authorization': f'Bearer {token}'}
                requests.get(url, timeout=5, verify=False, headers=headers)

            except Exception as e:
                logger().error(
                    f'Se perdio la coneccion con Jaime -> reintentando en {_TIME_BETWEEN_REQUESTS_SECONDS} seg')
                logger().error(e)
                connected_with_jaime = False

        else:
            try:
                url = get_var(Vars.JAIME_URL) + '/api/v1/agents/'
                host = socket.getfqdn()

                payload = {
                    'host': host,
                    'port': get_var(Vars.PYTHON_PORT),
                    'type': get_var(Vars.AGENT_TYPE).upper(),
                    'id': app.get_id_agent()
                }

                result = requests.post(
                    url, json=payload, timeout=5, verify=False)
                if result.status_code != 201:
                    raise Exception(
                        f'Error status code from Jaime response -> {result.status_code}')

                token = result.text

                os.environ['JAIME_TOKEN'] = token
                connected_with_jaime = True

                logger().info(
                    f"Coneccion exitosa con Jaime -> URL: {get_var(Vars.JAIME_URL)}")

            except Exception as e:
                logger().error(
                    f'Error en coneccion con Jaime -> reintentando en {_TIME_BETWEEN_REQUESTS_SECONDS} seg')
                logger().error(e)

        time.sleep(_TIME_BETWEEN_REQUESTS_SECONDS)


def disconnect_with_jaime():
    global _THREAD_CONNECTION_JAIME_ACTIVE
    _THREAD_CONNECTION_JAIME_ACTIVE = False


def test_cluster(url, token, type) -> Dict[str, str]:

    if type == 'OPENSHIFT':
        text = subprocess.getoutput(
            f"oc login --server={url} --token={token} --insecure-skip-tls-verify")

        return {
            'success': 'Logged into' in text,
            'text': text
        }

    return {
        'success': False,
        'text': 'Tipo de cluster no encontrado'
    }
