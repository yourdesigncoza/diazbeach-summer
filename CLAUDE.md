# CLAUDE.md

Static one-page holiday-let site (`index.html`) plus a printable A6 QR card (`card.html`) for a flat on Beach Boulevard West, Diaz Beach. Plain HTML/CSS/JS: no package manager, no bundler, no tests, no linter. GitHub Pages serves the repo root from `main` (`https://yourdesigncoza.github.io/diazbeach-summer/`), so every file committed at the root is public.

`README.md` is the owner-facing guide: how to edit `assets/js/config.js` (season, rates, bookings, contact, photos, places) and the table of rebuild commands. Read it before changing either.

## Commands

```bash
python3 -m http.server 8000      # preview at http://localhost:8000/ (the map needs HTTP; file:// won't load it)
```

Card preview: `http://localhost:8000/card.html` (A6) and `card.html?sheet=a4` (four-up). Python tools need Pillow (`build_images.py`) and segno (`build_qr.py`); `fetch_osm.py` needs network access to the Overpass API; `build_card.sh` needs `google-chrome` and `pdftoppm`.

Verification is manual: load the page in a browser and check the console, the calendar, the map pins and the card.

## Architecture

**Script chain.** Both pages load `config.js` → `common.js`; `index.html` then loads `site.js`. Order matters:
- `config.js` sets `window.SITE`, the single source for anything date-, price-, contact-, photo- or place-related, plus the `town` and `occasion` used on the postmark and in enquiry messages.
- `common.js` derives everything from it, exposes `window.Stay`, and on load fills `[data-fill="<key>"]` (keys = the `values` object), `[data-link="whatsapp|email|tel"]` and `[data-postmark]`. New config-driven text goes into `values`, then into markup as `data-fill`.
- `card.html` clones its `<template>` in an inline script *before* `common.js` runs, so `fill()` reaches every card copy.
- `site.js` builds the gallery, lightbox, availability calendar, map pins, places list and the phone-only bottom dock. Every WhatsApp/email button uses `data-link`, so they all open the same `generic()` message.

**Dates.** Everything is a UTC-midnight millisecond timestamp (`Stay.parse` uses `Date.UTC`; arithmetic is `DAY` steps; formatting uses `getUTC*`). Never mix in local-time `Date`. A booking `{from, to}` blocks nights `from` up to but not including `to`. The calendar is display only (no date picking): season days show open or booked, and guests send their own dates.

**Rates.** `common.js` sorts `rates` by `minNights` descending. `values.rateFrom`/`rateLongNights` come from the longest tier, `rateStd`/`rateStdNights` from the shortest. The rates `<dl>` in `index.html` shows exactly those two, so a third tier in config won't appear on the page without a markup change.

**Map.** `tools/data/map.json` holds the map frame (`bbox`), title, labels and trail names. `tools/fetch_osm.py` downloads `tools/data/osm.json` for that frame, and `tools/build_map.py` turns it into `assets/img/map.svg` (base layers only; sea plus coastline if the frame has coast, otherwise plain land with an `inland` class) and writes its lat/lng bounds to the SVG's `data-bbox`. `site.js` fetches the SVG and projects `SITE.places` and `SITE.home` onto it linearly from that bbox. Places outside the bbox become edge arrows. `label: n|s|e|w` sets which side of the pin the name sits.

**Photos.** Files follow `assets/img/photos/<slug>-<width>.webp` (800 and 1600; the hero `sea-view` also 2400, and `og.jpg` is cropped from it). `tools/build_images.py` maps slugs to raw files (`SOURCES`) and redacts house numbers (`COVER`) and number plates or faces (`BLUR`), including in `og.jpg`. `config.js` `photos` sets gallery order and captions. A new photo needs an entry in both. `images_raw/` is gitignored and only exists locally. Gallery layout rule (in the `config.js` comment): plain photos between `wide` ones come in multiples of 4.

**Card and print files.** `print/estoril-villas.pdf`, `print/estoril-villas.png` and `print/card-a4.pdf` are committed build outputs from `./tools/build_card.sh` (headless Chrome against a temporary server on port 8799). Regenerate them after changing `card.html`, `config.js` values the card shows, or the QR code. The QR (`assets/img/qr.svg`) encodes the `og:url` in `index.html`, which is the one place the site address lives.

**Styles.** `assets/css/tokens.css` holds the colour/font tokens and the postmark styles shared by both pages; `assets/css/site.css` is page-only. The card's own styles are inline in `card.html` (sized in mm). Breakpoints: 600, 720, 900px. The hero title's size comes from `--title-fit` on the `<h1>` (the town name's width in em, plus about .15); re-measure it if the town name changes.

## Gotchas

- House copy (description, beds, amenities, "Sleeps 6", meta/OG description, town name) is hard-coded in `index.html`, and partly repeated in `card.html`. It is not in `config.js`, apart from `town` and `occasion`.
- One flat rate (R3 000 a night): `rates` has one tier and the rates `<dl>` one row, and the hero, dock and card say "R3 000 a night" without "from". To add tiers again, restore the second `<dl>` row (`rateLongNights`/`rateFrom`) and the "from" wording.
- "Verified accommodation" (owner approved by Vakansie verblyf in Mosselbaai, ref VM0091): the page shows it as an HTML pill in the hero and as the approval image above "Who sleeps where" (`.verified-badge`), both styled by a small inline `<style>` in `index.html` so the engine CSS stays the same as other listings. The card shows the image too (`.badge` on the photo). The image is built as the `verified` slug in `build_images.py` from `images_raw/verified-badge.png`: a copy of `13.52.59.jpeg` with the unit number painted out in the shield colour. Never publish the original image. Recreate the copy if `images_raw/` is rebuilt:
  `python3 -c "from PIL import Image, ImageOps, ImageDraw; im = ImageOps.exif_transpose(Image.open('images_raw/WhatsApp Image 2026-10-22 at 13.52.59.jpeg')).convert('RGB'); ImageDraw.Draw(im).rectangle((317, 486, 379, 536), fill=im.getpixel((350, 470))); im.save('images_raw/verified-badge.png')"`
- `tools/build_map.py` differs from the template engine: `land()` closes the coastline round the land side of a box outside the frame. The template closes it with a straight line from end to start, which fills the sea as land when the coast bends round a bay, as it does here.
- `source/` holds the owner's WhatsApp photo dump and is gitignored. `images_raw/moonrise-crop.jpeg` is a landscape crop of `13.53.00.jpeg`, made so the moon stays in frame; recreate it if `images_raw/` is rebuilt.
- Privacy is deliberate: no street number or exact address anywhere. The `home` pin is approximate, and photos are redacted at build time. Keep it that way.
- Copy is South African English (`en-ZA`: stoep, braai, favourite). Prices are formatted by `Stay.rand` (`R3 000`), and WhatsApp links assume a South African number (`common.js` adds country code 27).
- Commit messages follow conventional commits with a scope, e.g. `feat(content): …`, `style(mobile): …`, `chore(card): …`.
