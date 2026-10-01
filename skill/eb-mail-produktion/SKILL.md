---
name: eb-mail-produktion
description: Kompletter Produktions-Workflow für Essentialbag-(EB-)Kampagnen-Mails: in Figma „EB-Mails-Static“ bauen oder ändern (Heroes mit Handy-Mockups und Tracker Karte, offizielle Find-My/Find-Hub-Badges, Scarcity, Knockout-CTAs), exportieren, in Slices schneiden und als neue Template-Kopien in Klaviyo-Entwürfe hochladen (inkl. aller A/B-Varianten, EB-Footer, Prüfungen). Nutze diesen Skill immer, wenn eine EB-/Essentialbag-Mail, ein Hero-Bild, ein Mockup oder ein Klaviyo-Mail-Upload gebaut, geändert oder aktualisiert wird, und beim Umzug in einen neuen Claude-Account („gleicher Output wie vorher“).
---

# EB-Mail-Produktion

Bündelt alles, was in den Black-Member-, Iris- und Titan-Kampagnen gelernt wurde, damit jede Session und jeder Account denselben Output in derselben Geschwindigkeit liefert. Antworten auf Deutsch, kurz, ohne Fachjargon.

**Pfade:** `SKILL=<Ordner dieser Datei>`, `PLAYBOOK=$SKILL/../..` (dieses Repo). Eigene Brand-Daten, Kampagnen und Bild-Assets liegen NICHT im öffentlichen Repo, sondern privat: `$PLAYBOOK/agency/`, `$PLAYBOOK/campaigns/`, `$PLAYBOOK/assets/mockups/` selbst anlegen (siehe README).

## 0. Preflight (jede neue Session/jeder neue Account, ~1 Minute)
1. `python3 $SKILL/scripts/preflight.py` → Python-Pakete, Klaviyo-Key + Account, Assets, Memory, Skills.
2. Connectoren prüfen (nur lesend):
   - Figma: `use_figma` auf `<FIGMA_FILE_KEY>` → `figma.root.children.map(p=>p.name)` muss „E-Mails“ und „Statics“ liefern. Fehler „Starter-Plan“/„no access“ → falscher Figma-Login oder Plan ohne Full Seat.
   - Klaviyo: Preflight-Skript (REST) reicht; MCP optional.
   - Chatarmin/Higgsfield nur, wenn die Aufgabe sie braucht.
3. Fehlt etwas: konkret sagen, was („Figma ist mit einem anderen Account verbunden“), nicht improvisieren. Umzugs-Anleitung: `references/umzug-checkliste.md`.

## 1. Vor dem Bauen laden
- `references/regeln-design-copy.md` (verbindliche Design-/Copy-Regeln, immer).
- Brand: eigenes `BRAND.md` (privat, z. B. `$PLAYBOOK/agency/Brands/<brand>/BRAND.md`) mit Fakten, Farben, Fonts. Neue Brand → Skill `/email-design`.
- Learnings: `$PLAYBOOK/LEARNINGS.md`. Eigene Kampagnen (Copy-Decks, IDs) privat unter `$PLAYBOOK/campaigns/<name>/` führen.

## 2. Bauen/Ändern in Figma → `references/figma-workflow.md`
- Nur Datei `<FIGMA_FILE_KEY>`, Nodes per Name suchen.
- Texte mit Erhalt der Fettungen ändern, Höhe vorher/nachher vergleichen, auto-width neu zentrieren.
- Hero-Bilder lokal bauen → `references/hero-mockups.md` (Handy-Greenscreen + Homographie, Karte groß im Vordergrund auf Spiegelboden, Fade-Grenzen). Dann `upload_assets` ohne `count` + curl, Fill tauschen, Temp-Node löschen.
- Badges: fertige PNGs in `assets/badges/`.
- Layout-Änderungen (Hero größer): Section-Shift aller Nodes unterhalb, Frame-Höhe anpassen.

## 3. QA (Pflicht, nie ungesehen liefern)
- Export über TMP-Frames (`rescale(1.5)`), `download_assets` je `nodeId`, mit `scripts/stitch_parts.py` zusammensetzen, Vorschau ansehen.
- Checkliste: Karte komplett sichtbar und nicht in Fades; keine Umbrüche zwischen Zahl und Einheit; Umlaute; keine Gedankenstriche; jede Sektion hat CTA; Badges weiß; Handy-Displays befüllt; nichts überlappt Labels.
- Vorschau-JPG ans Team schicken (SendUserFile), kurze Zusammenfassung.

## 4. Klaviyo-Upload → `references/klaviyo-und-connectoren.md`
- Config-JSON schreiben (Vorlage im Docstring von `scripts/klaviyo_sync.py`), dann `python3 $SKILL/scripts/klaviyo_sync.py config.json [m1 m2 …]`.
- Das Skript: 1620-px-Slices (Baseline-JPEG, ≤ ~760 KB), Upload, **neues** Template mit EB-Footer (DARK v2 / LIGHT), Zuweisung an **jede Variante** der Kampagne (A/B-Tests), Prüfung von Links, Slices, Abmelde-/Präferenz-Tags, Status.
- Ergebnis muss pro Variante „OK“ zeigen und die Kampagne „Draft“ bleiben. Nie senden/planen ohne OK.
- Danach `TMP-`-Frames in Figma löschen, Copy-Deck um einen Änderungsblock ergänzen (Template-IDs, Hashes, was geändert wurde).

## 5. Lernen festhalten
Neue Erkenntnis (Team-Feedback, Tool-Bug, Workaround) → in die passende Datei unter `references/` schreiben (und ins Claude-Gedächtnis), damit der nächste Account sie auch hat. Bei „Learnings ins Playbook übernehmen“ zusätzlich das GitHub-Repo pflegen: `references/playbook-repo.md`.

## Harte Regeln
- Klaviyo-Key nie ausgeben; Templates nie überschreiben; Kampagnen bleiben Entwurf.
- **Geplante/gesendete Kampagnen nicht ändern** (Status vorher prüfen; `klaviyo_sync.py` überspringt sie automatisch). Geplante nur nach ausdrücklichem OK mit `--auch-geplante`.
- Chatarmin: nie ohne OK bei Meta einreichen oder senden; speichern mit „Save as Draft“.
- Exporte/Uploads nur auf Anfrage; Temporäres ins Scratchpad.
- Tracker Karte: Hauptdarsteller, unverändert (echtes Foto), nie schwebend, nie in Fade/Label-Zone.
