"""Image helpers used to recolor viewer textures by team hue."""

import logging
import uuid
from collections import Counter
from functools import cache
from typing import cast

import arcade
from PIL import Image

MIN_IMPORTANT_SATURATION = 50
MIN_IMPORTANT_VALUE = 50

logger = logging.getLogger(__name__)


@cache
def hue(image_path: str) -> int:
    """Get most common hue in important pixels (saturated, not transparent…).

    Args:
        image_path: path of the image to analyze

    Returns:
        the most common hue (rounded to tens)
    """
    image = Image.open(image_path)
    alphas = list(cast("list[int]", image.getdata(band=3)))
    hsv_image = image.convert("HSV")
    hues = list(cast("list[int]", hsv_image.getdata(band=0)))
    saturations = list(cast("list[int]", hsv_image.getdata(band=1)))
    values = list(cast("list[int]", hsv_image.getdata(band=2)))
    important_hues = [
        hue // 10 * 10
        for hue, saturation, value, alpha in zip(
            hues, saturations, values, alphas, strict=False
        )
        if (
            saturation > MIN_IMPORTANT_SATURATION
            and value > MIN_IMPORTANT_VALUE
            and alpha != 0
        )
    ]
    counter = Counter(important_hues)
    return counter.most_common(1)[0][0]


@cache
def hue_changed_texture(image_path: str, target_hue: int) -> arcade.Texture:
    """Return a texture where the dominant hue is shifted to `target_hue`."""
    logger.info("Managing %s", image_path)

    target_hue = target_hue * 256 // 360

    original_image = Image.open(image_path)
    original_hue = hue(image_path)
    offset_hue = 256 + target_hue - original_hue
    alpha_channel = original_image.split()[-1]
    hsv_image = original_image.convert("HSV")
    h, s, v = hsv_image.split()
    hue_data = h.point(lambda i: (i + offset_hue) % 256)
    adjusted_hue_image = Image.merge("HSV", (hue_data, s, v))
    adjusted_hue_image_rgb = adjusted_hue_image.convert("RGB")
    final_image = Image.merge("RGBA", (*adjusted_hue_image_rgb.split(), alpha_channel))
    return arcade.Texture(name=str(uuid.uuid4()), image=final_image)
