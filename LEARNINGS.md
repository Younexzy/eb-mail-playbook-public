# Learnings A–Z · EB-Mail-Produktion

Alles, was wir bei Essentialbag (Smart Wallets & Tracker Karten) über Kampagnen-Mails gelernt haben: Kampagnen-Mails (A–L, aktueller Workflow), dazu alle früheren Projekte (M–T: Betreffzeilen, Drops, Klaviyo-Flows, Shopify, Chatarmin, Produktbilder, Packaging, Agentur-System). Jede neue Erkenntnis kommt hier rein **und** in den Skill (`skill/eb-mail-produktion/references/`).

Format pro Punkt: **Regel** · Warum · Wie anwenden. Neueste Änderungen stehen im [CHANGELOG](CHANGELOG.md).

---

## A · Copy & Sprache
- **Keine Gedankenstriche** (– —) in Mail-Copy. Team-Regel. Punkt, Komma oder Doppelpunkt nutzen.
- **Umlaute immer korrekt** (ä ö ü ß), nie ae/oe/ue.
- **Nichts erfinden.** Fakten, Zahlen, Reviews nur aus BRAND.md oder Briefing. Fehlt etwas: „Mir fehlt: …“.
- **Trust-Zahlen:** 160.000+ zufriedene Kunden · 4,4/5 Trustpilot · 60 Tage Rückgaberecht.
- **Tracker Karte = „Tracker-Map“:** In übersetzten Briefings heißt die Tracker Karte manchmal „Tracker-Map“.
- **Pro vs. Standard** (für Vergleiche): Pro sieht aus wie eine Kreditkarte, BLACK MEMBER Gravur, echter Chip-Look. Beide: Apple „Wo ist?“ + Google Find Hub, kabellos aufladbar. Dicke 1,8 vs. 1,9 mm ist ungeklärt → nie nennen.

## B · Scarcity
- **„Limitiert auf 1.000 Stück“** in jeder Mail einer limitierten Kampagne.
- **Platzierung:** Eyebrow ganz oben (z. B. „EARLY ACCESS · NUR 1.000 STÜCK“) + eine zweite Stelle im Body (fett im Hero-Sub, Bundle-Sub, Beleg-Kopf).
- **Geschütztes Leerzeichen** zwischen Zahl und Einheit (`1.000 Stück`), sonst bricht „1.000 / Stück“ um (passiert in Mail 1).
- Nur einbauen, wo die Zeile nicht umbricht: Text-Höhe vorher/nachher vergleichen.

