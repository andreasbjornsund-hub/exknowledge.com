#!/usr/bin/env python3
"""HAG network link policy (approved by Andreas 2026-09-30). Idempotent; run after any chrome/nav rebuild.

  python3 scripts/hag_link_policy.py <site-host> [--dry-run]      (from the repo root)

1. Links to xshielder.com: rel gets "sponsored" (+ noopener when target=_blank) and UTM tags
   utm_source=<site>&utm_medium=referral&utm_campaign=hag_network&utm_content=<page or footer>.
2. Links to competitors (COMPETITORS below, incl. subdomains): rel gets "nofollow".
3. Links to the other network sites inside <header>/<nav>/<footer>: removed (with an <li> that only wraps them).
   Links between network sites inside the page text are left as they are (followed).
   On hazardousareaguide.com (the network hub) chrome links are kept but marked nofollow.
4. Footer block (between hag-sponsor markers, replaced on every run): "This site's main sponsor is Xshielder.
   Want to sponsor this site? Contact us." + "Part of the Hazardous Area Guide network." in the page language.
5. Click tracking: <script src="<asset dir>/hag-links.js?v=<hash>" defer> before </body> (marker-guarded).
"""
import hashlib
import html
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

NETWORK = ["exknowledge.com", "explosionproofradios.com", "explosionprooftablets.com", "hazardousareaguide.com",
           "intrinsicallysafeheadsets.com", "intrinsicallysafephones.com"]
HUB = "hazardousareaguide.com"
# Xshielder competitors: makers and sellers of hazardous-area phones, tablets, cameras and enclosures.
# Not listed on purpose: Xshielder partners (Exloc, Mobexx, Atea ...), standards bodies, general Ex equipment makers.
COMPETITORS = ["xciel.com", "atexxo.com", "ecom-ex.com", "pepperl-fuchs.com", "isafe-mobile.com", "bartec.com",
               "bartec.de", "aegex.com", "conquest-ex.com", "getac.com", "zebra.com", "pixavi.com", "atex-shop.de",
               "atexshop.com", "intrinsicallysafestore.com", "sonimtech.com", "cyrus.com", "cyrus-technology.de",
               "smart-ex.com", "tabex.com", "ruggedexphones.com"]
CONTACT = {"exknowledge.com": "/about.html", "intrinsicallysafeheadsets.com": "https://hazardousareaguide.com/#contact"}
ASSET_DIR = {"exknowledge.com": "js"}
T = {  # {X} = Xshielder link, {C} = contact link, {N} = network name (linked or plain)
    "en": ("This site's main sponsor is {X}.", "Want to sponsor this site? {C}.", "Contact us", "Part of the {N} network."),
    "de": ("Hauptsponsor dieser Website ist {X}.", "Möchten Sie diese Website sponsern? {C}.", "Kontaktieren Sie uns", "Teil des {N}-Netzwerks."),
    "nl": ("De hoofdsponsor van deze website is {X}.", "Wilt u deze website sponsoren? {C}.", "Neem contact met ons op", "Onderdeel van het {N}-netwerk."),
    "es": ("El patrocinador principal de este sitio es {X}.", "¿Quiere patrocinar este sitio? {C}.", "Contáctenos", "Parte de la red {N}."),
    "pt": ("O principal patrocinador deste site é a {X}.", "Quer patrocinar este site? {C}.", "Fale conosco", "Parte da rede {N}."),
    "no": ("Hovedsponsor for dette nettstedet er {X}.", "Vil du sponse nettstedet? {C}.", "Kontakt oss", "En del av {N}-nettverket."),
    "sv": ("Huvudsponsor för den här webbplatsen är {X}.", "Vill du sponsra webbplatsen? {C}.", "Kontakta oss", "En del av nätverket {N}."),
    "da": ("Hovedsponsor for dette website er {X}.", "Vil du sponsorere sitet? {C}.", "Kontakt os", "En del af {N}-netværket."),
    "fi": ("Tämän sivuston pääsponsori on {X}.", "Haluatko sponsoroida sivustoa? {C}.", "Ota yhteyttä", "Osa {N} -verkostoa."),
    "it": ("Lo sponsor principale di questo sito è {X}.", "Vuoi sponsorizzare questo sito? {C}.", "Contattaci", "Parte della rete {N}."),
    "ar": ("الراعي الرئيسي لهذا الموقع هو {X}.", "هل ترغب في رعاية هذا الموقع؟ {C}.", "تواصل معنا", "جزء من شبكة {N}."),
}

