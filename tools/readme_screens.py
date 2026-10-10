# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Matěj "Wolf" Holyszewski, OK2MTB

"""
Screen images for the README (docs/img/).

Usage:
    python tools/readme_screens.py

A Python copy of the rendering in main.cpp: the font and map are read from the sources,
texts are in English and the data is sample data. Pixels are solid, no grid, framed like the display.
When a screen layout changes in main.cpp, this script needs updating too.
A real snapshot from the board is made by tools/snapshot.py.
Needs Pillow.
"""
import math
import os
import re
import sys
from PIL import Image, ImageDraw

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
outdir = os.path.join(root, "docs", "img")
os.makedirs(outdir, exist_ok=True)
src = open(os.path.join(root, "src", "main.cpp"), encoding="utf-8").read()
mapsrc = open(os.path.join(root, "src", "maps.h"), encoding="utf-8").read()

# ---------- font ----------
font = {}
for m in re.finditer(r'\{"((?:[^"\\]|\\.)*)",\s*\{((?:\s*"[.# ]*",?)+)\s*\}\}', src):
    chars = m.group(1).replace('\\"', '"')
    rows = re.findall(r'"([.# ]*)"', m.group(2))
    if len(rows) == 7:
        for i, c in enumerate(chars):
            font[c] = [r[i * 6:i * 6 + 5] for r in rows]

# ---------- maps ----------
maps = {}
for m in re.finditer(r'static const MapView (\w+) = \{([-\d.]+)f, ([-\d.]+)f, ([-\d.]+)f, ([-\d.]+)f, \{(.*?)\}\};', mapsrc, re.S):
    vals = [int(v, 16) for v in re.findall(r'0x([0-9A-Fa-f]{2})', m.group(6))]
    maps[m.group(1)] = dict(west=float(m.group(2)), east=float(m.group(3)), north=float(m.group(4)),
                            south=float(m.group(5)), bits=vals)


def tw(t, scale=1):
    return (len(t) * 6 - 1) * scale if t else 0


class Fb:
    def __init__(s):
        s.p = [[False] * 128 for _ in range(64)]

    def px(s, x, y, on=True):
        if 0 <= x < 128 and 0 <= y < 64:
            s.p[y][x] = on

    def rect(s, x, y, w, h, on=True):
        for j in range(h):
            for i in range(w):
                s.px(x + i, y + j, on)

    def text(s, t, x, y, scale=1, on=True):
        for c in t:
            g = font.get(c) or font.get(c.upper())
            if g:
                for r in range(7):
                    for i in range(5):
                        if g[r][i] == '#':
                            s.rect(x + i * scale, y + r * scale, scale, scale, on)
            x += 6 * scale

    def right(s, t, r, y, scale=1, on=True):
        s.text(t, r - tw(t, scale) + 1, y, scale, on)

    def header(s, left, right=""):
        s.rect(0, 0, 128, 9)
        s.text(left, 1, 1, 1, False)
        if right:
            s.right(right, 126, 1, 1, False)


# ---------- sample data ----------
CALL, LOC = "OK2MTB", "JN89"
HOME = (49.2, 17.5)
UTC = (16, 21, 37)                     # 10 Oct 2026, 18:21 CEST – the terminator is just crossing Europe
SPOTS = [  # call, band, SNR, km, lat, lon (stations that heard OK2MTB in this session)
    ("S52D", "80", 8, 388, 46.1, 14.8),
    ("F1UVN-RSPDX", "80", -1, 1011, 48.6, 3.8),
    ("IT9IVN", "80", -7, 1272, 37.6, 14.9),
    ("EA4RCW", "80", -13, 1871, 40.4, -3.7),
]


def clock():
    f = Fb()
    f.text("UTC", 0, 0)
    f.right("SAT 10 OCT 2026", 127, 0)
    f.text("%02d:%02d" % UTC[:2], 0, 11, 3)
    f.text(":%02d" % UTC[2], 93, 18, 2)
    f.text("%02d:%02d" % (UTC[0] + 2, UTC[1]), 0, 38, 2)
    f.text("CEST", 64, 45)
    f.text(CALL, 0, 57)
    f.right(LOC, 127, 57)
    return f


