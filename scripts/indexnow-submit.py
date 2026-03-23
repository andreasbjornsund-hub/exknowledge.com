#!/usr/bin/env python3
"""
Submit URLs to IndexNow (Bing + Yandex + IndexNow.org).
Usage: python3 scripts/indexnow-submit.py URL1 URL2 ...
       python3 scripts/indexnow-submit.py --sitemap   (submit all sitemap URLs)
"""

import urllib.request
import json
import sys
import re
from pathlib import Path

KEY = "exka37789b4d65d987b9dd57357"
KEY_LOCATION = "https://exknowledge.com/indexnow-key.txt"
HOST = "exknowledge.com"

ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
]

def submit(urls):
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }).encode()

    print(f"Submitting {len(urls)} URLs...")
    for api in ENDPOINTS:
        try:
            req = urllib.request.Request(api, data=payload, headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=10)
            print(f"  {api}: HTTP {resp.status} ✓")
        except Exception as e:
            print(f"  {api}: {e} ✗")

def main():
    if "--sitemap" in sys.argv:
        sitemap_path = Path(__file__).parent.parent / "sitemap.xml"
        sitemap = sitemap_path.read_text()
        urls = re.findall(r'<loc>(.*?)</loc>', sitemap)
        print(f"Found {len(urls)} URLs in sitemap")
        # Submit in batches of 100
        for i in range(0, len(urls), 100):
            batch = urls[i:i+100]
            submit(batch)
    else:
        urls = [u for u in sys.argv[1:] if u.startswith("http")]
        if not urls:
            print("Usage: python3 scripts/indexnow-submit.py URL1 URL2 ...")
            print("       python3 scripts/indexnow-submit.py --sitemap")
            sys.exit(1)
        submit(urls)

if __name__ == "__main__":
    main()
