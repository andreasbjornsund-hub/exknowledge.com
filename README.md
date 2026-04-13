# ExKnowledge.com

ExKnowledge is a multilingual reference site about hazardous areas and explosion protection. It covers ATEX, IECEx, UKEX / DSEAR-related topics, zone classification, equipment selection, protection methods, markings, certification, inspection, and practical field guidance.

**Live site:** https://exknowledge.com

## What is in the site

The site currently includes:
- **26 core content pages** in English
- **10 translated language versions** plus English, for **11 languages total**
- **7 English blog posts** with translated blog libraries across the language folders
- standalone utility/content pages like `about.html`, `links.html`, `partners.html`, `quiz.html`, and `survey.html`
- a separate certificate tool at `/exscanner/`
- a glossary section and supporting SEO / discovery files such as `sitemap.xml`, `robots.txt`, `llms.txt`, and verification files

## Current language coverage

Languages currently published:
- English (`/`)
- German (`/de/`)
- Norwegian (`/no/`)
- Spanish (`/es/`)
- Danish (`/da/`)
- Swedish (`/sv/`)
- Finnish (`/fi/`)
- Dutch (`/nl/`)
- Portuguese (`/pt/`)
- Italian (`/it/`)
- Arabic (`/ar/`)

## Repo structure

```text
exknowledge.com/
├── index.html
├── pages/                    # 26 English content pages
├── blog/                     # English blog index + posts
├── ar/ da/ de/ es/ fi/ it/ nl/ no/ pt/ sv/
│   ├── index.html
│   ├── pages/                # translated content pages
│   └── blog/                 # translated blog pages
├── exscanner/                # Ex Certificate Scanner app
├── glossary/                 # glossary section
├── css/
├── js/
├── images/
├── scripts/                  # maintenance / SEO / translation scripts
├── sitemap.xml
├── robots.txt
├── llms.txt
└── CNAME
```

## Current content footprint

Approximate current published footprint in the repo:
- **286 core content pages** across all 11 languages
- **77 blog post pages** across all 11 languages
- **11 homepages**
- **11 blog index pages**
- **5 standalone pages**
- **~388 HTML files total** in the repo

## Main topics covered

The content library includes pages on:
- ATEX directive basics
- ATEX equipment categories
- ATEX vs IECEx
- hazardous area classification
- zone classification
- gas groups
- temperature classes
- EPL
- Ex markings
- protection methods
- certification
- CompEx certification
- installation and inspection
- cable glands in hazardous areas
- dust explosion protection
- hydrogen explosion protection
- DSEAR regulations
- NEC 500 vs ATEX / IECEx
- equipment selection
- FAQ and cheat sheet style reference pages

## Deployment

This repo is deployed via **GitHub Pages** from the `main` branch to:
- **https://exknowledge.com**

## SEO and discovery

The site includes:
- canonical URLs
- hreflang tags across languages
- sitemap submission support via `sitemap.xml`
- `robots.txt`
- `llms.txt` and `llms-full.txt`
- verification / discovery files for external platforms
- JSON-LD / structured-data support on key pages

## Utility scripts

The `scripts/` folder contains helper scripts for tasks like:
- translation workflows
- SEO fixes
- page verification
- FAQ schema support
- IndexNow submission

## Notes

This README reflects the site as it exists now in the public repo, not an older reduced-content version.

## License

Content © ExKnowledge. All rights reserved.
