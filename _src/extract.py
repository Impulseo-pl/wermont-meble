"""Wyciaga tresc kazdej podstrony wermont.eu do tresc/<slug>.json: title, desc, h1, bloki (h2/h3/p/ul), faq, zdjecia."""
import re, html as H, json, glob, os
os.makedirs('tresc', exist_ok=True)
SKIP = re.compile(r'^(★|umów|zobacz realizacje|albo zadzwoń|zadzwoń|sprawdź|czytaj|wróć|poprzedni|następny|udostępnij)', re.I)

def clean(x):
    x = re.sub(r'<br\s*/?>', ' ', x)
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', '', x))).replace('‐', '-').strip()

def rich(x):
    """tresc akapitu z zachowaniem linkow wewnetrznych i pogrubien"""
    x = re.sub(r'<br\s*/?>', ' ', x)
    def a(m):
        href = m.group(1); txt = clean(m.group(2))
        mm = re.match(r'https://wermont\.eu/(.*)$', href)
        if mm: return '<a href="{R}%s">%s</a>' % (mm.group(1), txt)
        return txt
    x = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', a, x, flags=re.S)
    x = re.sub(r'<(strong|b)\b[^>]*>(.*?)</\1>', lambda m: '<strong>%s</strong>' % clean(m.group(2)), x, flags=re.S)
    x = re.sub(r'<(?!/?(a|strong)\b)[^>]+>', '', x)
    x = H.unescape(x).replace('‐', '-')
    x = x.replace('&', '&amp;').replace('&amp;amp;', '&amp;')
    return re.sub(r'\s+', ' ', x).strip()

for f in glob.glob('html/*.html'):
    slug = os.path.basename(f)[:-5]
    s = open(f, encoding='utf-8').read()
    title = clean(re.search(r'<title>(.*?)</title>', s, re.S).group(1))
    desc = H.unescape((re.findall(r'<meta name="description" content="([^"]*)"', s) or [''])[0]).replace('‐', '-')
    faq = []
    for ld in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
        try: d = json.loads(ld)
        except Exception: continue
        stack = [d]
        while stack:
            x = stack.pop()
            if isinstance(x, list): stack += x; continue
            if not isinstance(x, dict): continue
            if x.get('@type') == 'FAQPage':
                for q in x.get('mainEntity', []):
                    faq.append({'q': clean(q['name']), 'a': clean(q['acceptedAnswer']['text'])})
            stack += [v for v in x.values() if isinstance(v, (dict, list))]
    m = re.search(r'<main.*?</main>', s, re.S)
    m = m.group(0) if m else s
    m = re.sub(r'<(script|style|svg|noscript|form|nav)[^>]*>.*?</\1>', '', m, flags=re.S)
    blocks, h1 = [], ''
    for t in re.finditer(r'<(h1|h2|h3|h4|p|ul|ol|table)\b[^>]*>(.*?)</\1>', m, re.S):
        tag, inner = t.group(1), t.group(2)
        if tag in ('ul', 'ol'):
            items = [clean(li) for li in re.findall(r'<li[^>]*>(.*?)</li>', inner, re.S)]
            items = [i for i in items if i and len(i) < 400]
            if items: blocks.append({'t': 'ul', 'items': items})
            continue
        if tag == 'table':
            rows = [[clean(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)] for r in re.findall(r'<tr[^>]*>(.*?)</tr>', inner, re.S)]
            blocks.append({'t': 'table', 'rows': rows}); continue
        x = clean(inner)
        if not x or SKIP.match(x): continue
        if tag == 'h1': h1 = x; continue
        b = {'t': tag, 'x': x}
        if tag == 'p': b['h'] = rich(inner)
        blocks.append(b)
    # dedupe (Avada czesto duplikuje bloki mobile/desktop)
    seen, out = set(), []
    for b in blocks:
        k = json.dumps(b, ensure_ascii=False)
        if k in seen: continue
        seen.add(k); out.append(b)
    faqq = {q['q'] for q in faq}
    out = [b for b in out if not (b['t'] in ('h3', 'h4', 'p') and b.get('x') in faqq)]
    faqa = {q['a'] for q in faq}
    out = [b for b in out if not (b['t'] == 'p' and b.get('x') in faqa)]
    imgs = sorted(set(re.sub(r'-\d+x\d+(@2x)?(?=\.\w+$)', '', u).replace('-scaled', '').split('/')[-1]
                      for u in re.findall(r'wp-content/uploads/[^"\' ]+?\.jpe?g', m)))
    json.dump(dict(slug=slug, title=title, desc=desc, h1=h1, blocks=out, faq=faq, imgs=imgs),
              open(f'tresc/{slug}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(slug, len(out), 'blokow', len(faq), 'faq', len(imgs), 'zdj')
