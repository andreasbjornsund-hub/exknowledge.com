#!/usr/bin/env python3
"""Rebuild canonical, og:url, hreflang and sitemap.xml for the whole site (see DESIGN.md).
Usage (from the repo root): python3 scripts/build_seo.py
- English topic titles rewritten to <= 60 chars; cut-off titles ("...") rebuilt from the page h1
- meta descriptions > 160 chars trimmed at a sentence or word boundary
- self canonical, og:url and JSON-LD page url on every indexable page
- reciprocal hreflang sets for every page family (only real, translated pages)
- untranslated translated blog posts: noindex + canonical to the English post
- unlaunched pages (events, webinars, buying report): noindex
- broken og:image on the gas-group blog post family
- missing description / og / canonical on standalone pages
- footer: free PDF guide + privacy links, accessible "report an error" link
- sitemap.xml regenerated from the real, indexable pages
"""
import re, pathlib, json, html, collections, datetime

ROOT = 'https://exknowledge.com'
LANGS = ['ar', 'da', 'de', 'es', 'fi', 'it', 'nl', 'no', 'pt', 'sv']
HREFLANG = {'no': 'nb'}
TODAY = datetime.date.today().isoformat()
# Pages marked noindex (e.g. translated posts that are still English inside) stay out of hreflang and the sitemap.
UNTRANSLATED = set()
NOINDEX_PAGES = {'events.html', 'webinars.html', 'buying-report.html', '404.html'}
REDIRECT = re.compile(r'http-equiv="refresh"|location\.replace\(')
st = collections.Counter()

TITLES = {  # hand-written English titles (<= 60 chars)
 'pages/fundamentals.html': 'Explosion Protection Fundamentals: Fire Triangle, LEL, UEL',
 'pages/zone-classification.html': 'ATEX Zone Classification: Zones 0, 1, 2, 20, 21 and 22',
 'pages/gas-groups.html': 'Gas Groups IIA, IIB, IIC Explained: MESG and MIC',
 'pages/temperature-classes.html': 'Temperature Classes T1 to T6: Which T-Class Do You Need?',
 'pages/protection-methods.html': 'Ex Protection Methods: Ex d, Ex e, Ex i, Ex p, Ex n, Ex m',
 'pages/standards.html': 'Explosion Protection Standards: IEC 60079, ATEX, NEC 505',
 'pages/certification.html': 'ATEX and IECEx Certification: Notified Bodies and Tests',
 'pages/installation-inspection.html': 'Ex Installation and Inspection: IEC 60079-14 and -17',
 'pages/atex-equipment-categories.html': 'ATEX Equipment Categories 1, 2 and 3 Explained',
 'pages/compex-certification.html': 'CompEx Certification: Modules and Training Guide (2026)',
 'pages/nec-500-vs-atex-iec.html': 'NEC 500 and 505 vs ATEX/IEC: Comparison Guide',
 'pages/faq.html': 'ATEX and IECEx FAQ: Explosion Protection Questions',
 'pages/nr10-inmetro-brazil.html': 'NR-10 and INMETRO: Brazil Ex Certification (2026)',
 'pages/dsear-regulations-uk.html': 'DSEAR Regulations: UK Explosive Atmospheres Guide',
 'pages/atex-for-beginners.html': 'ATEX for Beginners: A Plain-Language Introduction',
 'pages/how-to-read-atex-nameplate.html': 'How to Read an ATEX Nameplate: Complete Decoding Guide',
 'pages/explosion-proof-vs-intrinsically-safe.html': 'Explosion Proof vs Intrinsically Safe: Full Comparison',
 'pages/dust-explosion-protection.html': 'Dust Explosion Protection: Zones, Prevention, Equipment',
 'pages/cable-glands-hazardous-areas.html': 'Cable Glands for Hazardous Areas: Ex d, Ex e, Barrier',
 'pages/hydrogen-explosion-protection.html': 'Hydrogen Explosion Protection: IIC Equipment and Safety',
 'pages/ex-equipment-selection-guide.html': 'Ex Equipment Selection Guide: Choosing the Right Method',
}
FOOT = {
 'en': ('Free PDF guide', 'Privacy'), 'de': ('Kostenloser PDF-Leitfaden', 'Datenschutz'), 'no': ('Gratis PDF-guide', 'Personvern'),
 'da': ('Gratis PDF-guide', 'Privatliv'), 'sv': ('Gratis PDF-guide', 'Integritet'), 'fi': ('Ilmainen PDF-opas', 'Tietosuoja'),
 'es': ('Guía PDF gratuita', 'Privacidad'), 'nl': ('Gratis PDF-gids', 'Privacy'), 'pt': ('Guia PDF gratuito', 'Privacidade'),
 'it': ('Guida PDF gratuita', 'Privacy'), 'ar': ('دليل PDF مجاني', 'الخصوصية'),
}
STANDALONE_META = {
 'interactives/zone-classification.html': 'Click through a fuel terminal schematic to see how each area is classified into gas and dust zones under IEC 60079-10-1 and -10-2.',
 'exscanner/index.html': 'Upload an ATEX or IECEx certificate PDF and read out the Ex marking, protection types, gas group, temperature class and EPL in seconds.',
 'about.html': None, 'api-docs.html': None, 'events.html': None, 'webinars.html': None,
}

