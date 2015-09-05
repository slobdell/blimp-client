import base64
import os
import requests

from celery import Celery

from blimp_client.common.image_resizer import ImageResizer
from blimp_client.global_settings import APP_SETTINGS

UPLOAD_FOLDER = APP_SETTINGS["UPLOAD_FOLDER"]
FINISHED_RESIZE_WIDTH = 1024

app = Celery('camera_streaming_tasks', broker='redis://localhost:6379/0')


@app.task(name="send_photo_to_self")
def send_photo_to_self(filename, recipient):
    full_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(full_path, "rb") as f:
        jpeg_string = f.read()

    resized_jpeg_string = ImageResizer.from_raw_string(
        jpeg_string
    ).resize_to_width(FINISHED_RESIZE_WIDTH)

    b64_jpeg_string = base64.urlsafe_b64encode(resized_jpeg_string)
    post_url = "%s/picture/" % APP_SETTINGS["IMAGE_LISTEN_URL"]
    post_data = {
        "b64jpeg": b64_jpeg_string,
        "phone_num_or_email": recipient
    }
    requests.post(post_url, data=post_data)
    os.remove(full_path)
