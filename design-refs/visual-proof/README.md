# Visual-proof design references

Stitch output, delivered 2026-08-17 as `stitch_elite_services_design_engine (4).zip`.
Four concepts, each as desktop + mobile (`code.html` + `screen.png`), plus the
`DESIGN.md` design-system spec that came with them.

Kept verbatim, including the concept we did not ship — regenerating is more
expensive than reworking.

## What happened to each

| Design | Status | Shipped as |
|---|---|---|
| `asymmetric_mosaic` | ported | `_pf_mosaic` / `.pf-mos` |
| `depth_stack` | ported, feature row cut | `_pf_stack` / `.pf-stk` |
| `image_selector` | **not ported yet** | — |
| `full_bleed_cinematic` | **not shipping** | — |

### `image_selector`
The category rail that swaps the photograph is worth having and is CSS-only.
Blocked on two things: its desktop interaction is `:hover`-only with no committed
state (dead on a touch tablet), so it needs rebuilding on the engine's three-tier
committed-radio / pointer / `:focus-visible` pattern; and its mobile variant
switches to a snap carousel needing five photographs, against a library ceiling of
four.

### `full_bleed_cinematic`
Not a fit, on four counts: one photograph only; `min-h-[80vh]`, which is hero scale
for a mid-page band; the photo ends up wallpaper behind a white copy card, so the
section stops being visual proof; and it is the closest of the four to the existing
`pf-cine`, so it would add a near-duplicate rather than a new look.

Worth reworking toward portrait/vertical emphasis — a direction none of the seven
current variants occupies.

## Everything here needs rewiring before use

These are Tailwind-CDN showcase pages, not engine code:

- Tailwind CDN → `GD_CSS`
- Google Fonts (Epilogue / Inter) → `var(--disp)` / `var(--body)`
- Material Symbols → `icon()`. Only 12 names exist; these files reference
  `verified`, `bolt`, `architecture`, `schedule` and `hardware`, none of which do.
- `lh3.googleusercontent.com` images → `select_photos()`
- Fixed Material-3 hexes → tokens

Two further traps:

- **`DESIGN.md` declares `display-lg: 72px`** — the size already rejected once for
  inverting the page-H1 hierarchy. None of the four concepts uses it (they all sit
  at `headline-lg`, 48px). Do not import it.
- **The supplied `screen.png` renders flatter the designs.** Their placeholder
  photography has invented UI baked into the pixels — a "Visual Proof: Depth Stack"
  browser title bar, "*Verified: Torque Check" and "*Image Ref: P-120" annotations.
  None of that is real content, and none of it survives contact with the photo
  library.

## The crop problem, measured

Every photograph in `brand/photos/` is landscape, 1376x768 (16:9). Measured against
each design's rendered photo box, with `object-fit:cover`:

| Slot | Box ratio | Visible % of source |
|---|---|---|
| `asymmetric_mosaic` tall plate | 0.59 | **33%** |
| `depth_stack` side plates | 0.75 | 42% |
| `depth_stack` centre | 0.80 | 45% |
| `image_selector` main | 1.12 | 63% |
| existing `.shots` (4/3) | 1.33 | 74% |
| existing `pf-tech` (16/10) | 1.60 | 89% |

All four crop harder than anything the engine already ships. A garage door is a
wide subject, so a centre third of the frame is rarely still a door. The ported
variants relax these deliberately — see the comments on `_pf_mosaic` and the
`.pf-stk` CSS block in `engine/build.py`.
