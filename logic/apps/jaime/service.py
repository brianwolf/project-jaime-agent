import socket
import subprocess
import time
from pathlib import Path
from threading import Thread
from typing import Dict
import os

import requests

from logic.apps.admin.configs import app
from logic.apps.admin.configs.variables import Vars, get_var
from logic.libs.logger import logger

_THREAD_CONNECTION_JAIME_ACTIVE: bool = True
_TIME_BETWEEN_REQUESTS_SECONDS: int = 3
_TOKEN: str = None


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
                f'Error Jaime connection -> retry {_TIME_BETWEEN_REQUESTS_SECONDS} sec')
            connected_with_jaime = False

        time.sleep(_TIME_BETWEEN_REQUESTS_SECONDS)


def _refresh_token_ok() -> bool:

    global _TOKEN

    url = get_var(Vars.JAIME_URL) + '/api/v1/login/refresh'
    headers = {'Authorization': f'Bearer {_TOKEN}'}

    result = requests.get(url, verify=False, headers=headers)

    if result.status_code != 200:
        logger.log.warning(
            f'Error Jaime connection -> {result.status_code}')
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
            f"Error Jaime connection -> {result.status_code}")
        return False

    global _TOKEN
    _TOKEN = token
    os.environ['JAIME_TOKEN'] = token

    logger.log.info(
        f"Connection successful -> URL: {get_var(Vars.JAIME_URL)}")
    return True


def disconnect_with_jaime():
    global _THREAD_CONNECTION_JAIME_ACTIVE
    _THREAD_CONNECTION_JAIME_ACTIVE = False


def test_cluster(url: str, token: str, type: str) -> Dict[str, str]:

    success = False
    text = f'Cluster with type {type} not supported'

    if type == 'OPENSHIFT':
        text = subprocess.getoutput(
            f"oc login --server={url} --token={token} --insecure-skip-tls-verify")

        success = 'Logged into' in text

    if type == 'KUBERNETES':

        subprocess.getoutput(f'mkdir -p {Path.home()}/.kube')

        with open(f'{Path.home()}/.kube/config', 'w') as file:
            file.write(f""" 
apiVersion: v1
kind: Config
clusters:
- name: jaime
  cluster:
    insecure-skip-tls-verify: true
    server: {url}
users:
- name: jaime
  user:
    token: {token}
contexts:
- name: jaime
  context:
    cluster: jaime
    user: jaime
    namespace: default
current-context: jaime
""")
        text = subprocess.getoutput(f"kubectl get nodes")
        success = 'Unable to connect' not in text and 'Error' not in text and 'refused' not in text

    if not success:
        logger.log.warn(
            f'Error on connect to cluster {type} type -> {text}')

    return {
        'success': success,
        'text': text
    }


def get_token() -> str:
    global _TOKEN
    return _TOKEN
