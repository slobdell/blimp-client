import time

from .servo_controller import ServoController
from .servo_command_listener import ServoCommandListener


def start_listening():
    servo_controller = ServoController()
    ServoCommandListener(servo_controller)
    while True:
        # not sure if sleep time matters, I just can't have above stuff go out
        # of scope
        time.sleep(0.1)


if __name__ == "__main__":
    start_listening()
