# The Kirra Suite

Promotional brochure site for **The Kirra Suite** — a designer 2-bedroom beachfront
apartment at Miles, Kirra Point, on the southern Gold Coast (QLD, Australia).

The site is a single static page (plain HTML, CSS and vanilla JS — no build step,
no dependencies) designed to be hosted on **GitHub Pages**.

## Structure

```
index.html              The whole page
assets/css/styles.css   Styles
assets/js/main.js        Gallery, lightbox, nav, scroll reveals
assets/img/gallery/      Web-optimized WebP (+ a few JPEG fallbacks)
tools/optimize_images.py Regenerates assets/img from the high-res originals
.nojekyll               Tells GitHub Pages to serve assets/ untouched
```

The high-resolution source photos are **not** committed — they live in the
non-code project root (`../images/`). Re-run the optimizer after adding or
changing originals:

```bash
python3 tools/optimize_images.py   # needs Pillow: pip install Pillow
```

## Local preview

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy (GitHub Pages)

1. Commit and push to `main` on `github.com/sburman/kirra_suite`.
2. In the repo: **Settings → Pages → Build and deployment**.
3. Source: **Deploy from a branch**, Branch: **`main`**, Folder: **`/ (root)`**.
4. The site publishes at `https://sburman.github.io/kirra_suite/`
   (a custom domain can be added later under the same settings).

## Booking

The primary call-to-action is **direct booking via POD Property Management**
(cheapest, no platform fees). Airbnb and Booking.com are offered as alternatives.
