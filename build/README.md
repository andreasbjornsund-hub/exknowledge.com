# ExKnowledge Build System

Generates all 198 HTML pages from shared templates + content + translations.

## Structure

```
build/
├── build.py              # Main build script
├── meta.json             # Page titles & descriptions
├── README.md
├── content/
│   ├── index.html        # Homepage content
│   ├── index_search.html # Hero search script
│   ├── blog/
│   │   └── index.html    # Blog listing content
│   └── pages/
│       ├── fundamentals.html
│       ├── zone-classification.html
│       └── ...           # 12 content pages
└── translations/
    ├── en.json           # English (base)
    ├── de.json           # German
    ├── no.json           # Norwegian
    └── ...               # 11 language files
```

## Usage

```bash
python3 build/build.py
```

Rebuilds all pages in-place. Commit and push to deploy.

## Making Changes

| Change | Edit | Then |
|--------|------|------|
| Nav items | `build.py` → `nav_html()` | Rebuild |
| Footer text | `translations/*.json` | Rebuild |
| Page content | `build/content/pages/*.html` | Rebuild |
| Add language | `translations/xx.json` + add to `LANGS` | Rebuild |
| Page title/SEO | `build/meta.json` | Rebuild |
| CSS | `css/style.css` (shared, no rebuild needed) | — |
| Fonts | `fonts/` (shared, no rebuild needed) | — |
