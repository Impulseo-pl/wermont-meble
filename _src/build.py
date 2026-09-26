"""Generator strony Wermont. Te same adresy URL co obecne wermont.eu (43 podstrony), tresci klienta,
nowy szablon. Uzycie:  python _src/build.py            -> demo (noindex, licznik otwarc)
                       BASE=https://wermont.eu/ python _src/build.py  -> produkcja"""
import os, re, json, html, hashlib
from zdjecia import ZDJ

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = os.environ.get('BASE', 'https://impulseo-pl.github.io/wermont-meble/')
DEMO = 'wermont.eu' not in BASE
WYM = json.load(open(os.path.join(HERE, 'wymiary.json')))
H1_WPISOW = {'kuchnia-bezuchwytowa-z-listwa-korytkowa-czysty-minimalizm-w-praktyce': 'Kuchnia bezuchwytowa z listwą korytkową - czysty minimalizm w praktyce',
             'fronty-do-kuchni-lakier-akryl-czy-drewno-jak-wybrac': 'Fronty do kuchni: lakier, akryl czy drewno? Jak wybrać',
             'jak-powstaje-kuchnia-na-wymiar-krok-po-kroku-od-pomiaru-do-montazu': 'Jak powstaje kuchnia na wymiar - krok po kroku, od pomiaru do montażu'}
def T(s):
    d = json.load(open(os.path.join(HERE, 'tresc', s + '.json'), encoding='utf-8'))
    d['h1'] = d['h1'] or H1_WPISOW.get(s, '')
    return d
def lead_z_opisu(d):
    return e(re.split(r'\s*(Bezpłatny pomiar|Tel\.|Zadzwoń)', d['desc'])[0].rstrip(' .') + '.')
CSS = open(os.path.join(HERE, 'styles.css'), encoding='utf-8').read()
CSS = re.sub(r'/\*.*?\*/', '', CSS, flags=re.S)
CSS = re.sub(r'\s*\n\s*', '', CSS)
e = html.escape

TEL, TEL_H, MAIL = '+48732139879', '732 139 879', 'biuro@wermont.eu'
FIRMA = BASE + '#firma'

# ---------------------------------------------------------------- mapa serwisu
USLUGI = [  # slug, nazwa w menu, zdjecia (pierwsze = glowne)
    ('meble-kuchenne', 'Kuchnie na wymiar', ['kuchnia-orzech-wyspa', 'kuchnia-dab-okno', 'kuchnia-granat', 'kuchnia-szuflady', 'kuchnia-naroznik-orzech', 'kuchnia-cegla', 'kuchnia-slupek-blachy', 'kuchnia-dab-wyspa']),
    ('meble-kuchenne-z-plyty-mdf', 'Kuchnie z MDF', ['kuchnia-mdf', 'kuchnia-mdf-2', 'kuchnia-mdf-4', 'kuchnia-mdf-3', 'kuchnia-mdf-5']),
    ('meble-kuchenne-drewniane', 'Kuchnie drewniane', ['kuchnia-cegla', 'kuchnia-klasyczna', 'kuchnia-cegla-2', 'kuchnia-klasyczna-2', 'kuchnia-slupek-drewno', 'kuchnia-klasyczna-3']),
    ('garderoby-i-szafy', 'Szafy i garderoby', ['szafa-wneka', 'garderoba-przedpokoj', 'szafa-szara', 'szafa-skos']),
    ('szafy-w-skosie', 'Szafy w skosie', ['szafa-skos', 'garderoba-przedpokoj', 'szafa-wneka']),
    ('meble-lazienkowe', 'Meble łazienkowe', ['lazienka-dab', 'lazienka-kamien', 'lazienka-szuflada', 'lazienka-lustro', 'lazienka-drewno', 'lazienka-dab-2']),
    ('fronty-meblowe', 'Fronty meblowe', ['kuchnia-granat-zabudowa', 'kuchnia-dab-b', 'bezuchwyt-egger', 'kuchnia-klasyczna-4']),
    ('projektowanie-mebli', 'Projektowanie mebli', ['wizualizacja', 'pomiar', 'kuchnia-dab-okno-2']),
]
MIASTA = {  # slug-koncowka: (mianownik, miejscownik, grupa)
    'skorzewo': ('Skorzewo', 'w Skorzewie', 'k'), 'koscierzyna': ('Kościerzyna', 'w Kościerzynie', 'k'),
    'lipusz': ('Lipusz', 'w Lipuszu', 'k'), 'stezyca': ('Stężyca', 'w Stężycy', 'k'),
    'wielki-klincz': ('Wielki Klincz', 'w Wielkim Klinczu', 'k'), 'nowy-klincz': ('Nowy Klincz', 'w Nowym Klinczu', 'k'),
    'nowa-karczma': ('Nowa Karczma', 'w Nowej Karczmie', 'k'), 'grabowo-koscierskie': ('Grabowo Kościerskie', 'w Grabowie Kościerskim', 'k'),
    'golubie': ('Gołubie', 'w Gołubiu', 'k'), 'lubiana': ('Łubiana', 'w Łubianie', 'k'), 'sikorzyno': ('Sikorzyno', 'w Sikorzynie', 'k'),
    'gdansk': ('Gdańsk', 'w Gdańsku', 't'), 'gdynia': ('Gdynia', 'w Gdyni', 't'), 'sopot': ('Sopot', 'w Sopocie', 't'),
    'kartuzy': ('Kartuzy', 'w Kartuzach', 'p'), 'zukowo': ('Żukowo', 'w Żukowie', 'p'), 'bytow': ('Bytów', 'w Bytowie', 'p'), 'lebork': ('Lębork', 'w Lęborku', 'p'),
}
GRUPY = {'k': 'Kościerzyna i okolice', 't': 'Trójmiasto', 'p': 'Kaszuby i reszta Pomorza'}
RODZ = [('kuchnie-na-wymiar-', 'Kuchnie na wymiar', 'kuchnie'), ('szafy-i-garderoby-na-wymiar-', 'Szafy i garderoby', 'szafy'),
        ('meble-lazienkowe-na-wymiar-', 'Meble łazienkowe', 'lazienki'), ('meble-na-wymiar-', 'Meble na wymiar', 'meble')]
LOKALNE = []
for u in open(os.path.join(HERE, 'urls.txt')):
    s = u.strip().rstrip('/').split('/')[-1]
    for pre, nazwa, typ in RODZ:
        if s.startswith(pre) and s[len(pre):] in MIASTA:
            LOKALNE.append((s, nazwa, typ, s[len(pre):])); break
