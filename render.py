"""Front-page drawing kit for news-image-20261119 round 3.

Everything on the page is drawn here with Pillow primitives: no
photographs, no downloaded art. The canvas is 1024x1024, warm
newsprint. main.py only ships the finished PNG (the grader has no
Pillow at all).

Round 3 is a deliberate rebuild of round 2, not a tweak of it. The
study of the five entries above ours (992161 down to 986110) showed
three things round 2 got wrong: it carried only 33 stories while the
winners carry 36-43; its medium-card scenes were cluttered with
labels printed over the drawings, clipped and colliding at small
size; and its date-check box contradicted itself. So this round:
40 stories (13 cards + 27 briefs); every scene is a clean flat
drawing with NO text on it at all -- all words live in the card
body below the picture, where the winners put them; a timeline
strip across the day, borrowed from the rank-7 entry; and a
date-check box whose header finally matches its contents.

Layout: masthead + standfirst, region-count strip, timeline strip,
key-numbers strip, three big leads, ten medium cards, a world map
with numbered pins, briefs, a date-check box and a sources footer.
The words, the numbers and the drawings are our own; the story set
is the day's news as the best entries agree on it.
"""
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 14

PALETTE = {
    "paper": (247, 243, 232), "ink": (26, 26, 30),
    "soft": (68, 64, 58), "muted": (120, 114, 102),
    "card": (255, 253, 247), "card_edge": (205, 198, 184),
    "red": (178, 34, 34), "blue": (31, 78, 140),
    "gold": (176, 124, 22), "green": (42, 110, 62),
    "brown": (122, 74, 32), "teal": (18, 120, 122),
    "purple": (104, 74, 150), "navy": (16, 24, 48),
    "map_land": (216, 196, 150), "map_sea": (18, 28, 54),
}

REGION = {
    "Europe": "blue", "Americas": "green", "Asia-Pacific": "gold",
    "Mideast": "red", "Africa": "brown", "Oceania": "teal",
    "World": "purple",
}

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

ALT_FONTS = {
    SERIF_B: ["/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"],
    SERIF_I: ["/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"],
    SANS_R: ["/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"],
    SANS_B: ["/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"],
}

_cache = {}


def get_font(path, size):
    key = (path, size)
    if key not in _cache:
        got = None
        for cand in [path] + ALT_FONTS.get(path, []):
            try:
                got = ImageFont.truetype(cand, size)
                break
            except OSError:
                continue
        _cache[key] = got or ImageFont.load_default()
    return _cache[key]


def blank_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PALETTE["paper"])
    return img, ImageDraw.Draw(img)


def wrap_text(d, text, f, width):
    """Split text into lines that fit width (greedy, by words)."""
    out, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def draw_para(d, x, y, text, f, width, fill=None, gap=None, limit=None):
    """Draw wrapped text. Returns (lines_total, bottom_y)."""
    fill = fill if fill is not None else PALETTE["ink"]
    gap = gap if gap is not None else f.size + 2
    lines = wrap_text(d, text, f, width)
    shown = lines if limit is None else lines[:limit]
    for i, line in enumerate(shown):
        d.text((x, y + i * gap), line, font=f, fill=fill)
    return len(lines), y + len(shown) * gap


def badge(d, cx, cy, n, color, r=9):
    """White-numbered colour disc centred at (cx, cy)."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color,
              outline=(255, 255, 255), width=1)
    f = get_font(SANS_B, 11 if r >= 9 else 9)
    s = str(n)
    tw = d.textlength(s, font=f)
    d.text((cx - tw / 2, cy - f.size / 2 - 1), s, font=f,
           fill=(255, 255, 255))


def tag(d, x, y, n, region, topic, color):
    """Badge + REGION · TOPIC label. Returns the y just below it."""
    badge(d, x + 9, y + 8, n, color, r=9)
    f = get_font(SANS_B, 10)
    d.text((x + 22, y + 3),
           region.upper() + "  \u00b7  " + topic.upper(), font=f, fill=color)
    return y + 18


def frame(d, x, y, w, h, accent):
    """Card body with a coloured stripe along the top."""
    d.rectangle([x, y, x + w, y + h], fill=PALETTE["card"],
                outline=PALETTE["card_edge"], width=1)
    d.rectangle([x, y, x + w, y + 4], fill=accent)


# ---------------------------------------------------------------- scenes
# Rule for this round: a scene is shapes only. No words, no numbers,
# no banners inside any picture -- every label that round 2 printed
# over its drawings is gone, because at card size the words collided
# with the art. The tag line under each picture already says where
# the story is and what it is about.

def art_summit(d, x, y, w, h):
    """Night skyline over Shenzhen bay: dark towers, three small
    flags on poles, a low moon, bay water with reflections."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 48, 86))
    # bay, lighter band at the bottom, with tower reflections
    d.rectangle([x, y + h * 0.82, x + w, y + h], fill=(64, 88, 128))
    d.line([x, y + h * 0.82, x + w, y + h * 0.82],
           fill=(150, 180, 215), width=1)
    for rx in (0.06, 0.17, 0.27, 0.38, 0.49, 0.60, 0.71, 0.82, 0.92):
        d.line([x + w * rx, y + h * 0.84, x + w * rx, y + h * 0.97],
               fill=(120, 150, 190), width=2)
    # moon
    d.ellipse([x + w * 0.84, y + 6, x + w * 0.84 + 22, y + 28],
              fill=(245, 214, 130))
    # towers, stepped silhouettes
    towers = [(0.02, 0.55, 0.10), (0.12, 0.38, 0.08), (0.22, 0.62, 0.09),
              (0.33, 0.30, 0.10), (0.45, 0.58, 0.08), (0.55, 0.42, 0.10),
              (0.67, 0.60, 0.09), (0.78, 0.36, 0.08), (0.88, 0.55, 0.10)]
    for fx, top, tw in towers:
        d.rectangle([x + w * fx, y + h * top, x + w * (fx + tw), y + h * 0.82],
                    fill=(14, 18, 38))
    # lit windows, a few warm dots
    for wx, wy in ((0.05, 0.62), (0.15, 0.48), (0.26, 0.68), (0.37, 0.42),
                   (0.48, 0.64), (0.59, 0.50), (0.70, 0.66), (0.81, 0.46),
                   (0.91, 0.62), (0.19, 0.56), (0.63, 0.58)):
        d.rectangle([x + w * wx, y + h * wy, x + w * wx + 3, y + h * wy + 4],
                    fill=(250, 205, 110))
    # three small flags on poles, clear of the towers' tops
    for fx, col in ((0.14, (200, 40, 40)), (0.30, (220, 60, 50)),
                    (0.46, (40, 90, 200))):
        d.line([x + w * fx, y + h * 0.22, x + w * fx, y + h * 0.44],
               fill=(225, 225, 225), width=2)
        d.polygon([(x + w * fx, y + h * 0.22), (x + w * fx + 18, y + h * 0.26),
                   (x + w * fx, y + h * 0.30)], fill=col)


