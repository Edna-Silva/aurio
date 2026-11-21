import math, random, re, sys, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
W, H, FPS = 1280, 720, 30
FD = r"C:\Windows\Fonts\%s"
F = lambda n, s: ImageFont.truetype(FD % n, s)
SUBF = F("georgia.ttf", 34); BIG = F("georgiab.ttf", 130); MID = F("georgiab.ttf", 46); BUB = F("georgiab.ttf", 40); MONO = F("consola.ttf", 30)
GREEN = (60, 255, 120); DKG = (10, 90, 50); SKIN = (112, 72, 52); SKIN_D = (88, 54, 38); HAIR = (24, 18, 16)
GOLD = (240, 200, 80)
rnd = random.Random(7)

def ease(t): t = max(0, min(1, t)); return t * t * (3 - 2 * t)
def clamp(t): return max(0, min(1, t))

def grad(w, h, top, bot):
    im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im)
    for y in range(h):
        k = y / (h - 1); d.line((0, y, w, y), fill=tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3)))
    return im

def glow_sprite(r, col, strength=1.0):
    s = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0)); px = s.load()
    for y in range(r * 2):
        for x in range(r * 2):
            dd = math.hypot(x - r, y - r) / r
            if dd < 1: px[x, y] = col + (int(255 * strength * (1 - dd) ** 2),)
    return s
GL = {}
def glow(img, cx, cy, r, col=GREEN, s=1.0):
    k = (r, col, s)
    if k not in GL: GL[k] = glow_sprite(r, col, s)
    img.alpha_composite(GL[k], (int(cx - r), int(cy - r)))

# ---------------- character sprites (supersampled) ----------------
def ss(w, h, k=3): return Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0)), k

