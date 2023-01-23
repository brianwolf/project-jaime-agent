import os
import socket
import subprocess
import time
from threading import Thread
from typing import Dict

import requests
from logic.apps.admin.configs import app
from logic.apps.admin.configs.variables import Vars, get_var
from logic.libs.logger import logger

_THREAD_CONNECTION_JAIME_ACTIVE = True
_TIME_BETWEEN_REQUESTS_SECONDS = 3


def connect_with_jaime():

    global _THREAD_CONNECTION_JAIME_ACTIVE
    _THREAD_CONNECTION_JAIME_ACTIVE = True

    thread = Thread(target=_thread_func)
    thread.start()


def _thread_func():

    connected_with_jaime = False

    while _THREAD_CONNECTION_JAIME_ACTIVE:

        try:
            if connected_with_jaime:
                connected_with_jaime = _refresh_token_ok()
            else:
                connected_with_jaime = _get_token_ok()

        except Exception as e:
            logger.log.error(e)
            logger.log.error(
                f'Error en conexion con Jaime -> reintentando en {_TIME_BETWEEN_REQUESTS_SECONDS} seg')
            connected_with_jaime = False

        time.sleep(_TIME_BETWEEN_REQUESTS_SECONDS)


def _refresh_token_ok() -> bool:

    url = get_var(Vars.JAIME_URL) + '/api/v1/login/refresh'
    token = os.getenv('JAIME_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}

    result = requests.get(url, verify=False, headers=headers)

    if result.status_code != 200:
        logger.log.warning(
            f'Error en conexion con Jaime -> {result.status_code}')
        return False

    return True


def _get_token_ok() -> bool:

    url = get_var(Vars.JAIME_URL) + '/api/v1/agents/'
    payload = {
        'host': socket.getfqdn(),
        'port': get_var(Vars.PYTHON_PORT),
        'type': get_var(Vars.AGENT_TYPE).upper(),
        'id': app.get_id_agent()
    }

    result = requests.post(url, json=payload, verify=False)
    token = result.text

    if not token:
        logger.log.warning(
            f"Error en conexion con Jaime -> {result.status_code}")
        return False

    os.environ['JAIME_TOKEN'] = token
    logger.log.info(
        f"Conexion exitosa con Jaime -> URL: {get_var(Vars.JAIME_URL)}")
    return True


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
