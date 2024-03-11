#!/usr/bin/env python
import shutil

import cards
import util.pdf


OUTPUT_CARDS_PATH = "./data/cards"
OUTPUT_PDF_PATH = "./data/pdf/all_cards.pdf"


all_cards = cards.load_cards()

# Create card image files
shutil.rmtree(OUTPUT_CARDS_PATH, ignore_errors=True)
cards.render_cards(all_cards, OUTPUT_CARDS_PATH)

# Create PDF file for Print & play
util.pdf.combine_images_to_a4_pdf(OUTPUT_CARDS_PATH, OUTPUT_PDF_PATH, image_w=2.5, image_h=3.5, margin=0)
