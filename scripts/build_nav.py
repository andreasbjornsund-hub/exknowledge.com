#!/usr/bin/env python3
"""Rebuild the site navigation on every page (see DESIGN.md).

One canonical, translated, accessible nav: real buttons for the menu and the
dropdown triggers, labels in the page's language, links to translated pages
when they exist. Also fixes the language selector's selected option, adds
dir="rtl" to Arabic pages, keeps consent-banner.js ahead of Google tags and
uses one favicon set. Safe to re-run; run it after translate-pages.py.

Usage (from the repo root): python3 scripts/build_nav.py
"""
import re, pathlib, html, collections

LANGS = ['de', 'no', 'da', 'sv', 'fi', 'es', 'nl', 'pt', 'it', 'ar']
L = {
 'en': dict(knowledge='Knowledge', resources='Resources', community='Community', about='About', menu='Menu',
   fundamentals='Fundamentals', zones='Zone Classification', protection='Protection Methods', standards='Standards &amp; Regulations',
   tclass='Temperature Classes', gas='Gas Groups', categories='Equipment Categories', quickref='Quick Reference', faq='FAQ',
   quiz='Quiz', survey='Survey', blog='Blog', podcast='Podcast', glossary='Glossary', training='Training',
   visual='Visualisations', certmap='Certification Map', partners='Partners', links='Industry Links'),
 'de': dict(knowledge='Wissen', resources='Ressourcen', community='Community', about='Über uns', menu='Menü',
   fundamentals='Grundlagen', zones='Zonenklassifizierung', protection='Zündschutzarten', standards='Normen &amp; Vorschriften',
   tclass='Temperaturklassen', gas='Gasgruppen', categories='Gerätekategorien', quickref='Kurzreferenz', faq='FAQ',
   quiz='Quiz', survey='Umfrage', blog='Blog', podcast='Podcast', glossary='Glossar', training='Schulung',
   visual='Visualisierungen', certmap='Zertifizierungskarte', partners='Partner', links='Branchenlinks'),
 'no': dict(knowledge='Kunnskap', resources='Ressurser', community='Fellesskap', about='Om oss', menu='Meny',
   fundamentals='Grunnleggende', zones='Soneklassifisering', protection='Beskyttelsesmetoder', standards='Standarder og forskrifter',
   tclass='Temperaturklasser', gas='Gassgrupper', categories='Utstyrskategorier', quickref='Hurtigreferanse', faq='Spørsmål og svar',
   quiz='Quiz', survey='Spørreundersøkelse', blog='Blogg', podcast='Podkast', glossary='Ordliste', training='Opplæring',
   visual='Visualiseringer', certmap='Sertifiseringskart', partners='Partnere', links='Bransjelenker'),
 'da': dict(knowledge='Viden', resources='Ressourcer', community='Fællesskab', about='Om os', menu='Menu',
   fundamentals='Grundlæggende', zones='Zoneklassificering', protection='Beskyttelsesmetoder', standards='Standarder og forskrifter',
   tclass='Temperaturklasser', gas='Gasgrupper', categories='Udstyrskategorier', quickref='Hurtig reference', faq='Ofte stillede spørgsmål',
   quiz='Quiz', survey='Undersøgelse', blog='Blog', podcast='Podcast', glossary='Ordliste', training='Kurser',
   visual='Visualiseringer', certmap='Certificeringskort', partners='Partnere', links='Branchelinks'),
 'sv': dict(knowledge='Kunskap', resources='Resurser', community='Gemenskap', about='Om oss', menu='Meny',
   fundamentals='Grunder', zones='Zonklassificering', protection='Skyddsmetoder', standards='Standarder och föreskrifter',
   tclass='Temperaturklasser', gas='Gasgrupper', categories='Utrustningskategorier', quickref='Snabbreferens', faq='Vanliga frågor',
   quiz='Quiz', survey='Enkät', blog='Blogg', podcast='Podd', glossary='Ordlista', training='Utbildning',
   visual='Visualiseringar', certmap='Certifieringskarta', partners='Partner', links='Branschlänkar'),
 'fi': dict(knowledge='Tietämys', resources='Resurssit', community='Yhteisö', about='Tietoa meistä', menu='Valikko',
   fundamentals='Perusteet', zones='Vyöhykeluokitus', protection='Suojausmenetelmät', standards='Standardit ja määräykset',
   tclass='Lämpötilaluokat', gas='Kaasuryhmät', categories='Laiteryhmät', quickref='Pikaopas', faq='Usein kysytyt kysymykset',
   quiz='Tietovisa', survey='Kysely', blog='Blogi', podcast='Podcast', glossary='Sanasto', training='Koulutus',
   visual='Visualisoinnit', certmap='Sertifiointikartta', partners='Kumppanit', links='Alan linkit'),
 'es': dict(knowledge='Conocimiento', resources='Recursos', community='Comunidad', about='Acerca de', menu='Menú',
   fundamentals='Fundamentos', zones='Clasificación de zonas', protection='Métodos de protección', standards='Normas y reglamentos',
   tclass='Clases de temperatura', gas='Grupos de gases', categories='Categorías de equipos', quickref='Referencia rápida', faq='Preguntas frecuentes',
   quiz='Cuestionario', survey='Encuesta', blog='Blog', podcast='Pódcast', glossary='Glosario', training='Formación',
   visual='Visualizaciones', certmap='Mapa de certificación', partners='Socios', links='Enlaces del sector'),
 'nl': dict(knowledge='Kennis', resources='Bronnen', community='Community', about='Over ons', menu='Menu',
   fundamentals='Basisprincipes', zones='Zone-indeling', protection='Beschermingsmethoden', standards='Normen en regelgeving',
   tclass='Temperatuurklassen', gas='Gasgroepen', categories='Apparatuurcategorieën', quickref='Snelle referentie', faq='Veelgestelde vragen',
   quiz='Quiz', survey='Enquête', blog='Blog', podcast='Podcast', glossary='Woordenlijst', training='Training',
   visual='Visualisaties', certmap='Certificeringskaart', partners='Partners', links='Branchelinks'),
 'pt': dict(knowledge='Conhecimento', resources='Recursos', community='Comunidade', about='Sobre', menu='Menu',
   fundamentals='Fundamentos', zones='Classificação de zonas', protection='Métodos de proteção', standards='Normas e regulamentos',
   tclass='Classes de temperatura', gas='Grupos de gases', categories='Categorias de equipamentos', quickref='Referência rápida', faq='Perguntas frequentes',
   quiz='Questionário', survey='Inquérito', blog='Blog', podcast='Podcast', glossary='Glossário', training='Formação',
   visual='Visualizações', certmap='Mapa de certificação', partners='Parceiros', links='Links do setor'),
 'it': dict(knowledge='Conoscenze', resources='Risorse', community='Comunità', about='Chi siamo', menu='Menu',
   fundamentals='Nozioni fondamentali', zones='Classificazione delle zone', protection='Metodi di protezione', standards='Norme e regolamenti',
   tclass='Classi di temperatura', gas='Gruppi di gas', categories='Categorie di apparecchiature', quickref='Riferimento rapido', faq='Domande frequenti',
   quiz='Quiz', survey='Sondaggio', blog='Blog', podcast='Podcast', glossary='Glossario', training='Formazione',
   visual='Visualizzazioni', certmap='Mappa delle certificazioni', partners='Partner', links='Link di settore'),
 'ar': dict(knowledge='المعرفة', resources='الموارد', community='المجتمع', about='من نحن', menu='القائمة',
   fundamentals='الأساسيات', zones='تصنيف المناطق', protection='طرق الحماية', standards='المعايير واللوائح',
   tclass='فئات درجات الحرارة', gas='مجموعات الغازات', categories='فئات المعدات', quickref='مرجع سريع', faq='الأسئلة الشائعة',
   quiz='اختبار', survey='استبيان', blog='المدونة', podcast='بودكاست', glossary='مسرد المصطلحات', training='التدريب',
   visual='تصورات مرئية', certmap='خريطة الشهادات', partners='الشركاء', links='روابط الصناعة'),
}

