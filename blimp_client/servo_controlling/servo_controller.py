# TODO no one listening on this channel right now
from blimp_client.adafruit.servo_channel import ServoChannel


class ServoController(object):

    def __init__(self):
        self.pan_controller = ServoChannel(0, 400, 444, neutral_val=422)
        self.tilt_controller = ServoChannel(1, 400, 444, neutral_val=422)

    def action_from_strings(self, pan_tilt_stop, intensity):
        if pan_tilt_stop == 'pan':
            print intensity
            # TODO hardcoded negative at the moment
            self.pan_controller.set_intensity(-intensity)
        if pan_tilt_stop == 'tilt':
            self.tilt_controller.set_intensity(intensity)
        if pan_tilt_stop == 'stop':
            self.pan_controller.set_intensity(0.0)
            self.tilt_controller.set_intensity(0.0)