def solar():
    f = Fb()
    f.text("SFI 148", 0, 0)
    f.text("SN 112", 54, 0)
    f.right("A 8", 127, 0)
    f.text("K 2", 0, 8)
    nv = "NVIS60"
    f.text(nv, 43 - tw(nv) // 2, 8)
    f.right("XRAY C1.2", 127, 8)
    f.text("FOF2 5.9", 0, 16)
    f.right("MUF 17.8", 127, 16)
    f.text("BAND", 0, 24)
    f.text("DAY", 36, 24)
    f.text("NIGHT", 84, 24)
    for x in range(0, 128, 2):
        f.px(x, 31)
    cond = [[1, 1], [1, 2], [2, 3], [3, 3]]
    word = {1: "GOOD", 2: "FAIR", 3: "POOR"}
    for i, g in enumerate(["80-40", "30-20", "17-15", "12-10"]):
        y = 33 + i * 8
        f.text(g, 0, y)
        for j in range(2):
            x = 84 if j else 36
            t = word[cond[i][j]]
            if cond[i][j] == 1:
                f.rect(x - 1, y - 1, tw(t) + 2, 9)
                f.text(t, x, y, 1, False)
            else:
                f.text(t, x, y)
    return f


def psk_list():
    f = Fb()
    f.header("HEARD ME: %d" % len(SPOTS))
    for i, (call, band, snr, km, _, _) in enumerate(SPOTS):
        y = 11 + i * 9
        f.text(call[:9], 0, y)
        f.right(band, 72, y)
        f.right("%+d" % snr, 93, y)
        f.right(str(km), 127, y)
    return f


def subsolar():
    import calendar
    t = calendar.timegm((2026, 10, 10, UTC[0], UTC[1], UTC[2], 0, 0, 0))
    n = (t - 946728000.0) / 86400.0
    L = math.fmod(280.460 + 0.9856474 * n, 360.0)
    g = math.radians(math.fmod(357.528 + 0.9856003 * n, 360.0))
    lam = math.radians(L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g))
    eps = math.radians(23.439 - 0.0000004 * n)
    ra = math.degrees(math.atan2(math.cos(eps) * math.sin(lam), math.cos(lam)))
    gmst = math.fmod(280.46061837 + 360.98564736629 * n, 360.0)
    return math.degrees(math.asin(math.sin(eps) * math.sin(lam))), math.fmod(ra - gmst + 540.0, 360.0) - 180.0


def psk_map(name):
    m = maps[name]
    bit = lambda x, y: m["bits"][y * 16 + (x >> 3)] & (0x80 >> (x & 7))
    wrap = m["east"] - m["west"] >= 360
    f = Fb()
    decl, sublon = subsolar()
    sd, cd = math.sin(math.radians(decl)), math.cos(math.radians(decl))
    for y in range(64):
        lat = math.radians(m["north"] - (y + 0.5) * (m["north"] - m["south"]) / 64)
        a, b = math.sin(lat) * sd, math.cos(lat) * cd
        for x in range(128):
            if not bit(x, y):
                continue
            edge = (y > 0 and not bit(x, y - 1)) or (y < 63 and not bit(x, y + 1))
            if x > 0 or wrap:
                edge = edge or not bit((x + 127) & 127, y)
            if x < 127 or wrap:
                edge = edge or not bit((x + 1) & 127, y)
            lon = m["west"] + (x + 0.5) * (m["east"] - m["west"]) / 128
            day = a + b * math.cos(math.radians(lon - sublon)) > 0
            if edge or (day and not ((x + y) & 1)):
                f.px(x, y)

    def xy(lat, lon):
        return (int(math.floor((lon - m["west"]) / (m["east"] - m["west"]) * 128)),
                int(math.floor((m["north"] - lat) / (m["north"] - m["south"]) * 64)))
    for s in reversed(SPOTS):
        x, y = xy(s[4], s[5])
        f.rect(x - 3, y - 3, 7, 7, False)
        f.rect(x - 1, y - 1, 3, 3)
    x, y = xy(*HOME)
    f.rect(x - 3, y - 3, 7, 7, False)
    f.rect(x - 2, y - 2, 5, 5)
    f.rect(x - 1, y - 1, 3, 3, False)
    f.px(x, y)
    t = str(len(SPOTS))
    f.rect(0, 55, tw(t) + 3, 9, False)
    f.text(t, 1, 57)
    return f


# ---------- image: solid pixels, black display with rounded corners, transparent surroundings ----------
S, PAD, R = 4, 14, 14
ON = (140, 220, 255, 255)


def image(f):
    W, H = 128 * S + 2 * PAD, 64 * S + 2 * PAD
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, W - 1, H - 1], R, fill=(10, 12, 16, 255), outline=(60, 64, 72, 255), width=2)
    for y in range(64):
        for x in range(128):
            if f.p[y][x]:
                d.rectangle([PAD + x * S, PAD + y * S, PAD + x * S + S - 1, PAD + y * S + S - 1], fill=ON)
    return img


shots = [("clock", clock()), ("propagation", solar()), ("heard-list", psk_list()),
         ("heard-map", psk_map("MAP_EUROPE"))]
frames = []
for name, f in shots:
    img = image(f)
    img.save(os.path.join(outdir, name + ".png"))
    frames.append(img)
# animation for the top of the README: APNG (unlike GIF it handles both transparent surroundings and a black display)
frames[0].save(os.path.join(outdir, "demo.png"), save_all=True, append_images=frames[1:], duration=2500, loop=0,
               disposal=1)
print("ok", [n for n, _ in shots])