KNOW = [('fundamentals', 'pages/fundamentals.html', 'ph-fire'), ('zones', 'pages/zone-classification.html', 'ph-map-trifold'),
        ('protection', 'pages/protection-methods.html', 'ph-shield-check'), ('standards', 'pages/standards.html', 'ph-scales'),
        ('tclass', 'pages/temperature-classes.html', 'ph-thermometer-hot'), ('gas', 'pages/gas-groups.html', 'ph-flame'),
        ('categories', 'pages/atex-equipment-categories.html', 'ph-gear-six'), ('quickref', 'pages/cheat-sheet.html', 'ph-lightning'),
        ('faq', 'pages/faq.html', 'ph-question')]
RES = [('quiz', 'quiz.html', 'ph-exam'), ('survey', 'survey.html', 'ph-chart-bar'), ('blog', 'blog/', 'ph-newspaper'),
       ('podcast', 'podcast/', 'ph-microphone'), ('glossary', 'glossary/', 'ph-translate'), ('training', 'training.html', 'ph-chalkboard-teacher'),
       ('visual', 'visualisations.html', 'ph-eye'), ('certmap', 'certification-map.html', 'ph-globe-hemisphere-west')]
COM = [('partners', 'partners.html', 'ph-handshake'), ('links', 'links.html', 'ph-link')]