# In-text sponsored callouts (HAG test 3 pages where a link fits and none exists). Facts: tablets-steps/FACTS.md
# (iPad Pro 11 is ATEX Zone 1/21 only, no IECEx); iPhone 17 Pro Max is ATEX + IECEx Zone 1.
CALLOUTS = {
    "explosionprooftablets.com": {p: "ipad" for p in [
        "index.html", "nl/index.html", "de/index.html", "es/index.html", "pt-br/index.html",
        "best-atex-tablets-2026.html", "de/best-atex-tablets-2026.html", "zone-1-vs-zone-2-tablets.html",
        "de/zone-1-vs-zone-2-tablets.html", "nl/zone-1-vs-zone-2-tablets.html",
        "what-is-an-intrinsically-safe-tablet.html", "de/what-is-an-intrinsically-safe-tablet.html"]},
    "intrinsicallysafephones.com": {"nl/index.html": "iphone", "de/index.html": "iphone"},
}
PRODUCT_URL = {"ipad": {"en": "https://xshielder.com/products/atex-ipad", "de": "https://xshielder.com/de/products/atex-ipad",
                        "es": "https://xshielder.com/es/products/atex-ipad"},
               "iphone": {"en": "https://xshielder.com/products/smartphones/intrinsically-safe-smartphone",
                          "de": "https://xshielder.com/de/products/smartphones/intrinsically-safe-smartphone",
                          "es": "https://xshielder.com/es/products/smartphones/intrinsically-safe-smartphone"}}
CALLOUT_TEXT = {  # (label, product sentence, link text)
    "ipad": {"en": ("Sponsored", "Xshielder iPad Pro 11: an ATEX Zone 1/21 certified case for the Apple iPad Pro 11″.", "See the product"),
             "de": ("Gesponsert", "Xshielder iPad Pro 11: ein ATEX-zertifiziertes Gehäuse für Zone 1/21 für das Apple iPad Pro 11″.", "Zum Produkt"),
             "nl": ("Gesponsord", "Xshielder iPad Pro 11: een ATEX Zone 1/21-gecertificeerde behuizing voor de Apple iPad Pro 11″.", "Bekijk het product"),
             "es": ("Patrocinado", "Xshielder iPad Pro 11: una carcasa con certificación ATEX Zona 1/21 para el Apple iPad Pro 11″.", "Ver el producto"),
             "pt": ("Patrocinado", "Xshielder iPad Pro 11: uma capa com certificação ATEX Zona 1/21 para o Apple iPad Pro 11″.", "Ver o produto")},
    "iphone": {"en": ("Sponsored", "Xshielder iPhone 17 Pro Max: an iPhone in a case certified for ATEX and IECEx Zone 1.", "See the product"),
               "de": ("Gesponsert", "Xshielder iPhone 17 Pro Max: ein iPhone in einem ATEX- und IECEx-zertifizierten Gehäuse für Zone 1.", "Zum Produkt"),
               "nl": ("Gesponsord", "Xshielder iPhone 17 Pro Max: een iPhone in een ATEX- en IECEx-gecertificeerde behuizing voor Zone 1.", "Bekijk het product")},
}
C_START, C_END = "<!-- hag-callout:start -->", "<!-- hag-callout:end -->"
A_RE = re.compile(r"<a\b[^>]*>.*?</a>", re.I | re.S)
OPEN_RE = re.compile(r"<a\b[^>]*>", re.I | re.S)
START, END = "<!-- hag-sponsor:start -->", "<!-- hag-sponsor:end -->"
SCRIPT_MARK = "<!-- hag-links -->"


def host_of(href):
    h = urlparse(href).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def matches(host, domains):
    return any(host == d or host.endswith("." + d) for d in domains)


