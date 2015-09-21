#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servo_value = 421 # Min pulse length out of 4096

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
while (True):
  # Change speed of continuous servo on channel O
  print "setting to %s" % servo_value
  channel_number = 0
  pwm.setPWM(channel_number, 0, servo_value)
  servo_value += 1
  time.sleep(2)
  # 200 to 580
  # 220 to 580 where 420 was mid
  # 422 is midpoint
