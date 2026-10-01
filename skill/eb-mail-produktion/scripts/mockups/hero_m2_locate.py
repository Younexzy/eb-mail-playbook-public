"""Mail-2-Hero v5: iPhone mit Ortungsscreen der Tracker Karte Pro auf Spiegelboden, Karte steht daneben (wie Mail 1)."""
import numpy as np
from PIL import Image, ImageFilter
from hero_v2 import place2, extend, pad_v, crop_aspect
def floor_reflect(im, floor_y, depth=520, strength=0.30, x0=0, x1=None):
    a = np.array(im).astype(float); x1 = x1 or a.shape[1]
    src = a[floor_y - depth:floor_y, x0:x1][::-1]
    bg = a[floor_y:floor_y + depth, x0:x1]
    g = (np.linspace(strength, 0, depth) ** 1.4 / strength ** 0.4)[:, None, None]
    lum = src.mean(2, keepdims=True); mask = np.clip((lum - 20) / 60, 0, 1)          # nur helle Teile spiegeln
    a[floor_y:floor_y + depth, x0:x1] = bg * (1 - g * mask) + src * g * mask
    return Image.fromarray(a.clip(0, 255).astype('uint8'))
def build(card_h=820, card_x=300, card_floor=2330, H=2900, asp=1080/1250, cx=1300):
    base = Image.open('../mock-iphone-locate.png').convert('RGB')
    L = 900; T = 150
    ext = pad_v(extend(base, add_left=L, add_right=300), top=T, bottom=700)
    fy = 2103 + T
    ext = floor_reflect(ext, fy, x0=L + 450, x1=L + 1400)
    out, bb = place2(ext, card_h, card_floor, card_x, reflection=True, shadow=False)
    ytop = round(card_floor - 0.80 * H)
    cr, x0 = crop_aspect(out, ytop, H, asp, cx)
    return cr, dict(card=bb, ytop=ytop, x0=x0, size=cr.size, phone_top_rel=(325 + T - ytop) / H, card_bottom_rel=(card_floor - ytop) / H)
if __name__ == '__main__':
    S = '../preview/'; __import__('os').makedirs(S, exist_ok=True)
    ims = []
    for i, kw in enumerate([dict(card_h=820, card_x=380, card_floor=2330), dict(card_h=900, card_x=260, card_floor=2380)]):
        im, info = build(**kw); print(i, info); im.save(f'../hero-v5-m2-{i}.png'); ims.append(im)
    row = [r.resize((round(r.width * 560 / r.height), 560)) for r in ims]
    c = Image.new('RGB', (sum(r.width for r in row) + 10, 560), 'white'); x = 0
    for r in row: c.paste(r, (x, 0)); x += r.width + 10
    c.save(S + 'm2_v5.jpg', quality=85)
