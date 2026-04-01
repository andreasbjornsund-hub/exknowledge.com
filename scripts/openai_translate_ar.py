#!/usr/bin/env python3
"""Translate remaining Arabic guide pages using OpenAI - chunked approach."""
import json, os, re, time, urllib.request
from html.parser import HTMLParser

with open(os.path.expanduser("~/.openclaw/.env")) as f:
    for line in f:
        if line.startswith("OPENAI_API_KEY="):
            API_KEY = line.strip().split("=", 1)[1]
            break

SITE_DIR = "/tmp/exknowledge"

def call_openai(text, system_msg, model="gpt-4.1-mini", timeout=90):
    """Call OpenAI API."""
    payload = json.dumps({
        "model": model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": text},
        ]
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req, timeout=timeout)
    result = json.loads(resp.read())
    usage = result.get("usage", {})
    return result["choices"][0]["message"]["content"], usage


def extract_and_translate_chunks(html):
    """Extract text chunks from HTML, translate them, replace back."""
    # We'll translate the HTML in sections - split by major sections
    # Strategy: split by </section> or </article> or similar block boundaries
    # Then translate each chunk individually
    
    # First, protect non-translatable blocks
    protected = {}
    counter = [0]
    
    def protect(match):
        key = f"__PROTECTED_{counter[0]}__"
        counter[0] += 1
        protected[key] = match.group(0)
        return key
    
    work = html
    
    # Protect script tags (including JSON-LD)
    work = re.sub(r'<script[^>]*>.*?</script>', protect, work, flags=re.DOTALL)
    # Protect style tags
    work = re.sub(r'<style[^>]*>.*?</style>', protect, work, flags=re.DOTALL)
    # Protect SVG
    work = re.sub(r'<svg[^>]*>.*?</svg>', protect, work, flags=re.DOTALL)
    # Protect meta/link tags in head
    work = re.sub(r'<(meta|link)\s[^>]*/?>', protect, work)
    
    # Split into chunks at section boundaries (~4-8K chars each)
    # Find good split points
    split_pattern = r'(</(?:section|article|footer|header|nav|div class="[^"]*container)>)'
    parts = re.split(split_pattern, work)
    
    # Recombine into reasonable chunks
    chunks = []
    current = ""
    for part in parts:
        current += part
        if len(current) > 6000:
            chunks.append(current)
            current = ""
    if current:
        chunks.append(current)
    
    # If we couldn't split well, fall back to splitting the body
    if len(chunks) <= 1:
        # Split at <h2> boundaries
        h2_parts = re.split(r'(<h2[^>]*>)', work)
        chunks = []
        current = h2_parts[0]
        for i in range(1, len(h2_parts)):
            current += h2_parts[i]
            if len(current) > 5000 and i < len(h2_parts) - 1:
                chunks.append(current)
                current = ""
        if current:
            chunks.append(current)
    
    print(f"  Split into {len(chunks)} chunks", end="", flush=True)
    
    system_msg = """Translate the HTML content from English to Arabic. Rules:
1. Translate ONLY visible text (headings, paragraphs, lists, labels, alt text)
2. DO NOT translate or modify: HTML tags, attributes, class names, URLs, href values, src values, data attributes, CSS, placeholder markers like __PROTECTED_N__
3. Keep ALL HTML structure exactly as-is
4. Output ONLY the translated HTML, no explanation or code blocks"""
    
    translated_chunks = []
    for j, chunk in enumerate(chunks):
        # Skip chunks that are mostly protected placeholders / no real text
        text_only = re.sub(r'<[^>]+>', '', chunk)
        text_only = re.sub(r'__PROTECTED_\d+__', '', text_only).strip()
        if len(text_only) < 50:
            translated_chunks.append(chunk)
            continue
        
        try:
            result, usage = call_openai(chunk, system_msg, timeout=120)
            # Strip code blocks if present
            result = re.sub(r'^```html?\s*\n', '', result)
            result = re.sub(r'\n```\s*$', '', result)
            translated_chunks.append(result)
            print(".", end="", flush=True)
        except Exception as e:
            print(f"\n  Chunk {j} failed: {e}, keeping original")
            translated_chunks.append(chunk)
        time.sleep(0.5)
    
    # Reassemble
    full = "".join(translated_chunks)
    
    # Restore protected blocks
    for key, value in protected.items():
        full = full.replace(key, value)
    
    return full


def fix_arabic_page(html, page_name):
    """Post-process translated page."""
    html = re.sub(r'<html\s+lang="[^"]*"', '<html lang="ar" dir="rtl"', html)
    if 'dir="rtl"' not in html:
        html = html.replace('<html lang="ar"', '<html lang="ar" dir="rtl"')
    html = re.sub(
        r'<link rel="canonical" href="[^"]*"',
        f'<link rel="canonical" href="https://exknowledge.com/ar/pages/{page_name}.html"',
        html,
    )
    html = html.replace('href="../css/', 'href="/css/')
    html = html.replace('src="../js/', 'src="/js/')
    html = html.replace('src="../images/', 'src="/images/')
    html = re.sub(r'href="/pages/', 'href="/ar/pages/', html)
    html = re.sub(r'href="/blog/', 'href="/ar/blog/', html)
    html = re.sub(r'href="/"', 'href="/ar/"', html)
    return html


guides_todo = [
    "atex-for-beginners", "cable-glands-hazardous-areas", "compex-certification",
    "dust-explosion-protection", "ex-equipment-selection-guide",
    "explosion-proof-vs-intrinsically-safe", "hazardous-area-classification",
    "how-to-read-atex-nameplate", "hydrogen-explosion-protection",
]

print("=== OpenAI Arabic Translation (chunked) ===\n")

for i, guide in enumerate(guides_todo):
    src = os.path.join(SITE_DIR, "pages", f"{guide}.html")
    dst = os.path.join(SITE_DIR, "ar", "pages", f"{guide}.html")
    
    html = open(src, "r", encoding="utf-8").read()
    print(f"[{i+1}/9] {guide} ({len(html):,} chars)...")
    
    try:
        translated = extract_and_translate_chunks(html)
        translated = fix_arabic_page(translated, guide)
        
        # Validate
        if "</head>" not in translated or "</html>" not in translated:
            print(f"  ⚠ Structure issue, checking...")
            if "</head>" not in translated:
                print(f"  Missing </head>!")
            if "</html>" not in translated:
                print(f"  Missing </html>!")
        
        with open(dst, "w", encoding="utf-8") as f:
            f.write(translated)
        print(f"  ✓ Done")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
    
    time.sleep(1)

print("\n=== Validation ===")
all_ok = True
for guide in guides_todo:
    fp = os.path.join(SITE_DIR, "ar", "pages", f"{guide}.html")
    html = open(fp).read()
    has_head = "</head>" in html
    has_html = "</html>" in html
    has_faq = '"FAQPage"' in html
    ok = has_head and has_html
    if not ok: all_ok = False
    print(f"  {guide}: {'✓' if ok else '✗ BROKEN'} (FAQ: {'yes' if has_faq else 'no'})")

if all_ok:
    print("\nAll pages valid!")
else:
    print("\nSome pages need attention.")
