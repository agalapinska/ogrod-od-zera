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

import hashlib
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
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{opis}">
<meta name="color-scheme" content="light dark">

<!-- aplikacja instalowalna -->
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="ikony/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="ikony/apple-touch-icon.png">
<meta name="theme-color" content="#EDEEE7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#13160F" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Ogród od zera">
<meta name="mobile-web-app-capable" content="yes">
{head}
<style>
/* ---------- elementy powłoki aplikacji ---------- */
.app-pasek {{
  position: fixed;
  /* left + right zamiast left: 50% — przy left: 50% szerokość dostępna
     dla elementu to tylko połowa okna, więc pasek zwijał się i łamał tekst */
  left: 14px;
  right: 14px;
  margin-inline: auto;
  width: fit-content;
  bottom: calc(18px + env(safe-area-inset-bottom));
  z-index: 90;
  display: none;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px 12px;
  max-width: min(440px, calc(100vw - 28px));
  padding: 12px 14px 12px 18px;
  /* nie 100px: przy dwóch wierszach tekstu pastylka wygląda jak balon */
  border-radius: 20px;
  font-size: 14.5px;
  line-height: 1.35;
  color: var(--ink);
  background: color-mix(in srgb, var(--paper-2) 88%, transparent);
  -webkit-backdrop-filter: blur(16px) saturate(1.6);
  backdrop-filter: blur(16px) saturate(1.6);
  border: 1px solid color-mix(in srgb, var(--accent) 32%, transparent);
  box-shadow: 0 10px 30px -12px rgba(0, 0, 0, 0.5);
}}
.app-pasek[data-widoczny="tak"] {{ display: flex; }}
.app-pasek > span {{ flex: 1 1 190px; min-width: 0; }}

/* Pływający przycisk przewodnika i pasek powłoki dzielą prawy dolny róg —
   na czas paska podnosimy przycisk o jego zmierzoną wysokość. */
body[data-app-pasek="tak"] .fab {{
  bottom: calc(var(--h-app-pasek, 64px) + 30px + env(safe-area-inset-bottom));
}}
.app-pasek button {{
  font: inherit;
  font-size: 13.5px;
  white-space: nowrap;
  cursor: pointer;
  border-radius: 100px;
  padding: 7px 14px;
  min-height: 40px;
  border: 1px solid var(--accent);
  background: var(--accent);
  color: var(--paper);
}}
.app-pasek button.app-odrzuc {{
  background: none;
  color: var(--ink-2);
  border-color: transparent;
  padding-inline: 8px;
}}
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {{
  .app-pasek {{ background: var(--paper-2); }}
}}
/* w trybie aplikacji nie ma paska adresu — oddajemy ten margines treści */
@media (display-mode: standalone) {{
  .app-offline {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 95;
    display: none; text-align: center;
    padding: 5px 10px calc(5px + env(safe-area-inset-top));
    font-size: 12.5px; letter-spacing: 0.02em;
    background: var(--amber, #96671A); color: var(--paper);
  }}
  body[data-siec="offline"] .app-offline {{ display: block; }}
}}
</style>
</head>
<body>
<!-- Ten plik jest generowany przez build.py na podstawie src/{zrodlo}.
     Nie edytuj go bezpośrednio — zmiany wprowadzaj w pliku źródłowym. -->
<div class="app-offline" role="status">Tryb offline — zapisane wpisy działają dalej</div>
{body}

<div class="app-pasek" id="appPasek" role="status" aria-live="polite">
  <span id="appTekst"></span>
  <button type="button" id="appAkcja"></button>
  <button type="button" class="app-odrzuc" id="appOdrzuc" aria-label="Zamknij">✕</button>
</div>

<script>
/* ============================================================
   Powłoka aplikacji: instalacja, aktualizacje, stan sieci.
   Wstrzykiwane przez build.py — wspólne dla obu stron.
   ============================================================ */
