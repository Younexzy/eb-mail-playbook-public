import numpy as np
from PIL import Image, ImageFilter
def green_mask(a):
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    return (g > 150) & (g - r > 60) & (g - b > 60)
def fit_quad(mask):
    ys, xs = np.nonzero(mask); y0, y1 = ys.min(), ys.max(); x0, x1 = xs.min(), xs.max()
    band_y = range(int(y0 + (y1 - y0) * 0.2), int(y1 - (y1 - y0) * 0.2), 4)
    band_x = range(int(x0 + (x1 - x0) * 0.25), int(x1 - (x1 - x0) * 0.25), 3)
    L = np.array([(y, np.nonzero(mask[y])[0].min()) for y in band_y if mask[y].any()])
    R = np.array([(y, np.nonzero(mask[y])[0].max()) for y in band_y if mask[y].any()])
    T = np.array([(x, np.nonzero(mask[:, x])[0].min()) for x in band_x if mask[:, x].any()])
    B = np.array([(x, np.nonzero(mask[:, x])[0].max()) for x in band_x if mask[:, x].any()])
    lx = np.polyfit(L[:, 0], L[:, 1], 1); rx = np.polyfit(R[:, 0], R[:, 1], 1)   # x = a*y + b
    ty = np.polyfit(T[:, 0], T[:, 1], 1); by = np.polyfit(B[:, 0], B[:, 1], 1)   # y = a*x + b
    def inter(xl, yl):  # x = xl[0]*y+xl[1], y = yl[0]*x+yl[1]
        y = (yl[0] * xl[1] + yl[1]) / (1 - yl[0] * xl[0]); return (xl[0] * y + xl[1], y)
    return [inter(lx, ty), inter(rx, ty), inter(rx, by), inter(lx, by)]  # TL TR BR BL
def homography(src, dst):
    A = []
    for (x, y), (u, v) in zip(src, dst):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
    h = np.linalg.solve(np.array(A, float), np.array([c for p in dst for c in p], float)); return h
def place(base, screen, mask):
    quad = fit_quad(mask); sw, sh = screen.size
    # PIL PERSPECTIVE maps output coords -> input coords: solve dst(quad)->src(screen)
    coeffs = homography(quad, [(0, 0), (sw, 0), (sw, sh), (0, sh)])
    warped = screen.convert('RGB').transform(base.size, Image.PERSPECTIVE, tuple(coeffs), Image.BICUBIC)
    m = Image.fromarray((mask * 255).astype('uint8')).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    base.paste(warped, (0, 0), m); return quad
def split_masks(mask):
    cols = mask.any(axis=0); xs = np.nonzero(cols)[0]
    gaps = [i for i in range(1, len(xs)) if xs[i] - xs[i - 1] > 3]
    if not gaps: return [mask]
    cut = (xs[gaps[0] - 1] + xs[gaps[0]]) // 2
    a = mask.copy(); a[:, cut:] = False; b = mask.copy(); b[:, :cut] = False; return [a, b]