def hero_bust(age="adult", mouth="smirk", suit=True, shades=False, size=600):
    im, k = ss(size, size); d = ImageDraw.Draw(im); S = size * k
    P = lambda x, y: (x * S, y * S)
    body = (28, 160, 80) if suit else ((200, 120, 40) if age == "kid" else (70, 80, 120))
    bodyd = (14, 100, 55) if suit else ((150, 80, 30) if age == "kid" else (45, 52, 85))
    # shoulders
    bw = 0.40 if age != "kid" else 0.30
    d.polygon([P(0.5 - bw, 1.0), P(0.5 - bw + 0.02, 0.78), P(0.38, 0.68), P(0.62, 0.68), P(0.5 + bw - 0.02, 0.78), P(0.5 + bw, 1.0)], fill=body)
    d.polygon([P(0.5 - bw, 1.0), P(0.5 - bw + 0.02, 0.78), P(0.30, 0.80), P(0.28, 1.0)], fill=bodyd)
    d.rectangle([P(0.43, 0.58), P(0.57, 0.72)], fill=SKIN_D)  # neck
    if suit:
        d.polygon([P(0.40, 0.68), P(0.5, 0.80), P(0.60, 0.68), P(0.56, 0.66), P(0.5, 0.72), P(0.44, 0.66)], fill=(16, 110, 60))
        c = P(0.5, 0.90); r = 0.055 * S
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=(235, 235, 220)); r2 = r * .62
        d.ellipse([c[0] - r2, c[1] - r2, c[0] + r2, c[1] + r2], fill=(20, 200, 90)); r3 = r * .3
        d.ellipse([c[0] - r3, c[1] - r3, c[0] + r3, c[1] + r3], fill=(235, 255, 235))
    # head
    sc = 1.12 if age == "kid" else 1.0
    cx, cy, rx, ry = 0.5, 0.40, 0.17 * sc, 0.21 * sc
    for ex in (-1, 1):  # ears
        e = P(cx + ex * rx, cy + .02); er = 0.035 * S
        d.ellipse([e[0] - er, e[1] - er * 1.3, e[0] + er, e[1] + er * 1.3], fill=SKIN_D)
    d.ellipse([ (cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=SKIN)
    # hair
    if age == "kid":
        d.pieslice([(cx - rx - .01) * S, (cy - ry - .02) * S, (cx + rx + .01) * S, (cy + ry * .1) * S], 180, 360, fill=HAIR)
        for hx in (-.12, -.04, .04, .12):
            q = P(cx + hx, cy - ry - .005); rr = .035 * S
            d.ellipse([q[0] - rr, q[1] - rr, q[0] + rr, q[1] + rr], fill=HAIR)
    else:
        d.pieslice([(cx - rx - .005) * S, (cy - ry - .015) * S, (cx + rx + .005) * S, (cy + ry * .05) * S], 180, 360, fill=HAIR)
        d.rectangle([P(cx - rx + .005, cy - ry * .45), P(cx - rx + .03, cy - .0)], fill=HAIR)
        d.rectangle([P(cx + rx - .03, cy - ry * .45), P(cx + rx - .005, cy - .0)], fill=HAIR)
    # beard
    if age == "adult":
        pts = [P(cx - rx + .005, cy - .01), P(cx - rx + .01, cy + .10), P(cx - .10, cy + ry + .03), P(cx, cy + ry + .06),
               P(cx + .10, cy + ry + .03), P(cx + rx - .01, cy + .10), P(cx + rx - .005, cy - .01),
               P(cx + .12, cy + .06), P(cx + .06, cy + .075), P(cx - .06, cy + .075), P(cx - .12, cy + .06)]
        d.polygon(pts, fill=HAIR)
        d.rectangle([P(cx - .06, cy + .065), P(cx + .06, cy + .075)], fill=HAIR)
    elif age == "teen":
        d.ellipse([(cx - .08) * S, (cy + .09) * S, (cx + .08) * S, (cy + .16) * S], outline=None, fill=(50, 34, 28))
    # eyes
    ey = cy - .03; ew = .034 * sc * S
    for ex in (-.075, .075):
        c = P(cx + ex, ey)
        if shades: continue
        d.ellipse([c[0] - ew, c[1] - ew * .8, c[0] + ew, c[1] + ew * .8], fill=(250, 250, 250))
        pr = ew * .55; look = .006 * S
        d.ellipse([c[0] - pr + look, c[1] - pr, c[0] + pr + look, c[1] + pr], fill=(25, 15, 10))
        d.ellipse([c[0] + look, c[1] - pr * .7, c[0] + pr * .5 + look, c[1] - pr * .1], fill=(255, 255, 255))
        d.line([c[0] - ew * 1.2, c[1] - ew * 1.5 - (.004 * S if ex < 0 else 0), c[0] + ew * 1.2, c[1] - ew * 1.3 - (0 if ex < 0 else .012 * S)], fill=HAIR, width=int(.011 * S))
    if shades:
        for ex in (-.075, .075):
            c = P(cx + ex, ey)
            d.rounded_rectangle([c[0] - .055 * S, c[1] - .035 * S, c[0] + .055 * S, c[1] + .04 * S], radius=int(.015 * S), fill=(10, 10, 14))
            d.line([c[0] - .035 * S, c[1] - .02 * S, c[0] - .01 * S, c[1] - .02 * S], fill=(120, 255, 170), width=int(.006 * S))
        d.line([P(cx - .02, ey), P(cx + .02, ey)], fill=(10, 10, 14), width=int(.01 * S))
    # nose
    d.polygon([P(cx - .015, cy + .015), P(cx + .015, cy + .015), P(cx, cy - .02)], fill=SKIN_D)
    # mouth
    my = cy + .105 if age == "adult" else cy + .09
    if mouth == "smirk":
        d.arc([(cx - .05) * S, (my - .03) * S, (cx + .06) * S, (my + .02) * S], 15, 165, fill=(240, 220, 210), width=int(.010 * S))
        d.line([P(cx + .05, my - .005), P(cx + .068, my - .022)], fill=(240, 220, 210), width=int(.010 * S))
    elif mouth == "open":
        d.ellipse([(cx - .05) * S, (my - .02) * S, (cx + .05) * S, (my + .045) * S], fill=(60, 20, 20))
        d.ellipse([(cx - .03) * S, (my + .015) * S, (cx + .03) * S, (my + .045) * S], fill=(180, 70, 80))
    elif mouth == "smile":
        d.chord([(cx - .06) * S, (my - .04) * S, (cx + .06) * S, (my + .04) * S], 0, 180, fill=(250, 245, 240))
    elif mouth == "flat":
        d.line([P(cx - .04, my), P(cx + .04, my)], fill=(235, 215, 205), width=int(.010 * S))
    return im.resize((size, size), Image.LANCZOS)

def baby_sprite(size=520):
    im, k = ss(size, size); d = ImageDraw.Draw(im); S = size * k; P = lambda x, y: (x * S, y * S)
    d.ellipse([P(.05, .55), P(.95, 1.25)], fill=(245, 245, 250))
    d.ellipse([P(.10, .62), P(.90, 1.2)], fill=(225, 230, 240))
    d.ellipse([P(.22, .10), P(.78, .72)], fill=(128, 84, 62))
    d.pieslice([P(.26, .08), P(.74, .38)], 190, 350, fill=HAIR)
    for ex in (-1, 1):
        c = P(.5 + ex * .12, .40)
        d.arc([c[0] - .05 * S, c[1] - .02 * S, c[0] + .05 * S, c[1] + .05 * S], 200, 340, fill=HAIR, width=int(.015 * S))
        d.ellipse([c[0] - .01 * S + ex * .06 * S, c[1] + .04 * S, c[0] + .015 * S + ex * .06 * S, c[1] + .15 * S], fill=(120, 190, 255))
    d.ellipse([P(.40, .52), P(.60, .66)], fill=(70, 20, 25))
    d.ellipse([P(.44, .60), P(.56, .66)], fill=(190, 80, 90))
    d.ellipse([P(.30, .48), P(.38, .54)], fill=(190, 110, 90)); d.ellipse([P(.62, .48), P(.70, .54)], fill=(190, 110, 90))
    return im.resize((size, size), Image.LANCZOS)

def flyer_sprite(size=900):
    im, k = ss(size, size // 2); d = ImageDraw.Draw(im); S = size * k; P = lambda x, y: (x * S, y * S)
    suit = (28, 160, 80); suitd = (14, 100, 55)
    d.polygon([P(.05, .20), P(.40, .22), P(.40, .30), P(.04, .33)], fill=suitd)   # back leg
    d.polygon([P(.02, .26), P(.40, .26), P(.40, .36), P(.01, .30)], fill=suit)     # front leg
    d.polygon([P(.38, .17), P(.64, .17), P(.66, .33), P(.38, .35)], fill=suit)      # torso
    c = P(.52, .27); r = .04 * S
    d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=(235, 235, 220)); d.ellipse([c[0] - r * .6, c[1] - r * .6, c[0] + r * .6, c[1] + r * .6], fill=(20, 200, 90))
    d.polygon([P(.56, .14), P(.84, .10), P(.97, .13), P(.97, .20), P(.82, .19), P(.56, .24)], fill=suit)  # arm forward
    d.ellipse([P(.94, .10), P(1.0, .22)], fill=(30, 255, 130))
    head = hero_bust("adult", "smirk", True, False, 400).crop((90, 40, 310, 330)).rotate(-55, expand=True, resample=Image.BICUBIC)
    head = head.resize((int(head.width * 3 * .9), int(head.height * 3 * .9)))
    im.alpha_composite(head, (int(.55 * S), int(.06 * S)))
    return im.resize((size, size // 2), Image.LANCZOS)

def back_sprite(size=500):
    im, k = ss(size, int(size * 1.3)); d = ImageDraw.Draw(im); S = size * k; P = lambda x, y: (x * S, y * S)
    suit = (28, 160, 80)
    d.polygon([P(.1, 1.3), P(.14, .62), P(.36, .5), P(.64, .5), P(.86, .62), P(.9, 1.3)], fill=suit)
    d.polygon([P(.1, 1.3), P(.14, .62), P(.26, .66), P(.24, 1.3)], fill=(14, 100, 55))
    d.rectangle([P(.43, .42), P(.57, .56)], fill=SKIN_D)
    d.ellipse([P(.32, .08), P(.68, .50)], fill=HAIR)
    for ex in (-1, 1):
        d.ellipse([P(.5 + ex * .19 - .03, .28), P(.5 + ex * .19 + .03, .38)], fill=SKIN_D)
    return im.resize((size, int(size * 1.3)), Image.LANCZOS)

def child_sprite(size=360):
    return hero_bust("kid", "smile", False, False, size)

def kid_head(age, size=420): return hero_bust(age, "smirk" if age != "kid" else "smile", False, False, size)

SPR = {}
def spr(name, *a):
    key = (name,) + a
    if key not in SPR:
        SPR[key] = {"bust": hero_bust, "baby": baby_sprite, "flyer": flyer_sprite, "back": back_sprite, "child": child_sprite}[name](*a)
    return SPR[key]

# ---------------- backgrounds ----------------
def stars(w, h, n, seed=1):
    r = random.Random(seed); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = r.randrange(w), r.randrange(h); b = r.randrange(120, 255); s = r.choice((1, 1, 1, 2))
        d.ellipse([x, y, x + s, y + s], fill=(b, b, 255, 255))
    return im

def skyline(w, h, base, top, seed, col, win=(255, 220, 120), lit=0.3, wrecked=False):
    r = random.Random(seed); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = -20
    while x < w:
        bw = r.randrange(60, 150); bh = r.randrange(int((base - top) * .3), base - top); y = base - bh
        d.rectangle([x, y, x + bw, base], fill=col)
        if wrecked and r.random() < .4: d.polygon([(x + bw * .4, y), (x + bw * .7, y), (x + bw * .6, y + 40)], fill=(0, 0, 0, 0))
        for wx in range(x + 8, x + bw - 10, 16):
            for wy in range(y + 10, base - 10, 22):
                if r.random() < lit: d.rectangle([wx, wy, wx + 7, wy + 11], fill=win)
        if r.random() < .3: d.rectangle([x + bw // 2 - 2, y - 40, x + bw // 2 + 2, y], fill=col)
        x += bw + r.randrange(0, 14)
    return im

def planet(r, base=(20, 60, 90), atm=GREEN):
    im = Image.new("RGBA", (r * 2 + 80, r * 2 + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = r + 40
    for i in range(30, 0, -1):
        d.ellipse([c - r - i, c - r - i, c + r + i, c + r + i], fill=atm + (int(5 * (30 - i) / 30 * 3),))
    d.ellipse([c - r, c - r, c + r, c + r], fill=base)
    rr = random.Random(4)
    for _ in range(14):
        x, y = rr.randrange(-r, r), rr.randrange(-r, r)
        if math.hypot(x, y) < r * .8: d.ellipse([c + x - 40, c + y - 12, c + x + 40, c + y + 12], fill=(30, 100, 70))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([c - r - 90, c - r - 20, c + r - 90, c + r - 20], fill=(0, 0, 0, 170))
    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).ellipse([c - r, c - r, c + r, c + r], fill=255)
    sh.putalpha(ImageChops.multiply(sh.getchannel("A"), mask)); im.alpha_composite(sh)
    return im

def cam(bg, t, z0=1.0, z1=1.12, dx=0, dy=0):
    z = z0 + (z1 - z0) * t; bw, bh = bg.size; cw, ch = bw / z, bh / z
    x = (bw - cw) / 2 + dx * t; y = (bh - ch) / 2 + dy * t
    return bg.crop((int(x), int(y), int(x + cw), int(y + ch))).resize((W, H), Image.BILINEAR).convert("RGBA")

def sparkles(img, t, n=60, col=GREEN, up=True, seed=3, speed=1.0):
    r = random.Random(seed); d = ImageDraw.Draw(img)
    for i in range(n):
        x0 = r.random() * W; y0 = r.random() * H; sp = (0.3 + r.random()) * 60 * speed; ph = r.random() * 6.28
        y = (y0 - t * sp * (1 if up else -1)) % H; x = x0 + math.sin(t * 1.5 + ph) * 14; s = 1.5 + r.random() * 3.5
        a = int(120 + 100 * math.sin(t * 3 + ph))
        d.ellipse([x - s, y - s, x + s, y + s], fill=col + (max(30, min(255, a)),))

def paste_c(img, sp, cx, cy, scale=1.0, rot=0, alpha=1.0):
    s = sp
    if scale != 1.0: s = s.resize((int(s.width * scale), int(s.height * scale)), Image.BILINEAR)
    if rot: s = s.rotate(rot, expand=True, resample=Image.BILINEAR)
    if alpha < 1:
        a = s.getchannel("A").point(lambda v: int(v * alpha)); s = s.copy(); s.putalpha(a)
    img.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))

def bubble(img, text, x, y, a=1.0, tail=(0, 1)):
    d = ImageDraw.Draw(img); w = d.textlength(text, font=BUB) + 50; h = 80
    lay = Image.new("RGBA", (int(w + 60), 160), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([10, 10, 10 + w, 10 + h], radius=34, fill=(255, 255, 255, 245), outline=(20, 20, 20, 255), width=4)
    ld.polygon([(10 + w * .25, 10 + h - 2), (10 + w * .25 + 40, 10 + h - 2), (10 + w * .25 - 10, 10 + h + 50)], fill=(255, 255, 255, 245), outline=(20, 20, 20, 255))
    ld.line([(10 + w * .25 + 2, 10 + h), (10 + w * .25 + 38, 10 + h)], fill=(255, 255, 255, 255), width=6)
    ld.text((35, 22), text, font=BUB, fill=(15, 15, 15, 255))
    if a < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(lay, (int(x), int(y)))

def text_c(img, txt, font, y, col, a=1.0, stroke=0, sc=(0, 0, 0)):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); w = d.textlength(txt, font=font)
    d.text(((W - w) / 2, y), txt, font=font, fill=col + (int(255 * a),), stroke_width=stroke, stroke_fill=sc + (int(255 * a),)); img.alpha_composite(lay)

def vignette(img, k=0.55):
    global VIG
    if "VIG" not in globals():
        v = Image.new("L", (W, H), 0); d = ImageDraw.Draw(v)
        for i in range(60):
            a = int(255 * k * (1 - i / 60) ** 2); d.rectangle([i * 6, i * 4, W - i * 6, H - i * 4], outline=a, width=7)
        VIG = ImageChops.invert(v.filter(ImageFilter.GaussianBlur(10)))  # dark at edges
        VIG = v.filter(ImageFilter.GaussianBlur(10))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 255)); dark.putalpha(VIG); img.alpha_composite(dark)

# ---------------- scene artwork ----------------
BG = {}
def bg_book():
    im = grad(W, H, (5, 12, 8), (0, 0, 0)).convert("RGBA"); d = ImageDraw.Draw(im)
    # table
    d.rectangle([0, 520, W, H], fill=(25, 18, 14)); return im
def bg_city():
    im = grad(1500, 844, (20, 12, 20), (70, 30, 35)).convert("RGBA")
    im.alpha_composite(stars(1500, 400, 60, 2))
    im.alpha_composite(skyline(1500, 844, 700, 250, 11, (28, 22, 34, 255), lit=.12, wrecked=True))
    im.alpha_composite(skyline(1500, 844, 800, 120, 5, (12, 10, 16, 255), lit=.18, win=(255, 160, 80), wrecked=True))
    d = ImageDraw.Draw(im); d.rectangle([0, 800, 1500, 844], fill=(8, 6, 10)); return im
def bg_room():
    im = grad(W, H, (40, 25, 40), (90, 55, 40)).convert("RGBA"); d = ImageDraw.Draw(im)
    d.rectangle([380, 90, 900, 520], fill=(8, 18, 40), outline=(60, 40, 30), width=18)
    d.line([640, 90, 640, 520], fill=(60, 40, 30), width=12); d.line([380, 300, 900, 300], fill=(60, 40, 30), width=12)
    im.alpha_composite(stars(W, H, 0, 1)); st = stars(520, 420, 40, 9); im.alpha_composite(st, (380, 90))
    d.rectangle([0, 560, W, H], fill=(70, 45, 35)); return im
def bg_space():
    im = Image.new("RGBA", (1500, 844), (3, 6, 14, 255)); im.alpha_composite(stars(1500, 844, 350, 4)); return im
def bg_sunset():
    im = grad(1500, 844, (255, 150, 60), (40, 30, 70)).convert("RGBA")
    im = grad(1500, 844, (40, 30, 80), (255, 170, 70)).convert("RGBA")
    d = ImageDraw.Draw(im); d.ellipse([950, 380, 1190, 620], fill=(255, 220, 130))
    im.alpha_composite(skyline(1500, 844, 700, 300, 21, (60, 30, 60, 255), lit=.0))
    im.alpha_composite(skyline(1500, 844, 844, 330, 8, (25, 16, 36, 255), lit=.08)); return im
def bg_day_city():
    im = grad(1500, 844, (10, 20, 50), (30, 80, 90)).convert("RGBA")
    im.alpha_composite(stars(1500, 500, 80, 6))
    im.alpha_composite(skyline(1500, 844, 740, 260, 31, (14, 36, 54, 255), lit=.25))
    im.alpha_composite(skyline(1500, 844, 844, 200, 32, (7, 16, 28, 255), lit=.3, win=(150, 255, 190))); return im
def bg_party():
    return grad(W, H, (8, 40, 30), (3, 14, 12)).convert("RGBA")
for n, f in (("book", bg_book), ("city", bg_city), ("room", bg_room), ("space", bg_space), ("sunset", bg_sunset), ("daycity", bg_day_city), ("party", bg_party)):
    pass
def getbg(n):
    if n not in BG: BG[n] = globals()["bg_" + {"book": "book", "city": "city", "room": "room", "space": "space", "sunset": "sunset", "daycity": "day_city", "party": "party"}[n]]()
    return BG[n]

def book_img():
    im = Image.new("RGBA", (900, 520), (0, 0, 0, 0)); k = 3
    big = Image.new("RGBA", (900 * k, 520 * k), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    cover = (90, 52, 30); gold = (230, 185, 70)
    d.polygon([(40 * k, 260 * k), (450 * k, 330 * k), (450 * k, 500 * k), (40 * k, 430 * k)], fill=cover)
    d.polygon([(860 * k, 260 * k), (450 * k, 330 * k), (450 * k, 500 * k), (860 * k, 430 * k)], fill=(75, 42, 24))
    d.polygon([(70 * k, 250 * k), (450 * k, 320 * k), (450 * k, 480 * k), (70 * k, 412 * k)], fill=(238, 228, 195))
    d.polygon([(830 * k, 250 * k), (450 * k, 320 * k), (450 * k, 480 * k), (830 * k, 412 * k)], fill=(226, 214, 178))
    for i in range(7):
        y = 280 + i * 20
        d.line([(110 * k, (y - 8) * k), (420 * k, (y + 46) * k)], fill=(150, 130, 100), width=2 * k)
        d.line([(480 * k, (y + 46) * k), (790 * k, (y - 8) * k)], fill=(150, 130, 100), width=2 * k)
    c = (450 * k, 340 * k)
    d.ellipse([c[0] - 60 * k, c[1] - 60 * k, c[0] + 60 * k, c[1] + 60 * k], outline=gold, width=7 * k)
    d.ellipse([c[0] - 30 * k, c[1] - 30 * k, c[0] + 30 * k, c[1] + 30 * k], fill=(20, 200, 90))
    return big.resize((900, 520), Image.LANCZOS)

def scene_book(t, lf):
    im = getbg("book").copy(); a = ease(t / 0.35)
    glow(im, 640, 260, 420, GREEN, .55 * (0.6 + .4 * math.sin(t * 6) * .3 + .4))
    for i in range(7):  # rays
        ang = -90 + (i - 3) * 14 + math.sin(t * 2 + i) * 3
        x2 = 640 + math.cos(math.radians(ang)) * 900; y2 = 400 + math.sin(math.radians(ang)) * 900
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).polygon([(640, 400), (x2 - 30, y2), (x2 + 30, y2)], fill=(80, 255, 140, 26))
        im.alpha_composite(lay)
    bk = book_img(); paste_c(im, bk, 640, 400 + math.sin(t * 3) * 6, 1.1)
    sparkles(im, t * 8, 90)
    text_c(im, "ERA UMA VEZ...", BIG, 90, GOLD, ease((t - .25) / .3), 3, (60, 35, 0))
    return im

def scene_city(t, lf):
    im = cam(getbg("city"), t, 1.0, 1.18, 0, 40)
    d = ImageDraw.Draw(im)
    r = random.Random(5)
    for i in range(110):  # rain
        x = (r.random() * W + t * 40) % W; y = (r.random() * H + t * 900 * (.6 + r.random())) % H
        d.line([x, y, x - 6, y + 24], fill=(170, 190, 220, 90), width=1)
    if (t * 9) % 4 < .12: im.alpha_composite(Image.new("RGBA", (W, H), (200, 210, 255, 70)))
    glow(im, 900, 700, 360, (255, 60, 40), .25)
    # silhouetted people
    for i, x in enumerate((380, 450, 840)):
        d.ellipse([x - 14, 640 - i % 2 * 4, x + 14, 668], fill=(5, 5, 8)); d.polygon([(x - 22, 740), (x - 14, 664), (x + 14, 664), (x + 22, 740)], fill=(5, 5, 8))
    vignette(im, .7); return im

def scene_birth(t, lf):
    im = getbg("room").copy(); d = ImageDraw.Draw(im)
    tw = .7 + .3 * math.sin(t * 8)
    glow(im, 640 + 90, 190, 120, GREEN, tw);
    st = (730, 190); d.polygon([(st[0] + math.cos(math.radians(a * 36 - 90)) * (30 if a % 2 == 0 else 12), st[1] + math.sin(math.radians(a * 36 - 90)) * (30 if a % 2 == 0 else 12)) for a in range(10)], fill=(200, 255, 220))
    glow(im, 300, 300, 450, (255, 190, 90), .28)
    b = spr("baby", 520); paste_c(im, b, 640, 530 + math.sin(t * 5) * 4, 1.0, math.sin(t * 7) * 1.5)
    sparkles(im, t * 6, 30, (255, 220, 140), True, 8, .6)
    text_c(im, "21 DE DEZEMBRO", MID, 40, (190, 255, 160), ease((t - .1) / .2), 2, (0, 60, 20))
    vignette(im, .5); return im

def scene_grow(t, lf):
    im = grad(W, H, (30, 40, 70), (20, 70, 60)).convert("RGBA")
    d = ImageDraw.Draw(im); d.rectangle([0, 600, W, H], fill=(18, 30, 36))
    glow(im, 640, 360, 500, GREEN, .22)
    ages = ["kid", "teen", "adult"]; k = min(2, int(t * 3)); lt = t * 3 - k
    sc = [.85, .95, 1.1][k]
    for j in (k, k - 1):
        if j < 0: continue
        al = ease(lt / .25) if j == k else 1 - ease(lt / .25)
        if j == k and k == 0: al = 1
        paste_c(im, spr("bust", ages[j], "smirk" if j else "smile", False, False, 600), 640, 450 + math.sin(t * 4) * 5, sc, 0, al)
    txt = ["Criança", "Adolescente", "Aurio"][k]
    text_c(im, txt, MID, 40, (200, 255, 210), 1, 2, (0, 40, 20))
    if t > .72: bubble(im, "Calma, calma...", 700, 150, ease((t - .72) / .1))
    sparkles(im, t * 5, 40, (150, 255, 190), True, 12); vignette(im, .4); return im

def scene_ring(t, lf):  # t in [0,1]; three shots
    bg = getbg("space")
    if t < .34:
        u = t / .34; im = cam(bg, u, 1.0, 1.1)
        x = -100 + 1500 * ease(u * 1.05); y = 560 - 300 * math.sin(u * 3.0) * 1.0
        for i in range(30):
            q = i / 30; tx = x - q * 360; ty = 560 - 300 * math.sin(max(0, u - q * .15) * 3.0)
            glow(im, tx, ty, int(34 * (1 - q) + 4), GREEN, .5 * (1 - q))
        glow(im, x, y, 90, GREEN, .9)
        d = ImageDraw.Draw(im); d.ellipse([x - 26, y - 20, x + 26, y + 20], outline=(130, 255, 170), width=9); d.ellipse([x - 12, y - 8, x + 12, y + 8], outline=(255, 255, 255), width=3)
        pl = planet(130); paste_c(im, pl, 1030 - u * 60, 220); vignette(im, .5); return im
    if t < .62:
        u = (t - .34) / .28; im = cam(bg, u, 1.0, 1.08)
        pl = planet(220); paste_c(im, pl, 980, 460); paste_c(im, spr("bust", "adult", "smirk", False, False, 600), 480, 470, 1.0, 0, 1 - ease((u - .45) / .2))
        if u > .5: im.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(255 * clamp(1 - abs(u - .55) * 6)))))
        paste_c(im, spr("bust", "adult", "smirk", True, False, 600), 480, 470, 1.0, 0, ease((u - .45) / .2))
        glow(im, 560, 560, 140, GREEN, .5 * ease((u - .45) / .2)); sparkles(im, t * 10, 50)
        return im
    u = (t - .62) / .38
    return scene_report(u, lf, short=True)


