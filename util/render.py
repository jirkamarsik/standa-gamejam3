""" Utilities to render card images
"""
import logging
import re

from PIL import Image, ImageDraw, ImageFont

from util.remote_file import get_local_file_from_url


default_assets = None
default_font_file = None
default_img = None

def set_default_assets(assets):
    global default_assets
    default_assets = assets

def set_default_font_file(font_file):
    global default_font_file
    default_font_file = font_file

def set_default_img(img):
    global default_img
    default_img = img


def scale_rxy_to_xy(rxy, img=None):
    """Scale relative coordinates (like 0.3) to physical pixels in an image

    :param img:
    :param rxy: tuple of relative position in img, so (rx, ry) where elements
      are floats in range [0.0, 1.0]
    :return:
    """
    if img is None:
        img = default_img

    # assert 0.0 <= rxy[0] <= 1.0
    # assert 0.0 <= rxy[1] <= 1.0
    xy = (int(img.size[0] * rxy[0]), int(img.size[1] * rxy[1]))
    return xy


def scale_xy_to_rxy(xy, img=None):
    """Scale relative coordinates (like 0.3) to physical pixels in an image

    :param img:
    :param rxy: tuple of relative position in img, so (rx, ry) where elements
      are floats in range [0.0, 1.0]
    :return:
    """
    if img is None:
        img = default_img

    # assert 0 <= xy[0] <= img.size[0]
    # assert 0 <= xy[1] <= img.size[1]
    rxy = (xy[0] / img.size[0], xy[1] / img.size[1])
    return rxy


def transform_text_to_components(draw, text, font, assets):
    """Transform text with assets to list of individual components: texts and images

    :param text: example "hmmm is this a {duck}" where duck refers to image in assets dict
    :param font: font used in rendering, needed for sizes
    :param assets: dict of image assets
    :return: tuple (list of components: strings or images, list of (w, h) of components)
    """
    # split input text to list of individual elements
    text_lst = re.split(r"(\{[0-9A-Za-z _]+\}|\s+)", text)
    text_lst = [x for x in text_lst if x != ""]
    render_lst = []
    for text_part in text_lst:
        if re.match(r"\{[0-9A-Za-z _]+\}", text_part):
            # it's an image
            asset_name = text_part.replace("{", "").replace("}", "")
            asset_part = assets[asset_name]
            render_lst.append((asset_part, asset_part.size[0], asset_part.size[1]))
        else:
            # it's a string
            _, _, txt_length, txt_height = draw.textbbox((0, 0), text=text_part, font=font)
            render_lst.append((text_part, txt_length, txt_height))
    return render_lst


def render_text(rxy, text, font_size, font=None, text_color="black", align="center", anchor="la", img=None):
    if img is None:
        img = default_img
    if font is None:
        font = ImageFont.truetype(default_font_file, size=font_size)

    draw = ImageDraw.Draw(img)
    draw.text(scale_rxy_to_xy(rxy), text, fill=text_color, font=font, anchor=anchor, align=align)
    [x, y, width, height] = draw.textbbox(scale_rxy_to_xy(rxy), text, font=font, anchor=anchor, align=align)
    return [scale_xy_to_rxy((x, y)), scale_xy_to_rxy((width, height))]


def render_text_with_assets(rxy, text, font_size, font=None, assets=None, text_color="black", align="center", max_width=None, img=None, silent=False):
    """Render text that may include assets with {asset_name}

    Each asset is taken from assets and rendered centered

    :param rxy: center point for drawing text in relative units
    :param text: text to render

    :return: None, the text is rendered to img
    """
    if img is None:
        img = default_img
    if assets is None:
        assets = default_assets
    if font is None:
        font = ImageFont.truetype(default_font_file, size=font_size)

    draw = ImageDraw.Draw(img)
    render_lst = transform_text_to_components(draw, text, font, assets)
    if len(render_lst) == 0:
        return [rxy, rxy]
    # calculate full width to be rendered
    w = sum([obj_w for (_, obj_w, _) in render_lst])
    if max_width is not None:
        max_width = max_width * img.size[0]
        if w > max_width:
            w = max_width
    # calculate starting x position
    x, y = scale_rxy_to_xy(rxy)
    if align == "center":
        x0 = x - w / 2.0
    elif align == "left":
        x0 = x
    elif align == "right":
        x0 = x - w
    else:
        assert False, f"Unknown align: {align}"
    y0 = y
    x = x0
    y = y0
    max_h = max([obj_h for (_, _, obj_h) in render_lst])
    for obj, obj_w, obj_h in render_lst:
        if x > x0 and max_width is not None and x - x0 + obj_w > max_width:
            # go to new line
            x = x0
            y = y + max_h
            if obj == " ":
                continue
        if isinstance(obj, str):
            # render a string
            txt_length = draw.textlength(obj, font=font)
            if not silent:
                draw.text((x, y), obj, font=font, fill=text_color, anchor="la")
            x += txt_length
        else:
            # render an asset image
            if not silent:
                img.paste(obj, (int(x), int(y - obj.size[1] / 2)), obj.convert("RGBA"))
            x += obj.size[0]
    return [scale_xy_to_rxy((x0, y0)), scale_xy_to_rxy((x0 + w, y + max_h))]


def render_image(rxy, width, height, src_img_url, dst_img=None):
    if dst_img is None:
        dst_img = default_img

    src_img_fn = get_local_file_from_url(src_img_url)
    logging.info(f"opening {src_img_fn}")
    src_img = Image.open(src_img_fn)
    new_size = scale_rxy_to_xy((width, int(width / src_img.size[0] * src_img.size[1])))
    src_img = src_img.resize(new_size)
    xy = scale_rxy_to_xy(rxy)
    xy = [int(x) for x in xy]
    dst_img.paste(src_img, xy, src_img.convert("RGBA"))
    return [rxy, (rxy[0] + new_size[0], rxy[1] + new_size[1])]


def render_rectangle(rxy, width, height, line_width=int(0.5 * 300 / 25.4), line_color="black", img=None):
    if img is None:
        img = default_img

    draw = ImageDraw.Draw(img)
    bbox = [scale_rxy_to_xy(rxy), scale_rxy_to_xy((rxy[0] + width, rxy[1] + height))]
    draw.rectangle(bbox, outline=line_color, width=line_width)
    return bbox


def render_ellipse(rxy, width, height, line_width=int(0.5 * 300 / 25.4), line_color="black", img=None):
    if img is None:
        img = default_img

    draw = ImageDraw.Draw(img)
    bbox = [scale_rxy_to_xy(rxy), scale_rxy_to_xy((rxy[0] + width, rxy[1] + height))]
    draw.ellipse(bbox, outline=line_color, width=line_width)
    return bbox
