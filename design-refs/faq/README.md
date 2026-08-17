# FAQ design references

Stitch output from two rounds, 2026-08-17. Seven concepts, in two different
contexts — which is the thing to understand before porting any of them.

## The FAQ renders in two places, and they are not the same component

| Context | Where | Markup | Width |
|---|---|---|---|
| **Section** | homepage | its own `<section class="sec sec--soft">` | full, 1180px |
| **In-article** | service / area / guide pages | `<h2 id="faq">` + `<div class="faq">` inside `div.body` | **764–820px** |

The in-article case is the majority: **108 of 150 inner pages** carry one, against
one per homepage. It sits inside running prose with paragraphs above and below,
so it must read as part of the article rather than as a band dropped into it.

The three article layouts it must survive (`build_site.py`):

- `.article` — `1fr 320px`, sidebar right → body ~764px
- `.article--left` — `320px 1fr`, sidebar left → body ~764px
- `.article--wide` — single column, `max-width:820px`

## The concepts

### `section_desktop/`, `section_mobile/` — round one (full-width)
1. **Asymmetric Editorial** *(desktop)* — heading and eyebrow in a left column,
   questions in a right column, vertical rule between.
2. **Boxed cards** *(mobile)* — each question in its own bordered card.
3. **Numbered index** *(mobile)* — 01/02/03 numerals down the left, +/− toggles.

Caveat: these do not pair up. The desktop file has only concept 1, the mobile
file has only 2 and 3, so every one of them is missing half its responsive spec.
The mobile file also drifted to generic consultancy copy — "project timeline",
"scope changes" — with ~230-character answers. Real answers are ~140, so those
cards will be shorter and emptier than the render suggests.

### `in_article/` — round two (764px column) — the stronger set
4. **Minimal Definition List** — hairline rows, chevron, very quiet.
5. **Editorial Pull-Out** — tinted panel with a left accent border.
6. **Compact Grid** — 2-up bordered cards, **answers always visible**.
7. **Text-Led Stack** — no borders at all, type weight and whitespace only,
   **answers always visible**.

All four are shown in context with prose above and below, in both their 1-pair
and 4-pair states, and all four measured clean: biggest type 28px, no horizontal
scroll at 360px, grid collapsing to one column on mobile, and every collapsed
`<details>` keeping its answer in the DOM.

Concepts 6 and 7 keeping answers permanently visible is the safest option for the
structured data — there is no collapsed state to reason about at all.

## The content budget — the constraint that kills most FAQ designs

- **One to four Q&A pairs.** Not "about four". Measured across the packs:
  40 pages have exactly **1**, 24 have 2, 35 have 3, 8 have 4.
  Homepages always have 3–4; inner pages are where the single-pair case lives.
- Questions: ~40 characters typical, 92 longest.
- Answers: **~140 characters typical, 361 longest.** One to three sentences.
  There is no long-form answer copy.

A design that only reads well with six questions in two columns is unbuildable
here. Any candidate must be checked in its one-pair state first.

## Non-negotiables for any port

- **Answers must stay in the DOM while collapsed.** The page publishes
  `FAQPage` JSON-LD built from this content. Native `<details>/<summary>` gives
  this for free, which is what the current renderer uses.
- **No JavaScript.** The only script that ships is `NAVJS`.
- Keyboard operable with a visible focus state — again free with `<details>`.
- Tokens only; must read on both white and `--soft`.
- In-article variants: type at or below 28px, since the article's own `h2` is
  ~37px and anything larger inverts the hierarchy.

## Rewiring, as always

Tailwind CDN → `GD_CSS` · Epilogue/Inter → `var(--disp)` / `var(--body)` ·
Material Symbols `expand_more` → `icon("arrow")` or a CSS chevron ·
fixed Material-3 hexes → tokens.

`DESIGN.md` here is the same design-system spec shipped with every round. It
declares `display-lg: 72px`, the size already rejected once for inverting the
page-H1 hierarchy. None of these concepts uses it. Do not import it.