FOTO_TYP = {
    'kuchnie': ['kuchnia-orzech-wyspa', 'kuchnia-dab-okno', 'kuchnia-granat', 'kuchnia-dab-wyspa', 'kuchnia-cegla', 'kuchnia-dab-b', 'kuchnia-granat-biala', 'kuchnia-orzech-blat', 'kuchnia-dab-okno-2', 'kuchnia-witryna', 'kuchnia-mdf', 'kuchnia-orzech-wyspa-2'],
    'szafy': ['szafa-wneka', 'garderoba-przedpokoj', 'szafa-szara', 'szafa-skos'],
    'lazienki': ['lazienka-dab', 'lazienka-kamien', 'lazienka-lustro', 'lazienka-dab-2'],
    'meble': ['kuchnia-dab-okno', 'szafa-wneka', 'kuchnia-orzech-wyspa', 'lazienka-dab', 'kuchnia-cegla', 'garderoba-przedpokoj', 'kuchnia-granat', 'szafa-skos', 'kuchnia-dab-b', 'lazienka-kamien', 'kuchnia-witryna'],
}
WPISY = ['kuchnia-bezuchwytowa-z-listwa-korytkowa-czysty-minimalizm-w-praktyce',
         'fronty-do-kuchni-lakier-akryl-czy-drewno-jak-wybrac',
         'jak-powstaje-kuchnia-na-wymiar-krok-po-kroku-od-pomiaru-do-montazu']
WPIS_FOTO = {WPISY[0]: ['bezuchwyt-blat', 'bezuchwyt-egger', 'bezuchwyt-szuflady', 'bezuchwyt-zmywarka', 'bezuchwyt-blat-2'],
             WPISY[1]: ['kuchnia-granat-zabudowa', 'kuchnia-klasyczna-2', 'kuchnia-dab-b-2'],
             WPISY[2]: ['pomiar', 'wizualizacja', 'kuchnia-szuflady', 'kuchnia-dab-okno']}
DATY = {WPISY[0]: ('2026-07-12', '2026-07-12'), WPISY[1]: ('2026-07-12', '2026-07-30'), WPISY[2]: ('2026-07-12', '2026-09-15')}
OPINIE = [
    ('Panowie świetnie doradzili jak zrobić meble w naszej kuchni aby jak najlepiej wykorzystać miejsce. (…) Montaż również przeszedł bardzo sprawnie. Efekt przerósł nasze oczekiwania.', 'Daria Frąckiewicz'),
    ('Obie szafy okazały się być najlepiej wykonanymi meblami w trakcie całego remontu.', 'Marta Tchórzewska'),
    ('Byli przygotowani z ilością próbek blatów i płyt meblowych. (…) Chłopaki są wyjątkiem pośród stolarzy co »przychodzą o czasie i odbierają telefony«.', 'Daria'),
]
STOP = re.compile(r'^(Najczęściej zadawane pytania|Najczęstsze pytania|Zobacz również|Opinie naszych klientów|Komponenty i systemy|SŁUCHAMY|Przykładowe kuchnie|Porozmawiajmy|Chcesz podobne|Poznajmy się|Bezpłatny pomiar)', re.I)

# ---------------------------------------------------------------- pomocnicze
def img(k, sizes, R, cls='', eager=False, ratio=None):
    w, h, sz = WYM[k]
    src = ', '.join(f'{R}img/{k}-{s}.webp {s}w' for s in sz)
    mid = sz[1] if len(sz) > 1 else sz[0]
    st = f' style="object-position:{ZDJ[k][2]}"' if ZDJ[k][2] != '50% 50%' else ''
    load = ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    return (f'<img src="{R}img/{k}-{mid}.webp" srcset="{src}" sizes="{sizes}" width="{mid}" height="{round(h * mid / w)}"'
            f' alt="{e(ZDJ[k][1])}"{st}{load}{" class=" + chr(34) + cls + chr(34) if cls else ""}>')

def pick(lista, slug, n):
    """deterministyczny, rozny dla kazdej podstrony wybor zdjec"""
    i = int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(lista)
    return [lista[(i + j) % len(lista)] for j in range(min(n, len(lista)))]

def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '</script>'

def breadcrumbs(crumbs, R):
    li = ''.join(f'<li><a href="{R}{p}">{e(n)}</a></li>' for n, p in crumbs[:-1]) + f'<li aria-current="page">{e(crumbs[-1][0])}</li>'
    return f'<nav class="crumbs" aria-label="Jesteś tutaj"><ol>{li}</ol></nav>'

def crumbs_ld(crumbs, path):
    return {'@type': 'BreadcrumbList', '@id': BASE + path + '#okruszki', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + p} for i, (n, p) in enumerate(crumbs)]}

def faq_html(faq, tytul='Najczęściej zadawane pytania'):
    if not faq: return ''
    it = ''.join(f'<details><summary>{e(q["q"])}</summary><p>{e(q["a"])}</p></details>' for q in faq)
    return f'<section class="sec sec-tight" aria-labelledby="h-faq"><div class="wrap faq-wrap"><h2 id="h-faq">{tytul}</h2><div class="faq">{it}</div></div></section>'

def faq_ld(faq, path):
    return {'@type': 'FAQPage', '@id': BASE + path + '#faq', 'mainEntity': [
        {'@type': 'Question', 'name': q['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': q['a']}} for q in faq]}

def cta_band(R, tytul='Umów bezpłatny pomiar', tekst='Przyjedziemy, zmierzymy i podamy konkretną cenę już na pierwszym spotkaniu. Pomiar i wycena nic nie kosztują.'):
    return (f'<section class="cta-band"><div class="wrap cta-in"><div><h2>{tytul}</h2><p>{tekst}</p></div>'
            f'<div class="actions"><a class="btn btn-light" href="tel:{TEL}">Zadzwoń: {TEL_H}</a>'
            f'<a class="btn btn-line" href="{R}kontakt/#zapytanie">Napisz do nas</a></div></div></section>')

def aside_card(R, miejsce=''):
    return (f'<aside class="side-card"><h2>Bezpłatny pomiar{(" " + miejsce) if miejsce else ""}</h2>'
            f'<p>Przyjeżdżamy, mierzymy i podajemy konkretną cenę na pierwszym spotkaniu.</p>'
            f'<a class="side-tel" href="tel:{TEL}">{TEL_H}</a><p class="side-h">pon.–pt. 8:00–18:00</p>'
            f'<a class="btn btn-main btn-full" href="{R}kontakt/#zapytanie">Umów pomiar</a></aside>')

def opinia(i):
    t, a = OPINIE[i % len(OPINIE)]
    return f'<blockquote class="quote"><p>„{e(t)}”</p><footer>{e(a)}, opinia w Google</footer></blockquote>'

def tresc(blocks, R, zdjecia=(), wstaw_co=2):
    """bloki z obecnej strony klienta -> sekcje artykulu; zdjecia wstawiane miedzy sekcje"""
    out, n_sec, zi, lead = [], 0, 0, None
    for b in blocks:
        x = b.get('x', '')
        if b['t'] in ('h2', 'h3', 'h4') and STOP.match(x): break
        if b['t'] == 'p' and STOP.match(x): break
        if b['t'] == 'h2':
            n_sec += 1
            if n_sec > 1 and (n_sec - 1) % wstaw_co == 0 and zi < len(zdjecia):
                out.append(f'<figure class="in-fig">{img(zdjecia[zi], "(min-width: 1000px) 680px, 100vw", R)}<figcaption>{e(ZDJ[zdjecia[zi]][1])}</figcaption></figure>'); zi += 1
            out.append(f'<h2>{e(x)}</h2>')
        elif b['t'] in ('h3', 'h4'): out.append(f'<h3>{e(x)}</h3>')
        elif b['t'] == 'ul': out.append('<ul class="list">' + ''.join(f'<li>{e(i)}</li>' for i in b['items']) + '</ul>')
        elif b['t'] == 'table':
            rows = b['rows']
            out.append('<div class="tbl"><table><thead><tr>' + ''.join(f'<th scope="col">{e(c)}</th>' for c in rows[0]) + '</tr></thead><tbody>' +
                       ''.join('<tr>' + ''.join((f'<th scope="row">{e(c)}</th>' if j == 0 else f'<td>{e(c)}</td>') for j, c in enumerate(r)) + '</tr>' for r in rows[1:]) + '</tbody></table></div>')
        elif b['t'] == 'p':
            h = b['h'].replace('{R}', R)
            if len(x) < 110 and re.search(r'pomiar', x, re.I) and re.search(r'\?|bezpłatn', x):
                out.append(f'<p class="callout">{h} <a href="{R}kontakt/#zapytanie">Umów pomiar</a></p>')
            elif lead is None and not out: lead = h
            else: out.append(f'<p>{h}</p>')
    return lead, '\n'.join(out), zdjecia[zi:]