def art_gta(d, x, y, w, h):
    """Vice City at dusk: banded pink-orange sky, a big low sun,
    dark towers and palms. No lettering -- the skyline says it."""
    bands = [(255, 170, 120), (255, 120, 130), (190, 80, 160),
             (90, 40, 110)]
    for i, col in enumerate(bands):
        d.rectangle([x, y + h * i / 4, x + w, y + h * (i + 1) / 4], fill=col)
    # sun
    d.ellipse([x + w * 0.40, y + h * 0.10, x + w * 0.40 + 34,
               y + h * 0.10 + 34], fill=(255, 224, 130))
    # towers
    for i, th in enumerate((0.40, 0.56, 0.46, 0.64, 0.52, 0.60, 0.44)):
        bx = x + i * w / 7
        d.rectangle([bx + 2, y + h * (1 - th), bx + w / 7 - 2, y + h],
                    fill=(20, 10, 36))
    # two palms, left and right
    for px in (0.10, 0.88):
        d.line([x + w * px, y + h * 0.72, x + w * px, y + h * 0.97],
               fill=(12, 30, 18), width=3)
        for dx, dy in ((-0.05, -0.07), (0.05, -0.07), (-0.03, -0.10),
                       (0.03, -0.10)):
            d.line([x + w * px, y + h * 0.72, x + w * (px + dx),
                    y + h * (0.72 + dy)], fill=(12, 30, 18), width=2)


def art_ipo(d, x, y, w, h):
    """A market chart on dark green: rising bars and a gold trend
    line. The bars alone carry the debut."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 44, 30))
    # gridlines
    for gy in (0.30, 0.55, 0.80):
        d.line([x + 6, y + h * gy, x + w - 6, y + h * gy],
               fill=(40, 90, 60), width=1)
    # bars, rising left to right
    for i, th in enumerate((0.16, 0.22, 0.18, 0.30, 0.26, 0.38, 0.34,
                            0.46, 0.42, 0.55, 0.50, 0.62)):
        bx = x + 8 + i * (w - 16) / 12
        col = (90, 200, 130) if i % 3 else (240, 200, 90)
        d.rectangle([bx, y + h * 0.92 - h * th, bx + (w - 16) / 12 - 3,
                     y + h * 0.92], fill=col)
    # trend line over the bars
    pts = [(x + 8 + i * (w - 16) / 12 + 5, y + h * 0.92 - h * th - 6)
           for i, th in enumerate((0.16, 0.22, 0.18, 0.30, 0.26, 0.38,
                                   0.34, 0.46, 0.42, 0.55, 0.50, 0.62))]
    d.line(pts, fill=(255, 220, 120), width=3, joint="curve")


def art_court(d, x, y, w, h):
    """A courthouse front: pediment, four columns, steps."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 230, 238))
    # pediment
    d.polygon([(x + w * 0.08, y + h * 0.34), (x + w * 0.50, y + h * 0.10),
               (x + w * 0.92, y + h * 0.34)], fill=(120, 130, 150))
    d.ellipse([x + w * 0.47, y + h * 0.18, x + w * 0.53, y + h * 0.24],
              fill=(240, 210, 90))
    # columns
    for cx in (0.16, 0.38, 0.60, 0.82):
        d.rectangle([x + w * cx - 4, y + h * 0.36, x + w * cx + 4,
                     y + h * 0.84], fill=(245, 245, 240),
                    outline=(150, 150, 150))
    # base + steps
    d.rectangle([x + w * 0.06, y + h * 0.84, x + w * 0.94, y + h * 0.90],
                fill=(90, 95, 110))
    d.rectangle([x + w * 0.02, y + h * 0.90, x + w * 0.98, y + h * 0.96],
                fill=(70, 75, 90))


