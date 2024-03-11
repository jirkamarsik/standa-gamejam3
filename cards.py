import logging
import os
import re
from pathlib import Path

from PIL import Image

from util.gsheets import download_gsheets
from util.render import render_text, render_text_with_assets, render_image, render_rectangle, render_ellipse, set_default_img, set_default_assets, set_default_font_file


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


# Cards are defined in this Google sheet
CARD_SHEET_ID = "1vFIjrfHucrlN7fgcWcHVCxhSoMAYFCqkb8QN9GgcH2w"
CARD_SHEET_NAME = "cards"


DPI = 300

INCH = DPI * 1
CM = DPI * 1 / 2.54
MM = DPI * 1 / 25.4
PT = DPI * 1 / 72

CARD_SIZE = (int(2.5 * INCH), int(3.5 * INCH))

FONT_FILE = "assets/fonts/Tinos-Regular.ttf"


def load_cards():
    cards = []
    sheet = download_gsheets(CARD_SHEET_ID, CARD_SHEET_NAME)
    for card in sheet:
        # dropneme prazdne radky a jine nekompletni poznamky (e.g. suma poctu karet)
        if card["Název"] == "":
            continue
        count = int(card["Počet"]) if card["Počet"] != "" else 1
        for _ in range(count):
            cards.append(card)
    return cards


def render_card(card):
    img = Image.new("RGB", CARD_SIZE, color="white")
    set_default_img(img)
    set_default_assets({})
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

    if card["Speciální pravidla"]:
        textbox_padding = 0.03
        textbox_font_size = int(12 * PT)
        textbox_bbox = render_text_with_assets((0, 0), card["Speciální pravidla"], textbox_font_size, align="left", max_width=1.0 - 2 * textbox_padding, silent=True)
        textbox_height = textbox_bbox[1][1] - textbox_bbox[0][1] + 2 * textbox_padding
        bot = bot - textbox_height
        render_rectangle((0, bot), 1, textbox_height)
        render_text_with_assets((textbox_padding, bot + textbox_padding), card["Speciální pravidla"], textbox_font_size, align="left", max_width=1.0 - 2 * textbox_padding)

    image_height = bot - top
    image_padding = 0.03
    if image_height > 2 * image_padding and card["Art"] != "":
        render_image((image_padding, top + image_padding), 1 - 2 * image_padding, bot - top - 2 * image_padding, card["Art"])

    vb_width = 0.4 * INCH / CARD_SIZE[0]
    vb_height = 0.4 * INCH / CARD_SIZE[1]
    if card["VB"] != "" and card["VB"] != "0" and card["VB"] != 0:
        render_rectangle((0, top), vb_width, vb_height, fill_color="white")
        render_text((vb_width / 2, top + vb_height / 2), str(card["VB"]), font_size=int(16 * PT), anchor="mm")

    return img


def count_colors(cards):
    color_usages = {}
    color_costs = {}

    colors = ["R", "G", "B", "Y"]

    for color in colors:
        color_usages[color] = 0
        color_costs[color] = 0

    for card in cards:
        for color in colors:
            m = re.search(r"(\d*)\s*" + color, card["Cena"])
            if m:
                c = int(m.group(1)) if m.group(1) != "" else 1
                color_usages[color] = color_usages[color] + 1
                color_costs[color] = color_costs[color] + c

    print("Colors used:")
    print(color_usages)

    print("Color costs summed up:")
    print(color_costs)


def render_cards(cards, output_path):
    # create output path
    Path(output_path).mkdir(parents=True, exist_ok=True)
    # render each card
    for i, card in enumerate(cards, 1):
        img = render_card(card)
        img.save(f"{output_path}/card_{i:03}.png")