# ---------------------------------------------------------------- szkielet
MENU = [('meble-kuchenne/', 'Kuchnie'), ('garderoby-i-szafy/', 'Szafy'), ('meble-lazienkowe/', 'Łazienki'), ('fronty-meblowe/', 'Fronty'),
        ('realizacje/', 'Realizacje'), ('proces-realizacji/', 'Jak pracujemy'), ('category/poradniki/', 'Poradniki'), ('o-nas/', 'O nas'), ('kontakt/', 'Kontakt')]

def stopka(R):
    lok = {}
    for s, nazwa, typ, m in LOKALNE: lok.setdefault(nazwa, []).append((MIASTA[m][0], s))
    kol = ''.join(f'<div><h2>{e(n)}</h2><ul>' + ''.join(f'<li><a href="{R}{s}/">{e(m)}</a></li>' for m, s in sorted(v, key=lambda t: t[0])) + '</ul></div>'
                  for n, v in lok.items())
    return f'''<footer class="site-foot"><div class="wrap">
<div class="foot-top"><div class="foot-nap"><img src="{R}img/logo-wermont.png" width="160" height="21" alt="Wermont" class="foot-logo" loading="lazy">
<address>WERMONT – Meble Na Wymiar<br>ul. Kościelna 18, 83-400 Skorzewo<br>NIP 591-167-64-14</address>
<p><a href="tel:{TEL}">{TEL_H}</a><br><a href="mailto:{MAIL}">{MAIL}</a><br>pon.–pt. 8:00–18:00</p></div>
<div><h2>Oferta</h2><ul>{"".join(f'<li><a href="{R}{s}/">{e(n)}</a></li>' for s, n, _ in USLUGI)}</ul></div>
<div><h2>Firma</h2><ul><li><a href="{R}o-nas/">O nas</a></li><li><a href="{R}proces-realizacji/">Proces realizacji</a></li><li><a href="{R}realizacje/">Realizacje</a></li><li><a href="{R}zakres-dzialania/">Zakres działania</a></li><li><a href="{R}category/poradniki/">Poradniki</a></li><li><a href="{R}kontakt/">Kontakt</a></li></ul></div></div>
<div class="foot-loc">{kol}</div>
<div class="foot-bottom"><span>© 2026 WERMONT – Meble Na Wymiar · <a href="{R}polityka-prywatnosci/">Polityka prywatności</a> · <a href="https://www.facebook.com/wermontmeblenawymiar/" rel="noopener" target="_blank">Facebook</a> · <a href="https://www.instagram.com/wermont_meblenawymiar/" rel="noopener" target="_blank">Instagram</a></span><span>Zdjęcia: realizacje Wermont · Strona: Impulseo</span></div>
</div></footer>
<nav class="mobile-bar" aria-label="Szybki kontakt"><a href="tel:{TEL}">Zadzwoń</a><a href="{R}kontakt/#zapytanie">Umów pomiar</a></nav>'''

def strona(path, title, desc, body, graph, R, preload=None, akt='', og=None):
    url = BASE + path
    og_img = BASE + ('img/og.jpg' if not og else f'img/{og}-{WYM[og][2][-1]}.webp')
    menu = ''.join(f'<a href="{R}{p}"{" aria-current=" + chr(34) + "page" + chr(34) if akt == p else ""}>{n}</a>' for p, n in MENU)
    pre = ''
    if preload:
        k = preload[0]; sz = WYM[k][2]
        pre = (f'<link rel="preload" as="image" href="{R}img/{k}-{sz[1] if len(sz) > 1 else sz[0]}.webp" '
               f'imagesrcset="{", ".join(f"{R}img/{k}-{s}.webp {s}w" for s in sz)}" imagesizes="{preload[1]}" fetchpriority="high">')
    g = {'@context': 'https://schema.org', '@graph': graph}
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex, follow"><!-- DEMO: przy wdrozeniu BASE=https://wermont.eu/ -->' if DEMO else '<meta name="robots" content="index, follow, max-image-preview:large">'}
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#231f1b">
<meta property="og:type" content="{'article' if '"BlogPosting"' in json.dumps(graph) else 'website'}">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="Wermont – Meble Na Wymiar">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{R}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{R}apple-touch-icon.png">
<link rel="manifest" href="{R}site.webmanifest">
{pre}
<style>{CSS.replace('url(../fonts/', 'url(' + R + 'fonts/')}</style>
{ld(g)}
</head>
<body>
<a class="skip" href="#tresc">Przejdź do treści</a>
<header class="site-head"><div class="wrap head-in">
<a class="brand" href="{R or './'}" aria-label="Wermont – strona główna"><img src="{R}img/logo-wermont.png" width="160" height="21" alt="Wermont"><span class="brand-sub">stolarnia w Skorzewie</span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
<nav class="menu" id="menu" aria-label="Menu główne">{menu}<a class="head-tel" href="tel:{TEL}">{TEL_H}</a></nav>
</div></header>
<main id="tresc">
{body.replace("{R}", R)}
</main>
{stopka(R)}
<script src="{R}assets/app.js" defer></script>
</body>
</html>
'''

def zapisz(path, s):
    f = os.path.join(ROOT, path, 'index.html') if path else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(f), exist_ok=True)
    open(f, 'w', encoding='utf-8', newline='\n').write(s)

def rel(path): return '../' * path.count('/')

def webpage(path, name, typ='WebPage', crumbs=True, extra=None):
    d = {'@type': typ, '@id': BASE + path + '#strona', 'url': BASE + path, 'name': name, 'inLanguage': 'pl-PL',
         'isPartOf': {'@id': BASE + '#witryna'}, 'about': {'@id': FIRMA}}
    if crumbs: d['breadcrumb'] = {'@id': BASE + path + '#okruszki'}
    if extra: d.update(extra)
    return d

FIRMA_LD = {
    '@type': 'HomeAndConstructionBusiness', '@id': FIRMA, 'name': 'WERMONT – Meble Na Wymiar', 'alternateName': 'Wermont',
    'description': 'Stolarnia w Skorzewie pod Kościerzyną. Kuchnie, szafy, garderoby i meble łazienkowe na wymiar – projekt, produkcja i montaż.',
    'url': BASE, 'logo': BASE + 'apple-touch-icon.png', 'image': BASE + 'img/og.jpg', 'telephone': TEL, 'email': MAIL, 'vatID': 'PL5911676414',
    'priceRange': '$$', 'address': {'@type': 'PostalAddress', 'streetAddress': 'ul. Kościelna 18', 'postalCode': '83-400', 'addressLocality': 'Skorzewo', 'addressRegion': 'pomorskie', 'addressCountry': 'PL'},
    'geo': {'@type': 'GeoCoordinates', 'latitude': 54.16434, 'longitude': 17.97402},
    'hasMap': 'https://www.google.com/maps/place/Wermont+-+Meble+Na+Wymiar/@54.1634075,17.9769177,17z',
    'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '08:00', 'closes': '18:00'}],
    'areaServed': [{'@type': 'City', 'name': v[0]} for v in MIASTA.values()] + [{'@type': 'AdministrativeArea', 'name': 'województwo pomorskie'}],
    'sameAs': ['https://www.facebook.com/wermontmeblenawymiar/', 'https://www.instagram.com/wermont_meblenawymiar/'],
    'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Meble na wymiar', 'itemListElement': [
        {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n, 'url': BASE + s + '/'}} for s, n, _ in USLUGI]},
}
WITRYNA_LD = {'@type': 'WebSite', '@id': BASE + '#witryna', 'url': BASE, 'name': 'Wermont – Meble Na Wymiar', 'inLanguage': 'pl-PL', 'publisher': {'@id': FIRMA}}
SITEMAP = []

def hero_sub(R, crumbs, h1, lead, foto, extra=''):
    return f'''<section class="page-hero"><div class="wrap ph-grid"><div class="ph-text">{breadcrumbs(crumbs, R)}
