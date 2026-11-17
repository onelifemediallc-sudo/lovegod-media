"""Love God. paper-style verse card (adopted Nov 17, 2026).

1080x1350 (4:5). Light paper background like the reference Dustin liked; everything else in our colors:
teal #51B5A9 heading + ornaments, deeper teal #2A7F76 for verse text (readability), yellow #F8E34C highlights.

Every card gets a corner graphic ("motif") from MOTIFS. Use pick() so the graphic is different every time:
it reads ornament-log.csv and returns the least-recently-used motif plus the other corner layout and accent
than last time; never reuses a motif within the last 8 paper cards. After scheduling, log() each card.

    import paper
    m, lay, acc = paper.pick()
    paper.card("PSALM 107:1", ["O give thanks unto the LORD,", "for he is good:", ...], hi=1,
               tag=["Before you list what you need,", "list what He has done."],
               out="media/2026-11-19/p1.png", motif=m, layout=lay, accent=acc)
"""
import os, math, random, csv, zlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, "..", "fonts") + "/"
LOG = os.path.join(HERE, "..", "ornament-log.csv")
T = (0x51, 0xB5, 0xA9); DT = (0x2A, 0x7F, 0x76); Y = (0xF8, 0xE3, 0x4C)
W, H, K = 1080, 1350, 2  # K = supersampling for smooth ornaments

def lora(s):
    f = ImageFont.truetype(FD + "Lora-Variable.ttf", s); f.set_variation_by_axes([600]); return f
def pop(s): return ImageFont.truetype(FD + "Poppins-Medium.ttf", s)

def paper_bg(seed):
    random.seed(seed); im = Image.new("RGB", (W, H), (238, 237, 233)); px = im.load()
    for _ in range(60000):
        x, y = random.randrange(W), random.randrange(H); v = random.randint(205, 250); px[x, y] = (v, v, v - 3)
    return im.filter(ImageFilter.GaussianBlur(0.6))

class Pen:
    def __init__(s): s.im = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.im)
    def line(s, pts, c, w=3): s.d.line([(x * K, y * K) for x, y in pts], fill=c, width=int(w * K), joint="curve")
    def poly(s, pts, c=None, o=None, w=3): s.d.polygon([(x * K, y * K) for x, y in pts], fill=c, outline=o, width=int(w * K))
    def circ(s, x, y, r, c=None, o=None, w=3): s.d.ellipse(((x - r) * K, (y - r) * K, (x + r) * K, (y + r) * K), fill=c, outline=o, width=int(w * K))

