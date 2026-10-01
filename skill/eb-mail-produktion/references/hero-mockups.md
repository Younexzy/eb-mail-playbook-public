# Hero- und Mockup-Rezepte (Skripte in scripts/mockups, Assets: eigene Renders/Freisteller unter assets/mockups/src, nicht im öffentlichen Repo)

Arbeitsverzeichnis: `cd $PLAYBOOK/assets/mockups/src` und `PYTHONPATH=$PLAYBOOK/skill/eb-mail-produktion/scripts/mockups` (die Skripte nutzen relative Pfade).

## Handys
- Renders mit reinem Greenscreen im Display (Higgsfield nano_banana_pro): `iphone.png`, `pixel.png`, `duo.png` (iPhone + Pixel auf Spiegelboden), `iphone-lying.png`.
- Screen einsetzen: `composite.green_mask` → `split_masks` (bei duo) → `place(base, screen, mask)` (Homographie, Kantenfit). Gedrehte Screens: `quad_rot.screen_quad` (eigh statt SVD, sonst OOM).
- Grüne Bodenspiegelung danach ersetzen (Bereich unterhalb der Handys aus fertigem Mock übernehmen oder umfärben).
- Screens: `findmy-screen-2-anon.png` (iOS Objekte-Liste, anonymisiert), `findhub-screen.png` (Android Find Hub), `findmy-locate-screen.png` (iOS „Wo ist?“ ortet die Tracker Karte Pro: Pin = echtes Kartenfoto, Pulse, Route, „Wird geortet“) → Generator `findmy_locate.py`.

## Karte platzieren
- `hero_v2.place2(base, card_h_px, floor_y, x_left, reflection=True|False, shadow=…)`: echtes Kartenfoto, nur skaliert. Mit Spiegelboden `reflection=True, shadow=False`.
- `hero_v2.pad_v` / `extend` verlängern Boden/Seiten, `crop_aspect(im, ytop, H, aspect, cx)` schneidet auf das Seitenverhältnis des Figma-Hero-Nodes.
- **Fade-Grenzen einhalten:** Kartenunterkante ≤ (Fade-Start − 2 %) der Hero-Höhe, Handy-Oberkante unterhalb des Top-Fades. Werte vorher in Figma lesen (`hero/fade~free`, `hero/topfade~free`).
- Bewährte Kompositionen (Black Member × Limited Carbon, 30.09.2026):
  - Mail 1 + Mail 2: `duo` + Karte groß davor (`place2(pad_v(duo,bottom=560), 640–700, 1700, 520–560, reflection=True)`, Crop `H=(1700-150)/0.71`, Aspect 1080/1285). Mail 2 mit Ortungsscreen auf dem iPhone.
  - Mail 3: `iphone` + Karte groß vorn rechts (`card_h 860, floor 2130`, `pad_v(bottom=400)`).
  - Mail 4: `duo` + Karte vorn rechts, Hero-Rahmen auf 977 vergrößert.
- Liegende Karte (falls gewünscht): `lying_contact.py` (enger Kontaktschatten + Kartenkante). Das Team fand die liegende Variante trotzdem schwächer → stehend mit Spiegelung bevorzugen.

## Badges
- Badges selbst erzeugen: `build_badges.py <scale>` mit einem Screenshot der offiziellen Badges (`source-screenshot.png`) und Poppins in `fonts/` (Google Fonts, OFL). Nutzung der Apple-/Google-Badges nur gemäß deren Markenrichtlinien (Google-Logo als vermessener Vektor, Find-My-Icon aus Originalpixeln, Text Poppins Bold / SF Pro, Rand + Text weiß).
- In Figma: zwei Rechtecke 465×121 bei x60 / x555, Bild-Fill FIT, Namen `compat/badge-apple-findmy`, `compat/badge-google-findhub`, unter `compat/label` „FUNKTIONIERT MIT“.

## Higgsfield (nur für neue Renders/Szenen)
- Tools haben leere Schemas: `generate_image` nur mit `params:{model:"nano_banana_pro", aspect_ratio, resolution:"2k", input_images:[media_ids], prompt}`; `job_display` mit `id`; `jobs_wait` scheitert; Bilder per `media_import_url` (Figma-Asset-URL) importieren.
- Text/Logos/Gravuren nie von der KI „korrigieren“ lassen (wird schlechter) → lokal mit PIL.