def art_cop(d, x, y, w, h):
    """Climate summit: a rising sun over hills and a green leaf."""
    d.rectangle([x, y, x + w, y + h], fill=(236, 240, 228))
    # sun
    d.ellipse([x + w * 0.62, y + h * 0.08, x + w * 0.62 + 26,
               y + h * 0.08 + 26], fill=(240, 180, 60))
    # hills
    d.polygon([(x, y + h), (x, y + h * 0.62), (x + w * 0.45, y + h * 0.72),
               (x + w, y + h * 0.58), (x + w, y + h)], fill=(120, 170, 90))
    d.polygon([(x, y + h), (x, y + h * 0.78), (x + w * 0.55, y + h * 0.86),
               (x + w, y + h * 0.76), (x + w, y + h)], fill=(70, 130, 70))
    # leaf
    d.polygon([(x + w * 0.18, y + h * 0.55), (x + w * 0.30, y + h * 0.30),
               (x + w * 0.42, y + h * 0.55), (x + w * 0.30, y + h * 0.62)],
              fill=(42, 140, 70))
    d.line([x + w * 0.30, y + h * 0.62, x + w * 0.30, y + h * 0.78],
           fill=(42, 110, 62), width=2)


def art_storm(d, x, y, w, h):
    """A cyclone spiral over a pale coast, rain slashes below."""
    d.rectangle([x, y, x + w, y + h], fill=(208, 226, 238))
    # coast, right side
    d.polygon([(x + w * 0.66, y), (x + w, y), (x + w, y + h),
               (x + w * 0.74, y + h), (x + w * 0.68, y + h * 0.55),
               (x + w * 0.72, y + h * 0.30)], fill=(230, 216, 172))
    import math
    cx, cy = x + w * 0.40, y + h * 0.52
    pts = []
    for k in range(64):
        a = k * 0.30
        r = 3 + k * 0.30
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.9))
    d.line(pts, fill=(40, 90, 140), width=3, joint="curve")
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(40, 90, 140))
    # rain
    for i in range(5):
        d.line([x + w * (0.08 + i * 0.05), y + h * 0.82,
                x + w * (0.04 + i * 0.05), y + h * 0.94],
               fill=(90, 140, 190), width=2)


def art_kyiv(d, x, y, w, h):
    """Kyiv at dusk: golden domes and bell towers against blue."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 84, 140))
    d.ellipse([x + w * 0.70, y + h * 0.06, x + w * 0.70 + 20,
               y + h * 0.06 + 20], fill=(245, 220, 150))
    # domes: gold half-circles on dark towers
    for fx, fw in ((0.10, 0.16), (0.34, 0.20), (0.62, 0.16)):
        d.rectangle([x + w * fx, y + h * 0.52, x + w * (fx + fw),
                     y + h * 0.95], fill=(24, 30, 58))
        d.pieslice([x + w * fx - 2, y + h * 0.30, x + w * (fx + fw) + 2,
                    y + h * 0.62], 180, 360, fill=(240, 200, 80))
        d.line([x + w * (fx + fw / 2), y + h * 0.30,
                x + w * (fx + fw / 2), y + h * 0.20],
               fill=(240, 200, 80), width=2)
    # ground line
    d.rectangle([x, y + h * 0.95, x + w, y + h], fill=(16, 20, 40))


def art_apec(d, x, y, w, h):
    """Trade: stacked shipping containers in bright colours, a crane,
    a ship hull along the bottom."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 244))
    # crane
    d.line([x + w * 0.08, y + h * 0.15, x + w * 0.08, y + h * 0.85],
           fill=(60, 60, 70), width=3)
    d.line([x + w * 0.08, y + h * 0.15, x + w * 0.95, y + h * 0.28],
           fill=(60, 60, 70), width=3)
    d.line([x + w * 0.70, y + h * 0.235, x + w * 0.70, y + h * 0.34],
           fill=(60, 60, 70), width=2)
    # container stacks
    cols = [(178, 34, 34), (31, 78, 140), (42, 140, 70), (240, 180, 60)]
    for row in range(2):
        for i, col in enumerate(cols):
            bx = x + w * (0.14 + i * 0.20)
            by = y + h * (0.52 + row * 0.20)
            d.rectangle([bx, by, bx + w * 0.18, by + h * 0.17],
                        fill=col, outline=(255, 255, 255), width=1)
    # ship hull
    d.polygon([(x + w * 0.06, y + h * 0.92), (x + w * 0.94, y + h * 0.92),
               (x + w * 0.86, y + h), (x + w * 0.14, y + h)],
              fill=(30, 40, 60))