def hologram(im, lines, t, title="GUARDIÕES DO UNIVERSO", reveal=None):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); x0, y0, x1, y1 = 160, 90, 1120, 600
    d.rounded_rectangle([x0, y0, x1, y1], radius=22, fill=(10, 60, 40, 140), outline=(80, 255, 150, 230), width=3)
    for y in range(y0 + 6, y1, 8): d.line([x0 + 6, y, x1 - 6, y], fill=(80, 255, 150, 18))
    d.text((x0 + 36, y0 + 24), title, font=MID, fill=(150, 255, 190, 255))
    d.line([x0 + 36, y0 + 84, x1 - 36, y0 + 84], fill=(80, 255, 150, 200), width=2)
    # silhouette
    d.ellipse([x1 - 190, y0 + 110, x1 - 90, y0 + 210], outline=(80, 255, 150, 190), width=3)
    d.polygon([(x1 - 230, y0 + 440), (x1 - 210, y0 + 240), (x1 - 70, y0 + 240), (x1 - 50, y0 + 440)], outline=(80, 255, 150, 190), width=3)
    n = len(lines); shown = reveal if reveal is not None else n
    for i, (a, b, v) in enumerate(lines):
        if i >= shown: break
        y = y0 + 110 + i * 56
        d.text((x0 + 36, y), a + ":", font=MONO, fill=(180, 255, 205, 255)); d.text((x0 + 36 + 420, y), b, font=MONO, fill=(255, 235, 140, 255))
        d.rectangle([x0 + 36, y + 38, x0 + 36 + 560, y + 44], outline=(80, 255, 150, 120))
        w = 560 * v * ease(clamp(t * n - i + 1)); d.rectangle([x0 + 36, y + 38, x0 + 36 + w, y + 44], fill=(80, 255, 150, 230))
    return lay

