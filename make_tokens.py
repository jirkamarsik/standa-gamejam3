#!/usr/bin/env python
import shutil

import tokens
import util.pdf


OUTPUT_TOKENS_PATH = "./data/tokens"
OUTPUT_PDF_PATH = "./data/pdf/all_tokens.pdf"


# Create token image files
shutil.rmtree(OUTPUT_TOKENS_PATH, ignore_errors=True)
tokens.render_tokens(OUTPUT_TOKENS_PATH)

# Create PDF file for Print & play
util.pdf.combine_images_to_a4_pdf(OUTPUT_TOKENS_PATH, OUTPUT_PDF_PATH, image_w=0.6, image_h=0.6, margin=0)
