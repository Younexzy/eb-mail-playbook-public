# Klaviyo, Chatarmin und Connector-Workarounds

## Klaviyo (REST-Fallback)
- Key in `~/.klaviyo_api_key` (chmod 600). **Nie ausgeben**, nie in Chat/Logs/Memory. curl-Einzeiler mit `$(cat …)` blockt der Auto-Mode → immer Skript-Datei.
- Header: `Authorization: Klaviyo-API-Key <key>`, `revision: 2025-07-15`.
- **Bild-Rezept:** Slices 1620 px breit, `UnsharpMask(0.6, 60, 2)`, Baseline-JPEG q60 (runter bis q48 bis ≤ ~760 KB/Mail), `progressive=False` (progressive JPEGs rendert Klaviyo kaputt).
- 8 Slices pro Mail; bei Buttons mit unterschiedlichen Links link-genau schneiden (Schnitt zwischen den Buttons), sonst 8 gleiche.
- **Nie Templates überschreiben:** immer neues Template (`POST /templates/`, `editor_type: CODE`) + `POST /campaign-message-assign-template/` (Klaviyo legt einen Klon an).
- **A/B-Tests:** `send_strategy.method == 'ab_test_campaign'` → mehrere campaign-messages. JEDER Variante das Template zuweisen; Betreff/Absender der Varianten nicht anfassen (Testgegenstand). `scripts/klaviyo_sync.py` macht das automatisch.
- Prüfen nach jedem Upload: Links in richtiger Reihenfolge, neue Slice-URLs drin, `POST /template-render/` enthält `[unsubscribe_tag]` + `[manage_preferences_tag]`, Kampagne steht weiter auf **Draft**.
- Neue Kampagne: `send_strategy static` braucht `datetime` (Platzhalter, Team setzt Sendezeit selbst); Audiences: eigenes Aktiv-Segment included, Ausschluss-Segment excluded; Absender wie in bisherigen Kampagnen.
- Niemals senden/planen ohne ausdrückliches OK.
- **Geplante oder gesendete Kampagnen nicht anfassen:** Status vorher prüfen. „Queued without Recipients“ = geplant (Sendezeiten setzt das Team selbst). Änderungen dort nur nach ausdrücklichem OK (`--auch-geplante`), gesendete nie. A/B-Tests legt das Team oft selbst an (Varianten B/C, „Maverick Optimizer“, z. B. Absender-Test); Klaviyo kopiert dabei das Template von A.

## Chatarmin (Org-ID aus Chatarmin)
- `expectedOrganizationId` ist Pflicht bei Schreibcalls.
- Bei leerem Tool-Schema scheitern Arrays/Zahlen. Funktioniert: `chatarmin_update_template_draft` mit nur `templateId` + `bodyText`.
- Template-Duplikat im Dashboard (Templates → „…“ → Duplicate), Speichern mit „Save as Draft“ (nicht „Save template“). Nie ohne OK bei Meta einreichen oder Kampagnen senden.

## Figma-MCP
- Zahlen-Parameter (`count`, `defaultScale`) kommen als String an → siehe figma-workflow.md (upload_assets ohne count, Export per `rescale(1.5)`).

## Allgemein
- Zugangsdaten nie eintippen, nie ausgeben. Outbound-Aktionen (Senden, Veröffentlichen, Meta-Einreichung) nur nach OK.
