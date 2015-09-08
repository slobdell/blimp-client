import os

from twilio.rest import TwilioRestClient

from blimp_client.global_settings import COMPANY_SETTINGS


ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = COMPANY_SETTINGS["twilio_phone_number"].replace(" ", "").replace("-", "")


class ImageTexter(object):

    def __init__(self):
        self.client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    def text_image(self, to_phone_number, image_url):
        message = "Thanks for trying the camera!  The picture you took can be found at %s" % image_url

        self.client.messages.create(
            to=to_phone_number,
            from_=TWILIO_PHONE_NUMBER,
            body=message,
        )
