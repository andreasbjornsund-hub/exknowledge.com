#!/usr/bin/env python3
"""Create language redirect pages for every English page that has no translation.

Why: Cloudflare geo-redirects a first-time visitor from /<path> to /<lang>/<path>
(302 + a 24-hour geo_redirected cookie). For English-only pages such as
/ebook.html or /glossary/ that landed on a 404. Each missing /<lang>/<path> gets a
small noindex page that sends the visitor straight back to the English page. The
cookie set by the first redirect stops a loop. This matches the existing
translated redirect pages (e.g. no/about.html).

Safe to re-run: existing pages, translated or not, are never touched.
Usage (from the repo root): python3 scripts/build_lang_stubs.py
"""
import html, pathlib, re

LANGS = ['ar', 'da', 'de', 'es', 'fi', 'it', 'nl', 'no', 'pt', 'sv']
CONTINUE = {'ar': 'تابع إلى', 'da': 'Fortsæt til', 'de': 'Weiter zu', 'es': 'Continuar a', 'fi': 'Jatka sivulle',
            'it': 'Continua su', 'nl': 'Ga verder naar', 'no': 'Fortsett til', 'pt': 'Continuar para', 'sv': 'Fortsätt till'}
REDIRECT = re.compile(r'http-equiv="refresh"|location\.replace\(')
SKIP_DIRS = {'.git', '.audit', 'node_modules', 'scripts'} | set(LANGS)

created = 0
for p in sorted(pathlib.Path('.').rglob('*.html')):
    if SKIP_DIRS & set(p.parts) or p.name.startswith('google') or p.as_posix() == '404.html':
        continue
    s = p.read_text(encoding='utf-8', errors='replace')
    if REDIRECT.search(s[:6000]) and len(s) < 6000:
        continue  # English redirect page itself
    rel = p.as_posix()
    target = '/' + (rel[:-len('index.html')] if rel.endswith('index.html') else rel)
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    title = re.sub(r'\s+', ' ', t.group(1)).strip() if t else 'ExKnowledge'
    for lang in LANGS:
        out = pathlib.Path(lang) / rel
        if out.exists():
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        dir_attr = ' dir="rtl"' if lang == 'ar' else ''
        label = html.escape(re.sub(r'\s*\|\s*ExKnowledge$', '', html.unescape(title)))
        out.write_text(f'''<!doctype html>
<html lang="{lang}"{dir_attr}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex,follow">
  <meta http-equiv="refresh" content="0;url={target}">
  <link rel="canonical" href="https://exknowledge.com{target}">
  <title>{title}</title>
  <script>location.replace('{target}' + location.hash);</script>
</head>
<body>
  <p><a href="{target}">{CONTINUE[lang]} {label}</a></p>
</body>
</html>
''', encoding='utf-8')
        created += 1
print(f'redirect pages created: {created}')
