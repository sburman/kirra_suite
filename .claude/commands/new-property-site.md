# New Property Brochure Site

Build a complete static brochure site for a short-stay holiday property — same architecture, hosting strategy, SEO depth and marketing approach as The Kirra Suite (kirrasuite.com). The Kirra Suite codebase in this repo is the reference implementation; adapt everything to the new property.

## Minimum inputs required before starting

Before writing any code, confirm you have:

- **Photography**: path to the high-res image collection (or directory of originals)
- **Booking links**: direct/property-manager URL, Airbnb URL, Booking.com URL (any subset)
- **Property basics**: name, address (street, suburb, state, postcode), floor/level if apartment, bedroom count, bathroom count, max guests, standout feature (view, location, etc.)
- **Domain**: registered domain name (or placeholder — can be added later)
- **Host/manager**: name, platform (e.g. Airbnb Superhost), approximate review count and rating if known

If any of these are missing, ask before proceeding.

---

## Phase 1 — Property intake

Run through these questions conversationally and record the answers before touching any file:

1. What is the property's name and one-sentence positioning (e.g. "designer beachfront apartment, Level 8, directly across from Kirra Beach")?
2. What is the full address including postcode? What are the GPS coordinates (lat/lon to 4 decimal places)?
3. Key specs: bedrooms, bathrooms, max guests, parking, notable building amenities (pool, gym, etc.)?
4. What are the three or four most compelling nearby things — distance/walk time from property?
5. What is the check-in time, check-out time, pet policy?
6. Who manages the property — name, platform credentials, rough review count/rating?
7. What domain name will this live on?
8. Does the photography collection include: hero/exterior shot, living spaces, each bedroom, bathroom, kitchen, any outdoor/balcony, building/pool amenities, aerial or location shots?

Document the answers — they feed directly into schema markup, meta descriptions, and copy.

---

## Phase 2 — Visual identity

### Colour palette

Do not pick an arbitrary palette. Derive it from the property itself:

1. Study the photography — what are the dominant architectural colours? Glazing, roof, facade, interiors?
2. Look for art, soft furnishings or distinctive design elements in the interior shots that have strong colour character.
3. Choose **two** primary brand colours: one deep/dark (for headers, footer, cobalt/navy/charcoal tone), one warm/accent (for CTAs, eyebrows, icons — terracotta/coral/amber tone).
4. Round out with neutrals: a warm off-white for the page background (`--cream`), a slightly cooler off-white/sand for tinted sections (`--sand`), a near-black for body text (`--ink`), a mid-grey for secondary text (`--muted`), and a light grey for borders (`--line`).

Define as CSS custom properties in `:root`:
```css
:root {
  --cobalt:          /* deep brand colour */;
  --cobalt-deep:     /* 10–15% darker for hover states */;
  --terracotta:      /* warm accent */;
  --terracotta-dark: /* darker hover */;
  --sand:            /* tinted section background */;
  --cream:           /* base page background */;
  --ink:             /* body text */;
  --muted:           /* secondary text */;
  --line:            /* borders/dividers */;
  --white: #ffffff;
  --shadow:    0 12px 40px rgba(/* cobalt-deep rgb */, 0.13);
  --shadow-sm: 0 4px 18px  rgba(/* cobalt-deep rgb */, 0.08);
}
```

Variable names are semantic (cobalt, terracotta) not colour-literal (blue, red). Rename if the palette warrants it (e.g. `--slate`, `--ember`).

### Typography

Default pairing that works well for this type of site:
- Serif: **Fraunces** (headings — editorial, coastal feel)
- Sans: **Inter** (body, UI elements — clean, readable)

Load from Google Fonts. If the property has a strong existing brand using different fonts, match those instead.

### Favicon

Design a minimal abstract mark that fits the brand — not a photo crop, not a wordmark. The mark should work at 16×16px:

1. Deep-colour field (64×64 SVG with `rx="14"` rounded corners)
2. A single accent-colour shape evoking something about the property's location or character (a wave, a horizon line, a landform)
3. Use a cubic bezier path for organic shapes, not geometric primitives

