# Wermont – Meble Na Wymiar — demo

Lead: **Paweł**, WERMONT – Meble Na Wymiar, +48 732 139 879, biuro@wermont.eu,
ul. Kościelna 18, 83-400 Skorzewo (pod Kościerzyną, pomorskie). NIP 591-167-64-14.
Obecna strona: https://wermont.eu/ (WordPress/Avada, zrobiona przez Red Baron Support). CRM: `4c333db3-b7bf-43b3-acac-38ce9e4d46c3`.

Podgląd lokalny: `python -m http.server 8123`. Sprawdzanie opublikowanego dema przez nas — **zawsze z `?team=1`**.

## v2 (26.09.2026) — pełna struktura strony klienta, pod techniczne SEO

Klient ma już rozbudowaną stronę pod SEO (WordPress/Avada + Yoast, 43 adresy, w tym 24 lokalne landingi i 3 wpisy).
Dlatego v2 to **nie wizytówka, tylko przeniesienie całej struktury**: każdy z 43 adresów wermont.eu istnieje w demie
pod tą samą ścieżką (`/kuchnie-na-wymiar-gdansk/`, `/category/poradniki/` itd.), z treścią klienta (tytuły, opisy,
H1, akapity z linkami wewnętrznymi, FAQ), w nowym, lekkim szablonie. **Przy wdrożeniu nie trzeba ani jednego przekierowania 301.**

Generator: `python _src/build.py` (demo) albo `BASE=https://wermont.eu/ python _src/build.py` (produkcja: zdejmuje noindex,
przestawia canonical/og/JSON-LD/sitemap). Kontrola: `python _src/sprawdz.py` (H1, canonical, duplikaty title/description,
JSON-LD, martwe linki, alt/wymiary obrazów, pokrycie adresów starej strony). Treści: `_src/tresc/*.json`
(wyciągnięte z wermont.eu przez `_src/extract.py`), zdjęcia: `_src/zdjecia.py` (+ `zdjecia_webp.py`).

### Co jest technicznie lepsze niż na obecnej stronie
- CSS inline (0 blokujących plików), 1 skrypt (`defer`), fonty lokalne z preloadem, zero zewnętrznych skryptów przy wejściu
  (mapa OSM ładuje się dopiero po kliknięciu, bez GTM/Trustindex/jQuery).
- Obrazy WebP w 3 rozmiarach z `srcset`/`sizes`, `width`/`height` (CLS = 0), LCP z `preload` + `fetchpriority`.
- JSON-LD spięty w jeden graf przez `@id`: `HomeAndConstructionBusiness` (NAP, NIP, geo, godziny, 18 miejscowości),
  `WebSite`, `WebPage`/`AboutPage`/`ContactPage`/`CollectionPage`, `Service` na każdej usłudze i stronie lokalnej
  (z `areaServed` = konkretne miasto), `BreadcrumbList` wszędzie, `FAQPage` tam gdzie klient ma FAQ, `BlogPosting` z datami.
  Celowo bez `aggregateRating` (Google nie pokazuje gwiazdek z opinii o sobie na własnej stronie).
