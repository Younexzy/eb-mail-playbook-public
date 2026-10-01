"""EB-Pflicht-Footer an eine Bild-Slice-Mail hängen (self-contained, unabhängig vom App-Profil).
build(rows_html, preheader, title, 'dark'|'light', bg=None) -> komplettes HTML.
DARK = Dark-Mode-sichere v2 (Buttons/Icons als Bilder, Hintergrund = Mail-Grundfarbe, Standard #0B0B0D).
LIGHT = Footer-Block aus eb-email-footer-SKILL.md (Beige #FCF7EB).
Benötigte eigene Dateien in diesem Ordner (nicht im öffentlichen Repo): footer-dark-v2.html, eb-email-footer-SKILL.md (siehe README.md)."""
import glob, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
def _skill_md():
    local = os.path.join(HERE, 'eb-email-footer-SKILL.md')
    hits = glob.glob(os.path.expanduser('~/Library/Application Support/Claude*/local-agent-mode-sessions/skills-plugin/*/*/skills/eb-email-footer/SKILL.md'))
    if hits:  # neueste Version aus der App bevorzugen, sonst gebündelte Kopie
        newest = max(hits, key=os.path.getmtime)
        if os.path.getmtime(newest) > os.path.getmtime(local): return open(newest).read()
    return open(local).read()
def footer(variant):
    tag = 'DARK' if variant == 'dark' else 'LIGHT'
    m = re.search(r'(<!-- ===== EB FOOTER · ' + tag + r'.*?<!-- ===== /EB FOOTER · ' + tag + r' ===== -->)', _skill_md(), re.S)
    if not m: raise SystemExit('Footer-Block ' + tag + ' fehlt')
    return m.group(1)
def footer_dark_v2(bg='#0B0B0D'): return open(os.path.join(HERE, 'footer-dark-v2.html')).read().replace('#000000', bg)
def darkmode_meta(bg='#0B0B0D'): return open(os.path.join(HERE, 'darkmode-meta.html')).read().replace('#000000', bg)
def build(rows_html, preheader, title, variant, bg=None):
    bg = bg or ('#0B0B0D' if variant == 'dark' else '#FCF7EB')
    return f'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1" name="viewport"/>
<meta name="x-apple-disable-message-reformatting"/><title>{title}</title>
{darkmode_meta(bg) if variant == "dark" else ""}
<style>body{{margin:0;padding:0;background-color:{bg}}}table{{border-collapse:collapse}}img{{display:block;border:0;outline:none;text-decoration:none}}a{{text-decoration:none}}</style></head>
<body style="margin:0;padding:0;background-color:{bg};">
<div style="display:none;font-size:1px;color:{bg};line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{preheader}{'&#8203; ' * 6}</div>
<table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" style="background-color:{bg};" bgcolor="{bg}"><tr><td align="center">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" width="600" style="width:600px;max-width:600px;">{rows_html}</table>
</td></tr></table>
{footer_dark_v2(bg) if variant == "dark" else footer(variant)}
</body></html>'''