(function () {{
  "use strict";

  var pasek  = document.getElementById("appPasek");
  var tekst  = document.getElementById("appTekst");
  var akcja  = document.getElementById("appAkcja");
  var odrzuc = document.getElementById("appOdrzuc");
  var biezacaAkcja = null;

  function pokaz(trescTekstu, etykieta, fn) {{
    tekst.textContent = trescTekstu;
    akcja.textContent = etykieta;
    biezacaAkcja = fn;
    pasek.dataset.widoczny = "tak";
    document.body.dataset.appPasek = "tak";
    /* zmierzona wysokość trafia do zmiennej, bo pasek bywa dwuwierszowy */
    requestAnimationFrame(function () {{
      document.documentElement.style.setProperty(
        "--h-app-pasek", Math.round(pasek.getBoundingClientRect().height) + "px");
    }});
  }}
  function schowaj() {{
    pasek.dataset.widoczny = "nie";
    document.body.dataset.appPasek = "nie";
    biezacaAkcja = null;
  }}

  akcja.addEventListener("click", function () {{ if (biezacaAkcja) biezacaAkcja(); }});
  odrzuc.addEventListener("click", schowaj);

  /* ---------- stan sieci ---------- */
  function stanSieci() {{
    document.body.dataset.siec = navigator.onLine ? "online" : "offline";
  }}
  window.addEventListener("online", stanSieci);
  window.addEventListener("offline", stanSieci);
  stanSieci();

  /* ---------- zaproszenie do instalacji ---------- */
  var zdarzenieInstalacji = null;
  var KLUCZ_ODRZUCONE = "ogrod-instalacja-odrzucona";

  window.addEventListener("beforeinstallprompt", function (e) {{
    e.preventDefault();
    zdarzenieInstalacji = e;
    try {{ if (localStorage.getItem(KLUCZ_ODRZUCONE) === "1") return; }} catch (err) {{}}
    setTimeout(function () {{
      if (!zdarzenieInstalacji || pasek.dataset.widoczny === "tak") return;
      pokaz("Dodaj do ekranu głównego — działa też bez internetu.", "Zainstaluj", function () {{
        var p = zdarzenieInstalacji;
        zdarzenieInstalacji = null;
        schowaj();
        p.prompt();
      }});
    }}, 2500);
  }});

  odrzuc.addEventListener("click", function () {{
    if (zdarzenieInstalacji) {{
      try {{ localStorage.setItem(KLUCZ_ODRZUCONE, "1"); }} catch (err) {{}}
    }}
  }});

  window.addEventListener("appinstalled", function () {{
    zdarzenieInstalacji = null;
    schowaj();
  }});

  /* ---------- service worker ---------- */
  /* isSecureContext, nie sam protokół https — obejmuje też localhost,
     więc aplikację da się uruchomić i przetestować lokalnie. Tam, gdzie
     workera nie ma (podgląd artefaktu, dysk), rejestracja po prostu
     odpada w catch i strona działa dalej jako zwykła witryna. */
  var naszeOdswiezenie = false;
  var przeladowano = false;

  if ("serviceWorker" in navigator && window.isSecureContext) {{
    window.addEventListener("load", function () {{
      navigator.serviceWorker.register("sw.js").then(function (rej) {{
        function zaproponujOdswiezenie(oczekujacy) {{
          pokaz("Jest nowa wersja aplikacji.", "Odśwież", function () {{
            /* dopiero teraz zgadzamy się na przeładowanie strony */
            naszeOdswiezenie = true;
            schowaj();
            oczekujacy.postMessage("przejmij");
          }});
        }}
        if (rej.waiting && navigator.serviceWorker.controller) {{
          zaproponujOdswiezenie(rej.waiting);
        }}
        rej.addEventListener("updatefound", function () {{
          var nowy = rej.installing;
          if (!nowy) return;
          nowy.addEventListener("statechange", function () {{
            if (nowy.state === "installed" && navigator.serviceWorker.controller) {{
              zaproponujOdswiezenie(nowy);
            }}
          }});
        }});
      }}).catch(function () {{ /* brak workera to nie powód do awarii strony */ }});

      /* Przy pierwszej instalacji worker przejmuje stronę sam (clients.claim),
         co też odpala controllerchange. Bez tej flagi każde pierwsze wejście
         kończyłoby się zbędnym przeładowaniem w oczach użytkownika. */
      navigator.serviceWorker.addEventListener("controllerchange", function () {{
        if (!naszeOdswiezenie || przeladowano) return;
        przeladowano = true;
        location.reload();
      }});
    }});
  }}
}})();
</script>
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


def zbuduj_workera() -> None:
    """Wstawia do sw.js wersję wyliczoną z treści zbudowanych stron.

    Bez tego przeglądarka nie miałaby jak zauważyć, że coś się zmieniło:
    porównuje bajt po bajcie sam plik workera, a nie zasoby, które ten
    worker trzyma w cache. Skrót z treści stron sprawia, że każda realna
    zmiana daje nowy plik workera, a ten unieważnia stary cache.
    """
    skrot = hashlib.sha256()
    for wynik, _ in sorted(STRONY.values()):
        skrot.update((ROOT / wynik).read_bytes())
    skrot.update((ROOT / "manifest.webmanifest").read_bytes())
    wersja = skrot.hexdigest()[:12]

    szablon = (SRC / "sw.js").read_text(encoding="utf-8")
    cel = ROOT / "sw.js"
    cel.write_text(szablon.replace("__WERSJA__", wersja), encoding="utf-8")
    print(f"src/sw.js      ->  sw.js  (wersja {wersja})")


def main() -> None:
    for zrodlo, (wynik, opis) in STRONY.items():
        zbuduj(zrodlo, wynik, opis)
    zbuduj_workera()


if __name__ == "__main__":
    main()