<h1>{e(h1)}</h1>{f'<p class="lead">{lead}</p>' if lead else ''}{extra}
<div class="actions"><a class="btn btn-main" href="{R}kontakt/#zapytanie">Umów bezpłatny pomiar</a><a class="btn btn-sec" href="tel:{TEL}">{TEL_H}</a></div></div>
<figure class="ph-photo">{img(foto, "(min-width: 1000px) 46vw, 100vw", R, eager=True)}</figure></div></section>'''

def galeria(keys, R, tytul='Z naszych realizacji'):
    if not keys: return ''
    f = ''.join(f'<figure>{img(k, "(min-width: 1000px) 25vw, 50vw", R)}</figure>' for k in keys)
    return f'<section class="sec sec-linen sec-tight"><div class="wrap"><div class="gal-head"><h2>{tytul}</h2><a href="{R}realizacje/">Wszystkie realizacje</a></div><div class="gallery">{f}</div></div></section>'

def linki(tytul, items, R):
    if not items: return ''
    return f'<nav class="rel" aria-label="{e(tytul)}"><h2>{e(tytul)}</h2><ul>' + ''.join(f'<li><a href="{R}{p}">{e(n)}</a></li>' for n, p in items) + '</ul></nav>'

# ---------------------------------------------------------------- uslugi
for slug, nazwa, fotos in USLUGI:
    d, path = T(slug), slug + '/'
    R = rel(path)
    crumbs = [('Strona główna', ''), (nazwa, path)]
    lead, body, rest = tresc(d['blocks'], R, fotos[1:])
    lok = [(f'{n} {MIASTA[m][0]}', s + '/') for s, n, typ, m in LOKALNE
           if (typ == 'kuchnie' and 'kuchen' in slug) or (typ == 'szafy' and 'szaf' in slug) or (typ == 'lazienki' and 'lazienk' in slug)]
    inne = [(n, s + '/') for s, n, _ in USLUGI if s != slug]
    b = hero_sub(R, crumbs, d['h1'], lead, fotos[0])
    b += f'''<section class="sec"><div class="wrap art-grid"><article class="prose">{body}</article>
<div class="side">{aside_card(R)}{opinia(len(slug))}</div></div></section>'''
    b += galeria(rest[:4] if len(rest) >= 4 else (rest + [k for k in FOTO_TYP['kuchnie'] if k not in fotos])[:4], R)
    b += faq_html(d['faq'])
    b += f'<section class="sec sec-tight"><div class="wrap rel-grid">{linki("Gdzie robimy " + nazwa.lower(), lok, R)}{linki("Zobacz też", inne, R)}</div></section>'
    b += cta_band(R)
    g = [webpage(path, d['title']), crumbs_ld(crumbs, path),
         {'@type': 'Service', '@id': BASE + path + '#usluga', 'name': d['h1'], 'serviceType': nazwa, 'provider': {'@id': FIRMA},
          'areaServed': {'@type': 'AdministrativeArea', 'name': 'województwo pomorskie'}, 'url': BASE + path,
          'image': BASE + f'img/{fotos[0]}-{WYM[fotos[0]][2][-1]}.webp'}]
    if d['faq']: g.append(faq_ld(d['faq'], path))
    akt = {'meble-kuchenne': 'meble-kuchenne/', 'garderoby-i-szafy': 'garderoby-i-szafy/', 'meble-lazienkowe': 'meble-lazienkowe/', 'fronty-meblowe': 'fronty-meblowe/'}.get(slug, '')
    zapisz(path, strona(path, d['title'], d['desc'], b, g, R, (fotos[0], '(min-width: 1000px) 46vw, 100vw'), akt, og=fotos[0]))
    SITEMAP.append((path, '0.8'))

# ---------------------------------------------------------------- strony lokalne
for slug, nazwa, typ, m in LOKALNE:
    d, path = T(slug), slug + '/'
    R = rel(path)
    mian, miejsc, grp = MIASTA[m]
    crumbs = [('Strona główna', ''), ('Zakres działania', 'zakres-dzialania/'), (d['h1'], path)]
    fotos = pick(FOTO_TYP[typ], slug, 6)
    lead, body, rest = tresc(d['blocks'], R, fotos[1:])
    lead = lead or lead_z_opisu(d)
    sasiedzi = [(f'{n} {MIASTA[mm][0]}', s + '/') for s, n, t2, mm in LOKALNE if s != slug and (mm == m or MIASTA[mm][2] == grp)][:8]
    usl = {'kuchnie': ['meble-kuchenne', 'projektowanie-mebli', 'fronty-meblowe'], 'szafy': ['garderoby-i-szafy', 'szafy-w-skosie'],
           'lazienki': ['meble-lazienkowe', 'fronty-meblowe'], 'meble': ['meble-kuchenne', 'garderoby-i-szafy', 'meble-lazienkowe', 'szafy-w-skosie']}[typ]
    usl = [(n, s + '/') for s, n, _ in USLUGI if s in usl]
    b = hero_sub(R, crumbs, d['h1'], lead, fotos[0], f'<p class="ph-meta">Stolarnia: ul. Kościelna 18, Skorzewo · pomiar {e(miejsc)} bezpłatny</p>')
    b += f'''<section class="sec"><div class="wrap art-grid"><article class="prose">{body}</article>
