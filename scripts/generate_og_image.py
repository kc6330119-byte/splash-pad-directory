#!/usr/bin/env python3
"""Generate the Open Graph share image for splashpadlocator.com.

Output: static/images/og-image.png (1200x630, PNG)

The image is checked into the repo (committed) and served by Netlify; rerun this
script if the brand text or palette changes. Pure PIL — no external assets.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630
OUTPUT = Path(__file__).resolve().parent.parent / "static" / "images" / "og-image.png"

# Cyan/sky palette matches site Tailwind classes (cyan-600 → sky-700)
TOP_COLOR = (8, 145, 178)        # cyan-600
BOTTOM_COLOR = (3, 105, 161)     # sky-700
ACCENT_LIGHT = (224, 247, 255)
WHITE = (255, 255, 255)

WORDMARK = "Splash Pad Locator"
TAGLINE = "Find Free Splash Pads Near You"
DOMAIN = "splashpadlocator.com"


def gradient_background():
    img = Image.new("RGB", (WIDTH, HEIGHT), TOP_COLOR)
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        r = int(TOP_COLOR[0] + (BOTTOM_COLOR[0] - TOP_COLOR[0]) * t)
        g = int(TOP_COLOR[1] + (BOTTOM_COLOR[1] - TOP_COLOR[1]) * t)
        b = int(TOP_COLOR[2] + (BOTTOM_COLOR[2] - TOP_COLOR[2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img


def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        try:
            font = ImageFont.truetype(path, size)
            return font
        except OSError:
            continue
    return ImageFont.load_default()


def draw_decorative_drops(draw):
    drops = [
        (130, 160, 26),
        (1040, 110, 18),
        (1075, 470, 22),
        (160, 480, 16),
        (970, 220, 12),
    ]
    for x, y, r in drops:
        draw.ellipse([x - r, y - r, x + r, y + r], outline=WHITE, width=3)


def main():
    img = gradient_background()
    draw = ImageDraw.Draw(img)

    title_font = load_font(96, bold=True)
    tagline_font = load_font(46)
    domain_font = load_font(32)

    # Drop emoji as a hero glyph next to the wordmark
    drop_size = 120
    drop_x, drop_y = 200, 220
    draw.ellipse(
        [drop_x - drop_size // 2, drop_y - drop_size // 2,
         drop_x + drop_size // 2, drop_y + drop_size // 2],
        fill=ACCENT_LIGHT,
    )
    drop_inner_color = (14, 116, 144)
    drop_inner = drop_size - 30
    draw.ellipse(
        [drop_x - drop_inner // 2, drop_y - drop_inner // 2,
         drop_x + drop_inner // 2, drop_y + drop_inner // 2],
        fill=drop_inner_color,
    )

    # Wordmark — anchored to baseline left of drop glyph
    wm_x = drop_x + drop_size // 2 + 40
    wm_y = drop_y - 70
    draw.text((wm_x, wm_y), WORDMARK, fill=WHITE, font=title_font)

    # Tagline — directly under wordmark
    tag_y = wm_y + 130
    draw.text((wm_x, tag_y), TAGLINE, fill=ACCENT_LIGHT, font=tagline_font)

    # Domain — bottom right
    dom_w = draw.textlength(DOMAIN, font=domain_font)
    draw.text((WIDTH - dom_w - 60, HEIGHT - 70), DOMAIN, fill=ACCENT_LIGHT, font=domain_font)

    draw_decorative_drops(draw)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, "PNG", optimize=True)
    print(f"Wrote {OUTPUT}  ({OUTPUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
