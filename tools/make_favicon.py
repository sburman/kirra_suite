#!/usr/bin/env python3
"""Generate the Kirra Suite favicon set from a simple coastal mark.

Mark: deep-teal rounded tile, a terracotta "sun", and a cream sand band —
echoing the site's palette. Writes an SVG (crisp at any size) plus PNG/ICO
rasters. Re-runnable; overwrites existing output.

Usage: python3 tools/make_favicon.py   (needs Pillow)
"""
from __future__ import annotations
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    raise SystemExit("Pillow is required: pip install Pillow")

REPO = Path(__file__).resolve().parent.parent
IMG = REPO / "assets" / "img"

TEAL = (26, 58, 58)
TERRA = (181, 103, 63)
SAND = (244, 239, 232)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="The Kirra Suite">
  <defs><clipPath id="r"><rect width="64" height="64" rx="14"/></clipPath></defs>
  <g clip-path="url(#r)">
    <rect width="64" height="64" fill="#1a3a3a"/>
    <circle cx="41" cy="25" r="11" fill="#b5673f"/>
    <path d="M0 46 q16 -7 32 0 t32 0 V64 H0 Z" fill="#f4efe8"/>
  </g>
</svg>
"""


def draw_mark(size: int, rounded: bool) -> Image.Image:
    # Supersample for smooth edges, then downscale.
    s = size * 4
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    radius = int(s * 0.22) if rounded else 0
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=radius, fill=TEAL)
    # Sun
    r = int(s * 0.17)
    cx, cy = int(s * 0.64), int(s * 0.39)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TERRA)
    # Sand band with a gentle wave top
    top = int(s * 0.72)
    pts = [(0, top)]
    import math
    for x in range(0, s + 1, max(1, s // 48)):
        pts.append((x, top - int(s * 0.05 * math.sin(x / s * math.pi * 2))))
    pts += [(s, s), (0, s)]
    d.polygon(pts, fill=SAND)
    # Re-clip rounded corners after the sand polygon
    if rounded:
        mask = Image.new("L", (s, s), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=radius, fill=255)
        im.putalpha(mask)
    return im.resize((size, size), Image.LANCZOS)


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    (IMG / "favicon.svg").write_text(SVG, encoding="utf-8")

    draw_mark(32, rounded=True).save(IMG / "favicon-32.png")
    draw_mark(192, rounded=True).save(IMG / "favicon-192.png")
    draw_mark(512, rounded=True).save(IMG / "favicon-512.png")
    # Apple touch icons are masked by iOS — fill the square (no rounding/alpha).
    apple = draw_mark(180, rounded=False).convert("RGB")
    apple.save(IMG / "apple-touch-icon.png")
    # Multi-size .ico at the repo root for default browser requests.
    draw_mark(64, rounded=True).save(
        REPO / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print("Wrote favicon.svg, favicon-32/192/512.png, apple-touch-icon.png, favicon.ico")


if __name__ == "__main__":
    main()