<div class="side">{aside_card(R, miejsc)}{opinia(len(slug))}</div></div></section>'''
    b += galeria(rest[:4] if len(rest) >= 4 else pick(FOTO_TYP['meble'], slug + 'g', 4), R, 'Meble z naszej stolarni')
    b += faq_html(d['faq'])
    b += f'<section class="sec sec-tight"><div class="wrap rel-grid">{linki("W tej okolicy robimy też", sasiedzi, R)}{linki("Oferta", usl, R)}</div></section>'
    b += cta_band(R, f'Bezpłatny pomiar {miejsc}')
    g = [webpage(path, d['title']), crumbs_ld(crumbs, path),
         {'@type': 'Service', '@id': BASE + path + '#usluga', 'name': d['h1'], 'serviceType': nazwa, 'provider': {'@id': FIRMA},
          'areaServed': {'@type': 'City', 'name': mian}, 'url': BASE + path}]
    if d['faq']: g.append(faq_ld(d['faq'], path))
    zapisz(path, strona(path, d['title'], d['desc'], b, g, R, (fotos[0], '(min-width: 1000px) 46vw, 100vw'), og=fotos[0]))
    SITEMAP.append((path, '0.6'))

# ---------------------------------------------------------------- poradniki
lista = ''
for i, slug in enumerate(WPISY):
    d, path = T(slug), slug + '/'
    R = rel(path)
    crumbs = [('Strona główna', ''), ('Poradniki', 'category/poradniki/'), (d['h1'], path)]
    fotos = WPIS_FOTO[slug]
    lead, body, _ = tresc(d['blocks'], R, fotos[1:], wstaw_co=2)
    pub, mod = DATY[slug]
    slow = len(re.sub('<[^>]+>', ' ', body).split())
    fmt = lambda s: f'{int(s[8:])}.{s[5:7]}.{s[:4]}'
    b = f'''<article class="post"><header class="wrap post-head">{breadcrumbs(crumbs, R)}<h1>{e(d['h1'])}</h1>
<p class="post-meta">Poradnik · <time datetime="{mod}">aktualizacja {fmt(mod)}</time> · ok. {max(1, round(slow / 200))} min czytania</p>
{f'<p class="lead">{lead}</p>' if lead else ''}</header>
<figure class="post-photo wrap">{img(fotos[0], "(min-width: 1000px) 1000px, 100vw", R, eager=True)}</figure>
<div class="wrap art-grid"><div class="prose">{body}</div><div class="side">{aside_card(R)}</div></div></article>'''
    b += cta_band(R)
    g = [webpage(path, d['title'], crumbs=True), crumbs_ld(crumbs, path),
         {'@type': 'BlogPosting', '@id': BASE + path + '#wpis', 'headline': d['h1'], 'description': d['desc'], 'datePublished': pub, 'dateModified': mod,
          'author': {'@id': FIRMA}, 'publisher': {'@id': FIRMA}, 'mainEntityOfPage': {'@id': BASE + path + '#strona'}, 'inLanguage': 'pl-PL',
          'image': BASE + f'img/{fotos[0]}-{WYM[fotos[0]][2][-1]}.webp', 'wordCount': slow}]
    zapisz(path, strona(path, d['title'], d['desc'], b, g, R, (fotos[0], '(min-width: 1000px) 1000px, 100vw'), og=fotos[0]))
    SITEMAP.append((path, '0.5'))
    lista += f'''<article class="card"><a href="../../{path}">{img(fotos[0], "(min-width: 1000px) 33vw, 100vw", "../../")}
