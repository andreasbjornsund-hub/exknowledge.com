# ExKnowledge design system

This file is the source of truth for how exknowledge.com looks and behaves.
The tokens live in `css/style.css` (`:root`). Shared behaviour lives in
`js/nav.js`, `js/search.js` and `js/forms.js`. Change those files, not
individual pages.

**Rule: no hard-coded colours, font sizes or radii in HTML.** Use a token or a
component class. If a page needs something new, add it here and in
`css/style.css` first.

## Character

An industrial reference. Warm off-white reading surfaces, near-black
"inverse" bands for navigation and calls to action, one amber accent. Square
corners. Calm, dense and legible, never decorative for its own sake.

## Colour

| Token | Value | Use |
|---|---|---|
| `--surface` | #f8f7f5 | Page background |
| `--surface-raised` | #ffffff | Article body, cards, inputs |
| `--surface-sunken` | #f0eeea | Hover rows, code, quiet panels |
| `--inverse` | #121110 | Nav, hero, dark bands |
| `--inverse-raised` | #1a1917 | Cards on dark bands, dropdowns |
| `--line` | #ddd9d2 | Hairlines on light surfaces |
| `--line-strong` | #c9c3b8 | Input borders, secondary button border |
| `--line-inverse` | #2a2825 | Hairlines on dark surfaces |
| `--ink` | #23211e | Headings and strong text on light (15:1) |
| `--ink-muted` | #5a544a | Body and secondary text on light (7:1) |
| `--ink-on-inverse` | #f0eeea | Headings on dark |
| `--ink-muted-on-inverse` | #a8a296 | Secondary text on dark (≥ 7:1) |
| `--accent` | #d4a843 | Fills (primary button, badges), and accent text **on dark only** |
| `--accent-hover` | #e0bc5e | Hover of accent fills |
| `--accent-ink` | #86621a | Links and accent text **on light** (5.2:1) |
| `--on-accent` | #121110 | Text on an accent fill (8.5:1) |
| `--success` / `--danger` / `--warning` | #2d7d46 / #b04236 / #9a5a14 | Status text on light |
| `--success-on-inverse` / `--danger-on-inverse` | #7cc98b / #f08a7e | Status text on dark |

Contrast rules:

- Body text must reach 4.5:1 and large text 3:1 (WCAG AA). Never put
  `--accent` text on a light surface. Use `--accent-ink`.
- Never put white text on amber. Use `--on-accent`.

### Light and dark surfaces

Older pages still use the legacy names `--text`, `--text-muted`,
`--text-bright` and `--border`. They are now **contextual**. On light
surfaces they resolve to `--ink-muted`, `--ink-muted` and `--ink`. Inside a
dark surface they resolve to light-on-dark values.

Dark surfaces are `.nav`, `.hero`, `.cta-strip`, `.dropdown`,
`.search-overlay`, `.inverse`, `.card--inverse`, `[data-surface="inverse"]`,
and any element with an inline `background:var(--bg-card)` or `var(--bg)`.
Mark a new dark block with `class="inverse"` or `data-surface="inverse"`.

## Type

- **Display:** Instrument Sans 600/700, for headings, buttons and nav.
- **Body:** Figtree 400/500.
- **Mono:** JetBrains Mono, for labels, codes and markings.
- No other families.

| Token | Size | Use |
|---|---|---|
| `--fs-caption` | 12px | Captions, table headers (minimum size) |
| `--fs-small` | 14px | Secondary text, buttons, labels |
| `--fs-body` | 16px | Body text, inputs (16px stops iOS zoom) |
| `--fs-lead` | 18px | Intro paragraph, h4 |
| `--fs-h3` | 20px | h3 |
| `--fs-h2` | 24px | h2 |
| `--fs-h1` | 32px | Page h1 |
| `--fs-hero` | clamp(36px, 5vw, 56px) | Home hero only |

Line height is 1.7 to 1.85 for body and 1.15 to 1.3 for headings. Use one h1
per page. Never skip a heading level for styling.

## Space, shape, depth