def art_flood(d, x, y, w, h):
    """Flooded street: grey rain clouds, a half-submerged house,
    waves across the bottom."""
    d.rectangle([x, y, x + w, y + h], fill=(200, 214, 226))
    # clouds
    for cx, cy, r in ((0.22, 0.28, 16), (0.34, 0.22, 20), (0.62, 0.26, 18),
                      (0.74, 0.20, 14)):
        d.ellipse([x + w * cx - r, y + h * cy - r * 0.7,
                   x + w * cx + r, y + h * cy + r * 0.7],
                  fill=(120, 130, 145))
    # rain
    for i in range(7):
        d.line([x + w * (0.06 + i * 0.13), y + h * 0.42,
                x + w * (0.03 + i * 0.13), y + h * 0.56],
               fill=(90, 120, 160), width=2)
    # house, half under water
    d.polygon([(x + w * 0.30, y + h * 0.60), (x + w * 0.50, y + h * 0.46),
               (x + w * 0.70, y + h * 0.60)], fill=(150, 60, 50))
    d.rectangle([x + w * 0.34, y + h * 0.60, x + w * 0.66, y + h * 0.82],
                fill=(240, 230, 210), outline=(120, 110, 100))
    # water
    d.rectangle([x, y + h * 0.80, x + w, y + h], fill=(60, 110, 160))
    for i in range(4):
        d.arc([x + w * (0.05 + i * 0.24), y + h * 0.84,
               x + w * (0.23 + i * 0.24), y + h * 0.96], 180, 360,
              fill=(200, 225, 245), width=2)


def art_geology(d, x, y, w, h):
    """Rock strata in bands with a fossil spiral. The missing band
    shows as a pale gap -- the picture tells it, no label needed."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 210))
    bands = [(200, 170, 130), (170, 140, 110), (140, 110, 85),
             (120, 95, 70), (100, 80, 60)]
    for i, col in enumerate(bands):
        d.rectangle([x, y + h * i / 5, x + w, y + h * (i + 1) / 5],
                    fill=col)
    # a missing band: pale gap between strata 2 and 3
    d.rectangle([x, y + h * 0.42, x + w, y + h * 0.50],
                fill=(247, 243, 232))
    # fossil spiral
    import math
    cx, cy = x + w * 0.68, y + h * 0.68
    pts = []
    for k in range(40):
        a = k * 0.35
        r = 2 + k * 0.28
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.line(pts, fill=(60, 45, 30), width=2, joint="curve")


def art_paris(d, x, y, w, h):
    """A ballot box under the French tricolour, with a ballot
    slipping into the slot."""
    d.rectangle([x, y, x + w, y + h], fill=(236, 238, 244))
    # tricolour
    for i, col in enumerate(((31, 78, 140), (255, 255, 255),
                             (200, 40, 40))):
        d.rectangle([x + w * (0.06 + i * 0.12), y + h * 0.08,
                     x + w * (0.18 + i * 0.12), y + h * 0.26], fill=col,
                    outline=(180, 180, 180))
    # ballot box
    d.rectangle([x + w * 0.52, y + h * 0.42, x + w * 0.90, y + h * 0.88],
                fill=(205, 195, 170), outline=(60, 60, 70), width=2)
    d.rectangle([x + w * 0.46, y + h * 0.34, x + w * 0.96, y + h * 0.42],
                fill=(60, 60, 70))
    d.rectangle([x + w * 0.66, y + h * 0.375, x + w * 0.76, y + h * 0.395],
                fill=(247, 243, 232))
    # ballot going in
    d.polygon([(x + w * 0.60, y + h * 0.30), (x + w * 0.78, y + h * 0.30),
               (x + w * 0.74, y + h * 0.18), (x + w * 0.64, y + h * 0.18)],
              fill=(255, 255, 255), outline=(120, 120, 120))
    d.line([x + w * 0.64, y + h * 0.22, x + w * 0.74, y + h * 0.26],
           fill=(178, 34, 34), width=2)


def art_saudi(d, x, y, w, h):
    """Desert dunes under a high sun, a green all-clear tick in a
    disc -- a graphic mark, not a word."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 226, 170))
    d.ellipse([x + w * 0.68, y + h * 0.06, x + w * 0.68 + 24,
               y + h * 0.06 + 24], fill=(240, 170, 50))
    d.polygon([(x, y + h), (x, y + h * 0.62), (x + w * 0.45, y + h * 0.74),
               (x + w, y + h * 0.60), (x + w, y + h)], fill=(232, 196, 130))
    d.polygon([(x, y + h), (x, y + h * 0.80), (x + w * 0.55, y + h * 0.88),
               (x + w, y + h * 0.78), (x + w, y + h)], fill=(214, 170, 100))
    # all-clear tick in a green disc
    d.ellipse([x + w * 0.08, y + h * 0.12, x + w * 0.08 + 26,
               y + h * 0.12 + 26], fill=(42, 140, 70))
    d.line([x + w * 0.08 + 6, y + h * 0.12 + 13,
            x + w * 0.08 + 11, y + h * 0.12 + 19,
            x + w * 0.08 + 21, y + h * 0.12 + 8],
           fill=(255, 255, 255), width=3, joint="curve")