def rot(cx, cy, pts, ang):
    a = math.radians(ang); return [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
def almond(L, wf=0.25):
    p = [(L * i / 30, L * wf * math.sin(math.pi * i / 30)) for i in range(31)]; return p + [(x, -y) for x, y in reversed(p)]
def arc(cx, cy, r, a0, a1, n=40): return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

# ---- motifs: draw centered at (x, y), s = scale (1 = about 100px radius); a = main color, b = accent ----
def m_waves(g, x, y, s, a, b):
    for i, c in enumerate([a, a, b]):
        yy = y - 30 * s + i * 30 * s
        g.line([(x - 130 * s + t, yy + 12 * s * math.sin(t / (260 * s) * 4 * math.pi)) for t in range(0, int(260 * s) + 1, 4)], c, 4)
def m_sun(g, x, y, s, a, b):
    r = 46 * s; g.circ(x, y, r, c=b)
    for k in range(14):
        t = 2 * math.pi * k / 14; r1, r2 = r + 14 * s, r + (40 if k % 2 == 0 else 26) * s
        g.line([(x + r1 * math.cos(t), y + r1 * math.sin(t)), (x + r2 * math.cos(t), y + r2 * math.sin(t))], a, 3)
def m_wheat(g, x, y, s, a, b):
    for x0, ang, L in [(x - 15 * s, -100, 200 * s), (x + 15 * s, -80, 190 * s)]:
        y0 = y + 100 * s; t = math.radians(ang); ex, ey = x0 + L * math.cos(t), y0 + L * math.sin(t)
        g.line([(x0, y0), (ex, ey)], a, 3)
        for j in range(5):
            u = 0.5 + j * 0.1; px, py = x0 + L * u * math.cos(t), y0 + L * u * math.sin(t)
            for sd in (-1, 1): g.poly(rot(px, py, almond(32 * s, 0.3), ang + sd * 28), c=b, o=a, w=2)
        g.poly(rot(ex, ey, almond(32 * s, 0.3), ang), c=b, o=a, w=2)
        g.line([(ex, ey), (ex + 36 * s * math.cos(t), ey + 36 * s * math.sin(t))], a, 2)
def m_cross(g, x, y, s, a, b):
    s *= 0.8; hw, v1, v2, hl, cy = 9 * s, 85 * s, 115 * s, 60 * s, y - 15 * s
    g.poly([(x - hw, cy - v1), (x + hw, cy - v1), (x + hw, cy - hw), (x + hl, cy - hw), (x + hl, cy + hw), (x + hw, cy + hw), (x + hw, cy + v2),
            (x - hw, cy + v2), (x - hw, cy + hw), (x - hl, cy + hw), (x - hl, cy - hw), (x - hw, cy - hw)], c=a)
    for k in range(16):
        t = 2 * math.pi * k / 16 + 0.2; r1, r2 = 95 * s, (125 if k % 2 else 140) * s
        g.line([(x + r1 * math.cos(t), cy + r1 * math.sin(t)), (x + r2 * math.cos(t), cy + r2 * math.sin(t))], b, 3)
def m_branch(g, x, y, s, a, b):
    ang = -65; t = math.radians(ang); L = 210 * s; x0, y0 = x - L / 2 * math.cos(t), y - L / 2 * math.sin(t)
    ex, ey = x0 + L * math.cos(t), y0 + L * math.sin(t); g.line([(x0, y0), (ex, ey)], a, 3)
    for u, sd in [(0.2, 1), (0.35, -1), (0.5, 1), (0.65, -1), (0.8, 1)]:
        px, py = x0 + L * u * math.cos(t), y0 + L * u * math.sin(t); g.poly(rot(px, py, almond(58 * s, 0.24), ang + sd * 45), o=a, w=3)
    g.poly(rot(ex, ey, almond(50 * s, 0.24), ang), o=a, w=3)
    for u in (0.3, 0.6): px, py = x0 + L * u * math.cos(t) + 26 * s, y0 + L * u * math.sin(t) + 6 * s; g.circ(px, py, 9 * s, c=b)
def m_moon(g, x, y, s, a, b):
    r = 60 * s; g.circ(x, y, r, c=b); g.circ(x + 30 * s, y - 12 * s, r * 0.82, c=(0, 0, 0, 0))
    for sx, sy, sr in [(95, -55, 16), (110, 40, 10), (55, 85, 8)]: star4(g, x + sx * s, y + sy * s, sr * s, a)
def star4(g, x, y, r, c):
    g.poly([(x, y - r), (x + r * 0.28, y - r * 0.28), (x + r, y), (x + r * 0.28, y + r * 0.28), (x, y + r), (x - r * 0.28, y + r * 0.28), (x - r, y), (x - r * 0.28, y - r * 0.28)], c=c)
def m_sparkles(g, x, y, s, a, b):
    star4(g, x - 20 * s, y - 10 * s, 52 * s, b); star4(g, x + 60 * s, y - 70 * s, 26 * s, a); star4(g, x + 55 * s, y + 55 * s, 18 * s, a)
    g.circ(x - 85 * s, y + 60 * s, 6 * s, c=a); g.circ(x + 95 * s, y - 5 * s, 5 * s, c=b)
def m_mountains(g, x, y, s, a, b):
    g.circ(x + 30 * s, y - 45 * s, 26 * s, c=b)
    g.line([(x - 150 * s, y + 60 * s), (x - 70 * s, y - 30 * s), (x - 20 * s, y + 20 * s), (x + 50 * s, y - 70 * s), (x + 150 * s, y + 60 * s)], a, 4)
    g.line([(x - 150 * s, y + 60 * s), (x + 150 * s, y + 60 * s)], a, 3)
def m_heart(g, x, y, s, a, b):
    pts = [(x + 4.2 * s * 16 * math.sin(t) ** 3, y - 4.2 * s * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 1.0)
           for t in [2 * math.pi * i / 120 for i in range(121)]]
    g.line(pts, a, 4); g.poly([(x - 6 * s, y - 40 * s), (x + 6 * s, y - 40 * s), (x + 6 * s, y - 18 * s), (x + 22 * s, y - 18 * s), (x + 22 * s, y - 6 * s), (x + 6 * s, y - 6 * s),
                               (x + 6 * s, y + 30 * s), (x - 6 * s, y + 30 * s), (x - 6 * s, y - 6 * s), (x - 22 * s, y - 6 * s), (x - 22 * s, y - 18 * s), (x - 6 * s, y - 18 * s)], c=b)
def m_flower(g, x, y, s, a, b):
    for k in range(8): g.poly(rot(x, y, almond(70 * s, 0.32), k * 45), o=a, w=3)
    g.circ(x, y, 18 * s, c=b)
def m_anchor(g, x, y, s, a, b):
    g.circ(x, y - 85 * s, 14 * s, o=a, w=4); g.line([(x, y - 71 * s), (x, y + 80 * s)], a, 5); g.line([(x - 45 * s, y - 45 * s), (x + 45 * s, y - 45 * s)], a, 5)
    g.line(arc(x, y + 10 * s, 70 * s, 20, 160), a, 5)
    for sx in (-1, 1): ax, ay = x + sx * 70 * s * math.cos(math.radians(20)), y + 10 * s + 70 * s * math.sin(math.radians(20)); g.poly([(ax, ay - 16 * s), (ax + sx * 12 * s, ay - 2 * s), (ax - sx * 10 * s, ay + 2 * s)], c=a)
    star4(g, x + 80 * s, y - 80 * s, 20 * s, b)
def m_book(g, x, y, s, a, b):
    for sd in (-1, 1):
        g.line([(x, y + 40 * s)] + [(x + sd * 130 * s * i / 20, y + 40 * s - 25 * s * math.sin(math.pi * i / 40)) for i in range(21)] + [(x + sd * 130 * s, y - 60 * s)]
               + [(x + sd * 130 * s * (20 - i) / 20, y - 60 * s - 25 * s * math.sin(math.pi * (20 - i) / 40)) for i in range(21)] + [(x, y - 60 * s)], a, 4)
        for j in range(3): yy = y - 40 * s + j * 22 * s; g.line([(x + sd * 25 * s, yy), (x + sd * 105 * s, yy - 6 * s)], b, 3)
    g.line([(x, y - 60 * s), (x, y + 40 * s)], a, 4)
def m_rainbow(g, x, y, s, a, b):
    for i, c in enumerate([a, b, a]): g.line(arc(x, y + 50 * s, (120 - i * 26) * s, 180, 360), c, 6)
    for cx in (-110, 110): g.circ(x + cx * s, y + 52 * s, 16 * s, o=a, w=3)
def m_candle(g, x, y, s, a, b):
    g.poly([(x - 22 * s, y - 20 * s), (x + 22 * s, y - 20 * s), (x + 22 * s, y + 100 * s), (x - 22 * s, y + 100 * s)], o=a, w=4)
    g.line([(x, y - 20 * s), (x, y - 38 * s)], a, 3); g.poly(rot(x, y - 34 * s, almond(70 * s, 0.3), -90), c=b)
    for k in range(9): t = math.radians(-180 + k * 22.5); g.line([(x + 70 * s * math.cos(t), y - 60 * s + 70 * s * math.sin(t)), (x + 92 * s * math.cos(t), y - 60 * s + 92 * s * math.sin(t))], a, 3)
def m_crown(g, x, y, s, a, b):
    p = [(x - 90 * s, y + 40 * s), (x - 100 * s, y - 50 * s), (x - 50 * s, y - 5 * s), (x, y - 70 * s), (x + 50 * s, y - 5 * s), (x + 100 * s, y - 50 * s), (x + 90 * s, y + 40 * s)]
    g.poly(p, o=a, w=4); g.line([(x - 90 * s, y + 60 * s), (x + 90 * s, y + 60 * s)], a, 4)
    for px, py in [(x - 100 * s, y - 50 * s), (x, y - 70 * s), (x + 100 * s, y - 50 * s)]: g.circ(px, py, 10 * s, c=b)
    g.circ(x, y + 15 * s, 12 * s, c=b)
MOTIFS = {"waves": m_waves, "sun": m_sun, "wheat": m_wheat, "cross": m_cross, "branch": m_branch, "moon": m_moon, "sparkles": m_sparkles,
          "mountains": m_mountains, "heart": m_heart, "flower": m_flower, "anchor": m_anchor, "book": m_book, "rainbow": m_rainbow,
          "candle": m_candle, "crown": m_crown}

def brackets(g, layout):
    m = 50
    if layout == "A":  # top-right + bottom-left
        g.line([(W - m - 300, m), (W - m, m), (W - m, m + 380)], T); g.circ(W - m - 300, m, 8, c=T)
        g.line([(m, H - m - 380), (m, H - m), (m + 300, H - m)], T); g.circ(m + 300, H - m, 8, c=T)
        return (W - 165, 165), (150, H - 140)
    g.line([(m + 300, m), (m, m), (m, m + 380)], T); g.circ(m + 300, m, 8, c=T)
    g.line([(W - m, H - m - 380), (W - m, H - m), (W - m - 300, H - m)], T); g.circ(W - m - 300, H - m, 8, c=T)
    return (165, 165), (W - 150, H - 140)

def card(ref, verse, hi, tag, out, motif, layout="A", accent="yellow", version="KING JAMES VERSION"):
    """ref: heading e.g. 'PSALM 84:11a'. verse: list of lines (KJV, exact). hi: index of the line to highlight (or None).
    tag: 1-2 lines of original encouragement shown on yellow bars. accent: 'yellow' (teal lines, yellow accents) or 'teal' (all-teal motif)."""
    im = paper_bg(zlib.crc32(out.encode())); g = Pen(); big, small = brackets(g, layout)
    a, b = (T, Y) if accent == "yellow" else (DT, T)  # yellow lines are too faint on paper, so the "teal" variant is all-teal
    MOTIFS[motif](g, *big, 0.8, a, b); MOTIFS[motif](g, *small, 0.5, a, b)
    y = 480; g.line([(W / 2 - 300, y), (W / 2 - 40, y)], T); g.line([(W / 2 + 40, y), (W / 2 + 300, y)], T)
    g.poly([(W / 2, y - 16), (W / 2 + 16, y), (W / 2, y + 16), (W / 2 - 16, y)], c=Y)
    for sd in (-1, 1): g.circ(W / 2 + sd * 30, y, 5, c=Y)
    lay = g.im.resize((W, H), Image.LANCZOS); im.paste(lay, (0, 0), lay)
    d = ImageDraw.Draw(im)
    fh = pop(120)
    while d.textlength(ref, font=fh) > 700: fh = pop(fh.size - 4)
    d.text((W / 2, 330), ref, font=fh, fill=T, anchor="mm")
    d.text((W / 2, 420), version, font=pop(28), fill=T, anchor="mm")
    ft = lora(48); tag_h = (len(tag) * 68 + 45) if tag else 0
    vs = 62
    while True:
        fv = lora(vs); lh = int(vs * 1.4)
        if max(d.textlength(l, font=fv) for l in verse) <= 860 and 545 + len(verse) * lh + tag_h <= H - 175: break
        vs -= 2
        if vs < 40: raise ValueError("verse too long for paper card; split or shorten")
    y = 545 + max(0, (H - 175 - 545 - len(verse) * lh - tag_h) // 3)
    for i, l in enumerate(verse):
        if i == hi:
            bw = d.textlength(l, font=fv); d.rectangle((W / 2 - bw / 2 - 14, y - 6, W / 2 + bw / 2 + 14, y + lh - 8), fill=Y)
        d.text((W / 2, y), l, font=fv, fill=DT, anchor="ma"); y += lh
    y += 45
    for l in tag:
        bw = d.textlength(l, font=ft)
        if bw > 900: raise ValueError("tag line too wide: " + l)
        d.rectangle((W / 2 - bw / 2 - 16, y - 4, W / 2 + bw / 2 + 16, y + 64), fill=Y); d.text((W / 2, y), l, font=ft, fill=DT, anchor="ma"); y += 68
    d.text((W / 2, H - 120), "Love God.", font=lora(40), fill=DT, anchor="ma")
    im.save(out)

def history():
    if not os.path.exists(LOG): return []
    with open(LOG) as f: return list(csv.DictReader(f))

def pick(exclude=()):
    """Least-recently-used motif (never one of the last 8), flipping layout and accent from the previous card.
    Pass exclude=[motifs already picked for the same day] when making several cards in one run."""
    h = history(); recent = [r["motif"] for r in h][::-1]
    last_use = {m: (recent.index(m) if m in recent else 10 ** 6) for m in MOTIFS}
    options = [m for m in MOTIFS if m not in exclude and m not in recent[:8]] or [m for m in MOTIFS if m not in exclude]
    m = max(options, key=lambda k: (last_use[k], -list(MOTIFS).index(k)))
    prev = h[-1] if h else {"layout": "B", "accent": "teal"}
    lay = "B" if prev["layout"] == "A" else "A"; acc = "teal" if prev["accent"] == "yellow" else "yellow"
    if exclude: lay, acc = ("A" if len(exclude) % 2 else "B"), ("yellow" if len(exclude) % 2 else "teal")
    return m, lay, acc

def log(date, post_time, ref, motif, layout, accent):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as f:
        w = csv.writer(f)
        if new: w.writerow(["date", "post_time", "reference", "motif", "layout", "accent"])
        w.writerow([date, post_time, ref, motif, layout, accent])
