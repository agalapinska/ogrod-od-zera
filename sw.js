/* Service worker aplikacji „Ogród od zera”.
   Plik jest generowany przez build.py — cc055ef66e99 podmieniana jest na skrót
   z treści zbudowanych stron, żeby każda realna zmiana unieważniła cache.
   Nie edytuj sw.js w katalogu głównym; źródłem jest src/sw.js. */

const WERSJA = "cc055ef66e99";
const CACHE = `ogrod-${WERSJA}`;

/* Powłoka aplikacji — wszystko, co musi działać bez sieci. */
const POWLOKA = [
  "./",
  "./index.html",
  "./kalendarz.html",
  "./manifest.webmanifest",
  "./ikony/ikona-192.png",
  "./ikony/ikona-512.png",
  "./ikony/ikona-maskowalna-512.png",
  "./ikony/apple-touch-icon.png",
  "./ikony/favicon.ico",
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) =>
      /* addAll przerywa całą instalację, gdy jeden zasób padnie —
         dlatego dokładamy pojedynczo i tolerujemy braki */
      Promise.all(
        POWLOKA.map((u) =>
          c.add(new Request(u, { cache: "reload" })).catch(() => null)
        )
      )
    )
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    (async () => {
      const nazwy = await caches.keys();
      await Promise.all(
        nazwy.filter((n) => n.startsWith("ogrod-") && n !== CACHE)
             .map((n) => caches.delete(n))
      );
      if (self.registration.navigationPreload) {
        await self.registration.navigationPreload.enable();
      }
      await self.clients.claim();
    })()
  );
});

/* Strona prosi o natychmiastowe przejęcie po kliknięciu „Odśwież”. */
self.addEventListener("message", (e) => {
  if (e.data === "przejmij") self.skipWaiting();
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  /* Nawigacje: najpierw sieć, żeby nowa wersja wchodziła od razu;
     bez sieci — wersja z cache, a w ostateczności strona główna. */
  if (req.mode === "navigate") {
    e.respondWith(
      (async () => {
        try {
          const wstepna = await e.preloadResponse;
          if (wstepna) {
            if (wstepna.ok) (await caches.open(CACHE)).put(req, wstepna.clone());
            return wstepna;
          }
          const z_sieci = await fetch(req);
          /* tylko udane odpowiedzi — inaczej offline serwowalibyśmy
             zapamiętane 404 albo stronę błędu hostingu */
          if (z_sieci.ok) (await caches.open(CACHE)).put(req, z_sieci.clone());
          return z_sieci;
        } catch {
          return (
            (await caches.match(req)) ||
            (await caches.match("./index.html")) ||
            new Response("Brak połączenia i brak kopii offline.", {
              status: 503,
              headers: { "Content-Type": "text/plain; charset=utf-8" },
            })
          );
        }
      })()
    );
    return;
  }

  /* Reszta zasobów: z cache od ręki, w tle odświeżenie. */
  e.respondWith(
    (async () => {
      const trafienie = await caches.match(req);
      const wSieci = fetch(req)
        .then((odp) => {
          if (odp && odp.ok && odp.type === "basic") {
            caches.open(CACHE).then((c) => c.put(req, odp.clone()));
          }
          return odp;
        })
        .catch(() => null);
      return trafienie || (await wSieci) || Response.error();
    })()
  );
});