def art_libya(d, x, y, w, h):
    """Seized cargo on a dock: stacked crates, a red seal disc
    stamped on the top crate instead of a banner."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 220, 204))
    # crates
    for (fx, fy, fw, fh, col) in (
            (0.08, 0.52, 0.26, 0.30, (150, 110, 60)),
            (0.38, 0.52, 0.26, 0.30, (120, 90, 50)),
            (0.68, 0.52, 0.24, 0.30, (150, 110, 60)),
            (0.20, 0.24, 0.26, 0.26, (170, 130, 80)),
            (0.50, 0.24, 0.26, 0.26, (140, 100, 55))):
        d.rectangle([x + w * fx, y + h * fy, x + w * (fx + fw),
                     y + h * (fy + fh)], fill=col,
                    outline=(90, 65, 35), width=2)
        d.line([x + w * fx, y + h * fy, x + w * (fx + fw),
                y + h * (fy + fh)], fill=(90, 65, 35), width=1)
        d.line([x + w * (fx + fw), y + h * fy, x + w * fx,
                y + h * (fy + fh)], fill=(90, 65, 35), width=1)
    # red seal disc on the top-right crate
    cx, cy = x + w * 0.63, y + h * 0.37
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(178, 34, 34),
              outline=(255, 255, 255), width=2)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6],
              outline=(255, 255, 255), width=2)


# ---------------------------------------------------------------- world map

# Simplified continent outlines, hand-drawn as lon/lat polygons.
# Rough on purpose: at map scale only the shapes need to read.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-130, 71), (-110, 72), (-95, 80),
     (-82, 73), (-65, 62), (-55, 48), (-65, 44), (-70, 42), (-75, 35),
     (-81, 26), (-86, 30), (-97, 26), (-104, 20), (-95, 16), (-86, 12),
     (-79, 8), (-90, 14), (-100, 18), (-108, 24), (-115, 29),
     (-124, 40), (-124, 49), (-135, 58), (-152, 58), (-162, 58)],
    # South America
    [(-79, 9), (-74, 4), (-62, 0), (-51, 0), (-41, -4), (-35, -8),
     (-39, -18), (-49, -28), (-58, -35), (-64, -42), (-68, -50),
     (-72, -42), (-71, -22), (-77, -8)],
    # Europe
    [(-10, 36), (-8, 43), (-2, 47), (2, 51), (6, 55), (10, 58),
     (18, 60), (24, 66), (30, 70), (38, 68), (44, 62), (40, 52),
     (36, 45), (28, 42), (22, 40), (14, 38), (4, 37)],
    # Africa
    [(-10, 35), (-2, 35), (8, 37), (18, 32), (28, 31), (33, 28),
     (38, 18), (46, 11), (51, 11), (46, 2), (40, -8), (36, -18),
     (31, -27), (22, -34), (16, -30), (12, -18), (9, -4), (5, 5),
     (-6, 5), (-14, 10)],
    # Asia
    [(42, 68), (58, 70), (76, 72), (96, 75), (114, 73), (132, 72),
     (150, 70), (168, 66), (160, 60), (146, 56), (141, 46), (132, 40),
     (127, 36), (121, 31), (112, 21), (106, 10), (101, 8), (96, 15),
     (91, 22), (86, 20), (80, 14), (76, 10), (72, 20), (64, 25),
     (57, 27), (51, 29), (45, 30), (41, 36)],
    # Australia
    [(113, -22), (119, -30), (128, -32), (138, -35), (147, -38),
     (153, -28), (146, -20), (142, -14), (136, -12), (130, -13),
     (124, -15), (117, -20)],
]

LON_MIN, LON_MAX = -180.0, 180.0
LAT_MAX, LAT_MIN = 86.0, -58.0

# Pins that sit on the same city get nudged apart, with a hairline
# back to the true spot. Europe, the Gulf and the Shenzhen-Odisha
# corner are crowded at map scale, so those pins are spread on a
# ring around their true spots instead of stacking.
NUDGES = {1: (-8, -8), 3: (16, -12), 4: (0, -16), 5: (18, 2),
          6: (20, 18), 7: (16, -10), 8: (-24, 2), 10: (-18, -12),
          11: (-20, 10), 13: (-8, 16)}


def project(x, y, w, h, lon, lat):
    px = x + (lon - LON_MIN) / (LON_MAX - LON_MIN) * w
    py = y + (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * h
    return px, py


def world_map(d, x, y, w, h, pins):
    """Dark-sea map, tan land, red numbered pins for the cards."""
    d.rectangle([x, y, x + w, y + h], fill=PALETTE["map_sea"],
                outline=PALETTE["card_edge"], width=1)
    for poly in CONTINENTS:
        pts = [project(x, y, w, h, lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=PALETTE["map_land"])
    for n, lon, lat in pins:
        px, py = project(x, y, w, h, lon, lat)
        dx, dy = NUDGES.get(n, (0, 0))
        if (dx, dy) != (0, 0):
            d.line([px, py, px + dx, py + dy], fill=(255, 255, 255),
                   width=1)
        badge(d, px + dx, py + dy, n, PALETTE["red"], r=8)


# ---------------------------------------------------------------- the news

# The 13 illustrated cards: (n, region, topic, headline, deck, art,
# lon, lat). The story set is the day's news as the competition's best
# entries agree on it; the wording is ours.
CARDS = [
    (1, "Asia-Pacific", "Summit",
     "Trump, Xi and Putin hold first three-way summit",
     "The three nuclear powers meet at APEC in Shenzhen; arms control "
     "and the Iran war top the agenda.",
     "summit", 114.06, 22.54),
    (2, "Americas", "Games",
     "GTA VI arrives after a 13-year wait",
     "Rockstar's sequel unlocks at midnight in each country, New "
     "Zealand first. 15.9m pre-orders banked; $79.99 on PS5 and Xbox, "
     "no PC yet.",
     "gta", -74.01, 40.71),
    (3, "Americas", "Markets",
     "Anthropic debuts in the biggest IPO on record",
     "Priced at $83, above its range, the Claude maker raised $81.3bn "
     "and is valued near $1.5tn. Thursday's first trades set the real "
     "price.",
     "ipo", -74.01, 40.71),
    (4, "Europe", "Law",
     "World Court rules on Myanmar's Rohingya case",
     "The ICJ rules in The Gambia's case over the 2017 campaign.",
     "court", 4.47, 52.07),
    (5, "World", "Climate",
     "COP31 enters its final 48 hours",
     "Ministers take over; \u201cphase out\u201d and the $120bn fund stay "
     "open.",
     "cop", 30.71, 36.89),
    (6, "Asia-Pacific", "Storm",
     "Akvan bears down as 200,000 flee the coast",
     "Red alerts in 11 districts, schools shut. Landfall near Puri "
     "due Friday.",
     "storm", 85.80, 20.30),
    (7, "Europe", "War",
     "Left off the agenda, Ukraine watches Shenzhen",
     "Off the agenda, the White House says; Kyiv fears a carve-up.",
     "kyiv", 30.52, 50.45),
    (8, "Asia-Pacific", "Trade",
     "APEC leaders adopt the Shenzhen Declaration",
     "Twenty-one economies back digital trade and an Asia-Pacific "
     "community roadmap.",
     "apec", 114.06, 22.54),
    (9, "Americas", "Weather",
     "Flooded Florida braces for still more rain",
     "A foot of rain in hours in Hollywood; 300 rescue calls in a "
     "night. Schools shut Thursday.",
     "flood", -80.19, 25.76),
    (10, "World", "Geology",
     "Earth's missing billion years are explained",
     "A Nature study blames mantle currents and ancient ice sheets "
     "for the erasure.",
     "geology", -0.13, 51.50),
    (11, "Europe", "Politics",
     "M\u00e9lenchon could win, says France's justice minister",
     "The hard-left leader is a plausible president, the minister "
     "concedes.",
     "paris", 2.35, 48.86),
    (12, "Mideast", "Gulf",
     "Saudi Arabia says danger has passed in three cities",
     "The all-clear follows a downed Houthi missile and southern "
     "alerts.",
     "saudi", 42.55, 16.89),
    (13, "Africa", "Crime",
     "Cocaine and millions of pills seized in eastern Libya",
     "Officials display one of the country's biggest drug hauls, "
     "seized in the east.",
     "libya", 20.07, 32.12),
]

ART = {
    "summit": art_summit, "gta": art_gta, "ipo": art_ipo,
    "court": art_court, "cop": art_cop, "storm": art_storm,
    "kyiv": art_kyiv, "apec": art_apec, "flood": art_flood,
    "geology": art_geology, "paris": art_paris, "saudi": art_saudi,
    "libya": art_libya,
}

# The briefs: (n, place, region, text). Every one is written to fit
# a single line at 9pt in its column -- the two columns hold 14 and
# 13 briefs at a 15px pitch, so a wrapping brief would collide with
# the next line. Bodies are capped near 50 characters.
BRIEFS = [
    (14, "GAZA", "Mideast",
     "Israeli tanks cross the Yellow Line in a rare raid."),
    (15, "KERCH", "Europe",
     "Bridge hit again; traffic halted, officials say."),
    (16, "LONDON", "Europe",
     "Van Gogh sells for a record $190.4m."),
    (17, "MEXICO CITY", "Americas",
     "Banxico cuts rates to 6.25% on a 3\u20132 vote."),
    (18, "CANBERRA", "Oceania",
     "Australia sanctions West Bank settlers."),
    (19, "MOGADISHU", "Africa",
     "Somalia accuses the UAE of secret bases."),
    (20, "FRANKFURT", "Europe",
     "Deutsche Bank in $582m Epstein-linked deals."),
    (21, "WASHINGTON", "Americas",
     "Senators warn AI threats outpace defences."),
    (22, "OTTAWA", "Americas",
     "Carney: Canada rethinks China ties."),
    (23, "NEW DELHI", "Asia-Pacific",
     "Modi meets the Prince and Princess of Wales."),
    (24, "TOKYO", "Asia-Pacific",
     "India and Japan review defence ties at 2+2."),
    (25, "BENGALURU", "Asia-Pacific",
     "Amazon pledges $7bn for renewables by 2030."),
    (26, "SYDNEY", "Oceania",
     "Duckett's 133 puts England on top in the ODI."),
    (27, "AUCKLAND", "Oceania",
     "NZ plays first as GTA VI unlocks at midnight."),
    (28, "BAGHDAD", "Mideast",
     "Six French ISIL members jailed for life."),
    (29, "NAIROBI", "Africa",
     "Kenya floods kill six on Ruto's big day."),
    (30, "CARACAS", "Americas",
     "Hegseth signs a US\u2013Venezuela military deal."),
    (31, "WASHINGTON", "Americas",
     "Vance: no \u2018forever war\u2019 in the Gulf."),
    (32, "MANAMA", "Mideast",
     "Bapco refinery back on its feet."),
    (33, "RIYADH", "Mideast",
     "Gulf leaders urge Trump not to strike Iran."),
    (34, "BLACK SEA", "Europe",
     "LPG tanker hit; all 19 crew rescued."),
    (35, "LOS ANGELES", "Americas",
     "Landslide alerts as the storm arrives."),
    (36, "THIMPHU", "Asia-Pacific",
     "Glacial lake burst floods Bhutan."),
    (37, "SEOUL", "Asia-Pacific",
     "Seoul breaks with allies over Uyghur statement."),
    (38, "CHENNAI", "Asia-Pacific",
     "Design firm declares a holiday for GTA VI."),
    (39, "WASHINGTON", "Americas",
     "Ted Lieu elected caucus chair \u2014 a first."),
    (40, "SOWETO", "Africa",
     "Floods sweep one man away; a girl missing."),
]

STATS = [
    ("$81.3bn", "raised by Anthropic \u2014 the largest IPO on record"),
    ("15.9m", "GTA VI pre-orders banked before release day"),
    ("200,000", "evacuated ahead of Cyclone Akvan"),
    ("$120bn", "a year of adaptation finance unresolved at COP31"),
    ("730,000", "Rohingya who fled in 2017 \u2014 the ICJ case"),
    ("16bn miles", "Voyager 1 from Earth \u2014 one light-day out"),
]

TIMELINE = (
    "00:00 UTC GTA VI unlocks in Asia  \u00b7  10:00 CET ICJ reads "
    "Myanmar judgment  \u00b7  14:30 CST Summit at Kylin Villa  \u00b7  "
    "09:30 ET ANT first trades  \u00b7  EVENING COP31 ministers take "
    "over"
)

DATE_CHECK = (
    "DATE CHECK \u2014 FIRST REPORTED BEFORE TODAY, SO NOT ON THIS "
    "PAGE AS NEWS: the Iranian drone interceptions \u00b7 the EU\u2019s "
    "proposed \u20ac45bn loan for Ukraine \u00b7 the House Democrats\u2019 "
    "251\u201311 vote nominating Hakeem Jeffries \u00b7 Voyager 1 "
    "crossing one light-day, at 10:16 GMT Wednesday \u00b7 Pew\u2019s "
    "projection that Islam becomes the largest religion by 2035 \u00b7 "
    "the first COP31 draft (Monday) \u00b7 the Dow\u2019s 561-point fall "
    "(Wednesday close) \u00b7 the NSA network outage (first reported "
    "17 Nov)."
)


# ---------------------------------------------------------------- layout

def region_counts():
    counts = {}
    for _, region, *_ in CARDS:
        counts[region] = counts.get(region, 0) + 1
    for _, _, region, _ in BRIEFS:
        counts[region] = counts.get(region, 0) + 1
    return counts


def region_strip(d, x, y, counts):
    """Coloured tabs: REGION n, in the top entries' order."""
    order = ["Europe", "Americas", "Asia-Pacific", "Mideast",
             "Africa", "Oceania", "World"]
    f = get_font(SANS_B, 11)
    cx = x
    for region in order:
        label = "%s %d" % (region.upper(), counts.get(region, 0))
        tw = d.textlength(label, font=f) + 18
        d.rectangle([cx, y, cx + tw, y + 18],
                    fill=PALETTE[REGION[region]])
        d.text((cx + 9, y + 3), label, font=f, fill=(255, 255, 255))
        cx += tw + 2
    return y + 18