def url_of(rel):
    if rel.endswith('index.html'):
        rel = rel[:-len('index.html')]
    return f'{ROOT}/{rel}'

def lang_of(rel):
    first = rel.split('/')[0]
    return first if first in LANGS else 'en'

def key_of(rel):
    l = lang_of(rel)
    return rel[len(l) + 1:] if l != 'en' else rel

def trim_desc(d, limit=160):
    if len(d) <= limit:
        return d
    cut = d[:limit]
    m = max(cut.rfind('. '), cut.rfind('! '), cut.rfind('? '))
    if m >= 70:
        return cut[:m + 1]
    w = cut.rsplit(' ', 1)[0].rstrip(',;:–-')
    return w + '.'

def meta(s, prop, attr='property'):
    m = re.search(rf'<meta {attr}="{re.escape(prop)}" content="([^"]*)"', s)
    return m.group(1) if m else None

def set_or_add(s, tag_re, new_tag, anchor_re=r'</title>'):
    if re.search(tag_re, s):
        return re.sub(tag_re, new_tag.replace('\\', '\\\\'), s, count=1)
    a = re.search(anchor_re, s)
    return s[:a.end()] + '\n  ' + new_tag + s[a.end():]

# ---------- collect pages ----------
pages = {}
for p in sorted(pathlib.Path('.').rglob('*.html')):
    if '.git' in p.parts or '.audit' in p.parts or p.name.startswith('google'):
        continue
    s = p.read_text(encoding='utf-8')
    if REDIRECT.search(s[:6000]) and len(s) < 6000:
        continue
    pages[p.as_posix()] = s

def indexable(rel, s):
    if rel in UNTRANSLATED or pathlib.Path(rel).name in NOINDEX_PAGES and lang_of(rel) == 'en':
        return False
    if key_of(rel) in NOINDEX_PAGES:
        return False
    if re.search(r'<meta name="robots" content="[^"]*noindex', s):
        return False
    return True

families = collections.defaultdict(dict)
for rel, s in pages.items():
    if indexable(rel, s):
        families[key_of(rel)][lang_of(rel)] = rel

