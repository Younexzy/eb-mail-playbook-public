"""Hero v2: Tracker Karte Pro prominenter (größer, weiter vorn). Karte = unverändertes Originalfoto, nur skaliert/platziert."""
import numpy as np
from PIL import Image, ImageFilter
from card_beside import extend, card, body_w, body_top, body_bottom
def place2(base, card_h_px, floor_y, x_left, reflection=True, shadow=True, refl_strength=1.0):
    s = card_h_px / (body_bottom - body_top)
    c = card if reflection else card.crop((0, 0, card.size[0], body_bottom + 6))
    c = c.resize((round(c.size[0] * s), round(c.size[1] * s)), Image.LANCZOS)
    if reflection and refl_strength != 1.0:
        a = np.array(c).astype(float); cut = round(body_bottom * s) + 2
        a[cut:, :, 3] *= refl_strength; c = Image.fromarray(a.clip(0, 255).astype('uint8'))
    y = round(floor_y - body_bottom * s)
    out = base.convert('RGBA')
    if shadow:
        sh = Image.new('RGBA', out.size, (0, 0, 0, 0)); a = np.zeros((out.size[1], out.size[0]), 'uint8')
        x0, x1 = x_left + int(20 * s), x_left + int((body_w - 20) * s)
        a[int(floor_y - 12):int(floor_y + 26), max(0, x0):x1] = 160
        sh.putalpha(Image.fromarray(a).filter(ImageFilter.GaussianBlur(16))); out = Image.alpha_composite(out, sh)
    out.alpha_composite(c, (x_left, y)); return out.convert('RGB'), (x_left, y, x_left + c.size[0], y + round(body_bottom * s))
def pad_v(base, top=0, bottom=0):
    a = np.array(base.convert('RGB')).astype(float); H, W, _ = a.shape
    parts = []
    if top:
        row = a[:10].mean(0); parts.append(np.repeat(row[None], top, 0) * np.linspace(0.9, 1.0, top)[:, None, None])
    parts.append(a)
    if bottom:
        row = a[-24:].mean(0); parts.append(np.repeat(row[None], bottom, 0) * np.linspace(1.0, 0.8, bottom)[:, None, None])
    return Image.fromarray(np.concatenate(parts, 0).clip(0, 255).astype('uint8'))
def crop_aspect(im, ytop, H, aspect, cx):
    W = round(H * aspect); x0 = max(0, min(im.width - W, round(cx - W / 2))); return im.crop((x0, ytop, x0 + W, ytop + H)), x0
