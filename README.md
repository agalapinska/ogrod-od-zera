# Od parapetu do grządki

Przewodnik na pierwszy sezon warzywny. Jedna strona, dwie ścieżki: uprawa
w mieszkaniu w bloku (parapet i balkon) albo na działce. Wybór ścieżki
przestawia całą treść — inne pojemniki, inne warzywa, inne rysunki, inny
kalendarz.

**Strona:** https://agalapinska.github.io/ogrod-od-zera/

## Co jest w środku

Osiem kroków, od oceny miejsca do kuchni:

1. Ile masz słońca (balkon) / metoda SWAGA (działka)
2. W czym rosnąć — pojemniki z odzysku albo grządka 3 × 1,2 m
3. Ziemia i kompost
4. 20 warzyw z danymi siewu, filtrowanych po ścieżce i kategorii
5. Kalendarz miesiąc po miesiącu, z podświetlonym bieżącym miesiącem
6. Podlewanie — progi, przy których faktycznie trzeba lać
7. Co pójdzie nie tak i co z tym zrobić
8. Zbiór i kuchnia

Plus lista kontrolna na pierwszy tydzień. Wybór ścieżki i odhaczone punkty
zapisują się w `localStorage`.

## Źródła

Wszystkie rozstawy, głębokości siewu, pojemności doniczek i okresy do zbioru
pochodzą z książek Huwa Richardsa: *Veg in One Bed*, *Grow Food for Free*,
*The Vegetable Grower's Handbook* oraz *The Self-Sufficiency Garden*
(z Samem Cooperem). Rozdział o kuchni odwołuje się do *Cook Express*
Heather Whinney, a warstwa wizualna do zbioru rycin *Plants and Flowers*
Bessette'a i Chapmana.

Treść jest własnym opracowaniem, nie tłumaczeniem. **Terminy kalendarzowe
zostały przesunięte z klimatu walijskiego (strefa 8) na polski (strefa 6–7):**
ostatnie przymrozki około 15 maja, pierwsze jesienne w drugiej połowie
października. Ilustracje są oryginalne (SVG), nie pochodzą ze skanów.

## Praca nad plikami

Źródłem prawdy jest **`ogrod.html`** — format artefaktu claude.ai, czyli bez
`<!doctype>`, `<html>`, `<head>` i `<body>`. Te znaczniki dokłada hosting
artefaktów w momencie publikacji.

**`index.html`** jest generowany i to jego serwuje GitHub Pages. Dokłada
doctype (bez niego przeglądarka wchodzi w tryb zgodności), deklarację
kodowania (polskie znaki) oraz `meta viewport` (bez niego telefon renderuje
stronę w szerokości desktopu).

Po każdej zmianie w `ogrod.html`:

```bash
python3 build.py
```

Nie edytuj `index.html` bezpośrednio — przy następnym budowaniu zmiany znikną.

Strona jest w całości samowystarczalna: jeden plik, bez zależności, bez
zewnętrznych skryptów, czcionek i obrazków. Działa też z dysku, po otwarciu
`index.html` w przeglądarce.