def get_attr(tag, name):
    m = re.search(rf'\b{name}\s*=\s*"([^"]*)"', tag, re.I) or re.search(rf"\b{name}\s*=\s*'([^']*)'", tag, re.I)
    return m.group(1) if m else None


def set_attr(tag, name, value):
    if get_attr(tag, name) is not None:
        return re.sub(rf'\b{name}\s*=\s*("[^"]*"|\'[^\']*\')', f'{name}="{value}"', tag, count=1, flags=re.I)
    return re.sub(r"^<a\b", f'<a {name}="{value}"', tag, count=1, flags=re.I)


def add_rel(tag, *tokens):
    rel = (get_attr(tag, "rel") or "").split()
    if (get_attr(tag, "target") or "").lower() == "_blank":
        tokens = tokens + ("noopener",)
    for t in tokens:
        if t not in rel:
            rel.append(t)
    return set_attr(tag, "rel", " ".join(rel))


def utm(href, site, content):
    u = urlparse(html.unescape(href))
    q = dict(parse_qsl(u.query, keep_blank_values=True))
    if "utm_source" in q:
        return href
    q.update({"utm_source": site, "utm_medium": "referral", "utm_campaign": "hag_network", "utm_content": content})
    return html.escape(urlunparse(u._replace(query=urlencode(q))), quote=True)


def chrome_spans(doc):
    spans = []
    for tag in ("header", "nav", "footer"):
        for m in re.finditer(rf"<{tag}\b.*?</{tag}>", doc, re.I | re.S):
            spans.append((m.start(), m.end()))
    return spans


def page_lang(doc, rel_path):
    m = re.match(r"(de|es|fr|it|nl|no|nb|sv|da|fi|pl|pt|pt-br|ar)/", rel_path)
    code = m.group(1) if m else ((re.search(r'<html[^>]*\blang="([^"]+)"', doc, re.I) or [None, "en"])[1]).lower()
    code = {"nb": "no", "pt-br": "pt"}.get(code, code[:2])
    return code if code in T else "en"


def contact_href(site, doc, lang, rel_path, root):
    if site in CONTACT:
        c = CONTACT[site]
        if c.startswith("/") and lang != "en":
            m = re.match(r"([a-z]{2}(?:-[a-z]{2})?)/", rel_path)
            if m and (root / m.group(1) / c.lstrip("/")).exists():
                return f"/{m.group(1)}{c}"
        return c
    m = re.search(r'href="([^"]*#(?:contact|kontakt|contacto|contato|kontakta)[^"]*)"', doc, re.I)
    return m.group(1) if m else "/#contact"


