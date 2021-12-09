import subprocess
import sys
from dataclasses import dataclass
from subprocess import PIPE
from typing import Dict

import yaml

_SERVER_FILE_NAME = 'servers.yaml'
_PARAMS_FILE_NAME = 'params.yaml'


@dataclass
class Client():
    url: str
    token: str
    version: str

    def __init__(self, url: str, token: str, version: str) -> "Client":
        self.url = url
        self.token = token
        self.version = version

    def login(self) -> str:
        short_version = self.version.split(".")[0]

        if short_version == "3":
            sh(f"{self.binary_name()} login {self.url} --token={self.token} --insecure-skip-tls-verify", echo=False)
            return

        sh(f"{self.binary_name()} login --server={self.url} --token={self.token} --insecure-skip-tls-verify", echo=False)

    def exec(self, cmd: str, echo: bool = True) -> str:
        final_cmd = f"{self.binary_name()} {cmd}"
        return sh(final_cmd, echo)

    def binary_name(self) -> str:
        return "oc"


def sh(cmd: str, echo: bool = True) -> str:

    if echo:
        print(cmd)

    result = subprocess.getoutput(cmd)

    if echo and result:
        print(result)

    return result if result else ""


def get_client(server_name: str) -> "Client":

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


def get_params() -> Dict[str, object]:
    with open(_PARAMS_FILE_NAME, 'r') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)
