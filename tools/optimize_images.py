#!/usr/bin/env python3
"""Optimize the Kirra Suite source photos for the web.

Reads the high-res originals from the project root `images/` folder (outside the
repo), renames them to semantic slugs, and writes web-sized WebP (plus JPEG
fallbacks) into assets/img/. Re-runnable: existing outputs are overwritten.

Usage:
    python3 tools/optimize_images.py
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is required: pip install Pillow")

# Source originals live in the non-code project root, one level above the repo.
REPO = Path(__file__).resolve().parent.parent
SRC = REPO.parent / "images"
OUT = REPO / "assets" / "img"
GALLERY = OUT / "gallery"

SRC_PREFIX = "Coastalimagesg_805_4 Miles Street-"

# Map original photo number -> (slug, category). Curated from a visual review.
MAPPING = {
    1: ("living-balcony", "Living"),
    2: ("balcony-ocean", "Views"),
    3: ("kitchen-dining", "Kitchen"),
    4: ("living-art", "Living"),
    5: ("kitchen-island", "Kitchen"),
    6: ("welcome-bubbles", "Touches"),
    7: ("coffee-station", "Touches"),
    8: ("living-dining-wide", "Living"),
    9: ("balcony-armchairs", "Views"),
    10: ("bedroom-master", "Bedrooms"),
    11: ("bedroom-master-detail", "Bedrooms"),
    12: ("bathroom-shower", "Bathroom"),
    13: ("bathroom-vanity", "Bathroom"),
    14: ("bathroom-wide", "Bathroom"),
    15: ("bedroom-second", "Bedrooms"),
    16: ("bedroom-second-sofabed", "Bedrooms"),
    17: ("bedroom-second-detail", "Bedrooms"),
    18: ("welcome-console", "Touches"),
    19: ("laundry", "Amenities"),
    20: ("building-entrance", "Building"),
    21: ("building-lobby", "Building"),
    22: ("building-exterior", "Building"),
    23: ("aerial-beach-wide", "Location"),
    24: ("aerial-beach", "Location"),
    25: ("pool-cabanas", "Resort"),
    26: ("pool", "Resort"),
}

# Output render sizes (max width in px) and quality.
SIZES = {
    "lg": (1600, 82),   # full-width / lightbox display
    "sm": (800, 80),    # gallery thumbnails / cards
}
# Images that also need a JPEG fallback (hero / social).
JPEG_FALLBACK = {"aerial-beach", "balcony-ocean", "living-balcony"}


def process(num: int, slug: str) -> list[str]:
    src = SRC / f"{SRC_PREFIX}{num}.jpg"
    if not src.exists():
        print(f"  ! missing source: {src.name}")
        return []
    written = []
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        for label, (max_w, quality) in SIZES.items():
            w, h = im.size
            scale = min(1.0, max_w / w)
            size = (round(w * scale), round(h * scale))
            resized = im.resize(size, Image.LANCZOS) if scale < 1.0 else im
            dest = GALLERY / f"{slug}-{label}.webp"
            resized.save(dest, "WEBP", quality=quality, method=6)
            written.append(dest.name)
            if slug in JPEG_FALLBACK and label == "lg":
                jdest = GALLERY / f"{slug}-{label}.jpg"
                resized.save(jdest, "JPEG", quality=quality, optimize=True, progressive=True)
                written.append(jdest.name)
    return written


def main() -> None:
    if not SRC.exists():
        sys.exit(f"Source folder not found: {SRC}")
    GALLERY.mkdir(parents=True, exist_ok=True)
    total = 0
    for num, (slug, _cat) in sorted(MAPPING.items()):
        files = process(num, slug)
        if files:
            total += len(files)
            print(f"  {num:>2} -> {slug}: {', '.join(files)}")
    print(f"\nDone. Wrote {total} files to {GALLERY.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
