from Queue import Queue
import os
import uuid

from blimp_client.common.image_resizer import ImageResizer
from blimp_client.global_settings import APP_SETTINGS

from .image_publisher import ImagePublisher
from .action_listener import ActionListener
from .python_canon_camera.boost_camera import CameraManager
from .tasks import send_photo_to_self


MAX_CONNECTION_RETRIES = 5
PREVIEW_RESIZE_WIDTH = 200
UPLOAD_FOLDER = APP_SETTINGS["UPLOAD_FOLDER"]


def init_camera(camera_manager):
    num_retries = 0
    # For Macs in particular, this daemon needs to be killed to free the camera for
    # us
    print "Killing interfering camera processes..."
    os.popen("killall PTPCamera")
    while num_retries < MAX_CONNECTION_RETRIES:
        success = camera_manager.initialize()
        if success:
            print "Successfully connected to the camera"
            return
        num_retries += 1
    # perhaps send myself a text message or something
    raise Exception("Could not get into camera")


def int_numpy_array_to_str(numpy_array_jpeg_bytes):
    return "".join(map(chr, numpy_array_jpeg_bytes))


class CameraStreamer(object):

    def __init__(self):
        self.image_publisher = ImagePublisher()
        self.camera_manager = CameraManager()
        init_camera(self.camera_manager)
        self.phone_number_queue = Queue()
        self.action_listener = ActionListener(self)

    def amend_phone_number(self, iso_formatted_phone_number):
        current_phone_numbers = {item for item in self.phone_number_queue.queue}
        if iso_formatted_phone_number in current_phone_numbers:
            return
        self.phone_number_queue.put(iso_formatted_phone_number)

    def _stream_frame_from_camera(self):
        numpy_array_jpeg_bytes = self.camera_manager.grab_frame()
        jpeg_string = int_numpy_array_to_str(numpy_array_jpeg_bytes)
        resized_jpeg_string = ImageResizer.from_raw_string(
            jpeg_string
        ).resize_to_width(PREVIEW_RESIZE_WIDTH)
        self.image_publisher.publish_frame(resized_jpeg_string)

    def _send_quality_picture_to_customer(self):
        numpy_array_jpeg_bytes = self.camera_manager.take_picture_and_transfer()
        jpeg_string = int_numpy_array_to_str(numpy_array_jpeg_bytes)
        filename = "%s.jpg" % uuid.uuid4()
        full_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(full_path, "w+") as f:
            f.write(jpeg_string)
        recipient = self.phone_number_queue.get()
        send_photo_to_self.delay(filename, recipient)

    def run(self):
        while True:
            self._stream_frame_from_camera()
            if not self.phone_number_queue.empty():
                self._send_quality_picture_to_customer()

if __name__ == "__main__":
    try:
        CameraStreamer().run()
    except KeyboardInterrupt:
        # Pubnub will otherwise not kill itself
        os.system('kill %d' % os.getpid())
