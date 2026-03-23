# ExKnowledge Page Template & Checklist

## When Adding a New Page

Every new HTML page MUST include all of the following. Use `scripts/verify-pages.py` to check.

### Head Section (in order)
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://unpkg.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; img-src 'self' https://images.unsplash.com https://img.youtube.com https://*.googletagmanager.com data:; connect-src 'self' https://www.google-analytics.com https://formsubmit.co https://region1.google-analytics.com; font-src 'self' https://cdnjs.cloudflare.com; frame-src https://www.youtube.com https://www.googletagmanager.com">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>PAGE TITLE. ExKnowledge</title>
<meta name="description" content="...">
<link rel="canonical" href="https://exknowledge.com/PATH">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:url" content="https://exknowledge.com/PATH">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ExKnowledge">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="...">
<meta property="og:image" content="https://exknowledge.com/images/og-default.png">
<meta name="twitter:image" content="https://exknowledge.com/images/og-default.png">
<!-- CSS -->
<link rel="stylesheet" href="/css/style.css">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/bold/style.css">
<!-- Favicon -->
<link rel="icon" href="data:image/svg+xml,...">
<!-- JSON-LD Schema -->
<script type="application/ld+json">[...]</script>
<!-- GTM -->
<script>...GTM-5VSBXBSL...</script>
```

### Nav (must include all)
- 7 nav items: Fundamentals, Zones, Protection, Standards, Quick Ref, Blog, Podcast
- `lang-select` dropdown
- `burger` mobile menu div (using `ph-bold ph-list` icon)

### Footer (must include all)
- Glossary link + Podcast link
- Built for engineers disclaimer
- Not a substitute disclaimer
- Podcast icons row: RSS, Apple Podcasts, Spotify, All Episodes

### Scripts (before </body>)
```html
<script src="/js/nav.js"></script>
<script src="/js/search.js"></script>
<script src="/js/reveal.js"></script>
```

### After Creating Pages
1. Run `python3 scripts/verify-pages.py` to check consistency
2. Add URL to `sitemap.xml`
3. Update `llms.txt` and `llms-full.txt` if applicable
4. Commit and push
5. Submit to IndexNow:
```python
python3 scripts/indexnow-submit.py https://exknowledge.com/pages/new-page.html
```

### For Translated Pages
- Copy the English page structure exactly
- Translate content (use glossary terms from glossary/index.html)
- Set correct `lang` attribute on `<html>` tag
- Update `hreflang` tags in `<head>`
- Keep all code examples, standard numbers, and proper nouns untranslated
- Arabic pages need `dir="rtl"` on `<html>` tag
- Norwegian uses `lang="nb"` in HTML but `/no/` in URL paths
