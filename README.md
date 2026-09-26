# Wermont – Meble Na Wymiar — demo

Lead: **Paweł**, WERMONT – Meble Na Wymiar, +48 732 139 879, biuro@wermont.eu,
ul. Kościelna 18, 83-400 Skorzewo (pod Kościerzyną, pomorskie). NIP 591-167-64-14.
Obecna strona: https://wermont.eu/ (WordPress/Avada, zrobiona przez Red Baron Support). CRM: `4c333db3-b7bf-43b3-acac-38ce9e4d46c3`.

Podgląd lokalny: `python -m http.server 8123`. Sprawdzanie opublikowanego dema przez nas — **zawsze z `?team=1`**.

## Założenia

Zwykła strona stolarni, bez ozdobników „AI”: ciepła biel i len, akcent orzechowy brąz (#7a4b27) wzięty z dekorów
na zdjęciach realizacji, ciemny grafit tylko w opiniach i stopce. Nagłówki **Literata**, tekst **Karla** (inne niż w
mk-bau i w pozostałych demach meblowych: Lora/Manrope, Cormorant/Inter). Logo w nagłówku — oryginalny znak klienta z wermont.eu.

**Wszystkie zdjęcia to realizacje Wermont** z ich obecnej strony (zero stocków) — lista w `zrodla-zdjec.html` i `_src/zrodla.json`.

Układ: hero (tekst + szerokie zdjęcie) → „Producent, nie pośrednik” z faktami → oferta w 4 naprzemiennych rzędach
(kuchnie, szafy, łazienki, fronty) → „Czego nie widać” (parametry konstrukcji, które klient sam podaje) → projekt
w PaletteCAD → galeria 8 realizacji → 3 opinie z Google → 4 kroki współpracy → kontakt z formularzem i mapą.
Zwracamy się na „Ty”, tak jak robi to obecna strona klienta.

## Techniczne SEO

- `title`, `description`, `canonical`, Open Graph (JPG 1200×630: `img/og.jpg`).
- JSON-LD: `HomeAndConstructionBusiness` (NAP, NIP, geo, godziny pn–pt 8–18, obszar, katalog usług, sameAs FB/IG) + `WebSite`.
  Celowo **bez `aggregateRating`** — Google nie pokazuje gwiazdek z opinii o sobie samym na własnej stronie.
- Jeden `h1`, poprawna hierarchia, link „przejdź do treści”, `lang="pl"`.
- Fonty lokalnie (woff2, latin + latin-ext, preload), obraz LCP z `preload` + `fetchpriority="high"`, `srcset`,
  `width`/`height` przy obrazkach, `loading="lazy"` poniżej pierwszego ekranu, bez ekranu ładowania.
- `sitemap.xml`, `robots.txt`, `404.html`, `favicon.svg`, `apple-touch-icon.png`, `site.webmanifest`, polityka prywatności.
- Menu na telefonie, dolny pasek „Zadzwoń / Umów pomiar”.
- Licznik otwarć demo (`demo_views`) — ostatnie IIFE w `assets/app.js`, skopiowane 1:1 z mk-bau.
- **DEMO ma `noindex`**. Przy wdrożeniu: usunąć `noindex`, podmienić `https://impulseo-pl.github.io/wermont-meble/`
  na `https://wermont.eu/` (canonical, og, JSON-LD, sitemap, robots), w 404.html ścieżki `/wermont-meble/` → `/`,
  podpiąć formularz, zachować przekierowania 301 ze starych adresów WordPressa (`/meble-kuchenne/`, `/kontakt/`,
  `/meble-na-wymiar-koscierzyna/` itd. — obecna strona ma sporo podstron lokalnych, nie wolno ich zgubić).

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
