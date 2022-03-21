import subprocess
from dataclasses import dataclass
from typing import Dict, List

import yaml

_SERVER_FILE_NAME = 'servers.yaml'
_PARAMS_FILE_NAME = 'params.yaml'


@dataclass
class Client():
    url: str
    token: str
    version: str


def _get_client(server_name: str) -> "Client":

    with open(_SERVER_FILE_NAME, 'r') as f:
        servers_dict = yaml.load(f.read(), Loader=yaml.FullLoader)

    for s in servers_dict:

        if s['name'] == server_name:
            return Client(
                url=s['url'],
                token=s['token'],
                version=s['version']
            )

    if not server_name in servers_dict:
        raise Exception(f'No existe el server de nombre {server_name}')


def sh(cmd: str, echo: bool = True) -> str:

    if echo:
        print(cmd)

    result = subprocess.getoutput(cmd)

    if echo and result:
        print(result)

    return result if result else ""


def get_servers_name() -> List[str]:

    with open(_SERVER_FILE_NAME, 'r') as f:
        servers_dict = yaml.load(f.read(), Loader=yaml.FullLoader)

    return servers_dict.keys()


def get_params() -> Dict[str, object]:

    with open(_PARAMS_FILE_NAME, 'r') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


def login_openshift(server_name) -> bool:

    client = _get_client(server_name)
    result = sh(
        f"oc login --server={client.url} --token={client.token} --insecure-skip-tls-verify")

    return 'Logged into' in result
