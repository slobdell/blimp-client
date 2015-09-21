from Adafruit_PWM_Servo_Driver import PWM


class ServoChannel(object):
    def __init__(self, channel_number, min_pwm_val, max_pwm_val, neutral_val=None):
        self.neutral_val = neutral_val or (max_pwm_val + min_pwm_val) / 2

        self.min_pwm_val = min_pwm_val
        self.max_pwm_val = max_pwm_val
        self.channel_number = channel_number

        self._pwm_driver = PWM(0x40)
        # TODO figure out what these values mean exactly
        self._pwm_driver.setPWMFreq(60)

    def set_intensity(self, percent):
        if percent is None:
            # hack
            return
        if abs(percent) > 1.0:
            raise TypeError("percent should be in 0.0..1.0")
        if percent < 0:
            range_pwm = self.neutral_val - self.min_pwm_val
            pwm_intensity = range_pwm * abs(percent)
            servo_value = self.neutral_val - pwm_intensity
        elif percent > 0:
            range_pwm = self.max_pwm_val - self.neutral_val
            pwm_intensity = range_pwm * abs(percent)
            servo_value = self.neutral_val + pwm_intensity
        elif percent == 0:
            servo_value = self.neutral_val
        self._pwm_driver.setPWM(self.channel_number, 0, int(servo_value))
