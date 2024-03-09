#!/usr/bin/env python

import shutil

import cards
import util.pdf

# Create card image files
shutil.rmtree("./data/cards", ignore_errors=True)
cards.render_cards()

# Create PDF file for Print & play
util.pdf.combine_images_to_a4_pdf("./data/cards", "./data/pdf/all_cards.pdf", image_w=2.5, image_h=3.5, margin=0)