<h2>{e(d['h1'])}</h2></a><p>{e(d['desc'])}</p><p class="post-meta"><time datetime="{mod}">{fmt(mod)}</time></p></article>'''

path = 'category/poradniki/'; R = rel(path); d = T('poradniki')
crumbs = [('Strona główna', ''), ('Poradniki', path)]
b = f'<section class="sec sec-first"><div class="wrap">{breadcrumbs(crumbs, R)}<h1>Poradniki</h1><p class="lead narrow">Jak wybrać fronty, jak powstaje kuchnia na wymiar i co warto wiedzieć przed pomiarem – piszemy z perspektywy stolarni.</p><div class="cards">{lista}</div></div></section>' + cta_band(R)
zapisz(path, strona(path, d['title'], d['desc'], b, [webpage(path, d['title'], 'CollectionPage'), crumbs_ld(crumbs, path)], R, akt=path))
SITEMAP.append((path, '0.4'))

# ---------------------------------------------------------------- proces realizacji
path = 'proces-realizacji/'; R = rel(path); d = T('proces-realizacji')
crumbs = [('Strona główna', ''), ('Proces realizacji', path)]
etapy_ul = next(b for b in d['blocks'] if b['t'] == 'ul')['items']
def etap(t):
    m = re.match(r'(\d)\s+(.+?)\s+(Bezpłatnie\s+)?([A-ZŁŚŻ].*)$', t)
    return m.group(1), m.group(2), m.group(4)
etapy = []
for t in etapy_ul:
    nr, rest_ = t.split(' ', 1)
    zd = re.split(r'(?<=[a-ząęółśżźćń])\s(?=[A-ZŁŚŻŹĆ])', rest_, 1)
    etapy.append((nr, zd[0], zd[1] if len(zd) > 1 else ''))
lead = next(b['h'] for b in d['blocks'] if b['t'] == 'p')
et = ''.join(f'<li><h3>{e(t)}</h3><p>{e(o)}</p></li>' for _, t, o in etapy)
std = [b for b in d['blocks'] if b['t'] == 'p' and re.match(r'(Obrzeże ABS|Więcej przestrzeni|Fundament)', b['x'])]
okucia, cur = [], None
blk = d['blocks']; i0 = next(i for i, b in enumerate(blk) if b.get('x', '').startswith('Okucia, które'))
for b in blk[i0 + 1:]:
    if b['t'] == 'h2': break
    if b['t'] == 'h3': cur = {'n': b['x'], 'o': '', 'l': []}; okucia.append(cur)
    elif cur and b['t'] == 'p' and not cur['o']: cur['o'] = b['x']
    elif cur and b['t'] == 'ul': cur['l'] = b['items']
ok_html = ''.join(f'<div class="spec-card"><h3>{e(o["n"])}</h3><p>{e(o["o"])}</p><ul>' + ''.join(f'<li>{e(x)}</li>' for x in o['l']) + '</ul></div>' for o in okucia)
b = f'''<section class="page-hero"><div class="wrap ph-grid"><div class="ph-text">{breadcrumbs(crumbs, R)}<h1>{e(d['h1'])}</h1><p class="lead">{lead}</p>
<div class="actions"><a class="btn btn-main" href="{R}kontakt/#zapytanie">Umów bezpłatny pomiar</a></div></div>
<figure class="ph-photo">{img('pomiar', "(min-width: 1000px) 46vw, 100vw", R, eager=True)}</figure></div></section>
<section class="sec"><div class="wrap"><h2>Pięć etapów – od pomiaru do montażu</h2><ol class="steps steps-5">{et}</ol></div></section>
<section class="sec sec-linen"><div class="wrap two"><div><h2>Detale, których nie widać na pierwszy rzut oka</h2>
<figure class="in-fig">{img('kuchnia-szuflady', "(min-width: 1000px) 40vw, 100vw", R)}</figure></div>
<div class="prose">{''.join(f'<p>{b_["h"]}</p>' for b_ in std)}</div></div></section>
<section class="sec"><div class="wrap"><h2>Okucia, które proponujemy w wycenach</h2><div class="spec-cards">{ok_html}</div></div></section>'''
b += faq_html(d['faq']) + cta_band(R)
zapisz(path, strona(path, d['title'], d['desc'], b, [webpage(path, d['title']), crumbs_ld(crumbs, path), faq_ld(d['faq'], path)], R, ('pomiar', '(min-width: 1000px) 46vw, 100vw'), path))
SITEMAP.append((path, '0.7'))

# ---------------------------------------------------------------- zakres dzialania
path = 'zakres-dzialania/'; R = rel(path); d = T('zakres-dzialania')
crumbs = [('Strona główna', ''), ('Zakres działania', path)]
opisy = {}
for i, bb in enumerate(d['blocks']):
    if bb['t'] == 'h3': opisy[bb['x']] = d['blocks'][i + 1]['h']
wiersze = ''
for gk, gn in GRUPY.items():
    mm = [m for m, v in MIASTA.items() if v[2] == gk]
    rows = ''
    for m in mm:
        strony = [(n, s) for s, n, t2, m2 in LOKALNE if m2 == m]
        rows += f'<tr><th scope="row">{e(MIASTA[m][0])}</th><td>' + ' · '.join(f'<a href="{R}{s}/">{e(n)}</a>' for n, s in strony) + '</td></tr>'
    op = next((v for k, v in opisy.items() if k.split(':')[0].split(' ')[0] in gn), '')
    wiersze += f'<div class="area-grp"><h2>{e(gn)}</h2>{f"<p>{op}</p>" if op else ""}<div class="tbl"><table><tbody>{rows}</tbody></table></div></div>'
wstep = next(bb['h'] for bb in d['blocks'] if bb.get('x', '').startswith('Nasza stolarnia'))
b = f'''<section class="sec sec-first"><div class="wrap">{breadcrumbs(crumbs, R)}<h1>Zakres działania</h1><p class="lead narrow">{wstep}</p>
<div class="areas">{wiersze}</div><p class="callout">Twojej miejscowości nie ma na liście? Zadzwoń: <a href="tel:{TEL}">{TEL_H}</a> – dojeżdżamy na pomiary na całym Pomorzu.</p></div></section>''' + cta_band(R)
zapisz(path, strona(path, d['title'], d['desc'], b, [webpage(path, d['title']), crumbs_ld(crumbs, path)], R))
SITEMAP.append((path, '0.6'))

# ---------------------------------------------------------------- o nas
path = 'o-nas/'; R = rel(path); d = T('o-nas')
crumbs = [('Strona główna', ''), ('O nas', path)]
ps = [bb['h'] for bb in d['blocks'] if bb['t'] == 'p'][:2]
ul = next(bb['items'] for bb in d['blocks'] if bb['t'] == 'ul')
lst = ''.join('<li><strong>' + e(x.split(':', 1)[0]) + '</strong>' + (e(':' + x.split(':', 1)[1]) if ':' in x else '') + '</li>' for x in ul)
b = hero_sub(R, crumbs, d['h1'], ps[0], 'kuchnia-dab-okno-2')
b += f'''<section class="sec"><div class="wrap two"><h2>Stolarstwo i technologia w jednym warsztacie</h2><div class="prose"><p>{ps[1]}</p><ul class="list">{lst}</ul></div></div></section>
<section class="sec sec-dark"><div class="wrap"><h2>Co piszą klienci</h2><p class="rev-sub">Ocena 5,0 na 5 w Google na podstawie 41 opinii.</p><div class="reviews">{''.join(opinia(i) for i in range(3))}</div></div></section>'''
b += galeria(['kuchnia-orzech-wyspa', 'szafa-wneka', 'lazienka-dab', 'kuchnia-granat'], R) + cta_band(R)
zapisz(path, strona(path, d['title'], d['desc'], b, [webpage(path, d['title'], 'AboutPage'), crumbs_ld(crumbs, path)], R, ('kuchnia-dab-okno-2', '(min-width: 1000px) 46vw, 100vw'), path))
SITEMAP.append((path, '0.5'))

# ---------------------------------------------------------------- realizacje
path = 'realizacje/'; R = rel(path); d = T('realizacje')
crumbs = [('Strona główna', ''), ('Realizacje', path)]
grupy = [('Kuchnie na wymiar', [k for k in ZDJ if k.startswith(('kuchnia', 'bezuchwyt'))]),
         ('Szafy, garderoby i zabudowy', [k for k in ZDJ if k.startswith(('szafa', 'garderoba'))]),
         ('Meble łazienkowe', [k for k in ZDJ if k.startswith('lazienka')])]
sek = ''
for n, ks in grupy:
    sek += f'<h2 class="gal-h">{e(n)} <span>{len(ks)} zdjęć</span></h2><div class="gallery gallery-all">' + ''.join(
        f'<figure>{img(k, "(min-width: 1000px) 25vw, 50vw", R)}</figure>' for k in ks) + '</div>'
wst = d['blocks'][0]['h'].replace('{R}', R)
b = f'<section class="sec sec-first"><div class="wrap">{breadcrumbs(crumbs, R)}<h1>{e(d["h1"])}</h1><p class="lead narrow">{wst}</p>{sek}</div></section>' + cta_band(R, 'Chcesz podobne wnętrze u siebie?')
zapisz(path, strona(path, d['title'], d['desc'], b, [webpage(path, d['title'], 'CollectionPage'), crumbs_ld(crumbs, path)], R, akt=path))
SITEMAP.append((path, '0.7'))

# ---------------------------------------------------------------- formularz
def formularz():
    return '''<form class="form" id="quote" novalidate><h2 id="zapytanie">Zapytanie o meble</h2>
<fieldset class="field"><legend>Jakie meble Cię interesują?</legend><div class="choice choice-2">
<label><input type="radio" name="type" value="Kuchnia">Kuchnia</label><label><input type="radio" name="type" value="Szafa lub garderoba">Szafa lub garderoba</label>
<label><input type="radio" name="type" value="Meble łazienkowe">Meble łazienkowe</label><label><input type="radio" name="type" value="Kilka pomieszczeń">Kilka pomieszczeń</label></div></fieldset>
<label class="field"><span>Imię</span><input name="name" autocomplete="given-name" required></label>
<label class="field"><span>Telefon</span><input name="tel" type="tel" autocomplete="tel" inputmode="tel" required></label>
<label class="field"><span>Miejscowość</span><input name="place" autocomplete="address-level2"></label>
<label class="field"><span>Kilka słów o pomieszczeniu (opcjonalnie)</span><textarea name="msg" rows="3"></textarea></label>
<label class="consent"><input type="checkbox" name="ok" required><span>Zgadzam się na kontakt w sprawie zapytania. Zasady w <a href="{R}polityka-prywatnosci/">polityce prywatności</a>.</span></label>
<button class="btn btn-main btn-full" type="submit">Wyślij zapytanie</button><p class="form-msg" role="status" aria-live="polite"></p></form>'''

def kontakt_blok(R, h='h2'):
    return f'''<div class="contact-grid"><div><{h} id="h-kontakt">Umów bezpłatny pomiar</{h}>