## C · Design-Grundregeln
- **Keine harten Farbblöcke** zwischen Sektionen. Eine Grundfarbe (Dark #0B0B0D), Kontraste als Panels mit Rand, Übergänge per Fade.
- **Hero (Apol-Anatomie):** Logo → Eyebrow → XXL-Headline ohne Effekte → Sub (Poppins Light, Bold-Fakten) → genau ein weißer CTA. Ausnahme Early Access: zusätzlich Outline-Button „EXKLUSIVE VORSCHAU“ unter jedem CTA.
- **Knockout-CTAs** (Text ausgestanzt), 960×148 bei x60, Poppins ExtraBold, Letter-Spacing −5 %.
- **CTA nach jeder Content-Sektion**, Labels variieren.
- **Benefits als Icon-Karten** im Grid, nie als Bullet-Liste. Der Member-Ausweis als Benefit-Darstellung wurde abgelehnt („gefällt mir nicht“); das 6er-Icon-Grid ist der Standard.
- **Kein Liquid-Glass, kein Glow** auf Headlines.

## D · Die Tracker Karte im Bild (wichtigster Punkt)
- **Hauptdarsteller jeder Hero:** groß, im Vordergrund, komplett sichtbar.
- **Nie in Fade- oder Label-Zone:** Kartenunterkante oberhalb des Hero-Bottom-Fades (Mail 1: ≤ 72 % der Hero-Höhe, Mail 3: ≤ 79 %, Mail 4: ≤ 68–74 %). Werte immer aus Figma lesen (`hero/fade~free`).
- **Nie schweben.** Abgelehnte Varianten:
  - schwebende Karte mit versetztem, weichem Schatten,
  - liegende Karte neben liegendem iPhone (auch mit Kontaktschatten noch „gefällt mir nicht“).
- **Gewinner-Aufbau (Mail 1, vom Team als Vorlage gewählt):** iPhone + Android auf Spiegelboden, Karte groß davor, stehend, mit eigener Spiegelung.
- **Mail 2 = wie Mail 1, aber das iPhone ortet die Karte** (Wo-ist-Karte mit Kartenfoto als Pin, Pulse, Route, „Wird geortet“).
- **Proportion:** nebeneinander ≈ 36 % der Handyhöhe (54/150 mm); im Vordergrund bis ~55 % (Perspektive rechtfertigt es).
- **Karte nicht bearbeitet aussehen lassen:** rembg-Alpha war nur ~86 % deckend → durchscheinend → Alpha härten (>170 → 255, MinFilter 3, Blur 0.9). Schatten nicht am Canvas-Rand abschneiden (Padding).
- **Generieren erlaubt** (seit 29.09.2026), aber jedes Bild im Eng-Crop prüfen: EB-Prägung, Chip, „BLACK MEMBER / MEMBER SINCE 2026 / VALID THRU 12/33“. Für Heroes bleibt das echte Foto die beste Wahl.

## E · Handy-Mockups
- **Greenscreen-Renders** (Higgsfield nano_banana_pro, Titan-Look) + echte Screens **lokal per Homographie** einsetzen. Screens nie generieren lassen (Schrift verschwimmt).
- **Displays nie leer:** Mail 1 mit ausgeschaltetem Display wurde verworfen („Display ist leer“).
- **Grüne Bodenspiegelung** des Greenscreens nach dem Einsetzen ersetzen (Bodenbereich aus fertigem Mock übernehmen).
- **Schräge Screens:** Kantenfit über `eigh` der Kovarianz, nicht volle SVD (OOM, Exit 137).
- **Persönliche Daten anonymisieren:** Adressen in echten Screenshots ersetzen („Friedrichstraße, Berlin“ / „Mitte • Jetzt“). Originale nie ins Repo.
- **Eigene Screens bauen:** `findmy_locate.py` (iOS „Wo ist?“ ortet die Karte), `findhub-screen.png` (Android Find Hub).

## F · Badges „Works with Apple Find My / Google's Find Hub“
- **Offizielle Badges statt selbstgebauter Kacheln**, in **Weiß** (Text + Rand), **Logos original**.
- Nicht in Higgsfield bauen: Die KI zeichnet Logos/Text neu und verfälscht sie.
- Rezept: Google-Logo aus dem Screenshot exakt vermessen und als Vektor neu gezeichnet (Abweichung 1,4/255), Find-My-Icon aus Originalpixeln hochskaliert mit scharfer Kreiskante, Text in Poppins Bold bzw. SF Pro neu gesetzt (Größe/Laufweite gegen das Original gefittet).
- Erzeugen mit `skill/eb-mail-produktion/assets/badges/build_badges.py` (eigener Screenshot der offiziellen Badges; Nutzung nur gemäß Markenrichtlinien von Apple/Google).

## G · Figma (Datei „EB-Mails-Static“)
- **Einzige Arbeitsdatei:** `<FIGMA_FILE_KEY>`, Figma-Account mit Zugriff auf die Datei, Team-Plan **Professional**. Auf Starter sperrt das MCP nach ~12 Calls.
- **Nodes per Name suchen**, nie IDs aus Listen raten (einmal bekam ein Text eine Bild-Füllung).
- **Text ändern mit Fettungen:** `insertCharacters(…, 'BEFORE')` + `deleteCharacters`, Fonts vorher laden.
- **Hero zu klein für die Karte?** Hero-Rahmen vergrößern und alles darunter verschieben (Mail 4: 737 → 977, Mail 2: 806 → 1285), statt das Motiv in die Fades zu quetschen.
- **Uploads:** `upload_assets` ohne `count` (1 URL pro Call), dann curl. `createImageAsync` gibt es nicht.
- **Export:** `defaultScale` als Zahl scheitert → TMP-Frames klonen und per `rescale(1.5)` skalieren, dann `download_assets` je `nodeId`. Danach TMP-Frames löschen.
- **QA** über den echten Export, nicht `get_screenshot` (rendert Fades falsch).
- Nur geänderte Teile neu exportieren (spart Figma-Calls und Zeit).

## H · Klaviyo
- **REST statt MCP** für Schreibcalls (MCP-Schema-Bug). Key in `~/.klaviyo_api_key`, nie ausgeben, nie per Chat.
- **Bilder:** 1620-px-Slices, UnsharpMask(0.6, 60, 2), **Baseline-JPEG** q60 (bis q48 für ≤ ~760 KB/Mail). Progressive JPEGs rendert Klaviyo kaputt.
- **8 Slices**, bei unterschiedlichen Button-Links link-genau zwischen den Buttons schneiden.
- **Templates nie überschreiben**, immer neue Kopie + Zuweisung.
- **A/B-Tests:** Jede Variante ist eine eigene Nachricht → allen das Template zuweisen. Das Team legt A/B/C oft selbst an (z. B. Absender-Test); Klaviyo kopiert dabei das Template von A.
- **Geplante oder gesendete Kampagnen nicht anfassen** (Vorfall 01.10.2026: Testlauf traf geplante Mail 4, Inhalt identisch, nichts versendet). `klaviyo_sync.py` überspringt sie seitdem automatisch.
- **Prüfen:** Links, neue Slices, `[unsubscribe_tag]` + `[manage_preferences_tag]`, Status.
- Das Team stellt Sendezeiten selbst ein → Entwürfe mit Platzhalter-Zeit.

## I · Footer
- **Jede Mail mit EB-Footer** in passender Farbe.
- **Dark-Mode-Problem:** HTML-Buttons kippen im Postfach-Dark-Mode (weiße Buttons werden dunkel). Lösung DARK v2: Buttons + Social-Icons als Bilder, `color-scheme`-Meta, Footer-Hintergrund = Mail-Grundfarbe (#0B0B0D, sonst sichtbare Kante).

## J · Chatarmin (WhatsApp)
- `expectedOrganizationId` ist Pflicht bei Schreibcalls.
- Leeres Tool-Schema → Arrays/Zahlen scheitern. Funktioniert: `update_template_draft` mit nur `templateId` + `bodyText`.
- Template im Dashboard duplizieren (Templates → „…“ → Duplicate), speichern mit **„Save as Draft“**, nie ohne OK bei Meta einreichen.
- Black-Member-Flow: Keyword „Ich will Black Member Early Access“, Link `api.whatsapp.com/send/?phone=<NUMMER>&text=<Keyword>`.

## K · Higgsfield
- Leere Schemas: `generate_image` nur mit `params:{model:"nano_banana_pro", aspect_ratio, resolution:"2k", input_images:[…], prompt}`; `job_display` mit `id`; `jobs_wait` scheitert; Import per `media_import_url`.
- Text/Gravuren nie von der KI korrigieren lassen (wird schlechter) → lokal mit PIL.

## L · Arbeitsweise & Geschwindigkeit
- Erst Regeln + Brand + Copy-Deck laden, dann bauen.
- Varianten lokal rendern und als Kontaktbogen vergleichen, bevor Figma angefasst wird.
- Alles Wiederkehrende als Skript (Footer, Slicing, Upload, Badges, Mockups), keine Handarbeit.
- Nach jedem Schritt Copy-Deck um einen Änderungsblock ergänzen (IDs, Hashes, was geändert wurde).
- Vorschau-JPG ans Team, kurze Zusammenfassung, offene Punkte nennen.

---

# Learnings aus allen früheren Projekten

## M · Betreffzeilen, Preheader & Text-Mails
- **Ton der Gewinner-Betreffs:** offene Schleife, nichts verraten, Auslassungspunkte, klingt wie ein angefangener Satz von einem Menschen („Du wirst sie nicht erkennen…“, „Bevor es alle erfahren…“, „Ausverkauft…“, „Boah ihr seid zu teuer“). Unter 45 Zeichen.
- **Preheader führt den Gedanken weiter**, wiederholt nie den Betreff.
- **Immer 3–5 Varianten** mit unterschiedlichem Hebel (Verlustangst, Neugier, Exklusivität, Fakt) liefern.
- **Text-Only-Mails vom Gründer** (Sonntags-Update, Danke-Mail, Vorabend-Erinnerung) funktionieren: persönlich, kurz, zentriert, ein Link, Fakten live aus Shopify.
- **Sequenz-Variation:** aufeinanderfolgende Mails bewusst unterschiedlich (hell → dunkel), damit es nicht nach Wiederholung aussieht.
- **WhatsApp-Broadcasts:** WhatsApp-Syntax (`*fett*`), `{{1}}` für den Namen, gleiche Story wie die Mail.

## N · Kampagnen-Muster
- **Drops:** Early Access (Do, 1 Stunde früher über eigenen Link/WhatsApp-Keyword) → Jetzt Live (Fr 10 Uhr) → Reminder („letztes Mal nach X Stunden weg“) → Last Call (Restmenge).
- **Zielgruppen-Variante ohne Verlosung:** eigene Positionierung (z. B. Geschenk-Angle) und eigene Akzentfarbe. Wer Bausteine einer Verlosungs-Kampagne kopiert, muss Verlosungs-Wording, Disclaimer und Los-Mechanik komplett entfernen.
- **Knappheit nur ehrlich:** Restmengen erst nennen, wenn die Zahl wirklich klein ist (sonst Platzhalter bis kurz vor Versand). Auflagen wie „limitiert auf 1.000 Stück“ nur mit Freigabe.
- **Verlosungs-Kampagnen:** jede Bestellung = 1 Los, eigene Gewinnspiel-Seite mit Teilnahmebedingungen, Disclaimer auf allen Kanälen, rechtliche Prüfung vor Start.
- **Eigene WhatsApp-Early-Access-Flows pro Drop** (Skill `/drop-early-access`): eigenes Keyword + Tag statt allgemeinem Welcome-Link. Spart deutlich Versandkosten, weil nur Interessenten angeschrieben werden.

## O · Klaviyo-Flows & Daten
- **Flow-Struktur nur im UI** (im UI nach Klick-Anleitung verdrahten); API schreibt Templates/Bilder. `PATCH /flow-actions/{id}` ändert einzelne Actions (Filter, Betreff, Branches); Name/Trigger brauchen Neubau.
- **Filter-Logik:** Bedingungen innerhalb einer Gruppe = ODER, Gruppen untereinander = UND. Für UND je eine Bedingung pro Gruppe. `metric_filters` nur ein Filter pro Bedingung.
- **Ein großer Teil der Klicks sind Bot-Klicks** (bei uns über ein Drittel, `Bot Click = true`) → jedes Klick-Gate darauf filtern.
- **Flow-Reports per API unzuverlässig** (leere Aggregation bei laufenden Flows) → Zahlen in der UI prüfen.
- `transactional: true` ignoriert die API → im UI setzen. Flow-API Rate-Limit: 1/s, 15/min, 100/Tag.
- **Suppression-Falle:** Im ⋯-Menü von Listen/Segmenten liegt „Aktuelle Mitglieder unterdrücken“ direkt neben „Unterdrückung aufheben“ → Verwechslung unterdrückt massenhaft Profile. Wiederherstellung per Hilfssegment + `bulk_unsuppress_profiles`. Job-Zähler lügen während der Verarbeitung (~5 Min warten); der UI-„Import“ auf „Unterdrückte Profile“ UNTERDRÜCKT; Massen-Unsuppress nur per API.
- **Service-Mails (ParcelWill-Versandverzögerung):** Plain Text bringt mehr Antworten als Design. Nichts automatisch versprechen (eine automatisch versprochene Ersatzlieferung erzeugte in V1 sehr viele Anfragen); Selbst-Check + Antragsseite statt mailto; Deutsche Post (Briefpost) ausfiltern; Schwellen als Bereiche, nie `equals`.

## P · Shopify
- **Künstliches Lager (−10.000):** nimmt eine Variante aus dem Shop, Direktlink/Checkout funktioniert weiter → ideal für „nur per Mail-Link kaufbar“-Drops. Nicht aufräumen.
- **Offer-Pages:** `pageUpdate` nur mit Body als GraphQL-Block-String (Variablen scheitern). Live-Body steht JSON-escaped in `ShopifyTC.resource_description`.
- Redirects sind case-insensitiv, `/pages/...` in Versalien liefert 404.
- `pageCreate isPublished:true` blockt der Auto-Mode → Entwurf anlegen, ein Mensch veröffentlicht.

## Q · Chatarmin (Ergänzung)
- EN-Rollout: Sprach-Tags `Sprache_EN`/`Sprache_DE`, Event-Flows (nur 1× möglich) verzweigen per ifElse auf den Tag.
- Veröffentlichen/Aktivieren von Flows macht ein Mensch im Dashboard (Auto-Mode blockt `publish_flow`).

## R · Produktdarstellung allgemein (Statics, PDP)
- **Produkt muss überall identisch aussehen.** Nur echte Fotos als Referenz, nie Renders als Anker. Jedes Bild im Eng-Crop gegen die Checkliste (Logo, Material, Hebel, Reißverschluss, Karten, Form) prüfen, Durchfaller nie einbauen.
- **Smart Wallet 3.0 Anatomie:** Hebel = kleiner schwarzer Block oben an der Seite (kein langer Clip), Alu-Seitenleiste mit senkrechtem „ESSENTIALBAG“, Monogramm klein (~1/9–1/10 der Front), nie frontal-flach, Karten stufig aufgefächert. Wording „Kunstleder“, nie „Echtleder“.
- **Tracker Karte 3.0 (normal):** matt schwarz, hochkant, „ESSENTIAL BAG“ oben links, Ring-Knopf; der „Works with Apple Find My“-Aufdruck ist entfernt → nur saubere Referenz nutzen, Badges als Layout-Ebene.
- **Was beim Team durchfällt:** Cutout-Collagen, liegende Lifestyle-Motive, „alles sieht gleich aus“ (immer gleiche Pose/Typo). **Was besteht:** stehende Studio-/Hand-Renders, echte Szenen, Variation in Pose und Layout, Produkt groß.
- Texte nie aus der KI, immer aus Figma.

## S · Packaging (nicht Mail, aber gelernt)
- Illustrator per ExtendScript (`osascript … do javascript`), Barcodes immer als GS1-PNG (vorher 1-Bit → 8-Bit RGB, sonst schwarze Fläche), Z-Order prüfen, Ergebnis per Vision-Decode gegenprüfen.
- Für die Fabrik: AI als Illustrator 2020 + PDF „Illustrator Default“ (nicht PDF/X-4), keine Umlaute/Sonderzeichen in Pfaden, Ordner je Produkt + `Barcodes/`.

## T · Agentur-System
- Design-System „agentic-email-designer“ (öffentliches GitHub-Repo von simon-schaeferai): MASTER-EMAIL-SYSTEM, FIGMA-RECIPES, Brand-Kits. Keine Produktion ohne freigegebenes BRAND.md. 
- Figma-Master-Library „EMAIL-SYSTEM-LIBRARY“ `<LIBRARY_FILE_KEY>`.
- Statics laufen in einer eigenen Session (eigener Skill).

---

## Chronik Black Member × Limited Carbon (29.09.–01.10.2026)
1. Briefing: 4 Mails (Early Access, Jetzt Live, Reminder „3 Stunden“, Last Call), Bundle Tracker Karte Pro Schwarz + Smart Wallet 3.0 Limited Carbon, Fokus Pro-Karte, Benefits vs. Standard.
2. Erste Builds; KI-veränderte Kartenbilder abgelehnt → nur echte Fotos. Member-Ausweis-Sektion abgelehnt → Icon-Grid.
3. Apple/Google-Kompatibilität ergänzt, „Exklusive Vorschau“-Buttons in Mail 1, Links (WhatsApp/Vorschau/Drop-Seite).
4. Klaviyo-Entwürfe, Footer-Skill, Dark-Mode-Fix (Footer als Bilder).
5. Figma-Umzug auf „EB-Mails-Static“ (neuer Account, Professional-Plan).
6. Chatarmin-Template per Dashboard-Duplikat + MCP-Body.
7. Realistische Handy-Mockups (iPhone + Android, Titan-Look) mit Find-My/Find-Hub-Screens; Karte neben die Handys.
8. Mail-1-Display aus → verworfen; Karte war halbtransparent → Alpha gehärtet.
9. Offizielle weiße Badges statt eigener Kacheln.
10. Karte prominenter in allen Heroes, komplett über den Fades; Mail-4-Hero vergrößert.
11. Mail 2: liegende Karte schwebte → Kontaktschatten → immer noch nicht gut → Aufbau wie Mail 1 + iPhone ortet die Karte; Hero vergrößert.
12. Scarcity „1.000 Stück“ in allen Mails.
13. A/B-Varianten B/C von Mail 1 nachgezogen.
14. Skill `eb-mail-produktion` + Umzugspaket + dieses Repo.
