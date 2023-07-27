import logging
import os
import subprocess
from dataclasses import dataclass
from logging.handlers import WatchedFileHandler
from pathlib import Path
from typing import Dict, List
from uuid import uuid4

import paramiko
import requests
import yaml

# ==========================================================
# PRIVATE
# ==========================================================

_PARAMS_FILE_NAME = 'params.yaml'
_LOG_FILE_NAME = 'logs.log'


@dataclass
class ClusterClient():
    url: str
    token: str


@dataclass
class ServerClient():
    host: str
    port: str
    user: str
    password: str


def _get_cluster_client(cluster_name: str) -> "ClusterClient":
    try:
        url = os.getenv('JAIME_URL')
        token = os.getenv('JAIME_TOKEN')
        headers = {'Authorization': f'Bearer {token}'}
        cluster_dict = requests.get(
            f'{url}/api/v1/clusters/{cluster_name}', headers=headers).json()

    except Exception as e:
        log.error(e)
        raise Exception('Error on get clusters')

    return ClusterClient(
        url=cluster_dict['url'],
        token=cluster_dict['token']
    )


def _get_server_client(server_name: str) -> "ServerClient":
    try:
        url = os.getenv('JAIME_URL')
        token = os.getenv('JAIME_TOKEN')
        headers = {'Authorization': f'Bearer {token}'}
        server_dict = requests.get(
            f'{url}/api/v1/servers/{server_name}', headers=headers).json()

    except Exception as e:
        log.error(e)
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
log.setLevel('INFO')
fh = WatchedFileHandler(_LOG_FILE_NAME)
fh.setLevel('INFO')
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
        token = os.getenv('JAIME_TOKEN')
        headers = {'Authorization': f'Bearer {token}'}
        return requests.get(f'{JAIME_URL}/api/v1/clusters/', headers=headers).json()

    except Exception as e:
        raise Exception('Error on get clusters')


def get_servers_name() -> List[str]:
    try:
        JAIME_URL = os.getenv('JAIME_URL')
        token = os.getenv('JAIME_TOKEN')
        headers = {'Authorization': f'Bearer {token}'}
        return requests.get(f'{JAIME_URL}/api/v1/servers/', headers=headers).json()

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

    subprocess.getoutput(f'mkdir -p {Path.home()}/.kube')

    with open(f'{Path.home()}/.kube/config', 'w') as file:
        file.write(f""" 
apiVersion: v1
kind: Config
clusters:
- name: jaime
  cluster:
    insecure-skip-tls-verify: true
    server: {client.url}
users:
- name: jaime
  user:
    token: {client.token}
contexts:
- name: jaime
  context:
    cluster: jaime
    user: jaime
    namespace: default
current-context: jaime
""")

    text = subprocess.getoutput(f"kubectl get nodes")

    return 'Unable to connect' not in text and 'Error' not in text and 'refused' not in text


def new_jaime_job(repo_name: str, module_name: str, agent_type: str, params: Dict[str, object] = {}, name: str = str(uuid4())) -> str:

    job_dict = {}
    job_dict['name'] = name
    job_dict['module_repo'] = repo_name
    job_dict['module_name'] = module_name
    job_dict['agent_type'] = agent_type
    job_dict['params'] = params

    yaml_str = str(yaml.dump(job_dict))

    JAIME_URL = os.getenv('JAIME_URL')
    token = os.getenv('JAIME_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'text/plain; charset=utf-8'
    }

    return requests.post(
        url=f'{JAIME_URL}/api/v1/jobs/',
        data=yaml_str,
        headers=headers
    ).text


def get_job_id() -> str:
    return sh('pwd').split('/')[-1]


def new_message(title: str, subject: str, body: str, files: list[str] = []) -> str:

    message_dict = {
        'title': title,
        'subject': subject,
        'body': body,
        'files': files,
        'job': get_job_id()
    }

    JAIME_URL = os.getenv('JAIME_URL')
    token = os.getenv('JAIME_TOKEN')
    headers = {
        'Authorization': f'Bearer {token}'
    }

    return requests.post(
        url=f'{JAIME_URL}/api/v1/messages/',
        json=message_dict,
        headers=headers
    ).text