Deliver: `assets/img/favicon.svg` plus raster set via `tools/make_favicon.py`. See the existing tool in this repo as the template — update colours, SVG path, and output sizes (32, 192, 512, apple-touch 180, ico multi-size 16/32/48).

---

## Phase 3 — File structure

```
index.html               Home (all primary sections)
guide.html               Evergreen local area guide
faq.html                 FAQ accordion + FAQPage schema
404.html                 Branded not-found page
assets/
  css/styles.css         All styles (single file, ~420 lines)
  js/main.js             Gallery, lightbox, nav, reveals (~155 lines)
  img/
    favicon.svg
    favicon-32.png
    favicon-192.png
    favicon-512.png
    apple-touch-icon.png
    gallery/             All optimised photos (WebP + JPEG fallbacks)
favicon.ico              Multi-size ICO at repo root
CNAME                    Custom domain
robots.txt               Crawl directives
sitemap.xml              Three-URL sitemap with lastmod
.nojekyll                Suppress GitHub Pages Jekyll processing
llms.txt                 Brief AI-readable property summary
llms-full.txt            Complete property facts for AI consumption
tools/
  optimize_images.py     Batch WebP conversion from high-res originals
  make_favicon.py        Regenerate favicon set from SVG geometry
```

No build step, no framework, no package.json. Everything ships as-is from the repo root.

---

## Phase 4 — Image pipeline

Before coding, process the photography:

