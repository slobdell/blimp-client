import os
from pubnub import Pubnub

from lib.constants import Constants
from lib.servo_controller import ServoController

PUBNUB_PUBLISH_KEY = os.environ['PUBNUB_PUBLISH_KEY']
PUBNUB_SUBSCRIBE_KEY = os.environ['PUBNUB_SUBSCRIBE_KEY']
# TODO: this should be camera commands not blimp_commands
LISTEN_CHANNEL = "blimp_commands"


class ActionListener(object):

    def __init__(self, blimp_runner):
        self.servo_controller = ServoController()
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