REPORT = [("Poder", "Extraordinário", 1.0), ("Coragem", "Inquestionável", .98), ("Lealdade", "Absoluta", 1.0), ("Aconselhar", "Elevada", .85), ("Sentido de humor", "Questionável", .4), ("Diplomacia", "Em formação", .25), ("Capacidade de roast", "Ameaça galáctica", 1.0)]
def scene_report(t, lf, short=False):
    bg = getbg("space"); im = cam(bg, t, 1.0, 1.08)
    pl = planet(200); paste_c(im, pl, 220, 640)
    glow(im, 640, 340, 520, GREEN, .22)
    if short:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); x0, y0, x1, y1 = 200, 130, 1080, 560
        d.rounded_rectangle([x0, y0, x1, y1], radius=22, fill=(10, 60, 40, 150), outline=(80, 255, 150, 230), width=3)
        d.text((x0 + 36, y0 + 24), "GUARDIÕES DO UNIVERSO", font=MID, fill=(150, 255, 190, 255))
        txt = ["Após uma avaliação rigorosa,", "confirmamos que o candidato possui", "todas as qualidades necessárias...", "embora recomendemos formação adicional", "em contenção verbal."]
        k = int(clamp(t / .8) * len(txt) + .999)
        for i, s in enumerate(txt[:k]): d.text((x0 + 36, y0 + 110 + i * 56), s, font=F("georgia.ttf", 38), fill=(210, 255, 225, 255) if i < 4 else (255, 230, 120, 255))
        im.alpha_composite(lay)
    else:
        reveal = int(clamp(t / .85) * len(REPORT) + .999)
        im.alpha_composite(hologram(im, REPORT, t, reveal=reveal))
        if t > .88:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); a = int(255 * ease((t - .88) / .1))
            d.rounded_rectangle([320, 616, 960, 676], radius=14, fill=(20, 120, 60, a)); w = d.textlength("CANDIDATO APROVADO", font=MID); d.text(((W - w) / 2, 622), "CANDIDATO APROVADO", font=MID, fill=(255, 255, 255, a)); im.alpha_composite(lay)
    sparkles(im, t * 8, 40); vignette(im, .5); return im

