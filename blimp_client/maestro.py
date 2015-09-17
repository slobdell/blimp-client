import json
import os
import shlex
import signal
import sys
import time
from subprocess import Popen

import requests

from global_settings import APP_SETTINGS, COMPANY_SETTINGS, CLIENT_SETTINGS


def populate_company_settings():
    access_token = CLIENT_SETTINGS["access_token"]
    unique_identifier = CLIENT_SETTINGS["unique_identifier"]
    base_url = APP_SETTINGS["OVERLORD_URL"]
    unformatted_url = "%s/api/me/?access_token=%s&unique_identifier=%s"
    full_url = unformatted_url % (base_url, access_token, unique_identifier)
    response = requests.get(full_url)
    response.raise_for_status()
    company_data = json.loads(response.content)
    COMPANY_SETTINGS.update(company_data)

    with open(APP_SETTINGS["COMPANY_SETTINGS_FILE"], "w+") as f:
        f.write(json.dumps(COMPANY_SETTINGS, indent=4))


def start_redis():
    command = "redis-server"
    process = Popen(shlex.split(command))
    return process.pid


def start_celery():
    command = "celery worker --autoreload --config=celeryconfig --concurrency=2"
    process = Popen(shlex.split(command))
    return process.pid


def start_web_server():
    command = "python -m http_listener.run"
    process = Popen(shlex.split(command))
    return process.pid


if __name__ == "__main__":
    while True:
        try:
            populate_company_settings()
            break
        except KeyboardInterrupt:
            sys.exit(0)
            pass
        except Exception as e:
            # generally means no network
            print e
            time.sleep(5)

    process_ids = []
    if COMPANY_SETTINGS['gphoto_camera_enabled']:
        process = Popen(shlex.split("python -m camera_streaming.camera_streamer"))
        process_ids.append(process.pid)

    if COMPANY_SETTINGS['android_camera_enabled']:
        pass  # I don't think I need to do anything

    process_ids.append(start_redis())
    process_ids.append(start_celery())
    process_ids.append(start_web_server())

    def kill_handler(signum, frame):
        print "KILLING CHILD PROCESSES FROM KILL CMD"
        for process_id in process_ids:
            os.system('kill %d' % process_id)
        sys.exit(0)

    signal.signal(signal.SIGTERM, kill_handler)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "KILLING PROCESSES FROM KEYBOARD INTERRUPT"
        for process_id in process_ids:
            os.system('kill %d' % process_id)
