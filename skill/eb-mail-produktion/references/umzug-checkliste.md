# Neuer Account / neuer Rechner: gleicher Output

Das Repo `eb-mail-playbook` enthält das gesamte Wissen (Learnings, Skill, Skripte, Mockup-Assets, Brand-Kit, Kampagnen-Archiv, Gedächtnis). Der EB-Ordner ist NICHT nötig, nur optional für Original-Rohfotos und alte Exporte.

## Was zusätzlich zum Repo nötig ist (kann nicht ins Repo)
| Baustein | Warum | Wie |
|---|---|---|
| Figma-Connector mit dem Account, der Zugriff auf die Mail-Datei hat (Professional-Plan) | Login | claude.ai → Einstellungen → Connectoren |
| Klaviyo, Chatarmin, Higgsfield, Shopify Connectoren | Logins | dito |
| `~/.klaviyo_api_key` (chmod 600) | Geheimnis, nie in GitHub | Datei anlegen; Key aus Klaviyo → Einstellungen → API-Keys. Nie per Chat schicken |
| Modell Opus 5.5 + gleicher Effort | App-Einstellung | Modellauswahl in der App |
| Python 3 + `pip3 install pillow numpy requests` | Laufzeit | einmalig |
| macOS (SF-Systemschrift für Screens/Badges) | Schrift | auf Windows/Linux Badges als fertige PNGs nutzen |

## Schritte
1. `git clone <URL dieses Repos>` (Ort egal, z. B. `~/EB/Repos/`).
2. `./scripts/install.sh` → verlinkt den Skill, spielt das Gedächtnis für den Repo-Ordner ein, prüft alles.
3. Connectoren verbinden (Tabelle oben), Klaviyo-Key-Datei anlegen.
4. In der Claude-App (Code-Tab) **den Repo-Ordner öffnen** und Opus 5.5 wählen. `CLAUDE.md` im Repo wird automatisch gelesen.
5. Für reine claude.ai-Chats ohne Code-Tab: `./scripts/make-skill-zip.sh` → ZIP unter Einstellungen → Skills hochladen.
6. In Claude: „Mach den Preflight aus eb-mail-produktion“.