1. Sort images into roles: hero, suite/living, bedrooms, bathroom, kitchen, amenities, building/exterior, aerial/location
2. Run `tools/optimize_images.py` (or write it if it doesn't exist) to produce:
   - `-lg.webp` at 1600px wide, quality 82 — full-size display
   - `-sm.webp` at 520px wide, quality 78 — mosaic thumbnails
   - Keep one `-lg.jpg` JPEG for the hero as an OG image fallback (OG meta can't use WebP universally)
3. Name files descriptively: `living-balcony`, `bedroom-master`, `aerial-beach-wide` — not `IMG_4521`
4. Target file sizes: lg ≤ 180KB, sm ≤ 45KB

Use `<picture>` + `<source type="image/webp">` throughout. Hero gets `fetchpriority="high"` and no `loading="lazy"`. Everything else is `loading="lazy"`.

---

## Phase 5 — Page implementation

### index.html sections (in order)

**`<head>`**
- `theme-color` = primary brand colour
- Preload hero image (WebP)
- Favicon link set (ico → svg → png32 → apple-touch)
- Open Graph: type=website, full title, description, image = hero jpg, image dimensions
- Twitter Card: summary_large_image
- JSON-LD: `["Apartment", "LodgingBusiness"]` (see Phase 6)

**Hero** (`min-height: 100svh`, full-bleed, text over gradient overlay)
- H1: lead with feeling/location, not the property name ("Beachfront mornings, legendary surf at your door")
- Sub-tag: one sentence, no more than 42 characters
- Two CTAs: primary = Check availability (→ #book), ghost = View the suite (→ #gallery)
- Overlay: `linear-gradient(180deg, cobalt-deep 45% opacity at top, cobalt-deep 78% at bottom)`

**Facts strip** (cobalt background, 5-column grid desktop)
- Bedroom count, bathroom count, guest capacity, floor/view, parking — most compelling stats
- Large serif number + small uppercase label

**Suite intro** (two-column split: text left, hero interior photo right)
- Eyebrow: "The Suite"
- H2: evocative, not descriptive
- 2 paragraphs max: first = feeling/experience, second = practical highlights
- CTA: "Book your stay" → #book (terracotta/primary button)

**Amenities** (auto-fit grid of cards with Material Symbols icons)
- 6–9 amenities, most distinctive first
- Material Symbols Outlined, weight 200, 1.75rem, terracotta
- Each card: icon + H3 + 1-sentence description

**Gallery** (`id="gallery"`)
- Mosaic: 5 standout photos, 3-column grid, first = large double-height tile
- Last tile: "Show all N photos" overlay that opens lightbox at photo 0
- Full lightbox: keyboard (←→ Escape), swipe touch, click-outside-to-close
- JS-driven, all photos in a `PHOTOS` array with slug + alt text

**Location** (`id="location"`)
- Full-width section head (heading + 2-sentence intro)
- Guide CTA tile (terracotta) full-width above the grid
- Two-column grid: aerial/context photo left (16:9, `align-items: center`), nearby list right
- Nearby list: name left, distance/descriptor right, border-bottom dividers

**Booking** (`id="book"`, tinted sand background)
- Host trust strip (cobalt): review count, star rating, years hosting, Superhost badge + one sentence. Use "+" suffixes on counts (1,100+ not 1,123) — evergreen
- Three booking cards: direct (featured, terracotta border, "Best price" flag), then OTA alternatives
- Direct card gets `.bcard--featured` with the most feature bullets

**Footer** (cobalt-deep background)
- Three columns: property name + address, Explore nav links, Book links
- JS-injected year — never hardcode it

### guide.html

Evergreen local area guide. Sections: the beach/surf, where to eat, coffee and bars, outdoor activities, getting here. No prices, no dates, no seasonal language. CTA pair at bottom: Book direct + Read the FAQ.

### faq.html

Native `<details>`/`<summary>` accordion. Cover: location, guests, bedrooms/bathrooms, parking, Wi-Fi/TVs, kitchen/laundry, pool/gym, airport, best price, families, walkability, check-in/out, pets, air-con, linen, streaming, cancellation, who manages it.

---

## Phase 6 — SEO and structured data

### Meta

Title: `[Property Name] | [Type] in [Suburb], [City/Region]`
Description: lead with specs, then location hook, then CTA ("Book direct and save").

Every page: canonical, og:url, og:title, og:description, og:image (absolute URL, JPEG), og:image dimensions, twitter:card=summary_large_image.

### JSON-LD (index.html)

`@graph` with two nodes:

```json
[
  {
    "@type": ["Apartment", "LodgingBusiness"],
    "@id": "https://[domain]/#apartment",
    "name": "...",
    "numberOfBedrooms": N,
    "numberOfBathroomsTotal": N,
    "occupancy": { "maxValue": N, "unitText": "guests" },
    "floorLevel": "N",
    "checkInTime": "T15:00",
    "checkOutTime": "T10:00",
    "petsAllowed": false,
    "geo": { "@type": "GeoCoordinates", "latitude": X.XXXX, "longitude": Y.YYYY },
    "address": { "@type": "PostalAddress", ... },
    "amenityFeature": [ ... ],
    "tourBookingPage": "...",
    "sameAs": [ "airbnb_url", "booking_url" ]
  },
  {
    "@type": "WebSite",
    "@id": "https://[domain]/#website",
    "url": "https://[domain]/",
    "name": "...",
    "about": { "@id": "https://[domain]/#apartment" }
  }
]
```

faq.html: `FAQPage` schema mirroring every visible question/answer.
guide.html + faq.html: `BreadcrumbList` schema.

### Supporting files

**sitemap.xml**: three URLs, `lastmod` = today, `changefreq`: monthly for index, yearly for subpages. Update lastmod whenever substantive content changes.

**robots.txt**: Allow all, include sitemap URL, explicitly welcome major AI crawlers: GPTBot, ClaudeBot, PerplexityBot, anthropic-ai, OAI-SearchBot, Googlebot.

**llms.txt**: one-paragraph property summary + links to all pages.

**llms-full.txt**: complete facts sheet — address, specs, check-in/out, policies, full amenity list, all nearby highlights with distances, booking channel URLs, management info. Structured with markdown headings. No fluff, just facts.

---

## Phase 7 — CSS architecture

Single `styles.css`, no preprocessor. Section order with `/* ---------- Section ---------- */` dividers:

1. `:root` custom properties
2. Reset + base (`box-sizing`, `img`, `html scroll-padding-top: 80px`)
3. Base typography (h1–h3 serif, body sans, link colour)
4. `.container`, `.section`, `.section--tint`, `.section__head`, `.eyebrow`
5. Buttons (`.btn`, `--primary`, `--ghost`, `--dark`, `--block`)
6. Header + nav (fixed, `is-scrolled` state, hamburger toggle)
7. Hero
8. Facts strip
9. Split layout
10. Amenities grid
11. Gallery mosaic
12. Lightbox
13. Location section
14. Booking cards + host trust strip
15. Footer
16. Subpage hero (`.page-hero`, `.page-hero--short`)
17. Prose article
18. FAQ accordion (native `<details>`)
19. Nav backdrop scrim (`#navBackdrop`)
20. Scroll reveal (`.reveal`, `.is-visible`)
21. `@media (max-width: 900px)` — mobile nav drawer, stack grids
22. `@media (max-width: 700px)` — mosaic reflow
23. `@media (max-width: 540px)` — facts strip single column
24. `@media (prefers-reduced-motion: reduce)`

**Critical mobile nav fix**: inside `@media (max-width: 900px)` add:
```css
.site-header.is-scrolled { backdrop-filter: none; background: var(--cream); }
```
`backdrop-filter` on a fixed ancestor creates a containing block for fixed children in Chromium — this clips the nav drawer to header height and makes menu items unclickable on Android. Removing it on mobile fixes the issue.

---

## Phase 8 — JavaScript

Single `main.js`, IIFE wrapper, `"use strict"`, no dependencies. Guarded per page with element existence checks. Sections:

1. **Gallery + lightbox** — guard: `document.getElementById('mosaic') && document.getElementById('lightbox')`
   - `PHOTOS` array: `{ slug, alt }` for every gallery photo
   - `MOSAIC` array: 5 indices into PHOTOS for the mosaic
   - Keyboard: ← → Escape; touch: swipe threshold 50px (`touchstart`/`touchend`, passive); click outside image closes
2. **Mobile nav** — toggle open/close, backdrop click-to-close, close on any nav link click
3. **Sticky header** — `is-scrolled` class when `window.scrollY > 40`, passive scroll listener
4. **Scroll reveal** — `IntersectionObserver` at threshold 0.12, `unobserve` after reveal; plain fallback for older browsers
5. **Footer year** — `document.getElementById('year').textContent = new Date().getFullYear()`

---

## Phase 9 — Deployment

1. Create GitHub repo (public — required for free GitHub Pages)
2. `git init`, initial commit, push to `main`
3. GitHub → Settings → Pages → Source: Deploy from branch → `main` → `/ (root)`
4. Add `CNAME` file at repo root containing the bare domain (`example.com`)
5. DNS at registrar:
   - Apex `@` → four A records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - AAAA records (optional): `2606:50c0:8000::153` through `…8003::153`
   - `www` → CNAME to `[github-username].github.io`
6. GitHub → Pages → Custom domain → enter domain → Enforce HTTPS once DNS resolves (~10 min)
7. Google Search Console: add property, verify via DNS TXT, submit sitemap URL

---

## Phase 10 — Post-launch

**Google Business Profile** (primary path to a Google Maps pin)
- Create at business.google.com → category: "Vacation home rental"
- Address = property address; fill photos, booking URL, check-in/out hours
- Verify (postcard, phone, or video) — can take days to weeks
- Encourage early guests to leave a Google review directly (separate from Airbnb reviews, shows on the map card)

**Google Hotel Search**
- Booking.com and Airbnb already feed this passively — no action needed
- Direct booking link requires Google Hotel Center integration via the property manager's channel manager (check whether their platform supports it)

**Evergreen maintenance discipline**
- Host stats: always "+" suffixes (`1,100+` reviews, `10+` years) — never needs updating
- No prices on the site — link out to booking platforms
- No seasonal language in guide.html or faq.html
- Update `sitemap.xml` lastmod whenever substantive content changes
- Run `tools/make_favicon.py` if brand colours change
- Run `tools/optimize_images.py` after adding new photos

---

## Reference implementation

The `kirra_suite/` repo is a complete deployed example of this pattern at **kirrasuite.com**. When uncertain about any implementation detail, read the existing code rather than inventing from scratch:

- `assets/css/styles.css` — complete design system
- `assets/js/main.js` — all interactivity patterns
- `index.html` — full page structure and schema
- `tools/make_favicon.py` — favicon generation
- `tools/optimize_images.py` — image processing pipeline