def process(doc, site, rel_path, root, asset_url):
    doc = re.sub(re.escape(START) + r".*?" + re.escape(END), "", doc, flags=re.S)  # re-insert fresh every run
    doc = re.sub(re.escape(C_START) + r".*?" + re.escape(C_END), "", doc, flags=re.S)
    slug = re.sub(r"(index)?\.html$", "", rel_path).strip("/") or "home"
    spans = chrome_spans(doc)
    in_chrome = lambda pos: any(s <= pos < e for s, e in spans)
    out, last, changes = [], 0, {"xshielder": 0, "competitor": 0, "network_removed": 0, "network_nofollow": 0}
    for m in A_RE.finditer(doc):
        full = m.group(0)
        tag = OPEN_RE.match(full).group(0)
        href = get_attr(tag, "href") or ""
        host = host_of(href) if href.startswith(("http://", "https://", "//")) else ""
        new = full
        if host.endswith("xshielder.com"):
            t2 = add_rel(set_attr(tag, "href", utm(href, site, "footer" if in_chrome(m.start()) else slug)), "sponsored")
            new = t2 + full[len(tag):]
            changes["xshielder"] += new != full
        elif matches(host, COMPETITORS):
            new = add_rel(tag, "nofollow") + full[len(tag):]
            changes["competitor"] += new != full
        elif host in NETWORK and host != site and in_chrome(m.start()):
            if site == HUB:
                new = add_rel(tag, "nofollow") + full[len(tag):]
                changes["network_nofollow"] += new != full
            else:
                new = ""
                changes["network_removed"] += 1
        out.append(doc[last:m.start()])
        out.append(new)
        last = m.end()
    out.append(doc[last:])
    doc = "".join(out)
    doc = re.sub(r"<li\b[^>]*>\s*</li>", "", doc)  # list items emptied by removed links

    lang = page_lang(doc, rel_path)
    product = CALLOUTS.get(site, {}).get(rel_path)
    spans = chrome_spans(doc)
    has_text_link = any(not any(s <= m.start() < e for s, e in spans) and "xshielder.com" in m.group(0)
                        for m in OPEN_RE.finditer(doc))
    if product and not has_text_link and product in CALLOUT_TEXT and lang in CALLOUT_TEXT[product]:
        label, sentence, cta = CALLOUT_TEXT[product][lang]
        href = utm(PRODUCT_URL[product].get(lang, PRODUCT_URL[product]["en"]), site, slug + "_callout")
        box = (f'{C_START}<aside class="hag-callout" style="margin:18px 0;padding:12px 16px;border:1px solid '
               f'rgba(127,127,127,.35);border-radius:8px;font-size:14px;line-height:1.55">'
               f'<span style="font-size:11px;letter-spacing:.06em;text-transform:uppercase;opacity:.7;margin-right:8px">'
               f'{label}</span>{sentence} <a href="{href}" rel="sponsored noopener" target="_blank" '
               f'style="text-decoration:underline">{cta}</a></aside>{C_END}')
        h1 = doc.lower().find("</h1>")
        h2 = doc.lower().find("<h2", h1) if h1 != -1 else -1
        if h2 != -1:
            doc = doc[:h2] + box + doc[h2:]
            changes["callout"] = 1
    s1, s2, cl, net = T[lang]
    x = (f'<a href="{utm("https://xshielder.com/", site, "footer_sponsor")}" rel="sponsored noopener" '
         f'target="_blank" style="color:inherit;text-decoration:underline">Xshielder</a>')
    c = f'<a href="{contact_href(site, doc, lang, rel_path, root)}" style="color:inherit;text-decoration:underline">{cl}</a>'
    n = ("Hazardous Area Guide" if site == HUB else
         '<a href="https://hazardousareaguide.com/" rel="nofollow" style="color:inherit;text-decoration:underline">'
         'Hazardous Area Guide</a>')
    block = (f'{START}<div class="hag-sponsor" style="font-size:13px;line-height:1.6;opacity:.85;margin:14px auto 0;'
             f'padding:0 16px 18px;max-width:1200px;text-align:center">'
             f'{s1.format(X=x)} {s2.format(C=c)} {net.format(N=n)}</div>{END}')
    i = doc.lower().rfind("</footer>")
    if i != -1:
        doc = doc[:i] + block + doc[i:]
    if asset_url:
        doc = re.sub(re.escape(SCRIPT_MARK) + r"<script[^>]*></script>", "", doc)
        j = doc.lower().rfind("</body>")
        if j != -1:
            doc = doc[:j] + f'{SCRIPT_MARK}<script src="{asset_url}" defer></script>' + doc[j:]
    return doc, changes


def main():
    site = sys.argv[1]
    dry = "--dry-run" in sys.argv
    root = Path.cwd()
    adir = ASSET_DIR.get(site, "assets")
    js_src = Path(__file__).with_name("hag-links.js").read_text()
    (root / adir).mkdir(exist_ok=True)
    if not dry:
        (root / adir / "hag-links.js").write_text(js_src)
    asset_url = f"/{adir}/hag-links.js?v={hashlib.sha1(js_src.encode()).hexdigest()[:10]}"
    total = {"files": 0, "xshielder": 0, "competitor": 0, "network_removed": 0, "network_nofollow": 0, "callout": 0}
    for f in sorted(root.rglob("*.html")):
        rel = f.relative_to(root).as_posix()
        if rel.startswith((".git/", "node_modules/")):
            continue
        doc = f.read_text(encoding="utf-8")
        if "<body" not in doc.lower():
            continue  # verification stubs
        new, ch = process(doc, site, rel, root, asset_url)
        if new != doc:
            total["files"] += 1
            for k, v in ch.items():
                total[k] += v
            if not dry:
                f.write_text(new, encoding="utf-8")
    print(site, total)


if __name__ == "__main__":
    main()
