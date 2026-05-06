#!/usr/bin/env python3
"""Generate favicon.ico for splashpadlocator.com.

Output: static/favicon.ico (multi-size: 16, 32, 48)

Simple cyan water-drop on transparent background. Pure PIL.
"""
from pathlib import Path

from PIL import Image, ImageDraw

OUTPUT = Path(__file__).resolve().parent.parent / "static" / "favicon.ico"

CYAN = (8, 145, 178, 255)
LIGHT = (224, 247, 255, 255)
TRANSPARENT = (0, 0, 0, 0)


def make_drop(size):
    """Render a stylized water drop on a transparent square."""
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Outer drop body — circle stretched into a teardrop
    pad = size // 8
    body_top = pad + size // 8
    body = [pad, body_top, size - pad, size - pad]
    draw.ellipse(body, fill=CYAN)

    # Tip — narrow triangle at the top blending into the circle
    tip_h = size // 3
    tip = [
        (size // 2, pad // 2),
        (size // 2 - size // 8, body_top + size // 8),
        (size // 2 + size // 8, body_top + size // 8),
    ]
    draw.polygon(tip, fill=CYAN)

    # Highlight
    hl_r = size // 8
    hl_x = size // 2 - size // 6
    hl_y = size // 2
    draw.ellipse(
        [hl_x - hl_r, hl_y - hl_r, hl_x + hl_r, hl_y + hl_r],
        fill=LIGHT,
    )
    return img


def main():
    sizes = [16, 32, 48, 64]
    # Render at the largest target size; PIL's ICO encoder downsamples to each
    # listed size when `sizes=` is passed.
    img = make_drop(max(sizes))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, format="ICO", sizes=[(s, s) for s in sizes])
    print(f"Wrote {OUTPUT}  ({OUTPUT.stat().st_size} bytes, sizes={sizes})")


if __name__ == "__main__":
    main()
