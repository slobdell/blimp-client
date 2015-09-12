from PIL import Image
from cStringIO import StringIO


class ImageRotater(object):

    def __init__(self, raw_data, quality=65):
        self.raw_data = raw_data
        self._quality = quality

    @classmethod
    def from_raw_string(cls, raw_data):
        try:
            return cls(raw_data)
        except IOError:
            raise

    def _image_to_raw_data(self, image, format):
        image_buffer = StringIO()
        image.save(image_buffer, format, quality=self._quality)
        image_buffer.seek(0)
        return image_buffer.read()

    def rotate(self, angle):
        if angle == 0:
            return self.raw_data

        image_buffer = StringIO(self.raw_data)
        image = Image.open(image_buffer)
        new_image = image.rotate(angle)
        return self._image_to_raw_data(new_image, image.format)
