#!/usr/bin/env python3
"""
Translate missing ExKnowledge pages using DeepL, OpenAI, and Google Translate.
Splits ~15 pages per provider across 4 languages (it, fi, da, ar).
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from html.parser import HTMLParser

DEEPL_KEY = "61f41621-eeab-40c9-bd52-63574b94309b"
DEEPL_URL = "https://api.deepl.com"

# Load OpenAI key
with open(os.path.expanduser("~/.openclaw/.env")) as f:
    for line in f:
        if line.startswith("OPENAI_API_KEY="):
            OPENAI_KEY = line.strip().split("=", 1)[1]
            break

LANGS = {
    'it': {'deepl': 'IT', 'openai': 'Italian', 'google': 'it', 'html_lang': 'it'},
    'fi': {'deepl': 'FI', 'openai': 'Finnish', 'google': 'fi', 'html_lang': 'fi'},
    'da': {'deepl': 'DA', 'openai': 'Danish', 'google': 'da', 'html_lang': 'da'},
    'ar': {'deepl': 'AR', 'openai': 'Arabic', 'google': 'ar', 'html_lang': 'ar'},
}

MISSING_PAGES = [
    'atex-directive', 'atex-for-beginners', 'atex-vs-iecex',
    'cable-glands-hazardous-areas', 'compex-certification',
    'dust-explosion-protection', 'ex-equipment-selection-guide',
    'explosion-proof-vs-intrinsically-safe', 'hazardous-area-classification',
    'how-to-read-atex-nameplate', 'hydrogen-explosion-protection'
]

# Assign providers: ~15 each across 44 pages (11 pages × 4 langs)
# DeepL: it (all 11) + fi first 4 = 15
# OpenAI: fi remaining 7 + da first 8 = 15  
# Google: da remaining 3 + ar all 11 = 14
ASSIGNMENTS = {}
for page in MISSING_PAGES:
    ASSIGNMENTS[('it', page)] = 'deepl'
for page in MISSING_PAGES[:4]:
    ASSIGNMENTS[('fi', page)] = 'deepl'
for page in MISSING_PAGES[4:]:
    ASSIGNMENTS[('fi', page)] = 'openai'
for page in MISSING_PAGES[:8]:
    ASSIGNMENTS[('da', page)] = 'openai'
for page in MISSING_PAGES[8:]:
    ASSIGNMENTS[('da', page)] = 'google'
for page in MISSING_PAGES:
    ASSIGNMENTS[('ar', page)] = 'google'

def translate_deepl(text, target_lang_code):
    """Translate HTML using DeepL API (preserves HTML tags)."""
    result = subprocess.run(
        ['curl', '-s', '-X', 'POST', f'{DEEPL_URL}/v2/translate',
         '-H', f'Authorization: DeepL-Auth-Key {DEEPL_KEY}',
         '-d', f'text={urllib.parse.quote(text)}',
         '-d', f'target_lang={target_lang_code}',
         '-d', 'source_lang=EN',
         '-d', 'tag_handling=html',
         '-d', 'split_sentences=nonewlines'],
        capture_output=True, text=True, timeout=120
    )
    data = json.loads(result.stdout)
    if 'translations' in data:
        return data['translations'][0]['text']
    else:
        print(f"  DeepL error: {data}", file=sys.stderr)
        return None

def translate_openai(text, target_lang_name):
    """Translate HTML using OpenAI API."""
    # Split into chunks if too large (OpenAI has token limits)
    payload = {
        "model": "gpt-4.1-mini",
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": f"You are a professional translator. Translate the following HTML content from English to {target_lang_name}. Preserve ALL HTML tags, attributes, classes, IDs, and structure exactly. Only translate visible text content. Keep technical terms (ATEX, IECEx, Zone 1, Zone 2, IP68, Ex d, Ex e, Ex i, etc.) as-is. Keep code snippets and URLs unchanged. Output ONLY the translated HTML, nothing else."},
            {"role": "user", "content": text}
        ]
    }
    result = subprocess.run(
        ['curl', '-s', 'https://api.openai.com/v1/chat/completions',
         '-H', f'Authorization: Bearer {OPENAI_KEY}',
         '-H', 'Content-Type: application/json',
         '-d', json.dumps(payload)],
        capture_output=True, text=True, timeout=180
    )
    data = json.loads(result.stdout)
    if 'choices' in data:
        content = data['choices'][0]['message']['content']
        # Strip markdown code fences if present
        if content.startswith('```'):
            content = re.sub(r'^```(?:html)?\s*', '', content)
            content = re.sub(r'\s*```$', '', content)
        return content
    else:
        print(f"  OpenAI error: {data.get('error', data)}", file=sys.stderr)
        return None

def translate_google(text, target_lang_code):
    """Translate text using Google Translate free API. Handles HTML by splitting into chunks."""
    # Google free API has size limits, split by paragraphs
    # For HTML, we'll translate the full page in chunks of ~4000 chars
    chunks = []
    current = ""
    for line in text.split('\n'):
        if len(current) + len(line) > 4000:
            chunks.append(current)
            current = line
        else:
            current += '\n' + line if current else line
    if current:
        chunks.append(current)
    
    translated_chunks = []
    for chunk in chunks:
        encoded = urllib.parse.quote(chunk)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang_code}&dt=t&q={encoded}"
        result = subprocess.run(
            ['curl', '-s', url],
            capture_output=True, text=True, timeout=30
        )
        try:
            data = json.loads(result.stdout)
            translated = ''.join(part[0] for part in data[0] if part[0])
            translated_chunks.append(translated)
        except (json.JSONDecodeError, IndexError, TypeError) as e:
            print(f"  Google error: {e}", file=sys.stderr)
            translated_chunks.append(chunk)  # Keep original on error
        time.sleep(0.5)  # Rate limit
    
    return '\n'.join(translated_chunks)

def adapt_html_for_lang(html, lang_code, page_name):
    """Update HTML metadata for the target language."""
    # Update html lang attribute
    html = re.sub(r'<html lang="en">', f'<html lang="{lang_code}">', html)
    
    # Update canonical URL
    html = re.sub(
        r'<link rel="canonical" href="https://exknowledge.com/pages/',
        f'<link rel="canonical" href="https://exknowledge.com/{lang_code}/pages/',
        html
    )
    
    # Update og:url
    html = re.sub(
        r'content="https://exknowledge.com/pages/',
        f'content="https://exknowledge.com/{lang_code}/pages/',
        html
    )
    
    # Fix relative paths (css, js, images, fonts)
    html = html.replace('href="../css/', 'href="../../css/')
    html = html.replace('src="../js/', 'src="../../js/')
    html = html.replace('src="../images/', 'src="../../images/')
    html = html.replace('href="../fonts/', 'href="../../fonts/')
    # Nav links: ../pages/ → ./  and ../ → ../
    html = html.replace('href="../pages/', 'href="./')
    html = html.replace('href="../index.html', 'href="../index.html')
    html = html.replace('href="../blog/', 'href="../../blog/')
    html = html.replace('href="../glossary/', 'href="../../glossary/')
    html = html.replace('href="../podcast/', 'href="../../podcast/')
    
    return html

def main():
    total = len(ASSIGNMENTS)
    done = 0
    providers_count = {'deepl': 0, 'openai': 0, 'google': 0}
    
    print(f"Translating {total} pages across 4 languages")
    print(f"Providers: DeepL ~15, OpenAI ~15, Google ~14")
    print()
    
    for (lang, page), provider in sorted(ASSIGNMENTS.items()):
        done += 1
        en_path = f"pages/{page}.html"
        out_dir = f"{lang}/pages"
        out_path = f"{out_dir}/{page}.html"
        
        if not os.path.exists(en_path):
            print(f"  ❌ EN source missing: {en_path}")
            continue
        
        if os.path.exists(out_path):
            print(f"  ⏭️  Already exists: {out_path}")
            continue
        
        os.makedirs(out_dir, exist_ok=True)
        
        with open(en_path, 'r') as f:
            en_html = f.read()
        
        lang_config = LANGS[lang]
        print(f"[{done}/{total}] {lang}/{page} via {provider}...", end=" ", flush=True)
        
        if provider == 'deepl':
            translated = translate_deepl(en_html, lang_config['deepl'])
        elif provider == 'openai':
            translated = translate_openai(en_html, lang_config['openai'])
        elif provider == 'google':
            translated = translate_google(en_html, lang_config['google'])
        
        if translated:
            # Adapt HTML metadata
            translated = adapt_html_for_lang(translated, lang, page)
            
            with open(out_path, 'w') as f:
                f.write(translated)
            
            providers_count[provider] += 1
            size = len(translated)
            print(f"✅ ({size:,} bytes)")
        else:
            print(f"❌ Translation failed")
        
        # Small delay between requests
        time.sleep(0.3)
    
    print(f"\n✅ Done! {sum(providers_count.values())}/{total} pages translated")
    print(f"   DeepL: {providers_count['deepl']}, OpenAI: {providers_count['openai']}, Google: {providers_count['google']}")

if __name__ == "__main__":
    main()
