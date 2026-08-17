# Od parapetu do grządki

Przewodnik na pierwszy sezon warzywny plus interaktywny kalendarz siewu
i zbiorów. Dwie ścieżki: uprawa w mieszkaniu w bloku (parapet i balkon) albo
na działce. Wybór ścieżki przestawia całą treść — inne pojemniki, inne
warzywa, inne rysunki, inny kalendarz — i przenosi się między stronami.

- **Przewodnik:** https://agalapinska.github.io/ogrod-od-zera/
- **Kalendarz:** https://agalapinska.github.io/ogrod-od-zera/kalendarz.html

## Kalendarz

Trzydzieści siedem upraw w rozdzielczości pół miesiąca, w czterech
osobnych pasmach: siew pod osłoną, siew wprost, przesadzanie, zbiór.
Pionowa kreska pokazuje dzisiejszą datę.

Na to nakłada się **warstwa własnych wpisów**. Zapisujesz, że coś posiałaś,
przesadziłaś albo zebrałaś, a strona:

- stawia znacznik na osi czasu danej uprawy,
- wylicza szacowany termin zbioru na podstawie liczby dni od siewu,
- przypomina w panelu „Co robić teraz”, co dojrzeje w ciągu trzech tygodni.

Wpisy siedzą w `localStorage` tej przeglądarki i nie są nigdzie wysyłane.
Sekcja „Kopia zapasowa” pozwala je wyeksportować i wczytać jako tekst
(przez pole tekstowe, a nie pobieranie pliku — pobieranie bywa blokowane
w osadzonych podglądach).

## Co jest w przewodniku

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

Źródłem prawdy jest katalog **`src/`**. Pliki są tam w formacie artefaktu
claude.ai, czyli bez `<!doctype>`, `<html>`, `<head>` i `<body>` — te
znaczniki dokłada hosting artefaktów w momencie publikacji.

| źródło | strona |
|---|---|
| `src/ogrod.html` | `index.html` |
| `src/kalendarz.html` | `kalendarz.html` |

Pliki w katalogu głównym są **generowane** i to je serwuje GitHub Pages.
Budowanie dokłada doctype (bez niego przeglądarka wchodzi w tryb zgodności),
deklarację kodowania (polskie znaki) oraz `meta viewport` (bez niego telefon
renderuje stronę w szerokości desktopu).

Po każdej zmianie w `src/`:

```bash
python3 build.py
```

Nie edytuj `index.html` ani `kalendarz.html` bezpośrednio — przy następnym
budowaniu zmiany znikną.

Strona jest w całości samowystarczalna: jeden plik, bez zależności, bez
zewnętrznych skryptów, czcionek i obrazków. Działa też z dysku, po otwarciu
`index.html` w przeglądarce.