def shield(im, cx, cy, r, t):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 255, 140, 45), outline=(150, 255, 190, 220), width=5)
    for i in range(6):
        a = math.radians(i * 60 + t * 40); d.line([cx + math.cos(a) * r * .3, cy + math.sin(a) * r * .3, cx + math.cos(a) * r, cy + math.sin(a) * r], fill=(150, 255, 190, 60), width=2)
    im.alpha_composite(lay)

def scene_action(t, lf):
    im = cam(getbg("daycity"), t, 1.0, 1.14, 0, 20)
    # people on the street
    d = ImageDraw.Draw(im)
    for x in (250, 310, 380, 450):
        ch = spr("child", 200); paste_c(im, ch, x, 700, .55 + (x % 3) * .03, 0, 1)
    # explosion flash early
    if t < .35:
        u = t / .35; glow(im, 1000, 560, int(180 + 220 * u), (255, 140, 40), .8 * (1 - u))
    if .35 <= t: shield(im, 350, 640, 190 + 8 * math.sin(t * 12), t)
    fx = -250 + 1700 * ease(t * 1.1 - .05); fy = 300 - 140 * math.sin(t * math.pi) + math.sin(t * 9) * 8
    for i in range(14):
        glow(im, fx - 150 - i * 40, fy + 20 + math.sin(t * 9 - i * .4) * 6, 40 - i * 2, GREEN, .35)
    paste_c(im, spr("flyer", 900), fx, fy, .85, -4)
    glow(im, fx + 340, fy - 6, 70, GREEN, .8)
    if .5 < t < .85: bubble(im, "Calma, calma...", 160, 120, ease((t - .5) / .06) * (1 - ease((t - .8) / .05)))
    sparkles(im, t * 6, 30); vignette(im, .4); return im

