"""Mail-2-Hero: liegende Tracker Karte Pro realistisch AUF dem Tisch (Kontaktschatten, AO, Kartenkante). Karteninhalt unverändert."""
from PIL import Image, ImageFilter, ImageChops
import numpy as np
def build(scale=0.88, x=230, y=760, edge=(1, 4), variant='A'):
    base = Image.open('../mock-iphone-lying.png').convert('RGBA')
    cut = Image.open('card-lying-clean.png').convert('RGBA')
    bb = cut.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox(); card = cut.crop(bb)
    s = (scale * 1134) / 1600
    card = card.resize((round(card.size[0] * s), round(card.size[1] * s)), Image.LANCZOS)
    P = 120; A = Image.new('L', (card.size[0] + 2 * P, card.size[1] + 2 * P), 0); A.paste(card.getchannel('A'), (P, P))
    def layer(alpha, color=(0, 0, 0)):
        l = Image.new('RGBA', alpha.size, color + (255,)); l.putalpha(alpha); return l
    shadows = {  # (blur, opacity, dx, dy)
        'A': [(34, 0.30, 10, 20), (12, 0.50, 4, 9), (5, 0.55, 0, 0), (2.2, 0.95, 1, 4)],
        'B': [(26, 0.38, 8, 16), (9, 0.55, 3, 7), (4, 0.6, 0, 0), (1.8, 1.0, 1, 3)],
    }[variant]
    for blur, k, dx, dy in shadows:
        a = A.filter(ImageFilter.GaussianBlur(blur)).point(lambda v, k=k: int(v * k))
        base.alpha_composite(layer(a), (x - P + dx, y - P + dy))
    # Kartenkante (Dicke ~0,8 mm): Silhouette leicht nach unten versetzt, dunkles Anthrazit mit Lichtkante
    ex, ey = edge
    side = A.filter(ImageFilter.GaussianBlur(0.6))
    base.alpha_composite(layer(side, (26, 26, 28)), (x - P + ex, y - P + ey))
    base.alpha_composite(card, (x, y))
    return base.convert('RGB'), (x, y, x + card.width, y + card.height)
if __name__ == '__main__':
    S = '../preview/'; __import__('os').makedirs(S, exist_ok=True)
    for v in 'AB':
        out, bb = build(variant=v); print(v, bb)
        out.save(f'../hero-v4-m2-{v}.png')
        out.crop((150 + 0, 150 + 500, 150 + 1400, 150 + 1300)).save(S + f'm2_contact_{v}.jpg', quality=90)
