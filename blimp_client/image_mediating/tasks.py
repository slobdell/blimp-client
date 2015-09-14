import os
import uuid

from celery import Celery
from pubnub import Pubnub

from blimp_client.common.facebook_rest_client import FacebookRestClient
from blimp_client.common.image_resizer import ImageResizer
from blimp_client.common.image_rotater import ImageRotater
from blimp_client.global_settings import APP_SETTINGS, COMPANY_SETTINGS

from .image_texter import ImageTexter
from .image_emailer import ImageEmailer
from .watermark import default_watermark
from .image_uploader import ImageUploader

app = Celery('this_can_be_anything', broker='redis://localhost:6379/0')
BUCKET_NAME = "public-blimp"
# TODO move to settings
PUBNUB_PUBLISH_KEY = COMPANY_SETTINGS["pubnub_publish_key"]
PUBNUB_SUBSCRIBE_KEY = COMPANY_SETTINGS["pubnub_subscribe_key"]


@app.task(name="some_unique_name")
def arbitrary_task(serializable_input):
    print "GOT HERE"


def company_salted_uuid(uuid_str):
    salt_uuid = COMPANY_SETTINGS["sell_photo_salt_uuid"]
    salt_byte_vals = [ord(char) for char in salt_uuid]
    input_byte_vals = [ord(char) for char in uuid_str]

    new_byte_vals = []
    for index in xrange(16):
        new_byte_val = salt_byte_vals[index] ^ input_byte_vals[index]
        new_byte_vals.append(new_byte_val)

    byte_str = "".join([chr(byte_val) for byte_val in new_byte_vals])
    return str(uuid.UUID(bytes=byte_str))


@app.task(name="send_photo")
def send_photo(filename, phone_num_or_email):
    """ Assume the input image is for sell width """
    full_path = "%s%s" % (APP_SETTINGS["UPLOAD_FOLDER"], filename)
    with open(full_path, "rb") as f:
        jpeg_string = f.read()

    jpeg_string = ImageRotater.from_raw_string(
        jpeg_string
    ).rotate(COMPANY_SETTINGS["picture_rotation"])

    watermark_jpeg_string = ImageResizer.from_raw_string(
        jpeg_string
    ).resize_to_width(COMPANY_SETTINGS["image_picture_view_width"])

    if COMPANY_SETTINGS["watermark_url"]:
        watermark_jpeg_string = default_watermark(watermark_jpeg_string)

    watermark_photo_uuid_str = str(uuid.uuid4())
    if COMPANY_SETTINGS["sell_photos"]:
        sell_photo_uuid_str = company_salted_uuid(watermark_photo_uuid_str)
        upload_image(jpeg_string, phone_num_or_email, sell_photo_uuid_str)

    watermark_image_url = upload_image(watermark_jpeg_string, phone_num_or_email, watermark_photo_uuid_str)
    # TODO if sell photos is online then we should instead do a new fucking URL
    print watermark_image_url

    print phone_num_or_email

    try:
        facebook_image_url = _possibly_post_to_facebook(watermark_image_url)
    except:  # Facebook token has expired
        facebook_image_url = None

    if COMPANY_SETTINGS["sell_photos"]:
        watermark_image_url = _sell_photo_url(watermark_image_url)

    image_url_for_user = facebook_image_url or watermark_image_url
    _send_image_back_to_user(phone_num_or_email, image_url_for_user)

    os.remove(full_path)


def _possibly_post_to_facebook(watermark_image_url):
    if COMPANY_SETTINGS["facebook_enabled"]:
        access_token = COMPANY_SETTINGS["facebook_access_token"]
        caption = ""
        if COMPANY_SETTINGS["sell_photos"]:
            sales_page_url = _sell_photo_url(watermark_image_url)
            caption = "View the high resolution, non-watermarked version here: %s" % sales_page_url
        FacebookRestClient(access_token).post_photo(watermark_image_url, caption)
        return "http://facebook.com/%s" % COMPANY_SETTINGS["facebook_service_id"]
    return ''


def _send_image_back_to_user(phone_num_or_email, watermark_image_url):
    if COMPANY_SETTINGS["web_flow"]:
        # TODO vars need renaming
        pubnub = Pubnub(
            publish_key=PUBNUB_PUBLISH_KEY,
            subscribe_key=PUBNUB_SUBSCRIBE_KEY,
        )
        pubnub.publish(phone_num_or_email, watermark_image_url)

    elif COMPANY_SETTINGS["sms_photos"]:
        ImageTexter().text_image(phone_num_or_email, watermark_image_url)

    elif COMPANY_SETTINGS["email_photos"]:
        ImageEmailer().email_image(phone_num_or_email, watermark_image_url)


def _sell_photo_url(watermark_image_url):
    url = "http://{domain_name}/view/{client_company_id}/?image={image_url}".format(
        domain_name=COMPANY_SETTINGS["domain_name"],
        client_company_id=COMPANY_SETTINGS["id"],
        image_url=watermark_image_url
    )
    return url


def upload_image(jpeg_bytes, phone_num_or_email, uuid_str):
    image_uploader = ImageUploader(BUCKET_NAME)
    output_path = "%s/%s/%s.jpg" % (COMPANY_SETTINGS["id"], _cleaned_recipient(phone_num_or_email), uuid_str)
    image_url = image_uploader.upload(output_path, jpeg_bytes)
    return image_url


def _cleaned_recipient(phone_num_or_email):
    phone_num_or_email = phone_num_or_email.replace("+", "")
    phone_num_or_email = phone_num_or_email.replace("@", "")
    phone_num_or_email = phone_num_or_email.replace(".", "")
    return phone_num_or_email


if __name__ == "__main__":
    arbitrary_task.delay("hello world")
