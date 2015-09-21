# TODO no one listening on this channel right now


class ServoController(object):

    def __init__(self):
        self.ACTION_DICT = {
            "start": {
                "left": self.start_left,
                "right": self.start_right,
                "up": self.start_up,
                "down": self.start_down,
            },
            "stop": {
                "left": self.stop_left,
                "right": self.stop_right,
                "up": self.stop_up,
                "down": self.stop_down,
                "all": self.stop_all,
            }
        }

    def action_from_strings(self, start_or_stop, direction, intensity):
        func = self.ACTION_DICT[start_or_stop][direction]
        func()

    def start_up(self, intensity):
        print "start up"

    def start_down(self, intensity):
        print "start down"

    def start_left(self, intensity):
        print "start left"

    def start_right(self, intensity):
        print "start right"

    def stop_right(self, intensity):
        print "stop right"

    def stop_left(self, intensity):
        print "stop left"

    def stop_up(self, intensity):
        print "stop up"

    def stop_down(self, intensity):
        print "stop down"

    def stop_all(self):
        self.stop_left()
        self.stop_right()
        self.stop_up()
        self.stop_down()
