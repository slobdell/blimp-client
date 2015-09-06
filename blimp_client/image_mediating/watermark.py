from PIL import Image, ImageEnhance
from cStringIO import StringIO
import requests

from blimp_client.global_settings import COMPANY_SETTINGS


class LazyCache(object):
    watermark = None


def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)


def _pil_image_to_jpeg_bytes(pil_image):
    image_buffer = StringIO()
    pil_image.save(image_buffer, "JPEG", quality=90)
    image_buffer.seek(0)
    return image_buffer.read()


def default_watermark(jpeg_bytes):
    image_buffer = StringIO(jpeg_bytes)
    pil_image = Image.open(image_buffer)

    if LazyCache.watermark is None:
        watermark_bytes = requests.get(COMPANY_SETTINGS["watermark_url"]).content
        watermark_buffer = StringIO(watermark_bytes)
        LazyCache.watermark = Image.open(watermark_buffer)

    mark = LazyCache.watermark
    updated_image = watermark(pil_image, mark, 'scale', 1.0)
    return _pil_image_to_jpeg_bytes(updated_image)
