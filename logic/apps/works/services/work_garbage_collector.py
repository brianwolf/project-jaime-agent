import os
import threading
import time
from datetime import datetime, timedelta

from logic.apps.filesystem.services import workingdir_service
from logic.apps.works.services import work_service
from logic.libs.logger.logger import logger

_THREAD_GARBAGE_ACTIVE = True


def garbabge_collector():

    for id in work_service.list_all_running():

        path = workingdir_service.fullpath(id)

        m_date = datetime.fromtimestamp(os.path.getmtime(path))

        if m_date + timedelta(minutes=10) < datetime.now():
            work_service.delete(id)
            workingdir_service.delete(id)
            logger().info(f'Deleted workingdir -> {id}')


def start_garbage_thread():

    global _THREAD_GARBAGE_ACTIVE
    _THREAD_GARBAGE_ACTIVE = True

    def thread_method():
        global _THREAD_GARBAGE_ACTIVE
        while _THREAD_GARBAGE_ACTIVE:
            garbabge_collector()
            time.sleep(30)

    thread = threading.Thread(target=thread_method)
    thread.start()


def stop_garbage_thread():
    global _THREAD_GARBAGE_ACTIVE
    _THREAD_GARBAGE_ACTIVE = False
