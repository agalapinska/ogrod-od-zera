#!/usr/bin/env python3
"""Buduje index.html (pełny dokument dla GitHub Pages) z ogrod.html.

ogrod.html jest źródłem prawdy. Jest zapisany w formacie artefaktu
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
SOURCE = ROOT / "ogrod.html"
TARGET = ROOT / "index.html"

SZABLON = """<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Przewodnik na pierwszy sezon warzywny \
z wyborem ścieżki: parapet i balkon w bloku albo grządka na działce.">
<meta name="color-scheme" content="light dark">
{head}
</head>
<body>
<!-- Ten plik jest generowany przez build.py na podstawie ogrod.html.
     Nie edytuj go bezpośrednio — zmiany wprowadzaj w ogrod.html. -->
{body}
</body>
</html>
"""


def main() -> None:
    tresc = SOURCE.read_text(encoding="utf-8")

    # <title> i <style> należą do <head>, cała reszta do <body>
    do_glowy = []

    def wytnij(wzorzec: str) -> None:
        nonlocal tresc
        for dopasowanie in re.findall(wzorzec, tresc, flags=re.S | re.I):
            do_glowy.append(dopasowanie.strip())
        tresc = re.sub(wzorzec, "", tresc, flags=re.S | re.I)

    wytnij(r"<title>.*?</title>")
    wytnij(r"<style>.*?</style>")

    TARGET.write_text(
        SZABLON.format(head="\n".join(do_glowy), body=tresc.strip()),
        encoding="utf-8",
    )
    print(f"Zapisano {TARGET.name} ({TARGET.stat().st_size:,} B)")


if __name__ == "__main__":
    main()
