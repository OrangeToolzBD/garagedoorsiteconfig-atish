# CTA band design references

Stitch output, 2026-08-17. Five concepts. **Already ported** — see
`cta_band()` in `engine/build.py` and the `.ctab--*` block in
`engine/build_site.py`.

Kept as the source of record for what was adapted and what was deliberately
not.

## Shipped as

| Stitch concept | Shipped variant |
|---|---|
| split bar on tint | `bar` |
| dark filled panel | (folded into the existing `panel` — the base `.cta-band` already was one) |
| boxed centred card | `card` |
| oversized asymmetric heading | `editorial`, **type capped** |
| full-bleed single-line bar | `strip`, **overflow fixed** |

## What was changed on the way in, and why

- **322px of horizontal overflow at 1280px.** The full-bleed bar's button group
  escaped the viewport. The shipped `strip` wraps instead, and pushes its
  actions with `margin-left:auto` that is reset below 900px.
- **A 72px heading.** That is the `display-lg` size already rejected once for
  inverting the page-H1 hierarchy; the brief had capped CTA headings at ~40px.
  Shipped `editorial` clamps to `clamp(1.6rem,3.1vw,2.45rem)` — 39px measured.
- **Three of twelve buttons under the 44px touch target.** All shipped variants
  measure 58px.
- **"View Pricing" on every concept.** There is no pricing, no pricing page, and
  pricing is on the no-invent list. Button labels come from the renderer:
  the call CTA (or a quote link where there is no phone) plus one of
  "Request a Quote" / "See Our Services".

## Two defects this work uncovered in existing code

- `.cta-band p` shipped as `rgba(255,255,255,.9)`, which is **4.32:1** against
  the lightest `--p` values in `themes.json` — below AA, on 154 themes.
  `contrast_failures()` never caught it because it scores only accent-derived
  colours. Now solid white (4.99:1), held by a new `cta_contrast_failures`
  gate that reads the alpha actually shipped in the built stylesheet.
- `call_btn()` drew the phone glyph on its no-phone fallback — a handset on a
  button that opens a quote form, on 998 of 1001 sites. Now an arrow.

## Note for future rounds

The design space here is small: a heading, one line, two buttons. Porting
Tailwind mockups cost more than writing the variants directly against the
engine's own tokens and button presets. If this section needs more variants
later, write them rather than generating them.
