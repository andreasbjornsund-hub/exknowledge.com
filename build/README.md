# ExKnowledge Build System

Source content and metadata for generating the site's 198 HTML pages.

## Structure

```
build/
├── meta.json               # Page titles, descriptions, per-language titles
├── translation-guide.md    # Rules and sidebar labels for translators
├── content/
│   ├── pages/              # English source fragments (12 files)
│   └── {lang}/pages/       # Translated source fragments
└── translations/
    ├── en.json             # English UI strings (base)
    ├── de.json
    ├── no.json
    └── ...                 # 11 language files
```

## Source Fragments vs Published Pages

**Source fragments** (`build/content/pages/*.html`):
- Body content only — no `<head>`, no nav, no footer
- Start with `<div class="content-layout">` or `<h1>`
- Used as input for building full pages

**Published pages** (`pages/*.html`, `{lang}/pages/*.html`):
- Full HTML documents with DOCTYPE, head, meta tags, nav, sidebar, footer
- Reference `/css/style.css`
- Include hreflang tags for all 11 languages

## Translation Workflow

1. Copy English source fragment from `build/content/pages/{page}.html`
2. Translate body text to target language
3. Save to `build/content/{lang}/pages/{page}.html`
4. Wrap with full HTML template:
   - `<head>` with translated title from `meta.json` (`title_{lang}` key)
   - Nav with translated labels
   - Sidebar with translated page names (see `translation-guide.md`)
   - Footer and burger menu JS
5. Save wrapped version to `{lang}/pages/{page}.html`
6. Commit both source fragment and published page

## Translation Rules

- Translate ALL body text
- Keep HTML structure, IDs, class names, and links exactly as-is
- Technical terms stay in original: Ex d, IEC 60079, ATEX, IECEx, EPL, T1-T6, IIA/IIB/IIC
- Image URLs stay unchanged
- Links use English filenames (`zone-classification.html`, not translated)

## meta.json

Contains per-page metadata:

```json
{
  "fundamentals": {
    "title": "Explosion Protection Fundamentals — ExKnowledge",
    "description": "The fire triangle, explosive atmospheres...",
    "title_de": "Grundlagen des Explosionsschutzes — ExKnowledge",
    "title_no": "Grunnleggende om eksplosjonsvern — ExKnowledge",
    ...
  }
}
```

## Making Changes

| Change | Edit | Then |
|--------|------|------|
| Page content (EN) | `build/content/pages/*.html` + `pages/*.html` | Commit & push |
| Page content (lang) | `build/content/{lang}/pages/*.html` + `{lang}/pages/*.html` | Commit & push |
| Page title/SEO | `build/meta.json` + update `<title>` in published page | Commit & push |
| CSS | `css/style.css` (no rebuild needed) | Commit & push |
| Nav items | Edit nav in each published page | Commit & push |
| Add language | Create `{lang}/` dir, translate all pages, add to lang selectors | Commit & push |
