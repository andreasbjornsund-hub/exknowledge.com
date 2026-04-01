#!/usr/bin/env python3
"""Translate remaining pages: IT+FI via DeepL, DA via OpenAI (chunked)."""

import json, os, re, subprocess, sys, time, urllib.parse

DEEPL_KEY = "61f41621-eeab-40c9-bd52-63574b94309b"

with open(os.path.expanduser("~/.openclaw/.env")) as f:
    for line in f:
        if line.startswith("OPENAI_API_KEY="):
            OPENAI_KEY = line.strip().split("=", 1)[1]
            break

PAGES = [
    'atex-directive', 'atex-for-beginners', 'atex-vs-iecex',
    'cable-glands-hazardous-areas', 'compex-certification',
    'dust-explosion-protection', 'ex-equipment-selection-guide',
    'explosion-proof-vs-intrinsically-safe', 'hazardous-area-classification',
    'how-to-read-atex-nameplate', 'hydrogen-explosion-protection'
]

def translate_deepl(html, target_lang):
    """DeepL handles HTML natively — send the whole page."""
    result = subprocess.run(
        ['curl', '-s', '-X', 'POST', 'https://api.deepl.com/v2/translate',
         '-H', f'Authorization: DeepL-Auth-Key {DEEPL_KEY}',
         '--data-urlencode', f'text={html}',
         '-d', f'target_lang={target_lang}',
         '-d', 'source_lang=EN',
         '-d', 'tag_handling=html',
         '-d', 'split_sentences=nonewlines'],
        capture_output=True, text=True, timeout=120
    )
    data = json.loads(result.stdout)
    if 'translations' in data:
        return data['translations'][0]['text']
    print(f"  DeepL error: {data}", file=sys.stderr)
    return None

def translate_openai_chunked(html, target_lang_name):
    """Split HTML into head+body, translate body in chunks."""
    # Split at </head> to preserve head mostly untranslated
    head_match = re.search(r'(.*?</head>)(.*)', html, re.DOTALL)
    if not head_match:
        return translate_openai_chunk(html, target_lang_name)
    
    head = head_match.group(1)
    body = head_match.group(2)
    
    # Translate title and meta descriptions in head
    head_translated = translate_openai_chunk(head, target_lang_name)
    if not head_translated:
        head_translated = head
    
    # Split body into ~15000 char chunks at section boundaries
    chunks = []
    current = ""
    for part in re.split(r'(</section>)', body):
        if len(current) + len(part) > 15000 and current:
            chunks.append(current)
            current = part
        else:
            current += part
    if current:
        chunks.append(current)
    
    translated_body = ""
    for i, chunk in enumerate(chunks):
        print(f"chunk {i+1}/{len(chunks)}", end=" ", flush=True)
        t = translate_openai_chunk(chunk, target_lang_name)
        translated_body += t if t else chunk
        time.sleep(0.5)
    
    return head_translated + translated_body

def translate_openai_chunk(text, target_lang_name):
    payload = {
        "model": "gpt-4.1-mini",
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": f"Translate the HTML from English to {target_lang_name}. Preserve ALL HTML tags, attributes, classes, IDs. Only translate visible text. Keep technical terms (ATEX, IECEx, Zone, Ex d, Ex e, Ex i, EPL, CE, IP68 etc.) as-is. Keep URLs unchanged. Output ONLY the translated HTML."},
            {"role": "user", "content": text}
        ]
    }
    result = subprocess.run(
        ['curl', '-s', 'https://api.openai.com/v1/chat/completions',
         '-H', f'Authorization: Bearer {OPENAI_KEY}',
         '-H', 'Content-Type: application/json',
         '-d', json.dumps(payload)],
        capture_output=True, text=True, timeout=120
    )
    try:
        data = json.loads(result.stdout)
        if 'choices' in data:
            content = data['choices'][0]['message']['content']
            if content.startswith('```'):
                content = re.sub(r'^```(?:html)?\s*', '', content)
                content = re.sub(r'\s*```$', '', content)
            return content
        print(f"  OpenAI error: {data.get('error', data)}", file=sys.stderr)
    except Exception as e:
        print(f"  Parse error: {e}", file=sys.stderr)
    return None

def adapt_html(html, lang):
    html = re.sub(r'<html lang="en">', f'<html lang="{lang}">', html)
    html = re.sub(
        r'href="https://exknowledge\.com/pages/',
        f'href="https://exknowledge.com/{lang}/pages/', html)
    html = re.sub(
        r'content="https://exknowledge\.com/pages/',
        f'content="https://exknowledge.com/{lang}/pages/', html)
    return html

def main():
    assignments = []
    for page in PAGES:
        assignments.append(('it', page, 'deepl', 'IT'))
        assignments.append(('fi', page, 'deepl', 'FI'))
        assignments.append(('da', page, 'openai', 'Danish'))
    
    total = len(assignments)
    done = 0
    
    for lang, page, provider, target in assignments:
        done += 1
        out_path = f"{lang}/pages/{page}.html"
        en_path = f"pages/{page}.html"
        
        if os.path.exists(out_path):
            print(f"[{done}/{total}] {out_path} — already exists, skipping")
            continue
        
        os.makedirs(f"{lang}/pages", exist_ok=True)
        
        with open(en_path, 'r') as f:
            en_html = f.read()
        
        print(f"[{done}/{total}] {lang}/{page} via {provider}...", end=" ", flush=True)
        
        if provider == 'deepl':
            translated = translate_deepl(en_html, target)
        elif provider == 'openai':
            translated = translate_openai_chunked(en_html, target)
        
        if translated:
            translated = adapt_html(translated, lang)
            with open(out_path, 'w') as f:
                f.write(translated)
            print(f"✅ ({len(translated):,} bytes)")
        else:
            print("❌ failed")
        
        time.sleep(0.5)
    
    print(f"\n✅ Done!")
    for lang in ['it','fi','da']:
        count = sum(1 for p in PAGES if os.path.exists(f"{lang}/pages/{p}.html"))
        print(f"  {lang}: {count}/11 pages")

if __name__ == "__main__":
    main()
