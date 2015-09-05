import os
from pubnub import Pubnub

from .constants import Constants

PUBNUB_PUBLISH_KEY = os.environ['PUBNUB_PUBLISH_KEY']
PUBNUB_SUBSCRIBE_KEY = os.environ['PUBNUB_SUBSCRIBE_KEY']
# TODO: need to incorporate client ID and all that shit
LISTEN_CHANNEL = "camera_commands"


class ActionListener(object):

    def __init__(self, blimp_runner):
        self.blimp_runner = blimp_runner
        self.pubnub = Pubnub(
            publish_key=PUBNUB_PUBLISH_KEY,
            subscribe_key=PUBNUB_SUBSCRIBE_KEY,
            cipher_key='',
            ssl_on=False
        )
        self.pubnub.subscribe(LISTEN_CHANNEL, self.callback)

    def callback(self, message, channel):
        if message['command'] == Constants.CMD_TAKE_PICTURE:
            phone_number = message['value']
            self.blimp_runner.amend_phone_number(phone_number)
        elif message['command'] in (Constants.CMD_START, Constants.CMD_STOP):
            self.servo_controller.action_from_strings(
                message['command'],
                message['value']
            )
