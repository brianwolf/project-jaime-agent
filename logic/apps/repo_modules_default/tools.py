import subprocess
from dataclasses import dataclass
from typing import Dict, List

import paramiko
import yaml

_SERVER_FILE_NAME = 'servers.yaml'
_CLUSTER_FILE_NAME = 'cluster.yaml'
_PARAMS_FILE_NAME = 'params.yaml'


@dataclass
class ClusterClient():
    url: str
    token: str
    version: str


@dataclass
class ServerClient():
    host: str
    port: str
    user: str
    password: str


def _get_cluster_client(cluster_name: str) -> "ClusterClient":

    with open(_CLUSTER_FILE_NAME, 'r') as f:
        clusters_dict = yaml.load(f.read(), Loader=yaml.FullLoader)

    for s in clusters_dict:

        if s['name'] == cluster_name:
            return ClusterClient(
                url=s['url'],
                token=s['token'],
                version=s['version']
            )

    if not cluster_name in clusters_dict:
        raise Exception(f'No existe el cluster de nombre {cluster_name}')


def _get_server_client(server_name: str) -> "ServerClient":

    with open(_SERVER_FILE_NAME, 'r') as f:
        servers_dict = yaml.load(f.read(), Loader=yaml.FullLoader)

    for s in servers_dict:

        if s['name'] == server_name:
            return ServerClient(
                host=s['host'],
                port=s['port'],
                user=s['user'],
                password=s['password']
            )

    if not server_name in servers_dict:
        raise Exception(f'No existe el server de nombre {server_name}')


def ssh(cmd: str, server_name: str, echo: bool = True) -> str:

    if echo:
        print(cmd)

    server = _get_server_client(server_name)

    ssh = paramiko.SSHClient()
    ssh.connect(hostname=server.host, username=server.user,
                password=server.password, port=server.port)
    _, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

    if echo and ssh_stdout:
        print(ssh_stdout)

    if echo and ssh_stderr:
        print(ssh_stderr)

    return ssh_stdout if ssh_stdout else ""


def sh(cmd: str, echo: bool = True) -> str:

    if echo:
        print(cmd)

    result = subprocess.getoutput(cmd)

    if echo and result:
        print(result)

    return result if result else ""


def get_clusters_name() -> List[str]:

    with open(_CLUSTER_FILE_NAME, 'r') as f:
        clusters_dict = yaml.load(f.read(), Loader=yaml.FullLoader)

    return clusters_dict.keys()


def get_servers_name() -> List[str]:

    with open(_SERVER_FILE_NAME, 'r') as f:
        servers_dict = yaml.load(f.read(), Loader=yaml.FullLoader)

    return servers_dict.keys()


def get_params() -> Dict[str, object]:

    with open(_PARAMS_FILE_NAME, 'r') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


def login_openshift(cluster_name) -> bool:

    client = _get_cluster_client(cluster_name)
    result = sh(
        f"oc login --server={client.url} --token={client.token} --insecure-skip-tls-verify")

    return 'Logged into' in result
