#!/usr/bin/env python3
"""Add a content-hash version (?v=xxxxxxxx) to every page's links to the shared CSS and JS.

Cloudflare serves /css and /js with a one-year browser cache, so without a version a returning
visitor keeps an old stylesheet or script after a deploy. Run this after changing any file in
css/ or js/ (it is idempotent and only rewrites links whose file content changed):

    python3 scripts/bust_cache.py
"""
import hashlib, os, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = {}
for d in ('css', 'js'):
    for f in (ROOT / d).glob('*.*'):
        if f.suffix in ('.css', '.js'):
            ASSETS[f.relative_to(ROOT).as_posix()] = hashlib.sha1(f.read_bytes()).hexdigest()[:8]

REF = re.compile(r'((?:href|src)=")([^"?#]*?(?:css|js)/[A-Za-z0-9_-]+\.(?:css|js))(\?v=[0-9a-f]+)?(")')

def main():
    changed = 0
    for page in ROOT.rglob('*.html'):
        if any(part in ('.git', '.audit', 'node_modules') for part in page.parts):
            continue
        s = page.read_text(encoding='utf-8')
        def repl(m):
            url = m.group(2)
            if url.startswith(('http:', 'https:', '//')):
                return m.group(0)
            target = (ROOT / url.lstrip('/')) if url.startswith('/') else (page.parent / url)
            rel = os.path.relpath(os.path.normpath(target), ROOT).replace(os.sep, '/')
            h = ASSETS.get(rel)
            return f'{m.group(1)}{url}?v={h}{m.group(4)}' if h else m.group(0)
        s2 = REF.sub(repl, s)
        if s2 != s:
            page.write_text(s2, encoding='utf-8')
            changed += 1
    print(f'pages updated: {changed}; assets: ' + ', '.join(f'{k}={v}' for k, v in sorted(ASSETS.items())))

if __name__ == '__main__':
    main()
