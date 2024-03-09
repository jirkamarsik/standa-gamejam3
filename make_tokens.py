#!/usr/bin/env python

import shutil

import tokens
import util.pdf

# Create card image files
shutil.rmtree("./data/tokens", ignore_errors=True)
tokens.render_tokens()

# Create PDF file for Print & play
util.pdf.combine_images_to_a4_pdf("./data/tokens", "./data/pdf/all_tokens.pdf", image_w=0.6, image_h=0.6, margin=0)