<p class="contact-lead">Zadzwoń albo zostaw numer w formularzu. Oddzwonimy i ustalimy termin pomiaru.</p>
<address class="nap"><a class="tel" href="tel:{TEL}">{TEL_H}</a><a href="mailto:{MAIL}">{MAIL}</a>
<span>WERMONT – Meble Na Wymiar<br>ul. Kościelna 18, 83-400 Skorzewo</span><span class="hours">Poniedziałek–piątek: 8:00–18:00</span></address>
<div class="map" data-src="https://www.openstreetmap.org/export/embed.html?bbox=17.954%2C54.154%2C17.994%2C54.174&amp;layer=mapnik&amp;marker=54.16434%2C17.97402">
<button type="button" class="map-btn">Pokaż mapę dojazdu</button>
<a href="https://www.google.com/maps/place/Wermont+-+Meble+Na+Wymiar/@54.1634075,17.9769177,17z" target="_blank" rel="noopener">Wyznacz trasę w Mapach Google</a></div></div>
{formularz().replace('{R}', R)}</div>'''

path = 'kontakt/'; R = rel(path); d = T('kontakt')
crumbs = [('Strona główna', ''), ('Kontakt', path)]
b = f'''<section class="sec sec-first"><div class="wrap">{breadcrumbs(crumbs, R)}<h1>Kontakt</h1>{kontakt_blok(R)}
<p class="area">Dojeżdżamy na pomiary w Kościerzynie i okolicy, w Kartuzach, Żukowie, Bytowie, Lęborku i w całym Trójmieście – zobacz <a href="{R}zakres-dzialania/">zakres działania</a>.</p></div></section>'''
zapisz(path, strona(path, d['title'], d['desc'], b, [FIRMA_LD, webpage(path, d['title'], 'ContactPage'), crumbs_ld(crumbs, path)], R, akt=path))
SITEMAP.append((path, '0.7'))

# ---------------------------------------------------------------- polityka
path = 'polityka-prywatnosci/'; R = rel(path)
crumbs = [('Strona główna', ''), ('Polityka prywatności', path)]
b = f'''<section class="sec sec-first"><div class="wrap doc">{breadcrumbs(crumbs, R)}<h1>Polityka prywatności</h1>
<h2>Administrator danych</h2><p>Administratorem danych osobowych jest WERMONT – Meble Na Wymiar, ul. Kościelna 18, 83-400 Skorzewo, NIP 591-167-64-14, tel. {TEL_H}, e-mail: {MAIL}.</p>
<h2>Jakie dane i po co</h2><p><strong>Zapytanie o meble.</strong> Imię, telefon, miejscowość, rodzaj mebli i treść wiadomości. Przetwarzamy je, żeby odpowiedzieć na zapytanie, umówić pomiar i przygotować wycenę (art. 6 ust. 1 lit. b RODO).</p>
<h2>Jak długo</h2><p>Dane z zapytania przechowujemy przez czas potrzebny na przygotowanie oferty i realizację umowy, a potem przez okres wymagany przepisami, np. podatkowymi.</p>
<h2>Twoje prawa</h2><p>Masz prawo dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przeniesienia oraz wniesienia sprzeciwu. Możesz też złożyć skargę do Prezesa Urzędu Ochrony Danych Osobowych.</p>
<h2>Pliki cookies</h2><p>Strona nie używa plików cookies do celów reklamowych ani analitycznych. Mapa dojazdu z serwisu OpenStreetMap ładuje się dopiero po kliknięciu.</p></div></section>'''
zapisz(path, strona(path, 'Polityka prywatności – Wermont Meble Na Wymiar', 'Polityka prywatności WERMONT – Meble Na Wymiar, Skorzewo.', b, [webpage(path, 'Polityka prywatności'), crumbs_ld(crumbs, path)], R))
SITEMAP.append((path, '0.1'))

# ---------------------------------------------------------------- strona glowna
path = ''; R = ''; d = T('home')
tab = next(bb for bb in d['blocks'] if bb['t'] == 'table')['rows']
tab_html = ('<div class="tbl tbl-cmp"><table><thead><tr>' + ''.join(f'<th scope="col">{e(c)}</th>' for c in tab[0]) + '</tr></thead><tbody>' +
            ''.join(f'<tr><th scope="row">{e(r[0])}</th><td>{e(r[1])}</td><td>{e(r[2])}</td></tr>' for r in tab[1:]) + '</tbody></table></div>')
oferta = [('meble-kuchenne', 'Kuchnie na wymiar', 'kuchnia-orzech-wyspa', 'Układ, fronty i okucia pod Twoje pomieszczenie. Kuchnie z MDF, z drewna, bezuchwytowe.'),
          ('garderoby-i-szafy', 'Szafy i garderoby', 'szafa-wneka', 'Szafy wnękowe, garderoby i zabudowy przedpokoju na całą wysokość ściany.'),
          ('meble-lazienkowe', 'Meble łazienkowe', 'lazienka-dab', 'Szafki podwieszane i podumywalkowe z obrzeżem ABS z trzech stron.'),
          ('szafy-w-skosie', 'Szafy w skosie', 'szafa-skos', 'Zabudowa poddasza docinana pod kąt dachu, bez martwych trójkątów.'),
          ('fronty-meblowe', 'Fronty meblowe', 'kuchnia-granat-zabudowa', 'Lakier RAL i NCS, akryl, drewno i fornir – do nowych mebli i na wymianę.'),
          ('projektowanie-mebli', 'Projekt z wizualizacją', 'wizualizacja', 'Projekt w PaletteCAD, poprawiany razem z Tobą, zanim cokolwiek trafi na maszynę.')]
of_html = ''.join(f'<a class="off" href="{s}/">{img(k, "(min-width: 1000px) 30vw, (min-width: 600px) 45vw, 100vw", R)}<h3>{e(n)}</h3><p>{e(o)}</p></a>' for s, n, k, o in oferta)
lok_k = ''.join(f'<li><a href="{s}/">{e(MIASTA[m][0])}</a></li>' for s, n, t2, m in LOKALNE if t2 == 'kuchnie')
lok_m = ''.join(f'<li><a href="{s}/">{e(MIASTA[m][0])}</a></li>' for s, n, t2, m in LOKALNE if t2 == 'meble')
wpisy = ''.join(f'<li><a href="{s}/">{e(T(s)["h1"])}</a></li>' for s in WPISY)
b = f'''<section class="hero"><div class="wrap hero-grid"><div class="hero-text">
<p class="hero-place">Stolarnia w Skorzewie pod Kościerzyną</p>
<h1>Meble na wymiar od producenta – Kościerzyna, Trójmiasto, Pomorskie</h1>
<p class="lead">Kuchnie, szafy, garderoby i meble łazienkowe. Mierzymy u Ciebie, projektujemy w PaletteCAD, tniemy na własnym CNC i montujemy naszą ekipą.</p>
<div class="actions"><a class="btn btn-main" href="kontakt/#zapytanie">Umów bezpłatny pomiar</a><a class="btn btn-sec" href="tel:{TEL}">Zadzwoń: {TEL_H}</a></div>
<p class="hero-note">Ocena 5,0 w Google z 41 opinii · cenę podajemy na pierwszym spotkaniu</p></div>
<figure class="hero-photo">{img('kuchnia-orzech-wyspa', "(min-width: 1000px) 44vw, 100vw", R, eager=True)}</figure></div></section>

