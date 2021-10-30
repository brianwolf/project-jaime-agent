import time

import requests
from logic.apps.admin.config.variables import Vars, get_var
from logic.apps.filesystem.services import workingdir_service
from logic.libs.logger.logger import logger
from threading import Thread

_THREAD_CONNECTION_JAIME_ACTIVE = True


def start(id: str, params_bytes: bytes, module_bytes: bytes, servers_bytes: bytes, tools_bytes: bytes):

    workingdir_service.create_by_id(id)

    base_path = workingdir_service.fullpath(id)

    with open(f'{base_path}/params.yaml', 'w') as f:
        f.write(params_bytes.decode())

    with open(f'{base_path}/module.py', 'w') as f:
        f.write(module_bytes.decode())

    with open(f'{base_path}/servers.yaml', 'w') as f:
        f.write(servers_bytes.decode())

    with open(f'{base_path}/tools.py', 'w') as f:
        f.write(tools_bytes.decode())

    _exec(id)


def _exec(id: str):

    base_path = workingdir_service.fullpath(id)


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
                    'host': get_var(Vars.PYTHON_HOST),
                    'port': get_var(Vars.PYTHON_PORT),
                    'type': get_var(Vars.AGENT_TYPE),
                }
                requests.post(url, json=payload, timeout=5)
                connect_with_jaime = True
                logger().info(
                    f"Coneccion exitosa con Jaime -> URL: {get_var(Vars.JAIME_URL)}")
            except Exception:
                logger().error(f'Error en coneccion con Jaime -> reintentando en 5 seg')

        time.sleep(5)