- Widoczne okruszki, sticky karta „Bezpłatny pomiar" na podstronach, linkowanie wewnętrzne: stopka z wszystkimi 24 stronami
  lokalnymi, bloki „W tej okolicy robimy też" i „Gdzie robimy…" (obecnie „Zobacz również" ma 3 linki).
- Zdjęcia: 56 realizacji klienta, nazwy plików opisowe (`kuchnia-orzech-wyspa-960.webp` zamiast `DSC_4080-scaled.jpg`), alt dla każdego.
  Stocki i rendery z obecnej strony (proj-1, kuchnia-mdf, lp1…) pominięte.

### Pomiar (ten sam dla obu, `_src/perf.py`: Playwright, telefon 412 px, 150 ms RTT / 1,6 Mb/s, CPU ×4, mediana z 3)
| | LCP | CLS | transfer | zapytania | zewn. domeny |
|---|---|---|---|---|---|
| wermont.eu — strona główna | 4,2 s | 0,19 | 1274 KB | 61 | 4 (GTM, GA, Trustindex, googleusercontent) |
| wermont.eu — /kuchnie-na-wymiar-gdansk/ | 6,9 s | 0,26 | 799 KB | 26 | 1 |
| **demo v3 — strona główna** (GitHub Pages, zdjęcie na całą szerokość) | **2,3–3,2 s** | **0,00** | 371 KB | 14 | 0 |
| **demo v3 — /kuchnie-na-wymiar-gdansk/** | **2,5 s** | **0,00** | 306 KB | 12 | 0 |

(v2 z mniejszym zdjęciem w hero miała 1,0–1,1 s; pełnoekranowe zdjęcie w v3 kosztuje ~1,5 s na Slow 4G.)
Progi Google (Core Web Vitals): LCP dobre ≤ 2,5 s, słabe > 4 s; CLS dobre ≤ 0,1, słabe > 0,25.
Uwaga: w Chrome preload fontu opóźniał pierwsze malowanie (FCP 3,5 s), dlatego fonty idą bez preloadu, a Karla z `font-display: optional`.
Strona klienta ma też długie „białe dziury” na zrzutach — elementy Avady animowane przy przewijaniu.

### Uczciwie o treści klienta
Treści lokalne klienta są dobre (unikalne, 1300–1900 słów, 6-gramowe podobieństwo między stronami ~10%) — więc sprzedajemy
**technikę i szybkość**, nie „napiszemy wam SEO od nowa”. Część stron ma powtórzoną sekcję (np. Gdańsk: „Kuchnie w gdańskich
kamienicach…” powtarza pierwszą) — do przeczyszczenia przy wdrożeniu.

## Założenia wyglądu (v3, 26.09 wieczorem — Szymon: „zmień projekt wizualny”)

Ciemny orzech (#231a14) w nagłówku, stopce, opiniach i panelach hero podstron; jasny papier i piasek w treści; jeden akcent
dębowy (#9a5b2c). Nagłówki **Newsreader** (z kursywą w akcencie), tekst **Hanken Grotesk**. Ostre krawędzie, bez zaokrągleń.
Strona główna: zdjęcie realizacji na całą szerokość (na telefonie inny, pionowy kadr), pasek 4 faktów, oferta w układzie
2 duże + 3 małe, **rysunek przekroju szafki 510 vs 560 mm w skali** (liczby z tabeli klienta), mozaika realizacji.
Podstrony: ciemny panel z H1 + zdjęcie do krawędzi ekranu, ciemna karta „Bezpłatny pomiar” przyklejona z boku.

## Skąd są fakty (zero zmyślonych liczb)

| Na stronie | Źródło |
|---|---|
| ul. Kościelna 18, 83-400 Skorzewo, NIP 591-167-64-14, tel., e-mail | stopka i /kontakt/ na wermont.eu |
| Godziny pn–pt 8:00–18:00 | wermont.eu/kontakt/ |
| Producent, nie pośrednik; własna stolarnia, CNC, własna ekipa montażowa | wermont.eu (strona główna, /o-nas/, /projektowanie-mebli/) |
| Bezpłatny pomiar i wycena, cena na pierwszym spotkaniu | wermont.eu (strona główna, /kontakt/) |
| Korpusy dolne 560 mm vs typowe 510 mm, ABS z 3 stron, Blum, Peka, Häfele Axilo do 150 kg | tabela porównawcza na stronie głównej wermont.eu, /meble-kuchenne/ |
| Okleiniarka krzywoliniowa, projekt w PaletteCAD, kilka tur poprawek | /meble-kuchenne/, /projektowanie-mebli/ |
| Fronty: lakier RAL/NCS, akryl, drewno lite/fornir, laminat | /fronty-meblowe/, /meble-kuchenne/ |
| Obszar: Kościerzyna i okolice, Kartuzy, Żukowo, Bytów, Lębork, Trójmiasto | /zakres-dzialania/ |
| Możliwość odwiedzenia warsztatu po umówieniu | /kuchnie-na-wymiar-skorzewo/ (FAQ) |
| Ocena 5,0/5 w Google z 41 opinii | widżet Trustindex na wermont.eu, stan z 26.09.2026 |
| 3 opinie (Daria Frąckiewicz, Marta Tchórzewska, Daria) | opinie Google cytowane na wermont.eu (skrócone „(…)”) |
| Termin realizacji — **bez liczby** („podajemy przy umawianiu pomiaru”) | tak pisze sam klient na stronie głównej |

## Do potwierdzenia z klientem (przed wdrożeniem)

1. **Liczba i ocena opinii Google** — 5,0 / 41 to stan z widżetu na 26.09.2026; przy wdrożeniu zaktualizować.
2. Zgoda autorek na cytowanie opinii z imienia i nazwiska (są publiczne w Google, ale lepiej mieć „tak” od klienta).
3. **Zdjęcia w pełnej rozdzielczości** — teraz pobrane z wermont.eu (część tylko 1500 px). Dobrze byłoby dostać zdjęcie
   stolarni/maszyn i ekipy — obecnie żadnego nie ma, a to najmocniejszy argument „producent, nie pośrednik”.
4. Czy wizualizacja w sekcji „Projekt” może zostać (ma znak wodny WERMONT) i czy pokazać obok zdjęcie tej samej kuchni po montażu.
5. **Sejfo-Meble** (sejfo-meble.pl) — w menu obecnej strony jest link do tej marki. Co to jest i czy ma być na nowej stronie.
6. Imię właściciela / osoby do kontaktu — na stronie nie podajemy nazwiska; czy Paweł chce się podpisać (np. w sekcji o firmie).
7. Aktualny termin realizacji — czy chce podawać widełki tygodni (strona lepiej konwertuje z liczbą, ale tylko prawdziwą).
8. Pełna nazwa prawna firmy do stopki i polityki prywatności (w stopce wermont.eu jest tylko „WERMONT – Meble Na Wymiar” + NIP).
9. Formularz — podpiąć wysyłkę na biuro@wermont.eu (teraz demo, nic nie wysyła). Na obecnej stronie działa GTM, GA i Meta Pixel — ustalić, czy przenosimy (wtedy baner cookies).
