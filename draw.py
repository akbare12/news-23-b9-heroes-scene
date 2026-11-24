#!/usr/bin/env python3
"""Draw the news-image-20261123 heroes-scene front page (1024x1024).

THE WORLD TODAY — Monday 23 November 2026. 31 stories, 6 regions.
Three big hero scenes on top, 10 small cards, world map + 31 numbered pins,
ALSO list, DATE CHECK box. Scenes are drawn illustrations, not photographs.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (169, 28, 28)
RED_D = (140, 20, 20)
NAVY = (20, 33, 61)
NAVY_L = (27, 42, 74)
GOLD = (212, 160, 23)
GREEN = (30, 125, 50)
AMBER = (180, 83, 9)
BLUE = (29, 78, 216)
GREY = (85, 85, 85)
LINE = (200, 190, 170)

REGIONS = [
    ("NORTH AMERICA", 8, (31, 78, 121)),
    ("EUROPE", 6, (197, 90, 17)),
    ("MIDDLE EAST", 6, (112, 48, 160)),
    ("ASIA-PACIFIC", 6, (46, 125, 50)),
    ("AFRICA", 3, (140, 109, 31)),
    ("WORLD", 2, (85, 85, 85)),
]
REGION_OF = {
    1: "ASIA-PACIFIC", 2: "WORLD", 3: "WORLD", 4: "NORTH AMERICA",
    5: "NORTH AMERICA", 6: "EUROPE", 7: "EUROPE", 8: "EUROPE",
    9: "EUROPE", 10: "EUROPE", 11: "EUROPE", 12: "AFRICA",
    13: "MIDDLE EAST", 14: "MIDDLE EAST", 15: "MIDDLE EAST",
    16: "MIDDLE EAST", 17: "MIDDLE EAST", 18: "MIDDLE EAST",
    19: "AFRICA", 20: "AFRICA", 21: "ASIA-PACIFIC", 22: "ASIA-PACIFIC",
    23: "ASIA-PACIFIC", 24: "ASIA-PACIFIC", 25: "ASIA-PACIFIC",
    26: "NORTH AMERICA", 27: "NORTH AMERICA", 28: "NORTH AMERICA",
    29: "NORTH AMERICA", 30: "NORTH AMERICA", 31: "NORTH AMERICA",
}
REGION_COLOR = {name: col for name, _, col in REGIONS}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = fnt.size + 2
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_lines(d, text, path, size, max_w, max_lines, min_size=7):
    """Shrink font until text fits max_lines at max_w; return (lines, font)."""
    s = size
    while s >= min_size:
        fnt = font(path, s)
        lines = wrap(d, text, fnt, max_w)
        if len(lines) <= max_lines:
            return lines, fnt
        s -= 1
    return wrap(d, text, font(path, min_size), max_w), font(path, min_size)


def chip(d, x, y, label):
    """Certainty chip; returns width."""
    colors = {"REPORTED": GREEN, "CLAIM": AMBER, "ONGOING": BLUE, "DENIAL": GREY}
    col = colors.get(label, GREY)
    fnt = font(SANS_B, 8)
    w = int(d.textlength(label, font=fnt)) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=col)
    d.text((x + 5, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- map data
NA = [(-168, 65), (-150, 70), (-130, 71), (-115, 68), (-100, 68), (-90, 66),
      (-82, 66), (-76, 62), (-68, 58), (-60, 55), (-55, 47), (-60, 45),
      (-65, 44), (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 26),
      (-84, 30), (-89, 29), (-94, 29), (-97, 26), (-97, 18), (-93, 15),
      (-88, 14), (-84, 12), (-80, 8), (-78, 7), (-82, 9), (-86, 12),
      (-90, 14), (-95, 16), (-100, 18), (-105, 20), (-110, 23), (-114, 29),
      (-120, 34), (-124, 40), (-125, 49), (-130, 55), (-140, 60),
      (-150, 61), (-158, 58), (-165, 60), (-168, 65)]
GREENLAND = [(-58, 64), (-45, 60), (-40, 65), (-30, 68), (-22, 70),
             (-25, 76), (-35, 80), (-50, 78), (-58, 72), (-58, 64)]
SA = [(-79, 9), (-75, 11), (-72, 12), (-64, 11), (-60, 9), (-52, 5),
      (-50, 0), (-44, -3), (-35, -8), (-38, -15), (-40, -22), (-48, -28),
      (-55, -35), (-58, -38), (-62, -41), (-65, -45), (-68, -50),
      (-70, -54), (-73, -50), (-73, -40), (-72, -30), (-70, -20),
      (-75, -15), (-78, -8), (-80, -4), (-81, 0), (-80, 5), (-79, 9)]
EUROPE = [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-1, 50),
          (2, 51), (5, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62),
          (10, 64), (13, 66), (18, 69), (25, 71), (30, 70), (35, 68),
          (40, 68), (45, 66), (48, 64), (50, 60), (45, 58), (40, 55),
          (35, 52), (30, 50), (28, 46), (23, 40), (26, 38), (23, 36),
          (19, 40), (15, 44), (12, 44), (8, 44), (3, 42), (0, 40),
          (-2, 37), (-6, 36), (-9, 37), (-10, 36)]
AFRICA = [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-5, 35), (0, 36),
          (10, 37), (11, 34), (15, 32), (20, 32), (25, 32), (30, 31),
          (32, 31), (34, 28), (35, 24), (37, 20), (39, 15), (41, 11),
          (43, 11), (48, 11), (51, 10), (44, 5), (41, 0), (40, -5),
          (39, -10), (35, -18), (33, -25), (28, -32), (20, -35),
          (17, -32), (15, -27), (13, -18), (12, -10), (13, -5), (9, 0),
          (9, 4), (-8, 5), (-13, 8), (-17, 12), (-17, 15)]
ASIA = [(30, 36), (35, 36), (36, 33), (40, 32), (43, 30), (48, 30),
        (50, 29), (52, 27), (55, 26), (58, 25), (60, 25), (62, 25),
        (66, 25), (68, 23), (72, 20), (75, 15), (77, 8), (80, 7),
        (80, 13), (85, 19), (88, 22), (91, 22), (93, 18), (95, 16),
        (98, 10), (100, 8), (103, 2), (104, 9), (106, 10), (108, 12),
        (109, 15), (106, 20), (108, 18), (110, 20), (114, 22), (118, 25),
        (120, 28), (122, 32), (120, 35), (122, 38), (124, 40), (127, 40),
        (130, 42), (132, 43), (135, 44), (138, 46), (140, 50), (142, 53),
        (142, 59), (140, 60), (136, 59), (133, 58), (130, 55), (128, 52),
        (125, 48), (122, 42), (118, 40), (115, 38), (110, 37), (108, 34),
        (105, 32), (100, 30), (98, 28), (95, 29), (92, 28), (88, 27),
        (85, 25), (82, 22), (80, 20), (78, 18), (75, 20), (72, 22),
        (70, 25), (68, 25), (66, 25), (63, 27), (60, 28), (57, 28),
        (55, 27), (52, 28), (50, 30), (48, 30), (45, 29), (42, 30),
        (40, 32), (38, 34), (35, 36), (33, 36), (30, 36)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (136, -12), (132, -11),
             (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51), (-5, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41),
         (143, 42), (145, 44), (142, 44), (140, 40), (138, 37), (135, 34),
         (132, 33), (130, 31)]
NZ = [(167, -45), (170, -42), (173, -40), (175, -38), (178, -38),
      (175, -40), (172, -43), (168, -46), (167, -45)]

CONTINENTS = [NA, GREENLAND, SA, EUROPE, AFRICA, ASIA, AUSTRALIA, UK, JAPAN, NZ]

# (story, lon, lat, dx, dy, kind) kind: R=reported, C=claim, O=ongoing
PINS = [
    (1, 127, 37.5, 0, 0, "R"), (2, -59.6, 13.2, 0, 0, "R"),
    (3, -150, -30, 0, 0, "R"), (4, -83, 42.3, -16, -6, "R"),
    (5, -122.4, 37.8, 0, 0, "R"), (6, 19, 52, 0, 0, "C"),
    (7, 37.6, 55.7, 0, 0, "C"), (8, 2.35, 48.85, 0, 0, "R"),
    (9, -2.24, 53.48, -10, -8, "R"), (10, 30.5, 50.45, 0, 0, "C"),
    (11, 30.7, 36.9, 0, 0, "R"), (12, 20.07, 32.1, -6, 0, "C"),
    (13, 34.8, 31, 12, -8, "O"), (14, 34.45, 31.5, -12, 8, "R"),
    (15, 35.2, 32, 14, 8, "R"), (16, 51.4, 35.7, 0, 0, "R"),
    (17, 35.5, 33.9, 0, 10, "R"), (18, 50.6, 26.2, 8, 6, "R"),
    (19, 32.5, 15.6, 0, 0, "R"), (20, 29.5, 1.5, 0, 0, "R"),
    (21, 90.4, 23.8, 0, 0, "R"), (22, 127, 37.5, 16, -10, "R"),
    (23, 127, 37.5, -16, 8, "R"), (24, 116.4, 39.9, -14, 0, "R"),
    (25, 127, 37.5, 14, 10, "R"), (26, -77, 38.9, 0, -10, "R"),
    (27, -77, 38.9, 14, 4, "R"), (28, -77, 38.9, -12, 6, "R"),
    (29, -74, 40.7, 20, -6, "R"), (30, -105, 39.7, 0, 0, "R"),
    (31, -97.7, 30.3, 0, 0, "R"),
]

HEROES = [
    dict(n=1, kicker="#1 ASIA · MARKETS", title="AI ROUT HITS ASIA",
         body="Kospi closes 4,708.54, sheds 161 pts. Samsung -3.1%, "
              "SK Hynix -2.5%. AI sell-off spreads from Wall Street.",
         source="Source: Yonhap · Korea JoongAng", chip="REPORTED",
         scene="kospi"),
    dict(n=2, kicker="#2 WORLD · UNITED NATIONS",
         title="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         body="UN chief urges global AI safety rules at the Bridgetown "
              "summit; 150 delegates back a risk framework.",
         source="Source: UN News · Reuters", chip="REPORTED",
         scene="guterres"),
    dict(n=3, kicker="#3 WORLD · POWER",
         title="US LEAD OVER CHINA AT RECORD LOW",
         body="Gap 5.3 narrowest since 2018. US diplomatic influence "
              "-6 to 76.7. India third at 40.5.",
         source="Source: Lowy Institute", chip="REPORTED",
         scene="power"),
]

CARDS = [
    dict(n=4, kicker="SPORT · US", title="Skubal signs $450M Mets deal",
         body="Two-time Cy Young winner, nine years — a record for a pitcher.",
         source="ESPN", chip="REPORTED"),
    dict(n=5, kicker="TECH · US", title="Anthropic IPO: $107.3B, largest ever",
         body="Claude maker raised at $83 a share on 19 Nov; debut close $97.17.",
         source="Bloomberg", chip="REPORTED"),
    dict(n=6, kicker="EUROPE · WAR", title="Poland: 3 Russian missiles crossed airspace",
         body="Kyiv says three Kh-101 entered Poland on Friday; Tusk: provocation.",
         source="AP", chip="CLAIM"),
    dict(n=7, kicker="EUROPE · SECURITY", title="Intel warns of Russian nuclear satellite",
         body="Moscow built a satellite to carry a nuclear warhead; launch next month.",
         source="Bloomberg", chip="CLAIM"),
    dict(n=8, kicker="EUROPE · ECONOMY", title="Paris: 100+ back 2% billionaire tax",
         body="Economists, politicians, unions rally behind France's 2% wealth tax.",
         source="AFP", chip="REPORTED"),
    dict(n=9, kicker="EUROPE · UK", title="Manchester: 12,000 cleared after scare",
         body="Substance scare empties arena district; no casualties reported.",
         source="AP", chip="REPORTED"),
    dict(n=10, kicker="EUROPE · WAR", title="Zelenskyy: 165 Russian missiles in a week",
         body="Kyiv says Moscow fired 165 missiles in seven days as US delays Patriots.",
         source="Kyiv", chip="CLAIM"),
    dict(n=11, kicker="EUROPE · CLIMATE", title="COP31: the day after",
         body="Sunday's collapse — 194 nations reject the Antalya pact — draws fury.",
         source="CNN", chip="REPORTED"),
    dict(n=12, kicker="AFRICA · LIBYA", title="Benghazi: UN demands probe of port attacks",
         body="Drones hit two Russian ships; UN calls for an investigation.",
         source="UN News", chip="CLAIM"),
    dict(n=13, kicker="MIDDLE EAST · ISRAEL", title="Israel unity talks resume",
         body="Likud and Gantz's Yesh Atid return to the table after Sunday's stall.",
         source="Reuters", chip="ONGOING"),
]

ALSO_COL_A = [
    ("MIDDLE EAST", [("14", "Gaza: two killed in strike"),
                     ("15", "West Bank: settler attacks"),
                     ("16", "Iran war: no deal in sight"),
                     ("17", "Lebanon: 264 kg explosives seized"),
                     ("18", "Bahrain: strike hits plant, 2 hurt")]),
    ("AFRICA", [("19", "Sudan: air defences down drones"),
                ("20", "DRC: fighting traps Ebola teams")]),
]
ALSO_COL_B = [
    ("ASIA-PACIFIC", [("21", "Bangladesh: Hasina jailed on return"),
                      ("22", "Seoul minister quits over exam chaos"),
                      ("23", "SK Telecom -7.3%, hype cools"),
                      ("24", "China eases margin rules"),
                      ("25", "Seoul readies 10T-won fund")]),
    ("NORTH AMERICA", [("26", "Bessent demands Nvidia answers"),
                        ("27", "FBI probes hack of police database"),
                        ("28", "Trump: Iran strikes may resume"),
                        ("29", "US futures jump 3% holiday week"),
                        ("30", "Tom Jackson dies at 75"),
                        ("31", "States sue SpaceX over AI claims")]),
]


def draw_kospi_scene(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # skyline
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 14:
        bw = rnd.randint(10, 18)
        bh = rnd.randint(18, 52)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(38, 58, 96))
        for wy in range(y + h - bh + 4, y + h - 4, 9):
            for wx in range(bx + 2, bx + bw - 2, 6):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(232, 197, 71))
        bx += bw + 3
    # falling chart
    pts = []
    n = 7
    for i in range(n):
        px = x + 14 + i * (w - 28) / (n - 1)
        py = y + 18 + i * (h - 52) / (n - 1) + (6 if i % 2 else -4)
        pts.append((px, py))
    d.line(pts, fill=(235, 64, 52), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255),
                  outline=(235, 64, 52), width=2)
    d.text((x + 10, y + 4), "intraday -5.8%", font=font(SANS, 11),
           fill=(255, 255, 255))
    f = font(SANS_B, 30)
    d.text((x + w - d.textlength("-3.3%", font=f) - 10, y + 2), "-3.3%",
           font=f, fill=(235, 64, 52))


def draw_guterres_scene(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # gold banner
    d.rectangle([x + w // 2 - 52, y + 6, x + w // 2 + 52, y + 24], fill=GOLD)
    d.text((x + w // 2, y + 8), "150 DELEGATES", font=font(SANS_B, 10),
           fill=(20, 20, 20), anchor="ma")
    # globe
    cx, cy, r = x + 62, y + h // 2 + 8, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 200),
              outline=(180, 210, 240), width=2)
    for k in range(-2, 3):
        d.arc([cx - r + abs(k) * 12, cy - r, cx + r - abs(k) * 12, cy + r],
              90, 270, fill=(180, 210, 240), width=1)
        d.arc([cx - r + abs(k) * 12, cy - r, cx + r - abs(k) * 12, cy + r],
              270, 90, fill=(180, 210, 240), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(180, 210, 240), width=1)
    d.line([cx - r + 8, cy - 22, cx + r - 8, cy - 22], fill=(180, 210, 240), width=1)
    d.line([cx - r + 8, cy + 22, cx + r - 8, cy + 22], fill=(180, 210, 240), width=1)
    # network nodes
    import random
    rnd = random.Random(11)
    nodes = []
    for _ in range(9):
        nx = x + w - rnd.randint(30, 150)
        ny = y + rnd.randint(30, h - 30)
        nodes.append((nx, ny))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if abs(nodes[i][0] - nodes[j][0]) + abs(nodes[i][1] - nodes[j][1]) < 90:
                d.line([nodes[i], nodes[j]], fill=(120, 160, 210), width=1)
    for nx, ny in nodes:
        d.ellipse([nx - 4, ny - 4, nx + 4, ny + 4], fill=(232, 197, 71),
                  outline=(255, 255, 255), width=1)
    # podium silhouette
    px, py = x + w - 52, y + h - 46
    d.ellipse([px - 8, py - 26, px + 8, py - 10], fill=(10, 10, 14))
    d.polygon([(px - 14, py - 10), (px + 14, py - 10), (px + 10, py + 16),
               (px - 10, py + 16)], fill=(10, 10, 14))
    d.rectangle([px - 22, py + 16, px + 22, y + h], fill=(30, 30, 40))


def draw_power_scene(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 246, 235))
    d.text((x + 10, y + 6), "ASIA POWER INDEX 2026", font=font(SANS_B, 12),
           fill=INK)
    bars = [("US", 78.9, (31, 78, 121)), ("CHINA", 73.6, (169, 28, 28)),
            ("INDIA", 40.5, (120, 120, 120))]
    by = y + 30
    maxw = w - 110
    for name, val, col in bars:
        d.text((x + 10, by), name, font=font(SANS_B, 12), fill=INK)
        d.rectangle([x + 74, by + 2, x + 74 + maxw * val / 100, by + 16],
                    fill=col)
        d.text((x + 80 + maxw * val / 100, by), f"{val:.1f}",
               font=font(SANS_B, 12), fill=INK)
        by += 26
    f = font(SANS_B, 16)
    d.text((x + 10, by + 2), "GAP 5.3", font=f, fill=RED)
    d.text((x + 92, by + 6), "narrowest since 2018", font=font(SANS, 11),
           fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top red rule
    d.rectangle([0, 0, W, 6], fill=RED)

    # masthead
    f_mast = font(SERIF, 46)
    d.text((8, 8), "THE WORLD TODAY", font=f_mast, fill=INK)
    f_side = font(SANS_B, 15)
    d.text((W - 8, 12), "31 STORIES", font=f_side, fill=INK, anchor="ra")
    d.text((W - 8, 32), "6 REGIONS", font=f_side, fill=INK, anchor="ra")

    # date strip
    d.text((8, 66), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 16),
           fill=RED)
    d.text((W - 8, 68), "AI ROUT  ·  AI RULES  ·  POWER SHIFT",
           font=font(SANS_B, 12), fill=GREY, anchor="ra")
    d.line([8, 88, W - 8, 88], fill=INK, width=2)

    # number strip
    nums = [("-3.3%", "KOSPI"), ("5.3", "US-CHINA GAP"),
            ("11,762", "EBOLA CASES"), ("10T WON", "SEOUL FUND"),
            ("$450M", "SKUBAL DEAL"), ("$107.3B", "ANTHROPIC IPO")]
    cw = (W - 16) / 6
    for i, (num, lab) in enumerate(nums):
        cx = 8 + i * cw
        f_num = font(SANS_B, 26)
        tw = d.textlength(num, font=f_num)
        d.text((cx + (cw - tw) / 2, 92), num, font=f_num, fill=RED)
        f_lab = font(SANS_B, 9)
        tw = d.textlength(lab, font=f_lab)
        d.text((cx + (cw - tw) / 2, 122), lab, font=f_lab, fill=INK)
        if i:
            d.line([cx, 94, cx, 134], fill=LINE, width=1)

    # region bar
    y0 = 138
    total = sum(c for _, c, _ in REGIONS)
    rx = 8
    for name, cnt, col in REGIONS:
        seg = (W - 16) * cnt / total
        d.rectangle([rx, y0, rx + seg - 1, y0 + 20], fill=col)
        label = f"{name} {cnt}"
        f_rb = font(SANS_B, 10)
        tw = d.textlength(label, font=f_rb)
        if tw < seg - 6:
            d.text((rx + (seg - tw) / 2, y0 + 4), label, font=f_rb,
                   fill=(255, 255, 255))
        rx += seg

    # UTC strip
    y0 = 160
    d.rectangle([8, y0, W - 8, y0 + 18], fill=NAVY)
    d.text((14, y0 + 3), "THE DAY IN UTC", font=font(SANS_B, 10),
           fill=(232, 197, 71))
    utc = ("~00:00 ASIA OPENS  ·  06:30 KOSPI -3.3%  ·  ~09:00 SEOUL FUND  ·  "
           "14:30 WALL ST +3%  ·  ~16:00 GUTERRES  ·  ~21:00 FBI HACK    "
           "(~ = APPROX.)")
    d.text((150, y0 + 3), utc, font=font(SANS, 10), fill=(255, 255, 255))

    # hero scenes + text
    hero_y, hero_h, hero_t = 180, 150, 124
    hw = int((W - 16 - 12) / 3)
    for i, hero in enumerate(HEROES):
        x = 8 + i * (hw + 6)
        if hero["scene"] == "kospi":
            draw_kospi_scene(d, x, hero_y, hw, hero_h)
        elif hero["scene"] == "guterres":
            draw_guterres_scene(d, x, hero_y, hw, hero_h)
        else:
            draw_power_scene(d, x, hero_y, hw, hero_h)
        ty = hero_y + hero_h + 6
        d.text((x, ty), hero["kicker"], font=font(SANS_B, 10), fill=RED)
        ty += 14
        tlines, tf = fit_lines(d, hero["title"], SERIF, 17, hw, 2)
        ty = draw_lines(d, x, ty, tlines, tf, INK, leading=tf.size + 2)
        ty += 2
        blines, bf = fit_lines(d, hero["body"], SANS, 11, hw, 3)
        ty = draw_lines(d, x, ty, blines, bf, INK, leading=bf.size + 3)
        ty += 3
        f_src = font(SANS, 9)
        d.text((x, ty), hero["source"], font=f_src, fill=GREY)
        chip(d, x + hw - 62, ty - 1, hero["chip"])

    # small cards: 2 rows x 5
    card_y0 = 452
    card_h, card_gap = 82, 4
    cw = int((W - 16 - 4 * 6) / 5)
    for r in range(2):
        for c in range(5):
            card = CARDS[r * 5 + c]
            x = 8 + c * (cw + 6)
            y = card_y0 + r * (card_h + card_gap)
            col = REGION_COLOR[REGION_OF[card["n"]]]
            d.rectangle([x, y, x + cw, y + card_h], outline=LINE, width=1,
                        fill=(255, 255, 255))
            d.rectangle([x, y, x + cw, y + 15], fill=col)
            d.text((x + 4, y + 2), f"#{card['n']} {card['kicker']}",
                   font=font(SANS_B, 8), fill=(255, 255, 255))
            ty = y + 18
            tlines, tf = fit_lines(d, card["title"], SANS_B, 11, cw - 8, 2)
            ty = draw_lines(d, x + 4, ty, tlines, tf, INK,
                            leading=tf.size + 1)
            blines, bf = fit_lines(d, card["body"], SANS, 9, cw - 8, 2)
            ty = draw_lines(d, x + 4, ty + 1, blines, bf, (60, 60, 60),
                            leading=bf.size + 2)
            by = y + card_h - 16
            d.text((x + 4, by), card["source"], font=font(SANS, 8),
                   fill=GREY)
            chip(d, x + cw - 62, by - 1, card["chip"])

    # map + ALSO header
    my = 624
    d.text((8, my), "THE WORLD — WHERE IT HAPPENED",
           font=font(SANS_B, 12), fill=RED)
    d.text((556, my + 2), "PIN = STORY NUMBER", font=font(SANS, 9),
           fill=GREY, anchor="ra")
    d.text((570, my), "ALSO ON MONDAY — 18 MORE STORIES",
           font=font(SANS_B, 12), fill=RED)

    # map
    mx, my0, mw, mh = 8, 646, 548, 192
    d.rectangle([mx, my0, mx + mw, my0 + mh], fill=(214, 232, 240),
                outline=LINE, width=1)

    def ll(lon, lat):
        return (mx + (lon + 180) / 360 * mw,
                my0 + (75 - lat) / 135 * mh)

    # grid
    for gx in range(-150, 181, 30):
        px, _ = ll(gx, 0)
        d.line([px, my0, px, my0 + mh], fill=(190, 210, 225), width=1)
    for gy in range(-60, 76, 30):
        _, py = ll(0, gy)
        d.line([mx, py, mx + mw, py], fill=(190, 210, 225), width=1)
    for poly in CONTINENTS:
        d.polygon([ll(lon, lat) for lon, lat in poly],
                  fill=(232, 220, 180), outline=(180, 165, 130))
    d.text((mx + 6, my0 + mh - 14), "N ↑", font=font(SANS_B, 9), fill=INK)

    pin_xy = {}
    for n, lon, lat, dx, dy, kind in PINS:
        px, py = ll(lon, lat)
        px += dx
        py += dy
        pin_xy[n] = (px, py)
        col = {"R": RED, "C": (217, 130, 23), "O": BLUE}[kind]
        d.ellipse([px - 6.5, py - 6.5, px + 6.5, py + 6.5], fill=col,
                  outline=(255, 255, 255), width=1)
        f_p = font(SANS_B, 8)
        tw = d.textlength(str(n), font=f_p)
        d.text((px - tw / 2, py - 5), str(n), font=f_p, fill=(255, 255, 255))
    # pin spacing check
    worst = 999
    for a in pin_xy:
        for b in pin_xy:
            if a < b:
                dist = ((pin_xy[a][0] - pin_xy[b][0]) ** 2 +
                        (pin_xy[a][1] - pin_xy[b][1]) ** 2) ** 0.5
                worst = min(worst, dist)
    print(f"min pin distance: {worst:.1f}px")

    # ALSO list
    ax = 570
    ay = my0
    f_hdr = font(SANS_B, 9)
    f_it = font(SANS, 9)
    col_w = 222
    for ci, col_data in enumerate([ALSO_COL_A, ALSO_COL_B]):
        cx = ax + ci * (col_w + 4)
        yy = ay
        for region, items in col_data:
            d.text((cx, yy), region, font=f_hdr,
                   fill=REGION_COLOR[region])
            yy += 13
            for num, txt in items:
                d.text((cx, yy), f"{num} {txt}", font=f_it, fill=INK)
                yy += 12

    # DATE CHECK
    dy = 842
    d.rectangle([8, dy, W - 8, dy + 90], outline=RED, width=2,
                fill=(255, 245, 240))
    d.text((14, dy + 6), "DATE CHECK", font=font(SANS_B, 13), fill=RED)
    d.text((W - 14, dy + 8), "WIRES READ UP TO 23:00 UTC",
           font=font(SANS_B, 9), fill=RED, anchor="ra")
    d.text((14, dy + 26),
           "Every story above happened or was first reported on Monday "
           "23 November 2026.",
           font=font(SANS_B, 10), fill=INK)
    left = ("LEFT OUT (not 23 Nov): Democrats reach 258 (22 Nov) · Sparta II "
            "fire (22 Nov) · El Chapo Isidro captured (22 Nov) · "
            "EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · "
            "ICJ Myanmar ruling (19 Nov).")
    lines = wrap(d, left, font(SANS, 10), W - 28)
    draw_lines(d, 14, dy + 44, lines, font(SANS, 10), INK, leading=13)
    ny = dy + 44 + len(lines) * 13 + 2
    d.text((14, ny),
           "NOT YET: Dymer search continues (14 missing) · 4 House races "
           "uncalled · COP32 venue not set · WHO evacuating trapped "
           "Ebola staff.",
           font=font(SANS, 10), fill=INK)

    # footer
    fy = 938
    d.text((8, fy), "SOURCES: AP · Reuters · Bloomberg · AFP · CNN · ESPN · "
                    "UN News · WHO · Kyiv · Lowy Institute · Korea "
                    "JoongAng · Morningstar",
           font=font(SANS, 9), fill=GREY)
    d.text((8, fy + 13), "CONFIRMED = 2+ outlets · REPORTED = carried by a "
                         "wire · CLAIM = one side alleges · ONGOING = "
                         "developing.  Red pin = reported · Amber pin = "
                         "claim (unverified).",
           font=font(SANS, 9), fill=GREY)
    d.text((8, fy + 28), "THE WORLD TODAY · 23 NOV 2026",
           font=font(SANS_B, 10), fill=INK)
    d.text((W - 8, fy + 28), "Scenes are drawn illustrations, not photographs.",
           font=font(SANS, 10), fill=GREY, anchor="ra")

    out = os.path.join(BASE, "entry.png")
    img.save(out, optimize=True)
    print(f"saved {out}: {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
