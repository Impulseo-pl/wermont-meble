"""Robi img/<klucz>-<szer>.webp (480/960/1600, bez powiekszania) z oryginalow z wermont.eu.
Uzycie: python zdjecia_webp.py <katalog z oryginalami>. Zapisuje _src/wymiary.json (klucz -> [szer, wys, [szerokosci]])."""
import sys, os, json
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(__file__))
from zdjecia import ZDJ

SRC = sys.argv[1]
ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'img')
os.makedirs(OUT, exist_ok=True)
wym = {}
for k, (plik, alt, poz) in ZDJ.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, plik))).convert('RGB')
    w, h = im.size
    szer = [s for s in (480, 960, 1600) if s < w] + ([w] if w <= 1600 else [])
    szer = sorted(set(szer))[:3]
    for s in szer:
        r = im.resize((s, round(h * s / w)), Image.LANCZOS) if s != w else im
        r.save(os.path.join(OUT, f'{k}-{s}.webp'), 'WEBP', quality=78, method=6)
    wym[k] = [w, h, szer]
    print(k, w, h, szer)
json.dump(wym, open(os.path.join(os.path.dirname(__file__), 'wymiary.json'), 'w'), indent=0)