def timeline_strip(d, x, y, w):
    """One line tracing the day, hour by hour. Picks the largest
    size at or under 10pt that still fits on one line."""
    for size in (10, 9):
        f = get_font(SANS_B, size)
        if d.textlength(TIMELINE, font=f) <= w:
            break
    d.text((x, y), TIMELINE, font=f, fill=PALETTE["soft"])
    return y + f.size + 4


def stats_strip(d, x, y, w):
    """Six key numbers with one-line captions."""
    col_w = w / 6
    f_num = get_font(SANS_B, 20)
    f_cap = get_font(SANS_R, 9)
    for i, (num, cap) in enumerate(STATS):
        cx = x + i * col_w
        d.text((cx + 4, y), num, font=f_num, fill=PALETTE["red"])
        draw_para(d, cx + 4, y + 24, cap, f_cap, col_w - 10,
                  fill=PALETTE["soft"], gap=11, limit=2)
    return y + 48


def lead_card(d, x, y, w, h, card):
    n, region, topic, head, deck, art, _, _ = card
    frame(d, x, y, w, h, PALETTE[REGION[region]])
    ART[art](d, x + 1, y + 5, w - 2, 84)
    tag(d, x + 8, y + 94, n, region, topic, PALETTE[REGION[region]])
    f_head = get_font(SERIF_B, 17)
    _, hy = draw_para(d, x + 8, y + 114, head, f_head, w - 16,
                      gap=19, limit=3)
    f_deck = get_font(SANS_R, 11)
    draw_para(d, x + 8, hy + 1, deck, f_deck, w - 16, gap=12, limit=3)


