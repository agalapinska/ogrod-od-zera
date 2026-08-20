# Od parapetu do grządki

Przewodnik na pierwszy sezon warzywny plus interaktywny kalendarz siewu
i zbiorów. Dwie ścieżki: uprawa w mieszkaniu w bloku (parapet i balkon) albo
na działce. Wybór ścieżki przestawia całą treść — inne pojemniki, inne
warzywa, inne rysunki, inny kalendarz — i przenosi się między stronami.

- **Przewodnik:** https://agalapinska.github.io/ogrod-od-zera/
- **Kalendarz:** https://agalapinska.github.io/ogrod-od-zera/kalendarz.html

## Aplikacja

Serwis jest aplikacją instalowalną (PWA). Na telefonie przeglądarka
zaproponuje „Dodaj do ekranu głównego”; na iPhonie robi się to ręcznie
przez Udostępnij → Do ekranu początkowego. Po instalacji uruchamia się
bez paska adresu, z własną ikoną, i **działa bez internetu** — co ma
znaczenie na działce z kiepskim zasięgiem.

Service worker (`sw.js`) trzyma w pamięci obie strony, manifest i ikony.
Strony pobiera najpierw z sieci, żeby zmiany wchodziły od razu, a z kopii
dopiero gdy sieci nie ma; pozostałe zasoby serwuje od ręki z cache
i odświeża w tle. Gdy pojawi się nowa wersja, na dole wyskakuje pasek
„Odśwież” — strona przeładowuje się tylko po kliknięciu, nigdy sama.

Wersja workera to skrót z treści zbudowanych stron, więc każda realna
zmiana unieważnia stary cache. Wylicza ją `build.py`.

Wpisy w kalendarzu i tak siedzą w `localStorage`, więc offline działa
w pełni — łącznie z dodawaniem nowych.

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

| źródło | wynik |
|---|---|
| `src/ogrod.html` | `index.html` |
| `src/kalendarz.html` | `kalendarz.html` |
| `src/sw.js` | `sw.js` (z podstawioną wersją) |

Poza tym w repo leżą pliki nieskładane z niczego: `manifest.webmanifest`,
`ikony/` oraz `.nojekyll` (wyłącza przetwarzanie przez Jekylla).

Budowanie dokłada do obu stron powłokę aplikacji — znaczniki manifestu
i ikon, kolory paska systemowego, rejestrację workera, pasek instalacji
i aktualizacji oraz wskaźnik trybu offline. Dlatego tych rzeczy nie ma
w plikach źródłowych: wersje publikowane jako artefakty claude.ai mają
zostać zwykłymi stronami.

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