<section class="sec"><div class="wrap two"><h2>Producent, nie pośrednik</h2><div class="intro-text">
<p>Wermont to lokalna stolarnia ze Skorzewa. Nie sprzedajemy mebli z katalogu i nie oddajemy zleceń podwykonawcom. Pomiar robimy u Ciebie w domu, projekt rysujemy sami, płyty tniemy na własnej maszynie CNC, a meble montuje nasza ekipa.</p>
<p>Dzięki temu rozmawiasz z ludźmi, którzy naprawdę robią Twoją kuchnię. Po umówieniu możesz przyjechać do warsztatu i obejrzeć próbki frontów, okucia i to, jak budujemy korpusy.</p>
<dl class="facts"><dt>Stolarnia</dt><dd>ul. Kościelna 18, 83-400 Skorzewo</dd><dt>Gdzie pracujemy</dt><dd>Kościerzyna i okolice, Kaszuby, Trójmiasto</dd>
<dt>Pomiar i wycena</dt><dd>bezpłatnie, cenę podajemy na pierwszym spotkaniu</dd><dt>Biuro</dt><dd>poniedziałek–piątek, 8:00–18:00</dd></dl></div></div></section>

<section class="sec sec-linen" id="oferta"><div class="wrap"><div class="sec-head"><h2>Co robimy</h2><p>Każdy mebel powstaje pod konkretne pomieszczenie: pod skos, wnękę, grzejnik w złym miejscu albo ścianę, która nie trzyma pionu.</p></div>
<div class="offers">{of_html}</div></div></section>

<section class="sec"><div class="wrap"><div class="sec-head"><h2>Meble gotowe a meble od Wermont</h2><p>Dwie kuchnie mogą wyglądać tak samo w dniu montażu. Różnica wychodzi po kilku latach: w szufladach, w narożniku i w krawędziach przy zlewie.</p></div>
{tab_html}</div></section>

<section class="sec sec-linen"><div class="wrap project"><figure class="project-photo">{img('wizualizacja', "(min-width: 1000px) 40vw, 100vw", R)}<figcaption>Wizualizacja kuchni przygotowana przed produkcją</figcaption></figure>
<div><h2>Kuchnię zobaczysz, zanim ją wytniemy</h2><p>Projekt robimy w programie PaletteCAD. Na wizualizacji widać układ szafek, kolory frontów, blat i oświetlenie, a nie tylko rysunek techniczny.</p>
<p>Projekt poprawiamy razem z Tobą w trzech turach, aż wszystko się zgadza: wysokości, szuflady, miejsce na sprzęt i budżet. Do produkcji idzie dokładnie to, co zaakceptujesz.</p>
<p><a href="proces-realizacji/">Zobacz pięć etapów realizacji</a></p></div></div></section>

<section class="sec"><div class="wrap"><div class="gal-head"><h2>Nasze realizacje</h2><a href="realizacje/">Wszystkie realizacje</a></div>
<div class="gallery">{''.join(f'<figure>{img(k, "(min-width: 1000px) 25vw, 50vw", R)}</figure>' for k in ['kuchnia-dab-okno', 'kuchnia-granat', 'kuchnia-cegla', 'lazienka-kamien', 'kuchnia-dab-b', 'szafa-szara', 'kuchnia-witryna', 'kuchnia-orzech-blat'])}</div></div></section>

<section class="sec sec-dark"><div class="wrap"><h2>Co piszą klienci</h2><p class="rev-sub">Ocena 5,0 na 5 w Google na podstawie 41 opinii. Poniżej trzy z nich.</p><div class="reviews">{''.join(opinia(i) for i in range(3))}</div></div></section>

<section class="sec"><div class="wrap"><h2>Jak pracujemy</h2><ol class="steps">
<li><h3>Pomiar i wycena</h3><p>Przyjeżdżamy, mierzymy dalmierzem laserowym i podajemy konkretną cenę już na tym spotkaniu. Bezpłatnie.</p></li>
<li><h3>Projekt z wizualizacją</h3><p>Rysujemy meble w PaletteCAD i poprawiamy projekt razem z Tobą, zanim cokolwiek trafi na maszynę.</p></li>
<li><h3>Produkcja w Skorzewie</h3><p>Meble powstają w naszej stolarni. Aktualny termin realizacji podajemy przy umawianiu pomiaru.</p></li>
<li><h3>Montaż</h3><p>Montuje nasza ekipa. Regulujemy fronty i sprzątamy po sobie.</p></li></ol></div></section>

<section class="sec sec-linen sec-tight"><div class="wrap loc-grid"><div><h2>Gdzie pracujemy</h2><p>Stolarnia jest w Skorzewie pod Kościerzyną. Na pomiary dojeżdżamy na Kaszuby, do Trójmiasta i dalej po Pomorzu. <a href="zakres-dzialania/">Pełny zakres działania</a></p></div>
<div><h3>Kuchnie na wymiar</h3><ul class="chips">{lok_k}</ul></div><div><h3>Meble na wymiar</h3><ul class="chips">{lok_m}</ul></div></div></section>

{faq_html(d['faq'], 'Najczęstsze pytania')}

<section class="sec sec-tight"><div class="wrap"><nav class="rel" aria-label="Poradniki"><h2>Z poradników</h2><ul>{wpisy}</ul></nav></div></section>

<section class="sec sec-linen" id="kontakt"><div class="wrap">{kontakt_blok(R)}</div></section>'''
zapisz('', strona('', d['title'], d['desc'], b, [FIRMA_LD, WITRYNA_LD, webpage('', d['title'], crumbs=False), faq_ld(d['faq'], '')], R, ('kuchnia-orzech-wyspa', '(min-width: 1000px) 44vw, 100vw')))
SITEMAP.insert(0, ('', '1.0'))

# ---------------------------------------------------------------- 404, sitemap, robots
p404 = strona('404', 'Nie ma takiej strony | Wermont – Meble Na Wymiar', 'Strona nie istnieje.',
              f'''<section class="sec sec-first"><div class="wrap doc"><h1>Nie ma takiej strony</h1><p class="lead">Adres mógł się zmienić. Zacznij od strony głównej albo zadzwoń: <a href="tel:{TEL}">{TEL_H}</a>.</p>
<div class="actions"><a class="btn btn-main" href="{BASE}">Strona główna</a><a class="btn btn-sec" href="{BASE}realizacje/">Realizacje</a></div></div></section>''', [], BASE)
p404 = p404.replace('<link rel="canonical" href="' + BASE + '404">', '').replace('content="noindex, follow"', 'content="noindex"')
open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8', newline='\n').write(p404)
DZIS = '2026-09-26'
sm = ''.join(f'<url><loc>{BASE}{p}</loc><lastmod>{DZIS}</lastmod><priority>{pr}</priority></url>\n' for p, pr in SITEMAP)
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
open(os.path.join(ROOT, 'robots.txt'), 'w', newline='\n').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
print(len(SITEMAP), 'stron;', 'DEMO' if DEMO else 'PRODUKCJA', BASE)