REDIRECT = re.compile(r'http-equiv="refresh"|location\.replace\(')

def real(path):
    p = pathlib.Path(path.rstrip('/') + ('/index.html' if path.endswith('/') else ''))
    if not p.exists():
        return False
    return not REDIRECT.search(p.read_text(encoding='utf-8', errors='replace')[:6000])

def href(lang, rel):
    if lang != 'en' and real(f'{lang}/{rel}'):
        return f'/{lang}/{rel}'
    return f'/{rel}'

def build_nav(lang, cur):
    t = L[lang]
    def items(lst):
        out = []
        for key, rel, icon in lst:
            h = href(lang, rel)
            is_cur = cur == h or (h.endswith('/') and cur == h + 'index.html')
            cur_attr = ' aria-current="page" class="active"' if is_cur else ''
            out.append(f'          <li><a href="{h}"{cur_attr}><i class="ph {icon}" aria-hidden="true"></i> {t[key]}</a></li>')
        return '\n'.join(out)
    def dd(label, icon, lst):
        return (f'      <li class="has-dropdown">\n'
                f'        <button type="button" class="dd-toggle" aria-expanded="false"><i class="ph {icon}" aria-hidden="true"></i> {label} <i class="ph ph-caret-down dd-arrow" aria-hidden="true"></i></button>\n'
                f'        <ul class="dropdown">\n{items(lst)}\n        </ul>\n      </li>')
    about_cur = ' aria-current="page" class="active"' if cur == '/about.html' else ''
    return ('<ul class="nav-links" id="site-nav">\n'
            + dd(t['knowledge'], 'ph-book-open-text', KNOW) + '\n'
            + dd(t['resources'], 'ph-folder-open', RES) + '\n'
            + dd(t['community'], 'ph-users-three', COM) + '\n'
            + f'      <li><a href="/about.html"{about_cur}><i class="ph ph-info" aria-hidden="true"></i> {t["about"]}</a></li>\n'
            + '    </ul>')

def ul_block(s, start):
    i = s.find('<ul', start); depth = 0; j = i
    while True:
        o = s.find('<ul', j + 1); c = s.find('</ul>', j + 1)
        if o != -1 and o < c:
            depth += 1; j = o
        else:
            if depth == 0:
                return i, c + 5
            depth -= 1; j = c

ICON_RE = re.compile(r'[ \t]*<link rel="(?:shortcut )?icon"[^>]*>\n?|[ \t]*<link rel="apple-touch-icon"[^>]*>\n?')
ICONS = ('  <link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
         '  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n'
         '  <link rel="apple-touch-icon" href="/apple-touch-icon.png">\n')
