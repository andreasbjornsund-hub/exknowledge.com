#!/usr/bin/env python3
"""Mark content tables with 4+ columns as .stack and label every cell with its column header (data-label),
so css/style.css can show them as one card per row on phones. Idempotent; run after adding or translating pages.
Usage (repo root): python3 scripts/mobile_tables.py"""
import html, pathlib, re

MIN_COLS = 4
TABLE = re.compile(r'<table\b[^>]*>.*?</table>', re.S)

def cells(row):
    return re.findall(r'<(t[hd])\b([^>]*)>(.*?)</\1>', row, re.S)

def label(txt):
    return html.escape(re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', txt))).strip(), quote=True)

def fix_table(m):
    t = m.group(0)
    rows = re.findall(r'<tr\b[^>]*>.*?</tr>', t, re.S)
    if not rows:
        return t
    head = re.search(r'<thead\b.*?</thead>', t, re.S)
    head_row = re.search(r'<tr\b[^>]*>.*?</tr>', head.group(0), re.S).group(0) if head else rows[0]
    hc = cells(head_row)
    if not hc or any(tag != 'th' for tag, _, _ in hc) or len(hc) < MIN_COLS or re.search(r'\b(colspan|rowspan)=', t):
        return t
    labels = [label(c[2]) for c in hc]
    open_tag = re.match(r'<table\b[^>]*>', t).group(0)
    if 'stack' not in open_tag:
        if 'class="' in open_tag:
            new_open = open_tag.replace('class="', 'class="stack ', 1)
        else:
            new_open = open_tag[:-1] + ' class="stack">'
        t = new_open + t[len(open_tag):]
    def fix_row(rm):
        row = rm.group(0)
        if row == head_row and not head:
            return row
        i = [0]
        def fix_cell(cm):
            tag, attrs = cm.group(1), cm.group(2)
            k = i[0]; i[0] += 1
            if 'data-label=' in attrs or k >= len(labels):
                return cm.group(0)
            return f'<{tag}{attrs} data-label="{labels[k]}">'
        return re.sub(r'<(t[hd])\b([^>]*)>', fix_cell, row)
    body = t
    if head:
        a, b = body.find(head.group(0)), len(head.group(0))
        pre, headpart, post = body[:a], body[a:a + b], body[a + b:]
        post = re.sub(r'<tr\b[^>]*>.*?</tr>', fix_row, post, flags=re.S)
        return pre + headpart + post
    first = re.search(r'<tr\b[^>]*>.*?</tr>', body, re.S)
    return body[:first.end()] + re.sub(r'<tr\b[^>]*>.*?</tr>', fix_row, body[first.end():], flags=re.S)

changed = tables = 0
for p in sorted(pathlib.Path('.').rglob('*.html')):
    if {'.git', '.audit', 'node_modules'} & set(p.parts):
        continue
    s = p.read_text(encoding='utf-8', errors='replace')
    if 'content-body' not in s or '<table' not in s:
        continue
    head, sep, body = s.partition('class="content-body"')
    if not sep:
        continue
    new_body = TABLE.sub(fix_table, body)
    if new_body != body:
        tables += len(re.findall(r'<table\b[^>]*class="stack', new_body)) - len(re.findall(r'<table\b[^>]*class="stack', body))
        p.write_text(head + sep + new_body, encoding='utf-8'); changed += 1
print(f'pages updated: {changed}, tables newly stacked: {tables}')
