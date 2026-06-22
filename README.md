# The Kirra Suite

Promotional brochure site for **The Kirra Suite**, a designer 2-bedroom beachfront
apartment in Kirra, on the southern Gold Coast (QLD, Australia).

A static site (plain HTML, CSS and vanilla JS, no build step or dependencies)
hosted on **GitHub Pages** at the custom domain **https://kirrasuite.com**.

## Structure

```
index.html               Home (hero, suite, amenities, mosaic gallery, location, booking)
guide.html               Evergreen Kirra & Coolangatta area guide
faq.html                 FAQ (native <details> accordion + FAQPage schema)
assets/css/styles.css    Styles
assets/js/main.js        Gallery, lightbox, nav, scroll reveals (guarded per page)
assets/img/gallery/      Web-optimized WebP (+ a few JPEG fallbacks)
assets/img/favicon*      Favicon set
favicon.ico              Root favicon
CNAME                    Custom domain for GitHub Pages
robots.txt, sitemap.xml  Crawl directives
.nojekyll                Tells GitHub Pages to serve assets/ untouched
tools/optimize_images.py Regenerates assets/img/gallery from the high-res originals
tools/make_favicon.py    Regenerates the favicon set
```

The high-resolution source photos are **not** committed. They live in the
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

Push to `main` on `github.com/sburman/kirra_suite`; Pages rebuilds automatically.
Source is **Deploy from a branch → `main` → `/ (root)`**.

## Custom domain (kirrasuite.com)

`kirrasuite.com` is registered. The `CNAME` file sets it on GitHub Pages. To make
it live:

1. **DNS** at the registrar (where `kirrasuite.com` is registered):
   - Apex `@` → four `A` records: `185.199.108.153`, `185.199.109.153`,
     `185.199.110.153`, `185.199.111.153` (and optionally the matching `AAAA`:
     `2606:50c0:8000::153`, `…8001::153`, `…8002::153`, `…8003::153`).
   - `www` → `CNAME` to `sburman.github.io`.
2. **Settings → Pages → Custom domain** is set automatically from the `CNAME`
   file on deploy; once DNS resolves, tick **Enforce HTTPS**.
3. **Google Search Console**: add the `kirrasuite.com` property, verify via DNS
   `TXT`, and submit `https://kirrasuite.com/sitemap.xml`.

## SEO notes

- Absolute `canonical`, Open Graph and JSON-LD URLs all point at the custom domain.
- `Apartment` schema on the home page; `FAQPage` on the FAQ; `BreadcrumbList` on
  the guide. Do **not** add `aggregateRating` until there are real guest reviews.
- Keep `guide.html`/`faq.html` date- and price-agnostic so they stay evergreen.
- After adding pages, update `sitemap.xml`.

## Booking

The primary call-to-action is **direct booking via POD Property Management**
(cheapest, no platform fees). Airbnb and Booking.com are offered as alternatives.
