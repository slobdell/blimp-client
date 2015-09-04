import base64
import os

from pubnub import Pubnub

PUBNUB_PUBLISH_KEY = os.environ['PUBNUB_PUBLISH_KEY']
PUBNUB_SUBSCRIBE_KEY = os.environ['PUBNUB_SUBSCRIBE_KEY']

PUBLISH_CHANNEL = "jpeg_stream"


class ImagePublisher(object):

    def __init__(self):
        self.pubnub = Pubnub(
            publish_key=PUBNUB_PUBLISH_KEY,
            subscribe_key=PUBNUB_SUBSCRIBE_KEY,
            cipher_key='',
            ssl_on=False)

    def publish_frame(self, jpeg_frame):
        message = base64.b64encode(jpeg_frame)
        self.pubnub.publish(PUBLISH_CHANNEL, message)