CONSENT = '<script src="https://hazardousareaguide.com/consent-banner.js"></script>'

stats = collections.Counter()
for p in sorted(pathlib.Path('.').rglob('*.html')):
    if '.git' in p.parts or '.audit' in p.parts or p.name.startswith('google'):
        continue
    rel = p.as_posix()
    s = o = p.read_text(encoding='utf-8')
    if REDIRECT.search(s[:6000]) and len(s) < 6000:
        continue  # redirect stubs
    lang = rel.split('/')[0] if rel.split('/')[0] in LANGS else 'en'
    cur = '/' + rel

    # html lang/dir
    if not re.search(r'<html\b', s):
        s = s.replace('<head>', f'<html lang="{lang}">\n<head>', 1); stats['html tag added'] += 1
    if lang == 'ar':
        s, k = re.subn(r'<html\b(?![^>]*\bdir=)([^>]*)>', r'<html\1 dir="rtl">', s, count=1); stats['ar dir'] += k

    # nav
    k = s.find('<ul class="nav-links"')
    if k != -1:
        a, b = ul_block(s, k)
        s = s[:a] + build_nav(lang, cur) + s[b:]
        stats['nav replaced'] += 1
    s, k = re.subn(r'<div class="burger"[^>]*>\s*<i class="ph-bold ph-list"></i>\s*</div>',
                   f'<button type="button" class="burger" aria-label="{L[lang]["menu"]}" aria-expanded="false" aria-controls="site-nav"><i class="ph-bold ph-list" aria-hidden="true"></i></button>', s)
    stats['burger'] += k

    # language select: correct "selected"
    m = re.search(r'(<select class="lang-select"[^>]*>)(.*?)(</select>)', s, re.S)
    if m:
        opts = m.group(2)
        opts = opts.replace(' selected>', '>')
        def is_mine(v):
            mm = re.match(r'/(ar|da|de|es|fi|it|nl|no|pt|sv)/', v)
            return (mm.group(1) if mm else 'en') == lang
        done = [False]
        def mark(mo):
            if not done[0] and is_mine(mo.group(1)):
                done[0] = True
                return f'<option value="{mo.group(1)}" selected>'
            return mo.group(0)
        opts = re.sub(r'<option value="([^"]*)">', mark, opts)
        s = s[:m.start(2)] + opts + s[m.end(2):]
        stats['lang select'] += 1

    # favicon set
    if '<head' in s and ('rel="icon"' in s or 'nav-links' in s):
        s = ICON_RE.sub('', s)
        if '<link rel="stylesheet"' in s:
            s = re.sub(r'[ \t]*(<link rel="stylesheet"[^>]*>)', lambda m: ICONS + '  ' + m.group(1), s, count=1)
        else:
            s = s.replace('</head>', ICONS + '</head>', 1)
        stats['favicons'] += 1

    # consent banner before any Google tag
    if CONSENT in s:
        first_g = min([i for i in (s.find('googletagmanager.com/gtm.js'), s.find('googletagmanager.com/gtag/js'), s.find("(function(w,d,s,l,i)")) if i != -1] or [-1])
        cpos = s.find(CONSENT)
        if first_g != -1 and cpos > first_g:
            s = s.replace(CONSENT + '\n', '', 1).replace(CONSENT, '', 1)
            # insert right after <head> opening + charset/viewport
            hm = re.search(r'<meta name="viewport"[^>]*>\n?', s) or re.search(r'<head[^>]*>\n?', s)
            s = s[:hm.end()] + '  ' + CONSENT + '\n' + s[hm.end():]
            stats['consent moved'] += 1

    # footer: drop links to unlaunched pages
    s, k = re.subn(r'[ \t]*<a href="/events\.html">[^\n]*?</a>\n', '', s); stats['footer events'] += k

    if s != o:
        p.write_text(s, encoding='utf-8')
print(dict(stats))
