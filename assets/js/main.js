/* The Kirra Suite interactivity: mosaic gallery, lightbox, nav, reveals.
   Runs on every page; the gallery/lightbox block is guarded so the shared
   nav, header and footer logic also work on subpages (guide, faq). */
(function () {
  "use strict";

  var IMG = "assets/img/gallery/";

  // ---- Mosaic gallery + lightbox (home page only) ----
  var mosaicEl = document.getElementById("mosaic");
  var lb = document.getElementById("lightbox");

  if (mosaicEl && lb) {
    // Full gallery order. Each entry maps to <slug>-sm.webp / <slug>-lg.webp.
    var PHOTOS = [
      { slug: "living-balcony",         alt: "Open-plan living room opening to the balcony and second bedroom" },
      { slug: "balcony-ocean",          alt: "Balcony dining setting with ocean views over Kirra Beach" },
      { slug: "living-dining-wide",     alt: "Living and dining area with designer furnishings" },
      { slug: "kitchen-dining",         alt: "Kitchen and dining with stone island and wishbone chairs" },
      { slug: "kitchen-island",         alt: "Designer kitchen with breakfast bar and gas cooktop" },
      { slug: "living-art",             alt: "Lounge with curated artwork beside the balcony" },
      { slug: "bedroom-master",         alt: "Master bedroom with king bed and coastal styling" },
      { slug: "bedroom-master-detail",  alt: "Master bedroom soft furnishings detail" },
      { slug: "bedroom-second",         alt: "Second bedroom and media room with sofa bed" },
      { slug: "bedroom-second-sofabed", alt: "Second bedroom queen sofa bed made up for guests" },
      { slug: "bedroom-second-detail",  alt: "Second bedroom styling detail" },
      { slug: "bathroom-shower",        alt: "Marble-look bathroom with walk-in rainfall shower" },
      { slug: "bathroom-vanity",        alt: "Bathroom vanity with premium guest amenities" },
      { slug: "bathroom-wide",          alt: "Bathroom opening through to the bedroom" },
      { slug: "welcome-bubbles",        alt: "Welcome sparkling wine and drinks on arrival" },
      { slug: "coffee-station",         alt: "Coffee station with pod machine and treats" },
      { slug: "welcome-console",        alt: "Welcome console with fresh towels and guest information" },
      { slug: "laundry",                alt: "Concealed laundry with washing machine and dryer" },
      { slug: "pool",                   alt: "Resort-style pool and sun deck" },
      { slug: "pool-cabanas",           alt: "Pool deck with cabanas and ocean breezes" },
      { slug: "building-lobby",         alt: "Light-filled lobby with curved lounge seating" },
      { slug: "building-exterior",      alt: "Beachfront tower above Kirra" },
      { slug: "aerial-beach",           alt: "Aerial view of Kirra Beach and the suite's location" },
      { slug: "aerial-beach-wide",      alt: "Wide aerial along Kirra Beach toward the hinterland" },
      { slug: "balcony-armchairs",      alt: "Balcony armchairs with a leafy Kirra outlook" }
    ];

    // Five standout photos for the mosaic. First = large tile, last carries "Show all".
    var MOSAIC = [0, 6, 3, 11, 18];
    var lbImg = document.getElementById("lbImage");
    var lbCap = document.getElementById("lbCaption");
    var current = 0;

    var openLightbox = function (index) {
      current = (index + PHOTOS.length) % PHOTOS.length;
      var p = PHOTOS[current];
      lbImg.src = IMG + p.slug + "-lg.webp";
      lbImg.alt = p.alt;
      lbCap.textContent = p.alt + "  ·  " + (current + 1) + " / " + PHOTOS.length;
      lb.classList.add("is-open");
      lb.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    };
    var closeLightbox = function () {
      lb.classList.remove("is-open");
      lb.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    };
    var step = function (dir) { openLightbox(current + dir); };

    MOSAIC.forEach(function (idx, pos) {
      var p = PHOTOS[idx];
      var tile = document.createElement("button");
      tile.className = "mosaic__tile" + (pos === 0 ? " mosaic__tile--lg" : "");
      tile.setAttribute("data-index", idx);
      var isLast = pos === MOSAIC.length - 1;
      tile.setAttribute("aria-label", isLast ? "Show all 26 photos" : "Enlarge: " + p.alt);
      var overlay = isLast
        ? '<span class="mosaic__more"><span class="icon">⊞</span>Show all photos<span class="count">' + PHOTOS.length + " photos</span></span>"
        : "";
      tile.innerHTML =
        '<img src="' + IMG + p.slug + '-sm.webp" alt="' + p.alt + '" loading="lazy" />' + overlay;
      tile.addEventListener("click", function () { openLightbox(isLast ? 0 : idx); });
      mosaicEl.appendChild(tile);
    });

    document.getElementById("lbClose").addEventListener("click", closeLightbox);
    document.getElementById("lbNext").addEventListener("click", function () { step(1); });
    document.getElementById("lbPrev").addEventListener("click", function () { step(-1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) closeLightbox(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") closeLightbox();
      else if (e.key === "ArrowRight") step(1);
      else if (e.key === "ArrowLeft") step(-1);
    });
  }

  // ---- Mobile nav (all pages) ----
  var nav = document.getElementById("nav");
  var toggle = document.getElementById("navToggle");
  if (nav && toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // ---- Sticky header state (all pages) ----
  var header = document.getElementById("header");
  if (header) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 40); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // ---- Reveal on scroll ----
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-visible"); });
  }

  // ---- Footer year (all pages) ----
  var yr = document.getElementById("year");
  if (yr) yr.textContent = new Date().getFullYear();
})();
