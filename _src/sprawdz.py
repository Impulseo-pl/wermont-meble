"""Kontrola techniczna SEO wszystkich stron z sitemap.xml."""
import re, os, json, sys, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = re.search(r'<loc>(.*?)</loc>', open(os.path.join(ROOT, 'sitemap.xml')).read()).group(1)
paths = [l[len(BASE):] for l in re.findall(r'<loc>(.*?)</loc>', open(os.path.join(ROOT, 'sitemap.xml')).read())]
bledy, tytuly, opisy = [], {}, {}
for p in paths:
    f = os.path.join(ROOT, p, 'index.html'); s = open(f, encoding='utf-8').read()
    t = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1)); d = html.unescape(re.search(r'name="description" content="([^"]*)"', s).group(1))
    tytuly.setdefault(t, []).append(p); opisy.setdefault(d, []).append(p)
    h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    if len(h1) != 1 or not h1[0].strip(): bledy.append(f'{p}: h1 x{len(h1)}')
    if f'<link rel="canonical" href="{BASE}{p}">' not in s: bledy.append(f'{p}: canonical')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(j)
        except Exception as ex: bledy.append(f'{p}: JSON-LD {ex}')
    for im in re.findall(r'<img [^>]*>', s):
        if 'alt="' not in im or 'width=' not in im: bledy.append(f'{p}: img bez alt/width')
    for h in re.findall(r'(?:href|src)="([^"#:]+?)(?:#[^"]*)?"', s) + [x.split(' ')[0] for x in re.findall(r'srcset="([^"]+)"', s) for x in x.split(', ')]:
        if h.startswith(('http', 'mailto', 'tel', '/')) or not h: continue
        tgt = os.path.normpath(os.path.join(ROOT, p, h))
        if not (os.path.isfile(tgt) or os.path.isfile(os.path.join(tgt, 'index.html'))): bledy.append(f'{p}: martwy link {h}')
    if len(t) > 70: print('  dlugi title', len(t), p)
for t, ps in tytuly.items():
    if len(ps) > 1: bledy.append(f'duplikat title: {ps}')
for d, ps in opisy.items():
    if len(ps) > 1: bledy.append(f'duplikat description: {ps}')
stare = [u.strip().replace('https://wermont.eu/', '') for u in open(os.path.join(ROOT, '_src', 'urls.txt')) if u.strip()]
brak = [u for u in stare if u not in paths]
print(len(paths), 'stron w sitemap;', len(stare) - len(brak), '/', len(stare), 'adresow z obecnego wermont.eu zachowanych 1:1')
print('brakujace:', brak)
print('BLEDY:', len(bledy)); [print(' ', b) for b in sorted(set(bledy))[:40]]