def scene_heart(t, lf):
    im = cam(getbg("sunset"), t, 1.0, 1.1, 0, 10)
    glow(im, 640, 300, 360, (255, 190, 120), .35)
    paste_c(im, spr("bust", "adult", "smile", True, False, 720), 520, 470 + math.sin(t * 3) * 4, .95)
    paste_c(im, spr("child", 420), 830, 590 + math.sin(t * 3 + 1) * 3, .85)
    # hand on shoulder
    d = ImageDraw.Draw(im); d.ellipse([760, 505, 830, 540], fill=(112, 72, 52)); d.polygon([(690, 560), (780, 520), (800, 545), (700, 600)], fill=(28, 160, 80))
    hs = 1 + .12 * math.sin(t * 7); h = 90 * hs; cx, cy = 650, 120
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.ellipse([cx - h, cy - h * .6, cx, cy + h * .4], fill=(60, 255, 140, 255)); ld.ellipse([cx, cy - h * .6, cx + h, cy + h * .4], fill=(60, 255, 140, 255))
    ld.polygon([(cx - h * .96, cy + h * .08), (cx + h * .96, cy + h * .08), (cx, cy + h * 1.1)], fill=(60, 255, 140, 255)); lay = lay.filter(ImageFilter.GaussianBlur(1)); glow(im, cx, cy + 20, 190, GREEN, .5); im.alpha_composite(lay)
    sparkles(im, t * 6, 40, (255, 230, 160), True, 14, .6); vignette(im, .45); return im

