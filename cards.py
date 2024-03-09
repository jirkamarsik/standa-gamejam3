""" Generate card images from card specification in CSV
"""
import logging
import os
from pathlib import Path

from PIL import Image, ImageFont

from util.gsheets import download_gsheets
from util.remote_file import get_local_file_from_url
from util.render import scale_rxy_to_xy, render_text_with_assets, render_image, render_rectangle, set_default_img, set_default_assets, set_default_font_file


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


# Cards are defined in this Google sheet
CARD_SHEET_ID = "1vFIjrfHucrlN7fgcWcHVCxhSoMAYFCqkb8QN9GgcH2w"
CARD_SHEET_NAME = "cards"
# Card images go to OUTPUT_PATH
OUTPUT_PATH = "data/cards"

DPI = 300

INCH = DPI * 1
CM = DPI * 1 / 2.54
MM = DPI * 1 / 25.4
PT = DPI * 1 / 72

CARD_SIZE = (int(2.5 * INCH), int(3.5 * INCH))

ASSET_SIZE = (int(5 * MM), int(5 * MM))
ASSETS = {}

FONT_FILE = "assets/fonts/Tinos-Regular.ttf"


CARDS = []

def load_cards():
    global CARDS
    CARDS = download_gsheets(CARD_SHEET_ID, CARD_SHEET_NAME)


def render_card(card):
    img = Image.new("RGB", CARD_SIZE, color="white")
    return img


def render_cards():
    # create output path
    Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
    # render each card
    for i, card in enumerate(CARDS, start=2):
        img = render_card(card)
        img.save(f"{OUTPUT_PATH}/card_{i:03}.png")


load_cards()