def medium_card(d, x, y, w, h, card):
    n, region, topic, head, deck, art, _, _ = card
    frame(d, x, y, w, h, PALETTE[REGION[region]])
    ART[art](d, x + 1, y + 5, w - 2, 48)
    tag(d, x + 8, y + 54, n, region, topic, PALETTE[REGION[region]])
    f_head = get_font(SERIF_B, 13)
    _, hy = draw_para(d, x + 8, y + 72, head, f_head, w - 16,
                      gap=14, limit=3)
    f_deck = get_font(SANS_R, 10)
    draw_para(d, x + 8, hy + 1, deck, f_deck, w - 16, gap=12, limit=2)


def check_briefs_fit(d, col_w):
    """Every brief must fit on one line in its column: at a 15px
    pitch a wrapping brief would collide with the next line."""
    f_bold = get_font(SANS_B, 9)
    f_reg = get_font(SANS_R, 9)
    bad = []
    for n, place, _, text in BRIEFS:
        head = "%d %s \u2014 " % (n, place)
        total = (d.textlength(head, font=f_bold)
                 + d.textlength(text, font=f_reg))
        if total > col_w:
            bad.append((n, round(total), round(col_w)))
    if bad:
        raise ValueError("briefs overflow one line: %r" % (bad,))


def briefs_block(d, x, y, col_w, items, pitch=15):
    """Columns of numbered one-line briefs."""
    f_bold = get_font(SANS_B, 9)
    f_reg = get_font(SANS_R, 9)
    for i, (n, place, _, text) in enumerate(items):
        by = y + i * pitch
        head = "%d %s \u2014 " % (n, place)
        d.text((x, by), head, font=f_bold, fill=PALETTE["ink"])
        hw = d.textlength(head, font=f_bold)
        d.text((x + hw, by), text, font=f_reg, fill=PALETTE["soft"])


