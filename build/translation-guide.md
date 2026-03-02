# ExKnowledge Translation Guide

## Overview

Each language needs 12 content pages + 1 homepage + 1 blog index + blog posts.

## Source and Output

- **English source fragments:** `build/content/pages/`
- **Translated source fragments:** `build/content/{lang}/pages/`
- **Published pages:** `{lang}/pages/` (full HTML with head, nav, sidebar, footer)

⚠️ **Source fragments are body-only HTML.** Published pages must be wrapped with the full HTML template before committing. See `build/README.md` for details.

## Pages (12 total)

1. `fundamentals.html`
2. `zone-classification.html`
3. `gas-groups.html`
4. `temperature-classes.html`
5. `protection-methods.html` (largest, ~17K)
6. `epl.html`
7. `ex-markings.html`
8. `standards.html`
9. `certification.html`
10. `installation-inspection.html`
11. `cheat-sheet.html`
12. `faq.html`

## Sidebar Labels

| Page | EN | NO | ES | DA |
|------|----|----|----|----|
| fundamentals | Fundamentals | Grunnleggende | Fundamentos | Grundlæggende |
| zone-classification | Zones | Soner | Zonas | Zoner |
| gas-groups | Gas Groups | Gassgrupper | Grupos de gas | Gasgrupper |
| temperature-classes | Temp. Classes | Temperaturklasser | Clases de temp. | Temperaturkl. |
| protection-methods | Protection | Vernemetoder | Protección | Beskyttelse |
| epl | EPL | EPL | EPL | EPL |
| ex-markings | Markings | Merkinger | Marcado | Mærkning |
| standards | Standards | Standarder | Normas | Standarder |
| certification | Certification | Sertifisering | Certificación | Certificering |
| installation-inspection | Installation | Installasjon | Instalación | Installation |
| cheat-sheet | Cheat Sheet | Hurtigoversikt | Guía rápida | Hurtigoversigt |
| faq | FAQ | FAQ | FAQ | FAQ |

| Page | SV | FI | NL | PT | IT | AR |
|------|----|----|----|----|----|----|
| fundamentals | Grunder | Perusteet | Basiskennis | Fundamentos | Fondamenti | الأساسيات |
| zone-classification | Zoner | Vyöhykkeet | Zones | Zonas | Zone | المناطق |
| gas-groups | Gasgrupper | Kaasuryhmät | Gasgroepen | Grupos de gás | Gruppi gas | مجموعات الغاز |
| temperature-classes | Temperaturkl. | Lämpötilaluokat | Temp.klassen | Classes de temp. | Classi di temp. | فئات الحرارة |
| protection-methods | Skyddsmetoder | Suojausmenetelmät | Bescherming | Proteção | Protezione | طرق الحماية |
| epl | EPL | EPL | EPL | EPL | EPL | EPL |
| ex-markings | Märkningar | Merkinnät | Markeringen | Marcações Ex | Marcature Ex | علامات Ex |
| standards | Standarder | Standardit | Normen | Normas | Norme | المعايير |
| certification | Certifiering | Sertifiointi | Certificering | Certificação | Certificazione | الشهادات |
| installation-inspection | Installation | Asennus | Installatie | Instalação | Installazione | التركيب |
| cheat-sheet | Snabböversikt | Pikaohje | Snelgids | Guia rápido | Guida rapida | مرجع سريع |
| faq | FAQ | FAQ | FAQ | FAQ | FAQ | FAQ |

## Translation Rules

1. **Translate ALL body text** to the target language
2. **Keep HTML structure** — all tags, IDs, class names, and `data-` attributes unchanged
3. **Keep links as-is** — filenames stay English (`zone-classification.html`, not translated)
4. **Keep image URLs unchanged** — same Unsplash images across all languages
5. **Technical terms stay in original:**
   - Standards: IEC 60079, EN 60079, ATEX 2014/34/EU, IECEx
   - Protection types: Ex d, Ex e, Ex i, Ex p, Ex n, Ex o, Ex q, Ex m
   - Equipment: EPL, Ga, Gb, Gc, Da, Db, Dc
   - Gas groups: IIA, IIB, IIC
   - Temperature classes: T1, T2, T3, T4, T5, T6
   - Zone numbers: Zone 0, Zone 1, Zone 2, Zone 20, Zone 21, Zone 22
6. **Code blocks:** translate comments/labels only, keep technical content
7. **Table headers:** translate, but keep data values in original where technical
8. **Avoid AI writing patterns:** no inflated significance, no promotional tone, no "it's important to note that", no rule of three unless natural

## Translation Quality

Apply humanizer principles — translations should read like a native engineer wrote them:
- Use natural sentence structures for the target language
- Avoid literal English calques
- Keep technical precision while writing naturally
- Short, direct sentences preferred over elaborate constructions

## Checklist Per Language

- [ ] All 12 source fragments in `build/content/{lang}/pages/`
- [ ] All 12 published pages in `{lang}/pages/` (full HTML)
- [ ] Homepage translated (`{lang}/index.html`)
- [ ] Blog index translated (`{lang}/blog/index.html`)
- [ ] Blog posts translated (`{lang}/blog/*.html`)
- [ ] Titles in `build/meta.json` (`title_{lang}` keys)
- [ ] Sidebar labels correct
- [ ] Language switcher works on all pages
- [ ] Committed and pushed

## Git

- **Repo:** `andreasbjornsund-hub/exknowledge.com`
- **Deploy:** Push to `main` → GitHub Pages auto-deploys
- PAT configured in git remote URL
