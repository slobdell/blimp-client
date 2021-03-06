from pubnub import Pubnub

from blimp_client.global_settings import CHANNEL_PREFIX, COMPANY_SETTINGS

from .constants import Constants

PUBNUB_PUBLISH_KEY = COMPANY_SETTINGS["pubnub_publish_key"]
PUBNUB_SUBSCRIBE_KEY = COMPANY_SETTINGS["pubnub_subscribe_key"]
# TODO: need to incorporate client ID and all that shit
LISTEN_CHANNEL = CHANNEL_PREFIX + "camera_commands"


class ActionListener(object):

    def __init__(self, camera_streamer):
        self.camera_streamer = camera_streamer
        self.pubnub = Pubnub(
            publish_key=PUBNUB_PUBLISH_KEY,
            subscribe_key=PUBNUB_SUBSCRIBE_KEY,
            cipher_key='',
            ssl_on=False
        )
        self.pubnub.subscribe(LISTEN_CHANNEL, self.callback)

    def callback(self, message, channel):
        # TODO update variable names, not necessary a phone numebr here
        if message['command'] == Constants.CMD_TAKE_PICTURE:
            phone_number = message['value']
            self.camera_streamer.amend_phone_number(phone_number)