def scene_reveal(t, lf):
    bg = getbg("space"); im = cam(bg, t, 1.0, 1.1)
    pl = planet(260); paste_c(im, pl, 980, 330)
    d = ImageDraw.Draw(im); d.polygon([(380, 720), (470, 560), (700, 540), (800, 720)], fill=(30, 28, 34))
    glow(im, 600, 380, 300, GREEN, .35 + .1 * math.sin(t * 6))
    paste_c(im, spr("back", 500), 600, 455, 1.0)
    # cape-less glow ring on hand
    sparkles(im, t * 6, 70)
    a = ease((t - .7) / .15)
    if a > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, int(150 * a))); im.alpha_composite(lay)
        glow(im, 640, 300, 500, GREEN, .35 * a)
        text_c(im, "AURIO", BIG, 200, GOLD, a, 4, (20, 100, 40)); text_c(im, "21 DE DEZEMBRO — O NASCIMENTO DE UMA LENDA", F("georgiab.ttf", 34), 380, (170, 255, 150), ease((t - .82) / .12))
    vignette(im, .5); return im

CONF = [(random.Random(i).random() * W, random.Random(i + 99).random(), random.choice([(60, 255, 130), (255, 220, 90), (255, 255, 255), (120, 200, 255)]), random.Random(i + 5).random() * 6.28) for i in range(120)]
def scene_party(t, lf):
    im = getbg("party").copy(); glow(im, 640, 400, 560, GREEN, .25)
    d = ImageDraw.Draw(im)
    # balloons
    for i, (x, c) in enumerate(((120, (255, 220, 90)), (230, (60, 255, 130)), (1050, (255, 220, 90)), (1160, (60, 255, 130)))):
        by = 220 + math.sin(t * 2 + i) * 14; d.ellipse([x - 46, by - 60, x + 46, by + 60], fill=c); d.line([x, by + 60, x + 6, by + 260], fill=(200, 200, 200), width=2)
    # cake
    d.rectangle([860, 560, 1060, 660], fill=(235, 220, 200)); d.rectangle([860, 560, 1060, 590], fill=(60, 220, 120)); d.rectangle([955, 520, 965, 560], fill=(255, 240, 200))
    fl = 1 + .2 * math.sin(t * 20); glow(im, 960, 506, 50, (255, 180, 60), .9); d.ellipse([952, 490, 968, 520 * 1], fill=(255, 200, 80))
    # hero waving with mug
    paste_c(im, spr("bust", "adult", "smile", True, False, 760), 480, 450 + math.sin(t * 4) * 4, 1.0)
    arm = 15 * math.sin(t * 9)
    ar = Image.new("RGBA", (200, 260), (0, 0, 0, 0)); ad = ImageDraw.Draw(ar); ad.polygon([(60, 260), (80, 40), (130, 40), (150, 260)], fill=(28, 160, 80)); ad.ellipse([60, 0, 150, 70], fill=SKIN)
    paste_c(im, ar.rotate(arm, expand=True, resample=Image.BILINEAR), 780, 520, 1.0)
    for x, ph, c, p2 in CONF:
        y = (ph * H + t * (120 + ph * 160)) % H; xx = x + math.sin(t * 2 + p2) * 20; d.rectangle([xx, y, xx + 8, y + 12], fill=c)
    sparkles(im, t * 8, 50, (255, 230, 150))
    for k, (cx, cy, hue) in enumerate(((220, 140, GREEN), (1010, 120, (255, 220, 90)))):
        u = (t * .8 + k * .45) % 1;
        for i in range(18):
            a = i / 18 * 6.28; rr = 20 + 150 * ease(u); d.ellipse([cx + math.cos(a) * rr - 4, cy + math.sin(a) * rr - 4 + 40 * u * u, cx + math.cos(a) * rr + 4, cy + math.sin(a) * rr + 4 + 40 * u * u], fill=hue + (int(255 * (1 - u)),))
    if t > .6: text_c(im, "FELIZ ANIVERSÁRIO, AURIO!", F("georgiab.ttf", 64), 36, GOLD, ease((t - .6) / .1), 3, (20, 100, 40))
    if t > .85: text_c(im, "QUE A VONTADE ESTEJA CONTIGO. SEMPRE.", F("georgiab.ttf", 34), 640, (200, 255, 200), ease((t - .85) / .1), 2, (0, 40, 20))
    vignette(im, .35); return im

