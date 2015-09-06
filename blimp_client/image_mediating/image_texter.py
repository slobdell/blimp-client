import os

from twilio.rest import TwilioRestClient


ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = "+18329003200"


class ImageTexter(object):

    def __init__(self):
        self.client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    def text_image(self, to_phone_number, image_url):
        message = "Here you go!"

        self.client.messages.create(
            to=to_phone_number,
            from_=TWILIO_PHONE_NUMBER,
            body=message,
            media_url=image_url,
        )