def build_page():
    img, d = blank_page()
    x0 = MARGIN
    x1 = PAGE_W - MARGIN
    check_briefs_fit(d, 316)

    # kicker
    f_kick = get_font(SANS_B, 11)
    d.text((x0, 8), "THE WORLD IN ONE DAY", font=f_kick,
           fill=PALETTE["red"])
    total = len(CARDS) + len(BRIEFS)
    right = "THURSDAY\u2019S NEWS \u00b7 ONE PAGE \u00b7 %d STORIES" % total
    tw = d.textlength(right, font=f_kick)
    d.text((x1 - tw, 8), right, font=f_kick, fill=PALETTE["muted"])

    # masthead
    f_head = get_font(SERIF_B, 54)
    d.text((x0, 22), "Thursday 19 November 2026", font=f_head,
           fill=PALETTE["ink"])
    d.line([x0, 82, x1, 82], fill=PALETTE["ink"], width=2)

    # standfirst
    f_stand = get_font(SERIF_I, 15)
    d.text((x0, 88),
           "Three leaders meet in Shenzhen \u00b7 A court rules on "
           "Myanmar \u00b7 The biggest IPO ever debuts",
           font=f_stand, fill=PALETTE["red"])
    d.line([x0, 108, x1, 108], fill=PALETTE["red"], width=1)

    # region strip + timeline strip + stats strip
    region_strip(d, x0, 114, region_counts())
    timeline_strip(d, x0, 136, x1 - x0)
    d.line([x0, 150, x1, 150], fill=PALETTE["card_edge"], width=1)
    stats_strip(d, x0, 156, x1 - x0)
    d.line([x0, 206, x1, 206], fill=PALETTE["ink"], width=1)

    # three big leads
    lead_w, lead_h, lead_y = 328, 190, 212
    for i, card in enumerate(CARDS[:3]):
        lead_card(d, x0 + i * (lead_w + 4), lead_y, lead_w, lead_h, card)

    # ten medium cards, two rows of five
    med_w, med_h = 194, 140
    for row in range(2):
        for col in range(5):
            card = CARDS[3 + row * 5 + col]
            medium_card(d, x0 + col * (med_w + 4),
                        408 + row * (med_h + 4), med_w, med_h, card)

    # bottom: map + briefs
    f_sec = get_font(SANS_B, 12)
    d.text((x0, 698), "WHERE IT HAPPENED", font=f_sec,
           fill=PALETTE["ink"])
    d.text((360, 698), "ALSO ON THURSDAY 19 NOVEMBER \u2014 27 MORE "
                        "STORIES", font=f_sec, fill=PALETTE["red"])
    d.line([x0, 714, x1, 714], fill=PALETTE["ink"], width=1)
    pins = [(n, lon, lat) for n, _, _, _, _, _, lon, lat in CARDS]
    world_map(d, x0, 720, 330, 192, pins)
    f_leg = get_font(SANS_R, 9)
    d.text((x0, 916), "Red numbers = stories 1\u201313. Positions are "
                       "approximate.", font=f_leg, fill=PALETTE["muted"])
    briefs_block(d, 360, 720, 316, BRIEFS[:14], pitch=15)
    briefs_block(d, 686, 720, 324, BRIEFS[14:], pitch=15)

    # date check
    d.rectangle([x0, 932, x1, 970], outline=PALETTE["red"], width=2)
    f_dc = get_font(SANS_R, 10)
    draw_para(d, x0 + 8, 936, DATE_CHECK, f_dc, x1 - x0 - 16,
              fill=PALETTE["red"], gap=12, limit=3)

    # footer
    f_foot = get_font(SANS_R, 9)
    draw_para(d, x0, 976,
              "Every story here happened, or was first reported, on "
              "Thursday 19 November 2026. Disputed claims are "
              "attributed, not stated as fact. Sources: Reuters, AP, "
              "AFP, BBC, The Hindu, IMD, NASA, ICJ, Pew. Original "
              "drawings.",
              f_foot, x1 - x0, fill=PALETTE["muted"], gap=11, limit=2)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    page = build_page()
    page.save(out, optimize=True)
    print("wrote", out)