- **Space:** a 4px base. Allowed values are 4, 8, 12, 16, 24, 32, 48, 64 and
  96px (`--space-1` … `--space-24`).
- **Radii:** `--radius` is 0 and the default for cards, buttons and inputs.
  `--radius-sm` (4px) is for badges only. `--radius-pill` is for filter chips
  only.
- **Shadows:** `--shadow-sm`, `--shadow-md`, `--shadow-lg`. Use them only for
  floating things: dropdowns, popups and modals.
- **Tap targets:** at least 44 × 44px (`--tap`) at phone widths.

## Components

| Class | What it is |
|---|---|
| `.btn` + `.btn--primary` | The one main action in a section: amber fill with dark text |
| `.btn` + `.btn--secondary` | An alternative action: hairline border, transparent |
| `.btn` + `.btn--ghost` | A low-emphasis action, retry or skip: text only |
| `.btn--sm`, `.btn--block` | Size and width modifiers |
| `.card` / `.card--inverse` | A light or dark card |
| `.field`, `.field-label` | Inputs, selects and textareas with a visible label |
| `.field-error` | An inline error shown directly under the field |
| `.form-status` | The form outcome, with `--ok` or `--error` |
| `.state-msg` | Loading, empty or error panels, e.g. map or search |

Every interactive element has the same set of states:

- hover
- pressed (`:active`, 1px nudge)
- `:focus-visible` (a 2px `--focus` outline)
- disabled (55% opacity, `not-allowed`)

Legacy classes (`.btn-primary`, `.cta-btn`, `.dl-btn` and others) have been
given those states. New work uses the classes above.

## Page rules

1. **One primary action per page.**

   | Page | Primary action |
   |---|---|
   | Home | "Start with the basics" |
   | Topic pages and guides | The free PDF pocket guide |
   | Blog | Newsletter |
   | Quiz, survey, ebook, partners, about | Their own form |

   Everything else uses the secondary or ghost style.
2. **Every page has:**
   - a `<title>` of 60 characters or fewer
   - a meta description of 160 characters or fewer
   - a canonical link
   - Open Graph title, description and image
   - the favicon set: `/favicon.svg`, `/favicon-32.png` and `/apple-touch-icon.png`
   - `<html lang>`, plus `dir="rtl"` on Arabic pages
3. **Nothing scrolls sideways at 320px.** Wide tables and code scroll inside
   their own box.
4. **Motion:** 150 to 400ms, easing `--ease`. Everything respects
   `prefers-reduced-motion`.

## Behaviour (shared scripts)

- **`js/nav.js`**
  - Adds a skip link.
  - The menu button and dropdown triggers are real buttons with
    `aria-expanded`.
  - Escape closes the innermost open thing and returns focus.
  - Dropdowns open on hover, keyboard focus or click.
  - Shows a two-letter language code under 420px.
  - `EXK.openDialog(el, opts)` gives any popup Escape handling, focus in, a
    focus trap and focus back.
- **`js/search.js`**
  - States: loading, results, no results, and unavailable with a retry
    button.
  - The search opens as a modal dialog (Ctrl/⌘ K).
- **`js/forms.js`**
  - Every form posts through formsubmit.co (AJAX) to the site inbox.
  - Fields are validated inline, with the error text under the field.
  - While sending, the button is disabled and reads "Sending…".
  - Then a success or failure message is announced to screen readers.
  - Mark a form with `data-exk-form`, plus optional `data-subject`,
    `data-success` and `data-on-success`.

## Generated pages

`build_blog.py` renders the English monthly posts. It copies the page chrome
(nav, footer, head tags, scripts) from the live `blog/index.html`, so it
stays in step with the site.

`translate-pages.py` renders the translations. After any translation run,
run these two commands. Both are safe to re-run and change nothing if the
site is already consistent.

```
python3 scripts/build_nav.py   # translated, accessible nav on every page
python3 scripts/build_seo.py   # canonical, og:url, hreflang, sitemap.xml
```

Translated pages that are still English inside get
`<meta name="robots" content="noindex, follow">` and a canonical link to the
English page until they are translated. `build_seo.py` keeps them out of
hreflang and the sitemap.
