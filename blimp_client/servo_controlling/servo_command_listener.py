from pubnub import Pubnub

from blimp_client.global_settings import CHANNEL_PREFIX, COMPANY_SETTINGS

PUBNUB_PUBLISH_KEY = COMPANY_SETTINGS["pubnub_publish_key"]
PUBNUB_SUBSCRIBE_KEY = COMPANY_SETTINGS["pubnub_subscribe_key"]
LISTEN_CHANNEL = CHANNEL_PREFIX + "servo_commands"


class ServoCommandListener(object):

    def __init__(self, servo_controller):
        self.servo_controller = servo_controller
        self.pubnub = Pubnub(
            publish_key=PUBNUB_PUBLISH_KEY,
            subscribe_key=PUBNUB_SUBSCRIBE_KEY,
            cipher_key='',
            ssl_on=False
        )
        self.pubnub.subscribe(LISTEN_CHANNEL, self.callback)

    def callback(self, message, channel):
        # not the best code for sure...
            self.servo_controller.action_from_strings(
                message['command'],
                message['value'],
            )
