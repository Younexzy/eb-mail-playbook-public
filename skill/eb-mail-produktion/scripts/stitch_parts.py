"""Figma-Teil-Exporte (TMP-Frames, bereits ×1.5 per rescale) zu einer 1620-px-Gesamtmail zusammensetzen.
python3 stitch_parts.py <ausgabe.png> <frame_hoehe_1x> teil1.png teil2.png …"""
import sys
from PIL import Image
out, H, parts = sys.argv[1], int(sys.argv[2]), [Image.open(p).convert('RGB') for p in sys.argv[3:]]
c = Image.new('RGB', (parts[0].width, sum(p.height for p in parts))); y = 0
for p in parts: c.paste(p, (0, y)); y += p.height
t = round(H * 1.5)
if c.height != t: c = c.resize((c.width, t), Image.LANCZOS)
c.save(out); print(out, c.size)
