import random
from enum import StrEnum
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


class Color(StrEnum):
    CORNFLOWER_BLUE = "#4A90D9"
    MEDIUM_SLATE_BLUE = "#7B68EE"
    MEDIUM_SEA_GREEN = "#5CB85C"
    SANDY_BROWN = "#F0AD4E"
    INDIAN_RED = "#D9534F"
    SKY_BLUE = "#5BC0DE"
    AMETHYST = "#9B59B6"
    TURQUOISE = "#1ABC9C"
    CARROT = "#E67E22"
    DODGER_BLUE = "#3498DB"
    EMERALD = "#27AE60"
    POMEGRANATE = "#C0392B"


AVATAR_COLORS = list(Color)

AVATAR_SIZE = (200, 200)
AVATAR_FONT_SIZE = 110
AVATAR_FALLBACK_FONT_SIZE = 80
AVATAR_TEXT_COLOR = "white"
AVATAR_TEXT_ANCHOR = (0, 0)
_WINDOWS_FONTS = "C:/Windows/Fonts"
_LINUX_FONTS = "/usr/share/fonts/truetype/dejavu"

AVATAR_FONT_PATHS = (
    f"{_WINDOWS_FONTS}/arialbd.ttf",
    f"{_WINDOWS_FONTS}/arial.ttf",
    f"{_LINUX_FONTS}/DejaVuSans-Bold.ttf",
    f"{_LINUX_FONTS}/DejaVuSans.ttf",
)


def generate_avatar_image(letter: str) -> ContentFile:
    bg_color = random.choice(AVATAR_COLORS)
    img = Image.new("RGB", AVATAR_SIZE, color=bg_color)
    draw = ImageDraw.Draw(img)
    text = (letter[0] if letter else "?").upper()

    font = None
    for font_path in AVATAR_FONT_PATHS:
        try:
            font = ImageFont.truetype(font_path, AVATAR_FONT_SIZE)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default(size=AVATAR_FALLBACK_FONT_SIZE)

    bbox = draw.textbbox(AVATAR_TEXT_ANCHOR, text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (AVATAR_SIZE[0] - w) / 2 - bbox[0]
    y = (AVATAR_SIZE[1] - h) / 2 - bbox[1]
    draw.text((x, y), text, fill=AVATAR_TEXT_COLOR, font=font)

    buf = BytesIO()
    img.save(buf, format="PNG")
    return ContentFile(buf.getvalue())
