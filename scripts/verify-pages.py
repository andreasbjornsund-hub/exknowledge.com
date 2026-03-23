#!/usr/bin/env python3
"""
ExKnowledge Page Verification Script
Run after any page additions/changes to catch consistency issues.
Usage: python3 scripts/verify-pages.py [--fix]
"""

import os
import sys
import re
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
FIX_MODE = "--fix" in sys.argv

CHECKS = {
    "X-Content-Type-Options": {
        "pattern": 'X-Content-Type-Options',
        "required": True,
        "fix_after": 'name="viewport"',
        "fix_line": '  <meta http-equiv="X-Content-Type-Options" content="nosniff">'
    },
    "Content-Security-Policy": {
        "pattern": "Content-Security-Policy",
        "required": True,
        "fix_after": "X-Content-Type-Options",
        "fix_line": '  <meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'self\' \'unsafe-inline\' https://www.googletagmanager.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://unpkg.com; style-src \'self\' \'unsafe-inline\' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; img-src \'self\' https://images.unsplash.com https://img.youtube.com https://*.googletagmanager.com data:; connect-src \'self\' https://www.google-analytics.com https://formsubmit.co https://region1.google-analytics.com; font-src \'self\' https://cdnjs.cloudflare.com; frame-src https://www.youtube.com https://www.googletagmanager.com">'
    },
    "Referrer-Policy": {
        "pattern": 'name="referrer"',
        "required": True,
        "fix_after": "Content-Security-Policy",
        "fix_line": '  <meta name="referrer" content="strict-origin-when-cross-origin">'
    },
    "GTM": {
        "pattern": "GTM-5VSBXBSL",
        "required": True,
    },
    "Canonical URL": {
        "pattern": 'rel="canonical"',
        "required": True,
    },
    "OG Title": {
        "pattern": 'og:title',
        "required": True,
    },
    "OG Description": {
        "pattern": 'og:description',
        "required": True,
    },
    "OG Image": {
        "pattern": 'og:image',
        "required": True,
    },
    "JSON-LD Schema": {
        "pattern": 'application/ld+json',
        "required": True,
    },
    "Language Selector": {
        "pattern": 'lang-select',
        "required": True,
    },
    "Burger Menu": {
        "pattern": 'burger',
        "required": True,
    },
    "Podcast Footer Icons": {
        "pattern": 'media.rss.com/exknowledge/feed.xml',
        "required": True,
    },
    "nav.js": {
        "pattern": 'nav.js',
        "required": True,
    },
    "search.js": {
        "pattern": 'search.js',
        "required": True,
        "exclude_dirs": ["exscanner"],
    },
    "reveal.js": {
        "pattern": 'reveal.js',
        "required": True,
        "exclude_dirs": ["exscanner"],
    },
    "Viewport": {
        "pattern": 'name="viewport"',
        "required": True,
    },
    "Podcast Nav Link": {
        "pattern": '/podcast/',
        "required": True,
        "exclude_dirs": ["exscanner"],
    },
}

def find_html_files():
    files = []
    for root, dirs, filenames in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "scripts")]
        for f in filenames:
            if f.endswith(".html"):
                files.append(os.path.join(root, f))
    return sorted(files)

def check_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    
    rel = os.path.relpath(filepath, ROOT)
    issues = []
    
    for name, check in CHECKS.items():
        # Skip checks for excluded directories
        exclude_dirs = check.get("exclude_dirs", [])
        if any(rel.startswith(d + "/") for d in exclude_dirs):
            continue
        
        if check["pattern"] not in content:
            issues.append(name)
    
    return issues

def main():
    files = find_html_files()
    print(f"Checking {len(files)} HTML files...\n")
    
    total_issues = 0
    issue_summary = {}
    
    for filepath in files:
        issues = check_file(filepath)
        if issues:
            rel = os.path.relpath(filepath, ROOT)
            total_issues += len(issues)
            print(f"  ❌ {rel}")
            for issue in issues:
                print(f"     Missing: {issue}")
                issue_summary[issue] = issue_summary.get(issue, 0) + 1
    
    print(f"\n{'='*60}")
    if total_issues == 0:
        print(f"✅ All {len(files)} pages pass all checks!")
    else:
        print(f"❌ {total_issues} issues across {len(files)} pages")
        print(f"\nIssue summary:")
        for issue, count in sorted(issue_summary.items(), key=lambda x: -x[1]):
            print(f"  {issue}: {count} files")
    
    # Check sitemap consistency
    sitemap_path = ROOT / "sitemap.xml"
    if sitemap_path.exists():
        sitemap = sitemap_path.read_text()
        sitemap_urls = re.findall(r'<loc>(.*?)</loc>', sitemap)
        print(f"\nSitemap: {len(sitemap_urls)} URLs")
        
        # Check for HTML files not in sitemap
        html_urls = set()
        for f in files:
            rel = os.path.relpath(f, ROOT)
            if rel.startswith("exscanner/"):
                continue
            url = f"https://exknowledge.com/{rel}"
            if rel == "index.html":
                url = "https://exknowledge.com/"
            elif rel.endswith("/index.html"):
                url = f"https://exknowledge.com/{rel[:-10]}"
            html_urls.add(url)
        
        missing_from_sitemap = html_urls - set(sitemap_urls)
        if missing_from_sitemap:
            print(f"  ⚠️  {len(missing_from_sitemap)} pages not in sitemap:")
            for u in sorted(missing_from_sitemap)[:10]:
                print(f"     {u}")
    
    return 0 if total_issues == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
