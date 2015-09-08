from PIL import Image
from cStringIO import StringIO


class ImageResizer(object):
    """
    USAGE:
    resized_jpeg_string = ImageResizer.from_raw_string(jpeg_string).resize_to_width(200)
    """

    def __init__(self, raw_data, quality=65):
        image_buffer = StringIO(raw_data)
        self._image = Image.open(image_buffer)
        self._width, self._height = self._image.size
        self._aspect_ratio = float(self._width) / self._height
        self._format = self._image.format
        self._quality = quality

    @classmethod
    def from_raw_string(cls, raw_data):
        try:
            return cls(raw_data)
        except IOError:
            raise

    def _image_to_raw_data(self, image):
        image_buffer = StringIO()
        image.save(image_buffer, self._format, quality=self._quality)
        image_buffer.seek(0)
        return image_buffer.read()

    def resize_to_width(self, target_width):
        if self._width <= target_width:
            return self._image_to_raw_data(self._image)

        target_height = self._infer_target_height(target_width)
        new_image = self._image.copy()
        new_image.thumbnail((target_width, target_height), Image.ANTIALIAS)
        return self._image_to_raw_data(new_image)

    def _infer_target_height(self, target_width):
        return target_width / self._aspect_ratio
