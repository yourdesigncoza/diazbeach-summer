#!/usr/bin/env python3
"""Turn the chosen raw photos into web-sized WebP files plus the social preview image.

Run from the project root:  python3 tools/build_images.py
Captions and gallery order live in assets/js/config.js; this file only maps raw files to slugs.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "images_raw"  # the owner's original photos; gitignored, never published
OUT = ROOT / "assets" / "img" / "photos"

# The hero photo: the page header, the card and the social preview (og.jpg).
HERO = "sea-view"
# slug -> raw file, as a path under images_raw/. Captions and gallery order live in assets/js/config.js.
SOURCES = {
    "sea-view": "WhatsApp Image 2026-10-22 at 13.52.59 (1).jpeg",
    "lounge": "WhatsApp Image 2026-10-22 at 13.53.02 (2).jpeg",
    "lounge-balcony": "WhatsApp Image 2026-10-22 at 13.53.02 (3).jpeg",
    "lounge-tv": "WhatsApp Image 2026-10-22 at 13.53.02 (1).jpeg",
    "sleeper-couch": "WhatsApp Image 2026-10-22 at 13.53.04 (1).jpeg",
    "balcony-braai": "WhatsApp Image 2026-10-22 at 13.53.00 (1).jpeg",
    "desk": "WhatsApp Image 2026-10-22 at 13.53.04.jpeg",
    "kitchen": "WhatsApp Image 2026-10-22 at 13.53.03.jpeg",
    "kitchen-fridge": "WhatsApp Image 2026-10-22 at 13.53.03 (1).jpeg",
    "kitchen-hob": "WhatsApp Image 2026-10-22 at 13.53.03 (2).jpeg",
    "main-bedroom": "WhatsApp Image 2026-10-22 at 13.53.04 (2).jpeg",
    "main-bedroom-2": "WhatsApp Image 2026-10-22 at 13.53.05.jpeg",
    "bedroom-2": "WhatsApp Image 2026-10-22 at 13.53.05 (2).jpeg",
    "bathroom": "WhatsApp Image 2026-10-22 at 13.53.02.jpeg",
    "moonrise": "moonrise-crop.jpeg",  # landscape crop of 13.53.00, so the moon stays in frame
    "verified": "verified-badge.png",  # card badge, not in the gallery: 13.52.59 with the unit number painted out
}

# Hidden before resizing. Boxes are pixels in the upright original (after EXIF rotation).
# COVER pastes a plain patch from dx pixels to the side over a house number: {slug: [((l, t, r, b), dx)]}.
COVER = {
    "balcony-braai": [((576, 520, 610, 580), -40)],  # two people walking on the pavement
}
# BLUR hides number plates, faces and anything else private: {slug: [(l, t, r, b)]}.
BLUR = {
    "kitchen-fridge": [(985, 580, 1160, 705)],  # notes on the fridge door, one with a PIN
}
# Where og.jpg crops the hero photo (0-1 across, 0-1 down).
OG_CENTRE = (0.5, 0.6)

WIDTHS = (800, 1600)
HERO_WIDTHS = WIDTHS + (2400,)
OG_SIZE = (1200, 630)


def load(name: str) -> Image.Image:
    return ImageOps.exif_transpose(Image.open(RAW / name)).convert("RGB")


def redact(img: Image.Image, slug: str) -> Image.Image:
    for (left, top, right, bottom), dx in COVER.get(slug, []):
        patch = img.crop((left + dx, top, right + dx, bottom))
        mask = Image.new("L", patch.size, 0)
        ImageDraw.Draw(mask).rectangle((6, 6, patch.width - 7, patch.height - 7), fill=255)
        img.paste(patch, (left, top), mask.filter(ImageFilter.GaussianBlur(4)))
    for box in BLUR.get(slug, []):
        img.paste(img.crop(box).filter(ImageFilter.GaussianBlur(18)), box[:2])
    return img


def save_webp(img: Image.Image, slug: str, width: int) -> None:
    w = min(width, img.width)
    out = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
    out.save(OUT / f"{slug}-{width}.webp", "WEBP", quality=78, method=6)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, name in SOURCES.items():
        img = redact(load(name), slug)
        for width in HERO_WIDTHS if slug == HERO else WIDTHS:
            save_webp(img, slug, width)
        print(f"{slug:14} {img.width}x{img.height}")
    og = ImageOps.fit(redact(load(SOURCES[HERO]), HERO), OG_SIZE, Image.LANCZOS, centering=OG_CENTRE)
    og.save(ROOT / "assets" / "img" / "og.jpg", "JPEG", quality=82, optimize=True, progressive=True)


if __name__ == "__main__":
    main()
