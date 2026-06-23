#!/usr/bin/env python3
"""Regenerate the Kirra Suite favicon set from the current brand mark.

Mark: cobalt rounded tile (#1e3d72) with a burnt orange-red wave horizon
(#cc4e2c) drawn as a cubic bezier S-curve — echoing the diptych paintings
in the apartment (deep cobalt right panel, warm orange-red left panel).

SVG path: M0 44 C16 24 48 58 64 44 V64 H0 Z  (in a 64×64 coordinate space)

Writes:
  assets/img/favicon.svg          — vector (primary)
  assets/img/favicon-32.png       — 32×32 raster
  assets/img/favicon-192.png      — 192×192 (PWA / Android)
  assets/img/favicon-512.png      — 512×512 (PWA splash)
  assets/img/apple-touch-icon.png — 180×180 (iOS home screen)
  favicon.ico                     — 16/32/48px multi-size (root, for bare requests)

Usage: python3 tools/make_favicon.py   (needs Pillow: pip install Pillow)
Re-runnable; overwrites existing output.
"""
from __future__ import annotations
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    raise SystemExit("Pillow is required: pip install Pillow")

REPO = Path(__file__).resolve().parent.parent
IMG  = REPO / "assets" / "img"

SVG = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="The Kirra Suite">
  <defs><clipPath id="r"><rect width="64" height="64" rx="14"/></clipPath></defs>
  <g clip-path="url(#r)">
    <rect width="64" height="64" fill="#1e3d72"/>
    <path d="M0 44 C16 24 48 58 64 44 V64 H0 Z" fill="#cc4e2c"/>
  </g>
</svg>
"""


def _cubic_bezier(p0, p1, p2, p3, n: int = 120):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u**3*p0[0] + 3*t*u**2*p1[0] + 3*t**2*u*p2[0] + t**3*p3[0]
        y = u**3*p0[1] + 3*t*u**2*p1[1] + 3*t**2*u*p2[1] + t**3*p3[1]
        pts.append((x, y))
    return pts


def draw_mark(size: int) -> Image.Image:
    s = size
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, s - 1, s - 1], fill="#1e3d72")

    # S-wave: M0 44 C16 24 48 58 64 44 (scaled from 64px design space)
    sc = s / 64
    wave = _cubic_bezier(
        (0  * sc, 44 * sc),
        (16 * sc, 24 * sc),
        (48 * sc, 58 * sc),
        (64 * sc, 44 * sc),
    )
    wave += [(s, s), (0, s)]
    draw.polygon(wave, fill="#cc4e2c")

    radius = max(1, round(14 * sc))
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=radius, fill=255)
    result = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    result.paste(img, mask=mask)
    return result


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)

    (IMG / "favicon.svg").write_text(SVG, encoding="utf-8")

    draw_mark(32).save(IMG / "favicon-32.png")
    draw_mark(192).save(IMG / "favicon-192.png")
    draw_mark(512).save(IMG / "favicon-512.png")
    draw_mark(180).save(IMG / "apple-touch-icon.png")
    draw_mark(48).save(REPO / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])

    print("favicon.svg, favicon-32/192/512.png, apple-touch-icon.png, favicon.ico written")


if __name__ == "__main__":
    main()
