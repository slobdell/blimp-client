import os
import uuid

from celery import Celery
from pubnub import Pubnub

from blimp_client.global_settings import APP_SETTINGS, COMPANY_SETTINGS

from .image_texter import ImageTexter
from .watermark import default_watermark
from .image_uploader import ImageUploader

app = Celery('this_can_be_anything', broker='redis://localhost:6379/0')
BUCKET_NAME = "public-blimp"
# TODO move to settings
PUBNUB_PUBLISH_KEY = os.environ['PUBNUB_PUBLISH_KEY']
PUBNUB_SUBSCRIBE_KEY = os.environ['PUBNUB_SUBSCRIBE_KEY']


@app.task(name="some_unique_name")
def arbitrary_task(serializable_input):
    print "GOT HERE"


@app.task(name="send_photo")
def send_photo(filename, phone_num_or_email):
    full_path = "%s%s" % (APP_SETTINGS["UPLOAD_FOLDER"], filename)
    with open(full_path, "rb") as f:
        jpeg_string = f.read()

    if COMPANY_SETTINGS["watermark_url"]:
        jpeg_string = default_watermark(jpeg_string)

    image_url = upload_image(jpeg_string, phone_num_or_email)
    print image_url

    if COMPANY_SETTINGS["web_flow"]:
        # TODO vars need renaming
        pubnub = Pubnub(
            publish_key=PUBNUB_PUBLISH_KEY,
            subscribe_key=PUBNUB_SUBSCRIBE_KEY,
        )
        pubnub.publish(phone_num_or_email, image_url)

    elif COMPANY_SETTINGS["sms_photos"]:
        ImageTexter().text_image("+14156606378", image_url)

    elif COMPANY_SETTINGS["email_photos"]:
        pass
    os.remove(full_path)


def upload_image(jpeg_bytes, phone_num_or_email):
    image_uploader = ImageUploader(BUCKET_NAME)
    output_path = "%s/%s.jpg" % (_cleaned_recipient(phone_num_or_email), str(uuid.uuid4()))
    image_url = image_uploader.upload(output_path, jpeg_bytes)
    return image_url


def _cleaned_recipient(phone_num_or_email):
    phone_num_or_email = phone_num_or_email.replace("+", "")
    phone_num_or_email = phone_num_or_email.replace("@", "")
    phone_num_or_email = phone_num_or_email.replace(".", "")
    return phone_num_or_email


if __name__ == "__main__":
    arbitrary_task.delay("hello world")
