import numpy as np
from PIL import Image
import sys

W = H = int(sys.argv[1]) if len(sys.argv) > 1 else 900
OUT = sys.argv[2] if len(sys.argv) > 2 else "ring.png"
sm = lambda a, b, x: np.clip((x - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((x - a) / (b - a), 0, 1))

def parts(p):
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    r = np.hypot(x, y); th = np.arctan2(y, x)
    top = np.clip(np.sin(th), 0, 1)
    t = 0.10 + 0.12 * top ** 2
    w = 0.27 + 0.10 * top
    rr = 0.06
    qx = np.abs(r - 1.0) - (t - rr); qz = np.abs(z) - (w - rr)
    dband = np.hypot(np.maximum(qx, 0), np.maximum(qz, 0)) + np.minimum(np.maximum(qx, qz), 0) - rr
    px = x / 0.68; pz = z / 0.58
    d2 = (np.hypot(px, pz) - 1) * 0.58
    yc = 1.12; dy = np.abs(y - yc) - 0.19
    a = d2 + 0.05; b = dy + 0.05
    dbez = np.hypot(np.maximum(a, 0), np.maximum(b, 0)) + np.minimum(np.maximum(a, b), 0) - 0.05
    k = 0.10
    h = np.clip(.5 + .5 * (dband - dbez) / k, 0, 1)
    d = dband * (1 - h) + dbez * h - k * h * (1 - h)
    return d

def sdf(p): return parts(p)

def normal(p):
    e = 1e-3
    n = np.stack([sdf(p + np.array([e, 0, 0])) - sdf(p - np.array([e, 0, 0])),
                  sdf(p + np.array([0, e, 0])) - sdf(p - np.array([0, e, 0])),
                  sdf(p + np.array([0, 0, e])) - sdf(p - np.array([0, 0, e]))], 1)
    return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)

# camera
tgt = np.array([0.0, 0.18, 0.0])
dirc = np.array([0.62, 0.78, 0.95]); dirc /= np.linalg.norm(dirc)
dist = 6.2
cam = tgt + dirc * dist
f = -dirc; up = np.array([0, 1.0, 0]); rt = np.cross(f, up); rt /= np.linalg.norm(rt); upc = np.cross(rt, f)
fov = np.tan(np.radians(15.5))
ys, xs = np.mgrid[0:H, 0:W]
u = (xs + .5) / W * 2 - 1; v = 1 - (ys + .5) / H * 2
rd = f[None, :] + (u.ravel()[:, None] * rt[None, :] + v.ravel()[:, None] * upc[None, :]) * fov
rd /= np.linalg.norm(rd, axis=1, keepdims=True)
ro = np.broadcast_to(cam, rd.shape).copy()

N = rd.shape[0]
tt = np.full(N, 3.0); hit = np.zeros(N, bool); alive = np.ones(N, bool)
for _ in range(140):
    idx = np.where(alive)[0]
    if idx.size == 0: break
    p = ro[idx] + rd[idx] * tt[idx, None]
    d = sdf(p)
    h = d < 4e-4
    hit[idx[h]] = True
    tt[idx] += d
    alive[idx[h]] = False
    alive[idx[tt[idx] > 10]] = False

col = np.zeros((N, 3)); alpha = hit.astype(float)
hi = np.where(hit)[0]
p = ro[hi] + rd[hi] * tt[hi, None]
n = normal(p)
V = -rd[hi]
# AO
ao = np.ones(len(hi))
for i, s_ in enumerate((0.06, 0.14, 0.25, 0.4)):
    ao -= np.clip(s_ - sdf(p + n * s_), 0, None) * (0.9 / (2 ** i)) / s_ * 0.5
ao = np.clip(ao, 0.25, 1)

