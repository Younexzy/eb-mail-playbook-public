"""Bild-Slice-Mails nach Klaviyo: slicen, komprimieren, hochladen, NEUE Template-Kopie anlegen,
JEDER Variante der Kampagne zuweisen (A/B-Tests!), prüfen. Nichts wird überschrieben, Kampagnen bleiben Entwurf.

Aufruf:  python3 klaviyo_sync.py config.json [mailkey ...] [--auch-geplante]
Schutz: Kampagnen, die NICHT „Draft“ sind (geplant/gesendet), werden übersprungen. Nur mit
--auch-geplante und nach ausdrücklichem OK ändern; gesendete Kampagnen nie.
config.json:
{ "out_dir": "…/klaviyo-vX", "version": "v9",
  "mails": { "m1": { "full_png": "…/m1-full.png",          # 1620 px breit (Figma-Frame × 1.5)
                     "campaign": "01M…",                  # Kampagnen-ID (alle Nachrichten werden aktualisiert)
                     "name": "Kampagne · DE · Dark Footer", "preheader": "…", "title": "…", "variant": "dark",
                     "cuts": [0, 825, …, 7519],           # optional: Frame-px (1×) für link-genaue Schnitte, sonst 8 gleiche
                     "links": ["https://…", …],           # 1 Link für alle oder 8 Links (einer pro Slice)
                     "alts": ["…", … 8 Stück] } } }
Key: ~/.klaviyo_api_key (nie ausgeben)."""
import json, urllib.request, os, re, uuid, sys
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'footer')); import eb_footer
KEY = open(os.path.expanduser('~/.klaviyo_api_key')).read().strip(); BASE = 'https://a.klaviyo.com/api'
HJ = {'Authorization': 'Klaviyo-API-Key ' + KEY, 'revision': '2025-07-15', 'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json'}
def req(method, path, body=None, headers=HJ, raw=None):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    try: return json.loads(urllib.request.urlopen(urllib.request.Request(BASE + path, data=data, headers=headers, method=method)).read() or b'{}')
    except urllib.error.HTTPError as e: raise SystemExit(f'{method} {path} -> {e.code}: {e.read().decode()[:600]}')
def upload(fn):
    b = uuid.uuid4().hex; name = os.path.basename(fn)
    body = (f'--{b}\r\nContent-Disposition: form-data; name="name"\r\n\r\n{name[:-4]}\r\n--{b}\r\nContent-Disposition: form-data; name="file"; filename="{name}"\r\nContent-Type: image/jpeg\r\n\r\n').encode() + open(fn, 'rb').read() + f'\r\n--{b}--\r\n'.encode()
    h = {k: HJ[k] for k in ('Authorization', 'revision', 'accept')}; h['content-type'] = f'multipart/form-data; boundary={b}'
    return req('POST', '/image-upload/', headers=h, raw=body)['data']['attributes']['image_url']
def slices(m, c, out_dir, ver):
    full = Image.open(c['full_png']).convert('RGB'); H = full.height
    cuts = [round(y * 1.5) for y in c['cuts']] if c.get('cuts') else [round(H * i / 8) for i in range(9)]
    cuts[-1] = H
    for q in (60, 56, 52, 48):                      # Ziel: ≤ ~760 KB pro Mail, Baseline-JPEG (nie progressive!)
        files = []
        for i in range(len(cuts) - 1):
            fn = os.path.join(out_dir, f'bm-{m}{ver}-{i+1:02d}.jpg')
            full.crop((0, cuts[i], full.width, cuts[i+1])).filter(ImageFilter.UnsharpMask(0.6, 60, 2)).save(fn, 'JPEG', quality=q, optimize=True, progressive=False)
            files.append(fn)
        tot = sum(os.path.getsize(f) for f in files)
        if tot <= 760_000: break
    print(m, f'q{q}', tot // 1000, 'KB'); return files
def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    force = '--auch-geplante' in sys.argv; args = [a for a in sys.argv[1:] if a != '--auch-geplante']
    cfg = json.load(open(args[0])); keys = args[1:] or list(cfg['mails'])
    out_dir = cfg['out_dir']; ver = cfg.get('version', 'vX'); os.makedirs(out_dir, exist_ok=True)
    log_p = os.path.join(out_dir, f'klaviyo-{ver}-ids.json'); log = json.load(open(log_p)) if os.path.exists(log_p) else {}
    for m in keys:
        c = cfg['mails'][m]
        st = req('GET', f"/campaigns/{c['campaign']}/")['data']['attributes']
        if st['status'] != 'Draft' and (not force or st['status'] in ('Sent', 'Sending', 'Cancelled')):
            print(f"{m}: ÜBERSPRUNGEN, Kampagne ist '{st['status']}' (Versand {st.get('send_time')}). Nur Entwürfe werden geändert; geplante nur mit --auch-geplante nach OK, gesendete nie."); continue
        files = slices(m, c, out_dir, ver); n = len(files)
        links = c['links'] if len(c['links']) == n else [c['links'][0]] * n
        alts = (c.get('alts') or [''] * n)[:n]
        urls = [upload(f) for f in files]
        rows = ''.join(f'<tr><td><a href="{l}" target="_blank"><img alt="{a}" src="{u}" style="display:block;border:0;outline:none;text-decoration:none;width:100%;height:auto;" width="600"/></a></td></tr>' for l, a, u in zip(links, alts, urls))
        html = eb_footer.build(rows, c['preheader'], c['title'], c.get('variant', 'dark'), c.get('bg'))
        tid = req('POST', '/templates/', {'data': {'type': 'template', 'attributes': {'name': f"{c['name']} · {ver}", 'editor_type': 'CODE', 'html': html}}})['data']['id']
        camp = req('GET', f"/campaigns/{c['campaign']}/?include=campaign-messages")
        status = camp['data']['attributes']['status']; strat = camp['data']['attributes'].get('send_strategy', {}).get('method')
        res = {'template': tid, 'images': urls, 'status': status, 'variants': {}}
        for msg in camp.get('included', []):          # ALLE Varianten (A/B-Test) bekommen das Template
            mid = msg['id']; label = msg['attributes']['definition'].get('label', '')
            req('POST', '/campaign-message-assign-template/', {'data': {'type': 'campaign-message', 'id': mid, 'relationships': {'template': {'data': {'type': 'template', 'id': tid}}}}})
            chk = req('GET', f'/campaign-messages/{mid}/?include=template'); t = chk['included'][0]; h = t['attributes']['html']
            got = re.findall(r'<a href="([^"]+)" target="_blank"><img alt', h)
            r = req('POST', '/template-render/', {'data': {'type': 'template', 'attributes': {'id': t['id'], 'context': {}}}})
            tags = sorted(set(re.findall(r'\[(?:unsubscribe|manage_preferences)_tag\]', r['data']['attributes']['html'])))
            ok = got == links and all(u in h for u in urls) and len(tags) == 2
            print(f"  {m} {label[-40:]!r}: clone {t['id']} | links {got == links} | slices {all(u in h for u in urls)} | tags {tags} | {'OK' if ok else 'PRÜFEN!'}")
            res['variants'][mid] = {'label': label, 'assigned': t['id'], 'ok': ok}
        print(m, status, '| send_strategy', strat, '| Varianten', len(res['variants']))
        log[m] = res; json.dump(log, open(log_p, 'w'), indent=1)
if __name__ == '__main__': main()
