import numpy as np
def fit_line(pts):
    c = pts.mean(0); w, V = np.linalg.eigh(np.cov((pts - c).T)); d = V[:, -1]; return c, d
def inter(l1, l2):
    (c1, d1), (c2, d2) = l1, l2; A = np.array([d1, -d2]).T; t = np.linalg.solve(A, c2 - c1); return c1 + t[0] * d1
def screen_quad(mask):
    ys, xs = np.nonzero(mask); P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0); w, V = np.linalg.eigh(np.cov((P - c).T)); d = V[:, -1]   # Längsachse
    if d[1] < 0: d = -d                                                  # d zeigt "nach unten" (Richtung Home-Ende)
    r = np.array([d[1], -d[0]])                                          # rechte Bildschirmseite
    # Randpixel
    m = mask; edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
    ey, ex = np.nonzero(edge); E = np.stack([ex, ey], 1).astype(float)
    u = (E - c) @ d; v = (E - c) @ r; ur, vr = np.ptp(u), np.ptp(v)
    def pick(cond): return E[cond]
    top = pick((u < u.min() + 0.03 * ur) & (np.abs(v) < 0.3 * vr))
    bot = pick((u > u.max() - 0.03 * ur) & (np.abs(v) < 0.3 * vr))
    lef = pick((v < v.min() + 0.03 * vr) & (np.abs(u) < 0.35 * ur))
    rig = pick((v > v.max() - 0.03 * vr) & (np.abs(u) < 0.35 * ur))
    T, B, L, R = map(fit_line, (top, bot, lef, rig))
    return [tuple(inter(T, L)), tuple(inter(T, R)), tuple(inter(B, R)), tuple(inter(B, L))]   # TL TR BR BL
