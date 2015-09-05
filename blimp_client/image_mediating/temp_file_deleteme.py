
from lib.image_texter import ImageTexter
self.image_texter = ImageTexter()
from lib.watermark import default_watermark

        watermarked_jpeg_string = default_watermark(resized_jpeg_string)
        recipient = self.phone_number_queue.get()
        self.image_texter.text_image(recipient, watermarked_jpeg_string)