for rel, s in list(pages.items()):
    o = s
    lang = lang_of(rel)
    key = key_of(rel)

    # ---- titles ----
    if rel in TITLES:
        s = re.sub(r'<title>.*?</title>', f'<title>{TITLES[rel]}</title>', s, count=1, flags=re.S); st['title rewritten'] += 1
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    if t:
        title = t.group(1).strip()
        if title.endswith('...') or title.endswith('…'):
            h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
            if h1:
                new = re.sub(r'<[^>]+>', ' ', h1.group(1)); new = re.sub(r'\s+', ' ', new).strip()
                if len(new) + 14 <= 60:
                    new += ' | ExKnowledge'
                s = s.replace(t.group(0), f'<title>{new}</title>', 1); title = new; st['cut-off title fixed'] += 1
                for prop in ('og:title',):
                    if (meta(s, prop) or '').endswith(('...', '…')):
                        s = re.sub(rf'(<meta property="{prop}" content=")[^"]*(")', rf'\g<1>{new}\2', s, count=1)
                if (meta(s, 'twitter:title', 'name') or '').endswith(('...', '…')):
                    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', rf'\g<1>{new}\2', s, count=1)
        if len(title) > 60 and title.endswith(' | ExKnowledge'):
            s = s.replace(f'<title>{title}</title>', f'<title>{title[:-len(" | ExKnowledge")]}</title>', 1); st['brand suffix dropped'] += 1

    # ---- description ----
    d = meta(s, 'description', 'name')
    if d and len(html.unescape(d)) > 160:
        nd = html.escape(trim_desc(html.unescape(d)), quote=True)
        s = s.replace(f'<meta name="description" content="{d}"', f'<meta name="description" content="{nd}"', 1); st['description trimmed'] += 1
    if d is None and rel in STANDALONE_META and STANDALONE_META[rel]:
        s = set_or_add(s, r'<meta name="description"[^>]*>', f'<meta name="description" content="{STANDALONE_META[rel]}">'); st['description added'] += 1

    idx = indexable(rel, s)
    self_url = url_of(rel)

    # ---- robots / canonical ----
    if rel in UNTRANSLATED:
        en_rel = key
        s = set_or_add(s, r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{url_of(en_rel)}">')
        if 'name="robots"' not in s:
            s = s.replace('</title>', '</title>\n  <meta name="robots" content="noindex, follow">', 1)
        st['untranslated blog hidden'] += 1
    elif key in NOINDEX_PAGES and rel != '404.html':
        if 'name="robots"' not in s:
            s = s.replace('</title>', '</title>\n  <meta name="robots" content="noindex, follow">', 1); st['unlaunched noindex'] += 1
    if idx:
        s = set_or_add(s, r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{self_url}">')
        # og tags
        if meta(s, 'og:url') is not None:
            s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{self_url}">', s, count=1)
        else:
            tt = re.search(r'<title>(.*?)</title>', s, re.S)
            dd = meta(s, 'description', 'name') or ''
            add = (f'<meta property="og:title" content="{tt.group(1).strip() if tt else "ExKnowledge"}">\n  '
                   f'<meta property="og:description" content="{dd}">\n  '
                   f'<meta property="og:url" content="{self_url}">\n  <meta property="og:type" content="website">\n  '
                   f'<meta property="og:image" content="{ROOT}/images/og-default.png">')
            s = set_or_add(s, r'<meta property="og:url"[^>]*>', add, anchor_re=r'<link rel="canonical"[^>]*>'); st['og added'] += 1
        # JSON-LD page url on translated pages pointed at the English page
        if lang != 'en':
            s = s.replace(f'"url": "{url_of(key)}"', f'"url": "{self_url}"').replace(f'"url":"{url_of(key)}"', f'"url":"{self_url}"')

    # ---- broken og:image (two URLs glued together) ----
    s, k = re.subn(r'(content=")https://images\.unsplash\.com/[^"?]*\?w=1000(https://images\.unsplash\.com/[^"?]*\?w=1000&q=80)q=80"', r'\1\2"', s); st['og:image fixed'] += k

    # ---- hreflang ----
    s = re.sub(r'[ \t]*<!-- hreflang -->\n', '', s)
    s = re.sub(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*"\s*/?>\n?', '', s)
    fam = families.get(key, {})
    if idx and len(fam) > 1:
        order = ['en'] + [l for l in LANGS if l in fam]
        tags = [f'<link rel="alternate" hreflang="{HREFLANG.get(l, l)}" href="{url_of(fam[l])}">' for l in order if l in fam]
        if 'en' in fam:
            tags.append(f'<link rel="alternate" hreflang="x-default" href="{url_of(fam["en"])}">')
        block = '\n  '.join(tags)
        c = re.search(r'<link rel="canonical"[^>]*>', s)
        s = s[:c.end()] + '\n  ' + block + s[c.end():]
        st['hreflang sets'] += 1

    # ---- footer links ----
    pdf, priv = FOOT[lang]
    m = re.search(r'(<footer class="footer">.*?)(<a href="/about\.html"><i class="ph ph-info"></i>[^<]*</a>\n)', s, re.S)
    if m and '/privacy.html' not in s[m.start():]:
        ind = re.search(r'([ \t]*)<a href="/about\.html"><i class="ph ph-info"></i>', s[m.start(2) - 20:m.end(2)]).group(1)
        add = f'{ind}<a href="/ebook.html"><i class="ph ph-file-pdf"></i> {pdf}</a>\n{ind}<a href="/privacy.html"><i class="ph ph-shield-check"></i> {priv}</a>\n'
        s = s[:m.end(2)] + add + s[m.end(2):]; st['footer links'] += 1
    s = s.replace('<a href="/about.html#feedback" style="color:var(--accent);font-size:11px">', '<a href="/about.html#feedback" class="footer-report">')
    s = s.replace('<a href="/about.html#feedback" style="color:var(--accent)">', '<a href="/about.html#feedback" class="footer-report">')

    if s != o:
        pathlib.Path(rel).write_text(s, encoding='utf-8'); pages[rel] = s

# ---------- language menu on English/translated blog pages: skip hidden translations ----------
for rel, s in list(pages.items()):
    m = re.search(r'(<select class="lang-select"[^>]*>)(.*?)(</select>)', s, re.S)
    if not m:
        continue
    def fix(mo):
        v = mo.group(1)
        target = v.lstrip('/')
        if target.endswith('/'):
            target += 'index.html'
        if target in UNTRANSLATED:
            st['lang option redirected'] += 1
            return mo.group(0).replace(f'value="{v}"', f'value="/{target.split("/")[0]}/blog/"')
        return mo.group(0)
    opts = re.sub(r'<option value="([^"]*)"', fix, m.group(2))
    if opts != m.group(2):
        s = s[:m.start(2)] + opts + s[m.end(2):]
        pathlib.Path(rel).write_text(s, encoding='utf-8'); pages[rel] = s

# ---------- sitemap ----------
def prio(rel):
    if rel == 'index.html': return '1.0'
    if rel.endswith('index.html') and rel.count('/') == 1 and lang_of(rel) != 'en': return '0.9'
    if '/pages/' in '/' + rel: return '0.8'
    if '/blog/' in '/' + rel: return '0.7'
    return '0.6'
urls = []
for rel, s in sorted(pages.items()):
    if rel == '404.html' or not indexable(rel, s):
        continue
    urls.append(f'  <url>\n    <loc>{url_of(rel)}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{prio(rel)}</priority>\n  </url>')
xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + '\n'.join(urls) + '\n</urlset>\n')
pathlib.Path('sitemap.xml').write_text(xml, encoding='utf-8')
st['sitemap urls'] = len(urls)
print(dict(st))
