#!/usr/bin/env python3
"""Translate ExKnowledge pages using DeepL API Free."""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse

API_KEY = "7e1c1cd6-8779-4b3e-9813-a2e482e7e5f1:fx"
API_URL = "https://api-free.deepl.com/v2/translate"
SITE_DIR = "/tmp/exknowledge"

# Language code mapping (our dirs → DeepL target codes)
LANG_MAP = {
    "de": "DE",
    "no": "NB",  # Norwegian Bokmål
    "es": "ES",
    "nl": "NL",
    "sv": "SV",
    "da": "DA",
    "fi": "FI",
    "pt": "PT-PT",
    "it": "IT",
    "ar": "AR",
}

# HTML lang attribute values
HTML_LANG = {
    "de": "de",
    "no": "nb",
    "es": "es",
    "nl": "nl",
    "sv": "sv",
    "da": "da",
    "fi": "fi",
    "pt": "pt",
    "it": "it",
    "ar": "ar",
}

# "Sources & References" heading translations
REF_HEADINGS = {
    "de": "Quellen &amp; Referenzen",
    "no": "Kilder og referanser",
    "es": "Fuentes y referencias",
    "nl": "Bronnen &amp; referenties",
    "sv": "Källor och referenser",
    "da": "Kilder og referencer",
    "fi": "Lähteet ja viitteet",
    "pt": "Fontes e referências",
    "it": "Fonti e riferimenti",
    "ar": "المصادر والمراجع",
}


def check_usage():
    req = urllib.request.Request(
        "https://api-free.deepl.com/v2/usage",
        headers={"Authorization": f"DeepL-Auth-Key {API_KEY}"},
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    used = data["character_count"]
    limit = data["character_limit"]
    print(f"DeepL usage: {used:,}/{limit:,} chars ({limit-used:,} remaining)")
    return used, limit


def translate_html(html_content, target_lang):
    """Translate HTML content via DeepL API."""
    data = urllib.parse.urlencode({
        "text": html_content,
        "source_lang": "EN",
        "target_lang": target_lang,
        "tag_handling": "html",
        "split_sentences": "nonewlines",
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Authorization": f"DeepL-Auth-Key {API_KEY}"},
    )
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    return result["translations"][0]["text"]


def fix_translated_page(html, lang, page_name, is_index=False):
    """Post-process translated HTML: fix lang attr, paths, meta."""
    # Fix html lang attribute
    html = re.sub(r'<html\s+lang="[^"]*"', f'<html lang="{HTML_LANG[lang]}"', html)

    # Fix canonical URL
    if is_index:
        html = re.sub(
            r'<link rel="canonical" href="[^"]*"',
            f'<link rel="canonical" href="https://exknowledge.com/{lang}/"',
            html,
        )
    else:
        html = re.sub(
            r'<link rel="canonical" href="[^"]*"',
            f'<link rel="canonical" href="https://exknowledge.com/{lang}/pages/{page_name}.html"',
            html,
        )

    # Fix CSS paths (ensure absolute)
    html = html.replace('href="../css/', 'href="/css/')
    html = html.replace("href='../css/", "href='/css/")

    # Fix JS paths
    html = html.replace('src="../js/', 'src="/js/')
    html = html.replace("src='../js/", "src='/js/")

    # Fix image paths
    html = html.replace('src="../images/', 'src="/images/')

    # Ensure references heading is in correct language (not re-translated)
    if lang in REF_HEADINGS:
        html = re.sub(
            r'<h2[^>]*>Sources\s*&amp;\s*References</h2>',
            f'<h2>{REF_HEADINGS[lang]}</h2>',
            html,
        )

    # Keep technical terms in English (ATEX, IECEx, Zone 1, etc. should survive DeepL mostly)
    
    return html


def translate_guides(lang):
    """Translate all 11 guide pages to a target language."""
    guides = [
        "atex-directive", "atex-for-beginners", "atex-vs-iecex",
        "cable-glands-hazardous-areas", "compex-certification",
        "dust-explosion-protection", "ex-equipment-selection-guide",
        "explosion-proof-vs-intrinsically-safe", "hazardous-area-classification",
        "how-to-read-atex-nameplate", "hydrogen-explosion-protection",
    ]

    target_dir = os.path.join(SITE_DIR, lang, "pages")
    os.makedirs(target_dir, exist_ok=True)

    deepl_lang = LANG_MAP[lang]
    total_chars = 0

    for i, guide in enumerate(guides):
        src = os.path.join(SITE_DIR, "pages", f"{guide}.html")
        dst = os.path.join(target_dir, f"{guide}.html")

        if not os.path.exists(src):
            print(f"  SKIP {guide} (source not found)")
            continue

        html = open(src, "r", encoding="utf-8").read()
        chars = len(html)
        total_chars += chars

        print(f"  [{i+1}/11] {guide} ({chars:,} chars)...", end=" ", flush=True)

        translated = translate_html(html, deepl_lang)
        translated = fix_translated_page(translated, lang, guide)

        with open(dst, "w", encoding="utf-8") as f:
            f.write(translated)

        print("✓")
        time.sleep(0.5)  # Be nice to the API

    return total_chars


def translate_index(lang):
    """Translate index.html to a target language."""
    src = os.path.join(SITE_DIR, "index.html")
    dst = os.path.join(SITE_DIR, lang, "index.html")

    html = open(src, "r", encoding="utf-8").read()
    chars = len(html)
    deepl_lang = LANG_MAP[lang]

    print(f"  index.html ({chars:,} chars)...", end=" ", flush=True)

    translated = translate_html(html, deepl_lang)
    translated = fix_translated_page(translated, lang, "index", is_index=True)

    with open(dst, "w", encoding="utf-8") as f:
        f.write(translated)

    print("✓")
    return chars


if __name__ == "__main__":
    print("=== DeepL ExKnowledge Translator ===\n")
    check_usage()
    print()

    tasks = sys.argv[1:]  # e.g. "de:guides" "no:index"
    if not tasks:
        print("Usage: python3 deepl_translate.py <lang>:<type> [...]")
        print("  Types: guides, index, all")
        print("  Example: python3 deepl_translate.py de:guides no:index")
        sys.exit(1)

    total = 0
    for task in tasks:
        lang, what = task.split(":")
        if lang not in LANG_MAP:
            print(f"Unknown language: {lang}")
            continue

        print(f"\n--- Translating {what} → {lang} ({LANG_MAP[lang]}) ---")

        if what in ("guides", "all"):
            total += translate_guides(lang)
        if what in ("index", "all"):
            total += translate_index(lang)

    print(f"\n=== Done! Total chars sent: ~{total:,} ===")
    print()
    check_usage()
