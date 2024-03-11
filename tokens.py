import logging
import os
from pathlib import Path

from PIL import Image

from util.render import render_text, set_default_img, set_default_assets, set_default_font_file


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


DPI = 300

INCH = DPI * 1
CM = DPI * 1 / 2.54
MM = DPI * 1 / 25.4
PT = DPI * 1 / 72

TOKEN_SIZE = (int(0.6 * INCH), int(0.6 * INCH))

FONT_FILE = "assets/fonts/Tinos-Regular.ttf"


def render_token(token):
    img = Image.new("RGB", TOKEN_SIZE, color="white")
    set_default_img(img)
    set_default_assets({})
    set_default_font_file(FONT_FILE)
    render_text((0.5, 0.5), f"{token['value']}{token['color']}", font_size=int(12 * PT), anchor="mm")
    return img


def render_tokens(output_path):
    # create output path
    Path(output_path).mkdir(parents=True, exist_ok=True)
    tokens = [{"value": value, "color": color} for value in [1, 2, 3, 4, 5] for color in ["R", "G", "B", "Y", ""] for count in range(20)]
    # render each token
    for i, token in enumerate(tokens, start=1):
        img = render_token(token)
        img.save(f"{output_path}/token_{i:03}.png")
