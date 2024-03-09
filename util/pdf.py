import os
from pathlib import Path

from PIL import Image, ImageDraw

A4_WIDTH_INCHES = 8.27
A4_HEIGHT_INCHES = 11.7

def combine_images_to_a4_pdf(input_path, output_filename, dpi=300, image_w=2.5, image_h=3.5, margin=10.0 / 300, border="black", border_width=3):
    """Combine images in input_path to multi-page PDF, try layout as many to a page as possible

    :param input_path: path with input images
    :param output_filename: filename for PDF to output
    :param dpi: DPI to use, eg 300
    :param image_w: width of an individual image, in inches
    :param image_h: height of an individual image, in inches
    :param margin: margin to use between images, in inches
    :param margin: color of border between cards, or None for no border
    :return:
    """
    # scale margin to pixels
    margin = int(margin * dpi)
    # Size of one PDF page.
    width, height = int(A4_WIDTH_INCHES * dpi), int(A4_HEIGHT_INCHES * dpi)
    # Size of one image (defaults are a poker card)
    card_w, card_h = int(image_w * dpi), int(image_h * dpi)
    images = os.listdir(input_path)
    images.sort()
    images = [os.path.join(input_path, img) for img in images]
    images_per_row = int(width / (card_w + 2 * margin))
    images_per_col = int(height / (card_h + 2 * margin))
    images_per_page = images_per_row * images_per_col
    Path(os.path.dirname(output_filename)).mkdir(parents=True, exist_ok=True)

    pad_x = int((width - images_per_row * card_w - (images_per_row - 1) * margin) / 2)
    pad_y = int((height - images_per_col * card_h - (images_per_col - 1) * margin) / 2)

    groups = [
        images[i : i + images_per_page] for i in range(0, len(images), images_per_page)
    ]
    for i, group in enumerate(groups):
        page = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(page)
        x, y = pad_x, pad_y
        for img_name in group:
            img = Image.open(img_name).resize((card_w, card_h))
            page.paste(img, box=(x, y))
            if border:
                draw.rectangle([(x, y), (x + card_w, y + card_h)], outline=border, width=border_width)
            x += img.size[0] + margin
            if x + img.size[0] + margin >= width:
                x = pad_x
                y += img.size[1] + margin
        page.save(output_filename, append=(i > 0))
