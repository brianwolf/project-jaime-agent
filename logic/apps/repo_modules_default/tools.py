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
    try:
        JAIME_URL = os.getenv('JAIME_URL')
        cluster_dict = requests.get(
            f'{JAIME_URL}/api/v1/clusters/{cluster_name}').json()

    except Exception:
        raise Exception('Error on get clusters')

    return ClusterClient(
        url=cluster_dict['url'],
        token=cluster_dict['token'],
        version=cluster_dict['version']
    )


def _get_server_client(server_name: str) -> "ServerClient":
    try:
        JAIME_URL = os.getenv('JAIME_URL')
        server_dict = requests.get(
            f'{JAIME_URL}/api/v1/servers/{server_name}').json()

    except Exception:
        raise Exception('Error on get clusters')

    return ServerClient(
        host=server_dict['host'],
        port=server_dict['port'],
        user=server_dict['user'],
        password=server_dict['password']
    )

# ==========================================================
# PUBLIC
# ==========================================================


# LOGGER
formatter = logging.Formatter(
    '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')
log = logging.getLogger()
log.setLevel('DEBUG')
fh = WatchedFileHandler('logs.log')
fh.setLevel('DEBUG')
fh.setFormatter(formatter)
log.addHandler(fh)


def ssh(server_name: str, cmd: str, echo: bool = False) -> str:

    if echo:
        log.info(cmd)

    server = _get_server_client(server_name)

    ssh = paramiko.SSHClient()
    ssh.connect(hostname=server.host, username=server.user,
                password=server.password, port=server.port)
    _, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

    if echo and ssh_stdout:
        log.info(ssh_stdout)

    if echo and ssh_stderr:
        log.info(ssh_stderr)

    return ssh_stdout if ssh_stdout else ""


def sh(cmd: str, echo: bool = False) -> str:

    if echo:
        log.info(cmd)

    result = subprocess.getoutput(cmd)

    if echo and result:
        log.info(result)

    return result if result else ""


def get_clusters_name() -> List[str]:
    try:
        JAIME_URL = os.getenv('JAIME_URL')
        return requests.get(f'{JAIME_URL}/api/v1/clusters/').json()

    except Exception as e:
        raise Exception('Error on get clusters')


def get_servers_name() -> List[str]:
    try:
        JAIME_URL = os.getenv('JAIME_URL')
        return requests.get(f'{JAIME_URL}/api/v1/servers/').json()

    except Exception as e:
        raise Exception('Error on get clusters')


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
    user: jaime
    namespace: default
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
