import logging
import os
import subprocess
from dataclasses import dataclass
from logging.handlers import WatchedFileHandler
from typing import Dict, List
from uuid import uuid4

import paramiko
import requests
import yaml

# ==========================================================
# PRIVATE
# ==========================================================

_SERVER_FILE_NAME = 'servers.yaml'
_CLUSTER_FILE_NAME = 'clusters.yaml'
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


# ==========================================================
# PUBLIC
# ==========================================================

def ssh(server_name: str, cmd: str, echo: bool = False) -> str:

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


def sh(cmd: str, echo: bool = False) -> str:

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


def login_kubernetes(cluster_name) -> bool:

    client = _get_cluster_client(cluster_name)

    sh('mkdir -p /root/.kube', echo=False)

    with open('/root/.kube/config', 'w') as file:
        file.write(f""" 
apiVersion: v1
kind: Config
clusters:
- cluster:
    insecure-skip-tls-verify: true
    server: {client.url}
  name: jaime
users:
- name: jaime
  user:
    token: {client.token}
contexts:
- context:
    cluster: jaime
    namespace: default
    user: jaime
  name: jaime
current-context: jaime
        """)

    result = sh(f"kubectl config view", echo=False)

    return 'jaime' in result


def new_jaime_work(repo_name: str, module_name: str, agent_type: str, params: Dict[str, object] = {}, name: str = str(uuid4())) -> str:

    work_dict = {}
    work_dict['name'] = name
    work_dict['module_repo'] = repo_name
    work_dict['module_name'] = module_name
    work_dict['agent_type'] = agent_type
    work_dict['params'] = params

    yaml_str = str(yaml.dump(work_dict))

    JAIME_URL = os.getenv('JAIME_URL')

    return requests.post(
        url=f'{JAIME_URL}/api/v1/works/',
        data=yaml_str,
        headers={'Content-Type': 'text/plain; charset=utf-8'}
    ).text


def logger() -> logging.Logger:

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    fh = WatchedFileHandler('logs.log')
    fh.setLevel('DEBUG')
    fh.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel('DEBUG')
    logger.addHandler(fh)

    return logger
