""" Generate card images from card specification in CSV
"""
import logging
import os
from pathlib import Path

from PIL import Image, ImageFont

from util.gsheets import download_gsheets
from util.remote_file import get_local_file_from_url
from util.render import scale_rxy_to_xy, render_text, render_text_with_assets, render_image, render_rectangle, render_ellipse, set_default_img, set_default_assets, set_default_font_file


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
    set_default_img(img)
    set_default_assets(ASSETS)
    set_default_font_file(FONT_FILE)
    top = 0

    header_height = 0.07
    header_padding = 0.025
    header_font_size = int(12 * PT)
    cost_bbox = render_text((1 - header_padding, top), card["Cena"], header_font_size, anchor="ra")
    render_text((header_padding, top), card["Název"], header_font_size, anchor="la")
    render_rectangle((0, top), cost_bbox[0][0] - header_padding, header_height)
    render_rectangle((cost_bbox[0][0] - header_padding, top), 1 - cost_bbox[0][0] + header_padding, header_height)
    top = top + header_height

    bot = 1
    slot_width = 0.6 * INCH / CARD_SIZE[0]
    slot_height = 0.6 * INCH / CARD_SIZE[1]
    ability_padding = 0.02
    ability_font_size = int(12 * PT)
    requirement_font_size = int(16 * PT)
    for i in range(3, 0, -1):
        if card[f"Pole {i} - efekt"] == "":
            continue
        ability_bbox = render_text_with_assets((0, 0), card[f"Pole {i} - efekt"], ability_font_size, align="left", max_width=1.0 - 3 * ability_padding - slot_width, silent=True)
        ability_height = max(ability_bbox[1][1] - ability_bbox[0][1] + 2 * ability_padding, slot_height + 2 * ability_padding)
        bot = bot - ability_height
        render_rectangle((0, bot), 1, ability_height)
        render_ellipse((ability_padding, bot + ability_padding), slot_width, slot_height)
        render_text((ability_padding + slot_width / 2, bot + ability_padding + slot_height / 2), card[f"Pole {i} - podmínky"], requirement_font_size, anchor="mm")
        render_text_with_assets((2 * ability_padding + slot_width, bot + ability_padding), card[f"Pole {i} - efekt"], ability_font_size, align="left", max_width=1.0 - 3 * ability_padding - slot_width)

    if card[f"Speciální pravidla"]:
        textbox_padding = 0.03
        textbox_font_size = int(12 * PT)
        textbox_bbox = render_text_with_assets((0, 0), card["Speciální pravidla"], textbox_font_size, align="left", max_width=1.0 - 2 * textbox_padding, silent=True)
        textbox_height = textbox_bbox[1][1] - textbox_bbox[0][1] + 2 * textbox_padding
        bot = bot - textbox_height
        render_rectangle((0, bot), 1, textbox_height)
        render_text_with_assets((textbox_padding, bot + textbox_padding), card["Speciální pravidla"], textbox_font_size, align="left", max_width=1.0 - 2 * textbox_padding)

    return img


def render_cards():
    # create output path
    Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
    # render each card
    for i, card in enumerate(CARDS, start=2):
        img = render_card(card)
        img.save(f"{OUTPUT_PATH}/card_{i:03}.png")


load_cards()
