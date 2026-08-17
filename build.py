#!/usr/bin/env python3
"""Buduje pełne dokumenty HTML dla GitHub Pages z plików w src/.

Pliki w src/ są źródłem prawdy. Są zapisane w formacie artefaktu
claude.ai, czyli bez <!doctype>, <html>, <head> i <body> — te znaczniki
dokłada hosting artefaktów w momencie publikacji.

GitHub Pages niczego nie dokłada, więc dla przeglądarki potrzebny jest
kompletny dokument: deklaracja kodowania (polskie znaki), meta viewport
(inaczej telefony renderują stronę w szerokości desktopu) oraz doctype
(inaczej przeglądarka wchodzi w tryb zgodności i psuje układ).

Użycie:  python3 build.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"

# źródło w src/  ->  (plik wynikowy w katalogu głównym, opis dla meta description)
STRONY = {
    "ogrod.html": (
        "index.html",
        "Przewodnik na pierwszy sezon warzywny z wyborem ścieżki: "
        "parapet i balkon w bloku albo grządka na działce.",
    ),
    "kalendarz.html": (
        "kalendarz.html",
        "Interaktywny kalendarz siewu i zbiorów dla 37 upraw, "
        "z możliwością zapisywania własnych wysiewów i zbiorów.",
    ),
}

SZABLON = """<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{opis}">
<meta name="color-scheme" content="light dark">
{head}
</head>
<body>
<!-- Ten plik jest generowany przez build.py na podstawie src/{zrodlo}.
     Nie edytuj go bezpośrednio — zmiany wprowadzaj w pliku źródłowym. -->
{body}
</body>
</html>
"""


def zbuduj(zrodlo: str, wynik: str, opis: str) -> None:
    tresc = (SRC / zrodlo).read_text(encoding="utf-8")

    # <title> i <style> należą do <head>, cała reszta do <body>
    do_glowy: list[str] = []

    def wytnij(wzorzec: str) -> None:
        nonlocal tresc
        do_glowy.extend(
            d.strip() for d in re.findall(wzorzec, tresc, flags=re.S | re.I)
        )
        tresc = re.sub(wzorzec, "", tresc, flags=re.S | re.I)

    wytnij(r"<title>.*?</title>")
    wytnij(r"<style>.*?</style>")

    cel = ROOT / wynik
    cel.write_text(
        SZABLON.format(
            opis=opis,
            zrodlo=zrodlo,
            head="\n".join(do_glowy),
            body=tresc.strip(),
        ),
        encoding="utf-8",
    )
    print(f"src/{zrodlo}  ->  {wynik}  ({cel.stat().st_size:,} B)")


def main() -> None:
    for zrodlo, (wynik, opis) in STRONY.items():
        zbuduj(zrodlo, wynik, opis)


if __name__ == "__main__":
    main()
