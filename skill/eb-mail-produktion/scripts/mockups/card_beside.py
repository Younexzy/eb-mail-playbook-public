import numpy as np
from PIL import Image, ImageFilter
cut = Image.open('card-cut-clean.png').convert('RGBA')
card = cut.crop((280, 1600, 1240, 2752))            # Karte + Spiegelung
body_w, body_top, body_bottom = 940, 10, 650         # Kartenkörper innerhalb des Crops (px)
def extend(base, add_right=0, add_left=0):
    a = np.array(base.convert('RGB')).astype(float); H, W, _ = a.shape
    def pad(col, n):   # Randspalten verlängern + leicht abdunkeln nach außen
        strip = np.repeat(col[:, None, :], n, axis=1)
        fade = np.linspace(1.0, 0.85, n)[None, :, None]; return strip * fade
    L = pad(a[:, :8].mean(axis=1), add_left)[:, ::-1] if add_left else np.zeros((H, 0, 3))
    R = pad(a[:, -8:].mean(axis=1), add_right) if add_right else np.zeros((H, 0, 3))
    return Image.fromarray(np.concatenate([L, a, R], axis=1).clip(0, 255).astype('uint8'))
def place(base, phone_h_px, floor_y, x_left, keep_reflection=True, shadow=True):
    s = (0.36 * phone_h_px) / (body_bottom - body_top)          # Kartenhöhe = 36 % der Handyhöhe (54 mm / 150 mm)
    c = card if keep_reflection else card.crop((0, 0, card.size[0], body_bottom + 6))
    c = c.resize((round(c.size[0] * s), round(c.size[1] * s)), Image.LANCZOS)
    y = round(floor_y - body_bottom * s)
    out = base.convert('RGBA')
    if shadow:
        sh = Image.new('RGBA', out.size, (0, 0, 0, 0)); a = np.zeros((out.size[1], out.size[0]), 'uint8')
        x0, x1 = x_left + int(20 * s), x_left + int((body_w - 20) * s)
        a[int(floor_y - 10):int(floor_y + 22), x0:x1] = 150
        sh.putalpha(Image.fromarray(a).filter(ImageFilter.GaussianBlur(14))); out = Image.alpha_composite(out, sh)
    out.alpha_composite(c, (x_left, y)); return out.convert('RGB')
