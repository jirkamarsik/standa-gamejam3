import logging
import os
from pathlib import Path

from PIL import Image, ImageFont

from util.render import scale_rxy_to_xy, render_text_with_assets, render_image, render_rectangle, set_default_img, set_default_assets, set_default_font_file


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


# Card images go to OUTPUT_PATH
OUTPUT_PATH = "data/tokens"

DPI = 300

INCH = DPI * 1
CM = DPI * 1 / 2.54
MM = DPI * 1 / 25.4
PT = DPI * 1 / 72

TOKEN_SIZE = (int(0.6 * INCH), int(0.6 * INCH))

ASSET_SIZE = (int(5 * MM), int(5 * MM))
ASSETS = {}

FONT_FILE = "assets/fonts/Tinos-Regular.ttf"


def render_token(token):
    img = Image.new("RGB", TOKEN_SIZE, color="white")
    set_default_img(img)
    set_default_assets(ASSETS)
    set_default_font_file(FONT_FILE)
    render_text_with_assets((0.5, 0.5), f"{token['value']}{token['color']}", int(12 * PT))
    return img


def render_tokens():
    # create output path
    Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
    tokens = [{"value": value, "color": color} for value in [1, 2, 3, 4, 5] for color in ["R", "G", "B", "Y", ""] for count in range(20)]
    # render each token
    for i, token in enumerate(tokens, start=2):
        img = render_token(token)
        img.save(f"{OUTPUT_PATH}/token_{i:03}.png")
