"""Umgebungs-Check für das EB-Mail-Playbook. Braucht nur das Repo. Gibt nie Secrets aus."""
import os, importlib, json, urllib.request, glob
ok = lambda b: '✅' if b else '❌'
home = os.path.expanduser('~')
SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PB = os.path.dirname(os.path.dirname(SKILL)) if os.path.basename(os.path.dirname(SKILL)) == 'skill' else None
miss = []
def chk(cond, label, fix=None):
    print('  ', ok(cond), label)
    if not cond and fix: miss.append(f'{label}: {fix}')
print('Python-Pakete:')
for p, pipn in [('PIL', 'pillow'), ('numpy', 'numpy'), ('requests', 'requests')]:
    try: importlib.import_module(p); chk(True, p)
    except Exception: chk(False, p, f'pip3 install {pipn}')
print('Playbook (Repo):')
chk(PB is not None, f'Repo gefunden: {PB}', 'Skill aus dem Repo nutzen (scripts/install.sh)')
if PB:
    for rel in ['LEARNINGS.md', 'CLAUDE.md']:
        chk(os.path.exists(os.path.join(PB, rel)), rel, 'Repo unvollständig → git pull')
    for rel in ['agency', 'campaigns', 'assets/mockups/src']:
        print('  ', '✅' if os.path.exists(os.path.join(PB, rel)) else '⚪', rel, '(eigene private Daten, optional)')
print('  ', '✅' if os.path.exists(os.path.join(SKILL, 'assets/badges/badge-apple-findmy-white-2x.png')) else '⚪', 'Badges (weiß, optional, mit build_badges.py erzeugen)')
sk = os.path.join(home, '.claude/skills/eb-mail-produktion/SKILL.md'); chk(os.path.exists(sk), 'Skill installiert (~/.claude/skills)', './scripts/install.sh')
mems = [m for m in glob.glob(os.path.join(home, '.claude/projects/*/memory/MEMORY.md')) if 'eb-mail-produktion' in open(m).read()]
key = '-' + PB.strip('/').replace('/', '-').replace('.', '-') if PB else ''
print('  ', '✅' if any(key in m for m in mems) else '⚪', 'Claude-Gedächtnis für den Repo-Ordner (optional)')
print('System:')
chk(os.path.exists('/System/Library/Fonts/SFNS.ttf'), 'SF-Systemschrift (nur für neue Screens/Badges)', 'nur macOS; fertige Badge-PNGs nutzen')
kp = os.path.join(home, '.klaviyo_api_key'); has = os.path.exists(kp)
chk(has, '~/.klaviyo_api_key', 'Datei anlegen (chmod 600), Key aus Klaviyo → Einstellungen → API-Keys, nie per Chat')
if has:
    try:
        k = open(kp).read().strip(); r = urllib.request.urlopen(urllib.request.Request('https://a.klaviyo.com/api/accounts/', headers={'Authorization': 'Klaviyo-API-Key ' + k, 'revision': '2025-07-15', 'accept': 'application/vnd.api+json'}), timeout=20)
        acc = json.loads(r.read())['data'][0]; chk(True, f"Klaviyo-Account {acc['attributes'].get('contact_information', {}).get('organization_name', '')} erreichbar")
    except Exception as e: chk(False, f'Klaviyo erreichbar ({type(e).__name__})', 'Key prüfen')
eb = os.environ.get('EB_ROOT', os.path.join(home, 'EB'))
print('Optional:', '✅' if os.path.isdir(eb) else '⚪', f'EB-Ordner mit Rohfotos ({eb}) – nur für neue Original-Fotos nötig')
print('\nConnectoren (Figma, Klaviyo, Chatarmin, Higgsfield, Shopify) prüft Claude selbst, siehe SKILL.md „Preflight“.')
print('\nERGEBNIS:', 'alles bereit ✅' if not miss else f'{len(miss)} Punkt(e) offen:')
for m in miss: print('  →', m)
