"""iOS-„Wo ist?“-Ortungsscreen (dunkel) für die Tracker Karte Pro. Pin zeigt das echte Kartenfoto."""
import numpy as np, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 920, 2000; SS = 2
SF = '/System/Library/Fonts/SFNS.ttf'
def font(size, w=400):
    f = ImageFont.truetype(SF, size * SS); f.set_variation_by_axes([100, min(96, max(17, size)), 400, w]); return f
def build(out='findmy-locate-screen.png'):
    im = Image.new('RGB', (W * SS, H * SS), (30, 31, 34)); d = ImageDraw.Draw(im)
    k = SS; rnd = random.Random(7)
    # --- Karte: Blöcke, Park, Wasser, Straßen
    for _ in range(70):
        x, y = rnd.randint(-60, W), rnd.randint(0, 1250); w, h = rnd.randint(60, 190), rnd.randint(50, 150)
        d.rounded_rectangle([x * k, y * k, (x + w) * k, (y + h) * k], radius=10 * k, fill=(38, 39, 43))
    d.polygon([(p[0] * k, p[1] * k) for p in [(560, 150), (800, 110), (860, 300), (640, 360)]], fill=(33, 52, 40))   # Park
    d.polygon([(p[0] * k, p[1] * k) for p in [(-10, 930), (300, 860), (520, 960), (520, 1020), (260, 950), (-10, 1030)]], fill=(28, 44, 66))  # Spree
    roads = [((-50, 420), (980, 330), 22), ((120, -20), (330, 1300), 20), ((-50, 760), (980, 640), 16), ((640, -20), (560, 1300), 18),
             ((-50, 150), (980, 60), 12), ((800, -20), (980, 1300), 10), ((-50, 1120), (980, 1050), 12), ((420, -20), (430, 1300), 9),
             ((-50, 560), (500, 1300), 9), ((700, 420), (980, 900), 8)]
    for (a, b, w) in roads:
        d.line([(a[0] * k, a[1] * k), (b[0] * k, b[1] * k)], fill=(62, 64, 70), width=w * k)
    lbl = font(22, 500)
    for txt, (x, y), ang in [('Friedrichstraße', (360, 1000), -85), ('Unter den Linden', (40, 380), -5), ('Torstraße', (520, 120), -5)]:
        t = Image.new('RGBA', (int(lbl.getlength(txt)) + 20, 60), (0, 0, 0, 0)); ImageDraw.Draw(t).text((10, 5), txt, font=lbl, fill=(140, 142, 150))
        t = t.rotate(ang, expand=True, resample=Image.BICUBIC); im.paste(t, (x * k, y * k), t)
    # --- Standort Nutzer (blauer Punkt)
    ux, uy = 250, 900
    for r, a in [(60, 40), (22, 255)]:
        ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse([(ux - r) * k, (uy - r) * k, (ux + r) * k, (uy + r) * k], fill=(10, 132, 255, a)); im.paste(ov, (0, 0), ov)
    d.ellipse([(ux - 22) * k, (uy - 22) * k, (ux + 22) * k, (uy + 22) * k], outline=(255, 255, 255), width=5 * k)
    # --- Ortungs-Pulse um die Karte
    px, py = 540, 600
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for r, a in [(250, 26), (185, 40), (125, 60)]:
        od.ellipse([(px - r) * k, (py - r) * k, (px + r) * k, (py + r) * k], fill=(52, 199, 89, a), outline=(52, 199, 89, a * 3), width=3 * k)
    im.paste(ov, (0, 0), ov); d = ImageDraw.Draw(im)
    # gestrichelte Route
    for t in np.linspace(0.08, 0.86, 16):
        x = ux + (px - ux) * t; y = uy + (py + 70 - uy) * t
        d.ellipse([(x - 6) * k, (y - 6) * k, (x + 6) * k, (y + 6) * k], fill=(10, 132, 255))
    # --- Pin mit echtem Kartenfoto
    R = 78
    d.polygon([((px - 26) * k, (py + R - 8) * k), ((px + 26) * k, (py + R - 8) * k), (px * k, (py + R + 34) * k)], fill=(255, 255, 255))
    d.ellipse([(px - R) * k, (py - R) * k, (px + R) * k, (py + R) * k], fill=(255, 255, 255))
    cut = Image.open('card-cut-clean.png').convert('RGBA'); c = cut.crop(cut.getchannel('A').getbbox())
    c = c.crop((0, 0, c.width, int(c.height * 0.62)))                       # Kartenkörper ohne Spiegelung
    inner = Image.new('RGB', (2 * (R - 8) * k, 2 * (R - 8) * k), (18, 18, 20))
    s = inner.width * 0.92 / c.width; cc = c.resize((round(c.width * s), round(c.height * s)), Image.LANCZOS)
    inner.paste(cc, ((inner.width - cc.width) // 2, (inner.height - cc.height) // 2), cc)
    m = Image.new('L', inner.size, 0); ImageDraw.Draw(m).ellipse([0, 0, inner.width - 1, inner.height - 1], fill=255)
    im.paste(inner, ((px - R + 8) * k, (py - R + 8) * k), m)
    # --- Statusleiste
    d.text((58 * k, 26 * k), '11:06', font=font(36, 600), fill=(255, 255, 255))
    for i, hgt in enumerate([10, 15, 20, 26]):
        x = 700 + i * 13; d.rounded_rectangle([x * k, (58 - hgt) * k, (x + 8) * k, 58 * k], radius=2 * k, fill=(255, 255, 255))
    d.rounded_rectangle([780 * k, 34 * k, 842 * k, 62 * k], radius=8 * k, outline=(255, 255, 255), width=3 * k)
    d.rounded_rectangle([785 * k, 39 * k, 830 * k, 57 * k], radius=4 * k, fill=(255, 255, 255))
    # --- Bottom Sheet
    top = 1180
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([0, (top - 6) * k, W * k, (H + 40) * k], radius=44 * k, fill=(0, 0, 0, 120))
    im.paste(sh.filter(ImageFilter.GaussianBlur(18 * k)), (0, 0), sh.filter(ImageFilter.GaussianBlur(18 * k))); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, top * k, W * k, (H + 40) * k], radius=44 * k, fill=(28, 28, 30))
    d.rounded_rectangle([(W / 2 - 40) * k, (top + 16) * k, (W / 2 + 40) * k, (top + 26) * k], radius=5 * k, fill=(90, 90, 96))
    d.text((56 * k, (top + 58) * k), 'Tracker Karte Pro', font=font(58, 700), fill=(255, 255, 255))
    d.text((56 * k, (top + 140) * k), 'Black Member', font=font(32, 500), fill=(170, 170, 176))
    d.text((56 * k, (top + 184) * k), 'Friedrichstraße, Berlin  ·  Jetzt', font=font(32, 400), fill=(142, 142, 147))
    # Chip „Wird geortet“
    d.rounded_rectangle([56 * k, (top + 246) * k, 360 * k, (top + 302) * k], radius=28 * k, fill=(29, 58, 38))
    d.ellipse([78 * k, (top + 265) * k, 96 * k, (top + 283) * k], fill=(52, 199, 89))
    d.text((110 * k, (top + 256) * k), 'Wird geortet', font=font(30, 600), fill=(90, 220, 120))
    # Aktionen
    for i, (lab, sub) in enumerate([('Ton abspielen', 'Aus'), ('Route', '6 Min. zu Fuß')]):
        x0 = 56 + i * 412; y0 = top + 346
        d.rounded_rectangle([x0 * k, y0 * k, (x0 + 392) * k, (y0 + 200) * k], radius=30 * k, fill=(44, 44, 46))
        cx, cy = x0 + 64, y0 + 62
        d.ellipse([(cx - 34) * k, (cy - 34) * k, (cx + 34) * k, (cy + 34) * k], fill=(10, 132, 255) if i else (52, 199, 89))
        if i == 0:  # Lautsprecher
            d.polygon([((cx - 16) * k, (cy - 9) * k), ((cx - 6) * k, (cy - 9) * k), ((cx + 6) * k, (cy - 19) * k), ((cx + 6) * k, (cy + 19) * k), ((cx - 6) * k, (cy + 9) * k), ((cx - 16) * k, (cy + 9) * k)], fill=(255, 255, 255))
            d.arc([(cx + 2) * k, (cy - 14) * k, (cx + 22) * k, (cy + 14) * k], -60, 60, fill=(255, 255, 255), width=4 * k)
        else:       # Pfeil
            d.polygon([((cx - 14) * k, (cy + 16) * k), (cx * k, (cy - 18) * k), ((cx + 14) * k, (cy + 16) * k), (cx * k, (cy + 8) * k)], fill=(255, 255, 255))
        d.text(((x0 + 30) * k, (y0 + 112) * k), lab, font=font(34, 600), fill=(255, 255, 255))
        d.text(((x0 + 30) * k, (y0 + 156) * k), sub, font=font(28, 400), fill=(142, 142, 147))
    # Liste
    y = top + 590
    for lab, val in [('Benachrichtigungen', 'Bei Zurücklassen'), ('Verloren-Modus', 'Aus')]:
        d.line([(56 * k, y * k), ((W - 56) * k, y * k)], fill=(58, 58, 60), width=2 * k)
        d.text((56 * k, (y + 34) * k), lab, font=font(34, 500), fill=(255, 255, 255))
        tw = font(30).getlength(val) / k; d.text(((W - 56 - tw) * k, (y + 38) * k), val, font=font(30), fill=(142, 142, 147))
        y += 110
    d.rounded_rectangle([(W / 2 - 140) * k, (H - 26) * k, (W / 2 + 140) * k, (H - 16) * k], radius=5 * k, fill=(230, 230, 235))
    im = im.resize((W, H), Image.LANCZOS); im.save(out); return im
if __name__ == '__main__':
    build()
