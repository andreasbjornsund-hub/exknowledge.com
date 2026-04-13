# ExKnowledge.com

Explosion protection reference site for engineers working in hazardous areas. Covers ATEX, IECEx, and UKCA certification, zone classification, protection methods, standards, and more.

**Live:** https://exknowledge.com

## Site Structure

```
exknowledge.com/
├── index.html              # English homepage
├── pages/                  # 12 English content pages
│   ├── fundamentals.html
│   ├── zone-classification.html
│   ├── gas-groups.html
│   ├── temperature-classes.html
│   ├── protection-methods.html
│   ├── epl.html
│   ├── ex-markings.html
│   ├── standards.html
│   ├── certification.html
│   ├── installation-inspection.html
│   ├── cheat-sheet.html
│   └── faq.html
├── blog/                   # Monthly industry roundups (EN)
│   ├── index.html
│   ├── 2025-11.html
│   ├── 2025-12.html
│   ├── 2026-01.html
│   └── 2026-02.html
├── {lang}/                 # 10 translated versions
│   ├── index.html          # Translated homepage
│   ├── pages/              # 12 translated content pages
│   └── blog/               # Translated blog
├── css/style.css           # Single shared stylesheet
├── fonts/                  # KHTeka font files (.otf)
├── images/                 # OG images, favicons
├── js/                     # Shared scripts
├── build/                  # Source content + metadata (see below)
└── exscanner/              # Ex Certificate Scanner (separate app)
```

## Languages (11)

| Code | Language   | Status       |
|------|-----------|--------------|
| en   | English    | ✅ Complete  |
| de   | German     | ✅ Complete  |
| no   | Norwegian  | ✅ Complete  |
| es   | Spanish    | ✅ Complete  |
| da   | Danish     | 🔄 11/12     |
| sv   | Swedish    | ⬜ Machine   |
| fi   | Finnish    | ⬜ Machine   |
| nl   | Dutch      | ⬜ Machine   |
| pt   | Portuguese | ⬜ Machine   |
| it   | Italian    | ⬜ Machine   |
| ar   | Arabic     | ⬜ Machine   |

## Stats

- **198 published HTML pages** (excl. build sources)
- **12 content pages × 11 languages** = 132 content pages
- **11 homepages** + **11 blog indexes** + **44 blog posts**
- **Single CSS file** — all pages share `/css/style.css`

## Design

- **Theme:** Light warm surface, dark nav, amber accent (`#d4a843`)
- **Fonts:** Space Grotesk (display), Source Serif 4 (body), JetBrains Mono (code/labels)
- **Style:** Sharp edges (0 border-radius), 1px borders, industrial editorial aesthetic
- **Responsive:** Mobile hamburger nav, collapsible sidebar, fluid typography

## Content Pages

Each page has:
- Full SEO: `<title>`, meta description, Open Graph, Twitter Card
- hreflang tags for all 11 languages
- Canonical URL
- Structured sidebar with current-page indicator
- Hero image (Unsplash, industrial/offshore themed)
- Navigation with language switcher

## Build System

Source content lives in `build/`:

```
build/
├── meta.json               # Page titles, descriptions, translated titles
├── content/
│   ├── pages/              # English source fragments (body content only)
│   └── {lang}/pages/       # Translated source fragments
└── translations/           # UI string translations (nav, footer, labels)
```

**Important:** Source fragments in `build/content/` are body-only HTML. Published pages in `pages/` and `{lang}/pages/` are full HTML documents with `<head>`, nav, sidebar, footer, and scripts.

### Workflow

1. Edit source fragment in `build/content/{lang}/pages/{page}.html`
2. Wrap with full HTML template (head, nav, sidebar, footer)
3. Write to `{lang}/pages/{page}.html`
4. Update `build/meta.json` if titles/descriptions changed
5. `git add -A && git commit && git push`

### CSS Changes

Edit `css/style.css` directly — no build step needed, all 198 pages reference it.

## Deployment

GitHub Pages from `main` branch. Push to deploy.

- **Domain:** exknowledge.com (custom domain via CNAME)

## SEO

- All pages have unique titles and meta descriptions
- hreflang tags on every page (11 languages + x-default)
- Canonical URLs prevent duplicate content
- JSON-LD structured data on key pages
- Sitemap at `/sitemap.xml`
- robots.txt configured

## License

Content © ExKnowledge. All rights reserved.
