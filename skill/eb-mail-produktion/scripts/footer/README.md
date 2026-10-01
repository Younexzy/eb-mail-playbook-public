# Footer-Dateien (eigene, nicht im öffentlichen Repo)

`eb_footer.build()` hängt jeder Mail den Brand-Footer an. Lege dafür hier ab:
- `footer-dark-v2.html` – Footer für dunkle Mails. Buttons und Social-Icons als **Bilder** (sonst kippen sie im Dark Mode des Postfachs), Hintergrundfarbe `#000000` als Platzhalter (wird durch die Mail-Grundfarbe ersetzt). Pflicht-Links: `{% manage_preferences_link %}`/`[manage_preferences_tag]` und `[unsubscribe_tag]`, Adresse/Impressum.
- `eb-email-footer-SKILL.md` – enthält den LIGHT-Footer zwischen `<!-- ===== EB FOOTER · LIGHT … -->` und `<!-- ===== /EB FOOTER · LIGHT ===== -->`.
- `darkmode-meta.html` ist enthalten (generisch).