SCENES = [scene_book, scene_city, scene_birth, scene_grow, scene_ring, scene_action, scene_heart, scene_report, scene_reveal, scene_party]
TEXT = [l for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "narr_text.txt"), encoding="utf8").read().split("\n---\n")]

def wrap(d, txt, font, maxw):
    cur, out = "", []
    for w in txt.split():
        c = (cur + " " + w).strip()
        if d.textlength(c, font=font) > maxw and cur: out.append(cur); cur = w
        else: cur = c
    return out + [cur]

def chunks(text):
    sents = [s.strip() for s in re.findall(r"[^.!?…]+[.!?…]*\s*", text.replace("......", "...")) if s.strip()]
    out = []
    for s in sents:
        if out and len(out[-1]) < 28: out[-1] += " " + s
        else: out.append(s)
    return out

def render(auddir, out, only=None, frames=None):
    durs = [float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{auddir}/s{i}.mp3"])) + 1.0 for i in range(1, 11)]
    ff = None
    if not frames:
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "fast", out], stdin=subprocess.PIPE)
    tmp = Image.new("RGBA", (W, H))
    for si, fn in enumerate(SCENES):
        if only is not None and si not in only: continue
        n = int(durs[si] * FPS); ch = chunks(TEXT[si]); tot = sum(len(c) for c in ch); acc = 0; ends = []
        for c in ch: acc += len(c); ends.append(acc / tot)
        for i in range(n):
            if frames and i not in [int(n * f) for f in frames]: continue
            t = i / n; im = fn(t, i / FPS).convert("RGBA")
            k = next((j for j, e in enumerate(ends) if t * (durs[si] - 1) / durs[si] <= e * (durs[si] - 1) / durs[si]), len(ch) - 1)
            d = ImageDraw.Draw(im, "RGBA"); ls = wrap(d, ch[k], SUBF, W - 200); h = len(ls) * 44 + 24
            if t < (durs[si] - 1) / durs[si]:
                for j, l in enumerate(ls):
                    w = d.textlength(l, font=SUBF); d.text(((W - w) / 2, H - h - 12 + j * 44), l, font=SUBF, fill=(245, 255, 245, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
            fade = min(1, i / 12, (n - i) / 12)
            fr = im.convert("RGB")
            if fade < 1: fr = Image.blend(Image.new("RGB", (W, H)), fr, fade)
            if frames: fr.save(f"preview_s{si+1}_{i}.png")
            else: ff.stdin.write(fr.tobytes())
    if ff: ff.stdin.close(); ff.wait()

if __name__ == "__main__":
    aud, out = sys.argv[1], sys.argv[2]
    if out == "preview": render(aud, None, frames=[.45, .85])
    elif len(sys.argv) > 3: render(aud, out, only=[int(sys.argv[3])])
    else: render(aud, out)
