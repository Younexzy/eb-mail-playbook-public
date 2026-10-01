# EB Mail Playbook

Ein erprobter Workflow, mit dem **Claude Code** Kampagnen-Mails für einen D2C-Shop baut: Design in **Figma**, realistische Produkt-Heroes mit Handy-Mockups, Export in Bild-Slices und Upload als Entwurf nach **Klaviyo**, inklusive A/B-Varianten, Dark-Mode-sicherem Footer und Prüfungen. Entstanden bei Essentialbag (Smart Wallets & Tracker Karten).

## Inhalt
| Datei/Ordner | Inhalt |
|---|---|
| [`LEARNINGS.md`](LEARNINGS.md) | Alle Learnings A–T: Copy, Scarcity, Design, Produktbilder, Figma-/Klaviyo-/Chatarmin-/Higgsfield-Workarounds, Flows, Shopify-Tricks, Betreffzeilen |
| [`skill/eb-mail-produktion/`](skill/eb-mail-produktion/SKILL.md) | Claude-Skill mit Workflow, Regeln und Skripten |
| `skill/…/scripts/klaviyo_sync.py` | Slices schneiden, komprimieren, als neue Template-Kopie hochladen, allen A/B-Varianten zuweisen, prüfen; überspringt geplante/gesendete Kampagnen |
| `skill/…/scripts/mockups/` | Handy-Greenscreen + Homographie, Karte auf Spiegelboden, „Wo ist?“-Ortungsscreen |
| `skill/…/assets/badges/build_badges.py` | Offizielle „Works with“-Badges in Weiß nachbauen (Logos original) |
| [`CLAUDE.md`](CLAUDE.md) | Wird von Claude Code automatisch gelesen |

## Schnellstart
```bash
git clone <URL dieses Repos> eb-mail-playbook && cd eb-mail-playbook
./scripts/install.sh
```
Dann den Ordner in Claude Code öffnen und „Mach den Preflight aus eb-mail-produktion“ sagen.

## Eigene Daten ergänzen (bleiben privat)
Nicht enthalten und bewusst nicht öffentlich: Brand-Kit, Kampagnen, Produktfotos, Handy-Renders, Footer-Dateien, IDs, API-Schlüssel. Lege sie lokal an (z. B. in einem privaten Fork):
- `agency/Brands/<brand>/BRAND.md` (Fakten, Farben, Fonts)
- `campaigns/<name>/` (Copy-Decks, Klaviyo-IDs)
- `assets/mockups/src/` (Greenscreen-Renders, Produkt-Freisteller), `assets/mockups/` (fertige Mockups)
- `skill/eb-mail-produktion/scripts/footer/` (siehe README dort)
- `~/.klaviyo_api_key` (chmod 600, nie committen)

## Voraussetzungen
Claude Code mit Connectoren für Figma (Professional-Plan), Klaviyo, optional Chatarmin, Higgsfield, Shopify · Python 3 mit `pillow numpy requests` · macOS für neue Screens/Badges (SF-Systemschrift).