base = np.array([0.01, 0.34, 0.09])
L1 = np.array([-0.55, 0.85, 0.55]); L1 /= np.linalg.norm(L1)
L2 = np.array([0.85, 0.25, 0.45]); L2 /= np.linalg.norm(L2)
def env(r):
    ry = r[:, 1]
    sky = np.where((ry > 0)[:, None], 1, 0) * 0
    c = (np.array([0.0, 0.03, 0.01])[None] * (1 - sm(-0.4, 0.5, ry))[:, None]
         + np.array([0.30, 0.95, 0.5])[None] * sm(0.15, 1.0, ry)[:, None] ** 1.5)
    for L, s_, k in ((L1, 1.6, 18), (L2, 0.9, 12)):
        c += (s_ * np.exp(k * (r @ L - 1)))[:, None] * np.array([0.9, 1.0, 0.95])[None]
    # horizon stripes (studio strip lights)
    c += (0.5 * np.exp(-((ry - 0.35) / 0.05) ** 2))[:, None] * np.array([0.6, 1, 0.7])[None]
    return c

ndv = np.clip((n * V).sum(1), 0, 1)
fres = 0.30 + 0.70 * (1 - ndv) ** 3
R = 2 * (n * V).sum(1)[:, None] * n - V
diff = np.clip(n @ L1, 0, 1) * 0.8 + np.clip(n @ L2, 0, 1) * 0.35
H1 = L1 + V; H1 /= np.linalg.norm(H1, axis=1, keepdims=True)
H2 = L2 + V; H2 /= np.linalg.norm(H2, axis=1, keepdims=True)
spec = 1.2 * np.clip((n * H1).sum(1), 0, 1) ** 140 + 0.6 * np.clip((n * H2).sum(1), 0, 1) ** 90
# emblem texture on bezel top
x, y, z = p[:, 0], p[:, 1], p[:, 2]
topface = (n[:, 1] > 0.82) & (y > 1.2)
uu = x / 0.60; vv = z / 0.50; rho = np.hypot(uu, vv)
panel = topface & (rho < 0.86)
dark = np.zeros(len(hi), bool)
dark |= panel & (rho > 0.48) & (rho < 0.70)
dark |= panel & (np.abs(vv) < 0.15) & (np.abs(uu) > 0.45) & (np.abs(uu) < 0.84)
dark |= panel & (np.abs(uu) < 0.26) & (np.abs(vv) > 0.62) & (np.abs(vv) < 0.84)
glowc = panel & (rho < 0.40)
bc = np.tile(base, (len(hi), 1))
bc[panel] = np.array([0.02, 0.30, 0.10])
bc[dark] = np.array([0.0, 0.07, 0.025])
shade = bc * (0.10 + 0.90 * diff)[:, None] * ao[:, None]
color = shade + env(R) * (fres * 1.5)[:, None] * np.array([0.45, 1.0, 0.6])[None] * (0.55 + 0.45 * ao)[:, None] + spec[:, None] * np.array([0.85, 1, 0.9])[None]
# subtle green bounce
color += np.array([0.0, 0.05, 0.015])[None] * (1 - ndv)[:, None]
# emissive centre + halo on panel
cg = 1 - sm(0.0, 0.40, rho)
cen = np.array([1.0, 1.0, 0.82])[None] * cg[:, None] + np.array([0.35, 1.0, 0.45])[None] * (1 - cg)[:, None]
color[glowc] = cen[glowc] * 1.15
halo = panel & ~glowc
color[halo] += (np.array([0.25, 0.9, 0.35])[None] * (np.exp(-((rho - 0.4) / 0.14) ** 2) * 0.7)[:, None])[halo]
# glow spill on bezel flank
spill = np.exp(-np.linalg.norm(p - np.array([0, 1.3, 0]), axis=1) ** 2 / 0.9) * 0.25
color += np.array([0.15, 0.8, 0.3])[None] * spill[:, None]
color = 1 - np.exp(-color * 1.4)
color = color ** (1 / 1.55)
col[hi] = color
img = np.dstack([np.clip(col.reshape(H, W, 3), 0, 1), alpha.reshape(H, W)])
im = Image.fromarray((img * 255).astype(np.uint8), "RGBA")
bbox = im.getchannel("A").getbbox(); print("bbox", bbox)
im.save(OUT)
