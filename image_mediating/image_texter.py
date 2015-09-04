import os
import uuid

from twilio.rest import TwilioRestClient

from lib.image_uploader import ImageUploader


ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
BUCKET_NAME = "public-blimp"
TWILIO_PHONE_NUMBER = "+18329003200"


class ImageTexter(object):

    def __init__(self):
        self.client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
        self.image_uploader = ImageUploader(BUCKET_NAME)

    @staticmethod
    def _no_plus(phone_number):
        return phone_number.replace("+", "")

    def text_image(self, to_phone_number, jpeg_bytes):
        output_path = "%s/%s.jpg" % (self._no_plus(to_phone_number), str(uuid.uuid4()))
        image_url = self.image_uploader.upload(output_path, jpeg_bytes)
        print image_url

        message = "Here you go!"

        self.client.messages.create(
            to=to_phone_number,
            from_=TWILIO_PHONE_NUMBER,
            body=message,
            media_url=image_url,
        )
