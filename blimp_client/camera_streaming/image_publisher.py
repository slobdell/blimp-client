import base64

from pubnub import Pubnub

from blimp_client.global_settings import CHANNEL_PREFIX, COMPANY_SETTINGS

PUBNUB_PUBLISH_KEY = COMPANY_SETTINGS["pubnub_publish_key"]
PUBNUB_SUBSCRIBE_KEY = COMPANY_SETTINGS["pubnub_subscribe_key"]

PUBLISH_CHANNEL = CHANNEL_PREFIX + "jpeg_stream"


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
