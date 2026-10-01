# Design- und Copy-Regeln (Team, verbindlich)

## Copy
- Deutsch, Du-Form, kurz und konkret. **Keine Gedankenstriche** (– —) in Mail-Copy, stattdessen Punkt, Komma oder Doppelpunkt.
- Umlaute immer korrekt (ä ö ü ß), nie ae/oe/ue.
- Nichts erfinden: Fakten, Zahlen, Reviews nur aus BRAND.md / Briefing. Fehlt etwas: „Mir fehlt: …“ melden.
- Trust-Zahlen Essentialbag: 160.000+ zufriedene Kunden · 4,4/5 Trustpilot · 60 Tage Rückgaberecht.
- Scarcity/Zahlen mit Einheit immer mit **geschütztem Leerzeichen** (`1.000 Stück`), sonst Umbruch zwischen Zahl und Wort.
- Scarcity-Platzierung (bewährt): Eyebrow ganz oben („EARLY ACCESS · NUR 1.000 STÜCK“) + eine zweite Stelle im Body (fett im Hero-Sub, Bundle-Sub, Beleg-Kopf). Nur ändern, wenn die Zeile nicht umbricht (Höhe vorher/nachher vergleichen).

## Design
- **Keine harten Farbblöcke** zwischen Sektionen: eine durchgehende Grundfarbe (Dark: #0B0B0D), Kontraste als Panels mit Rand, Übergänge per Fade.
- **Hero (Apol-Anatomie):** Logo → Eyebrow → XXL-Headline (1–2 Zeilen, kein Glow/Effekt) → Sub Poppins Light mit Bold-Fakten → GENAU EIN weißer CTA (Ausnahme auf Wunsch: Early Access zusätzlich Outline-Button „EXKLUSIVE VORSCHAU“).
- **Knockout-CTAs** (Text aus Balken ausgestanzt), eckig 960×148 bei x60, Poppins ExtraBold, Letter-Spacing −5 %.
- **CTA nach JEDER Content-Sektion**, Labels variieren. Trust-Zahlen + Footer ohne CTA.
- Benefits nie als Bullet-Liste: Icon-Karten im Grid (r24–28, Icon-Kreis, Bold-Titel, Subzeile).
- Kein Liquid-Glass, keine Glow-Effekte auf Headlines.
- Alles mittig, enge Sektionsabstände, kein toter Raum unter Hero-Motiven.

## Produktbilder (Tracker Karte Pro / Smart Wallet)
- Die **Tracker Karte ist Hauptdarsteller** jeder Hero: groß, im Vordergrund, komplett sichtbar, **nie in Fade- oder Label-Zone** (Kartenunterkante oberhalb des Hero-Bottom-Fades).
- Karte darf generiert werden (seit 29.09.2026), aber jedes Bild im Eng-Crop prüfen: EB-Prägung, Chip, „BLACK MEMBER / MEMBER SINCE 2026 / VALID THRU 12/33“ Buchstabe für Buchstabe. Für Heroes bevorzugt das echte Foto (Freisteller `card-cut-clean.png`, nur skalieren/platzieren).
- **Nie schweben lassen:** Karte steht auf Spiegelboden mit eigener Spiegelung (wie Mail-1-Hero) oder liegt mit engem Kontaktschatten + sichtbarer Kante. Versetzte, weiche Schatten wirken wie Schweben → abgelehnt.
- Realistische Proportion: Kartenhöhe ≈ 36 % der Handyhöhe nebeneinander; im Vordergrund bis ~55 % (Perspektive).
- Handy-Displays nie leer, nie generiert: echte/nachgebaute Screens per Homographie einsetzen. Persönliche Adressen in Screenshots ersetzen (z. B. „Friedrichstraße, Berlin“).
- Kompatibilität immer mit den **offiziellen Badges** „Works with Apple Find My“ / „Works with Google's Find Hub“ in Weiß (Logos original): `assets/badges/`.
- In übersetzten Briefings heißt die Tracker Karte manchmal „Tracker-Map“.

## Footer
- Jede Klaviyo-Mail endet mit dem EB-Footer: dunkle Mail → DARK v2 (Bild-Buttons, Dark-Mode-sicher, Hintergrund = Mail-Grundfarbe), helle Mail → LIGHT (#FCF7EB). `scripts/footer/eb_footer.py` macht beides.
