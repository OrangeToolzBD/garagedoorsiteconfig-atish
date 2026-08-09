# Porta Pros Site Engine

A small, data-driven static-site engine that turns each city's markdown content
repo into a polished, SEO/AEO/GEO-optimized porta-potty rental website. One design
pattern, one command, many cities — each with its own theme, logo, and content.

## Quick start

```bash
python engine.py logos    # crop brand logo marks (once, or when logos change)
python engine.py build    # build every site in config/sites.json -> dist/
python engine.py serve    # portal on :8000, each city on its own port
python engine.py audit    # SEO / AEO / GEO report
```

Open **http://localhost:8000/** for the portal.

## How it works

```
config/sites.json     ── which cities to build (domain, city, ST, address, theme, port, suburbs)
config/themes.json    ── reusable design themes (colour system + font pairing)
<domain>/content/     ── each city's markdown content repo (branch: content)
POTTY V1/             ── shared photo set (mapped to pages by slug)
logo_assets/          ── cropped brand logo marks (from engine "logos")
build_site.py         ── the renderer (markdown -> themed HTML + SEO/schema)
serve.py              ── local preview server (no-cache headers)
dist/<domain>/        ── the built site for each city (what gets deployed)
```

The renderer reads every `content/**/*.md` (frontmatter + body) and emits a full
landing page + inner article pages, applying the site's theme and the SEO features
below. Nothing about a city is hard-coded — it all comes from `config/`.

## The design pattern

**Homepage** (money `index.md`): sticky header w/ mega-menu → hero (image, chips,
dual CTA) → trust bar → services grid (image cards) → "why us" features →
3-step "how it works" → pricing table → service-areas dropdown → FAQ accordion →
CTA band → branded footer. Entrance + scroll-reveal animations (reduced-motion safe).

**Inner pages** (service / suburb / guide / trust): page hero → two-column article
(content + sticky quote card) → CTA → footer.

**Service Areas menu**: a dropdown of suburbs. If a site lists `suburbs` in
`sites.json`, that drives the menu and any missing suburb pages are auto-generated;
otherwise suburbs come from the content's `04-suburbs/` pages.

## SEO / AEO / GEO features (automatic)

- **SEO**: `<title>` trimmed to ≤60 chars, meta description, canonical, OpenGraph +
  Twitter cards, one `<h1>`/page, image alt text, **auto-generated `sitemap.xml`**
  (matches the actual pages) and `robots.txt`, deep internal linking.
- **AEO**: FAQ accordions on the homepage and **every service page**, each emitted as
  **`FAQPage` JSON-LD** (eligible for FAQ rich results / answer engines).
- **GEO**: rich JSON-LD `@graph` — `LocalBusiness` (NAP + logo + `areaServed` +
  `priceRange`), `Service`, `BreadcrumbList` — plus a generated **`/llms.txt`** so
  LLMs can read the business, services and service areas.

## Adding a city

```bash
python engine.py new bostonportapros.com --city "Boston" --st MA --area 617 \
    --street "1 Summer St" --zip 02110 --theme harbor-clay --tagline "Hub Rentals"
# then:
git clone <content-repo> bostonportapros.com     # so ./bostonportapros.com/content/ exists
python engine.py logos && python engine.py build && python engine.py serve
```

`--theme` is optional (auto-assigned round-robin). Themes live in
`config/themes.json` — add your own `{p, pd, accent, on_accent, display, body, fonts}`
(keep `--p` dark for white text and `--accent` light with a dark `--on_accent`).

## Deploying

Each `dist/<domain>/` is a self-contained static site (root-relative links, so host
it at the domain root). The built sites are pushed to each repo's `main` branch:

```bash
# per repo, from a clean checkout of the content branch:
git -C <domain> checkout --orphan main
git -C <domain> rm -rf . >/dev/null 2>&1
cp -r dist/<domain>/. <domain>/
git -C <domain> add -A && git -C <domain> commit -m "Deploy site"
git -C <domain> push -u origin main
git -C <domain> checkout content        # restore content for future rebuilds
```

## Notes

- Phone numbers are placeholders (`(area) 555-0100`) unless a `"phone"` is set on the
  site in `sites.json`.
- `logo_prep.py` maps each domain to a brand lockup by `site_id`; new cities need a
  lockup added there (or they fall back to a generated SVG mark).
- Requires Python 3 + Pillow (`pip install Pillow`) for the logo cropping step.
```
