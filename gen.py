#!/usr/bin/env python3
"""Render the 22 November 2026 world-news front page to entry.png.

Run in this repo:  python3 gen.py
Writes entry.png (1024x1024, PNG) next to this file.
Only the Python standard library plus Pillow is used at build time; the
shipped entry program (main.py) just copies the finished image, so the
graded run needs no network and no third-party code.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# Palette: newsprint paper, navy masthead, signal red, ink black.
PAPER = (247, 243, 234)
INK = (24, 24, 24)
NAVY = (16, 35, 60)
NAVY_LIGHT = (28, 58, 92)
RED = (178, 34, 28)
GOLD = (217, 164, 65)
GREY = (96, 96, 92)
LIGHT_GREY = (232, 228, 219)
WHITE = (255, 255, 255)
TEAL = (14, 110, 110)
ORANGE = (214, 106, 24)
GREEN = (46, 125, 50)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)            # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)              # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, color, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36                      # side margin
    right = W - mx

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 128], fill=NAVY)
    d.text((W / 2, 14), "THE WORLD TODAY", font=SERIF_B(62),
           fill=WHITE, anchor="ma")
    d.text((W / 2, 92), "SUNDAY, 22 NOVEMBER 2026", font=SANS_B(24),
           fill=GOLD, anchor="ma")
    d.rectangle([0, 128, W, 134], fill=RED)

    # ---- Lead story: Iran / Bahrain -------------------------------------
    ly = 152
    d.text((mx, ly), "MIDDLE EAST  •  GULF CRISIS", font=SANS_B(19),
           fill=RED)
    head_f = SERIF_B(43)
    head = wrap(d, "IRAN STRIKES US BASES IN BAHRAIN", head_f, 610)
    y = draw_lines(d, head, mx, ly + 30, head_f, INK, 50)

    deck_f = SANS(21)
    deck = wrap(
        d,
        "Tehran says its missiles and drones hit two US Patriot radars "
        "at bases in Bahrain. Bahrain says a civilian factory caught "
        "fire and no one was hurt. Tankers were also hit in the "
        "Strait of Hormuz.",
        deck_f, 610)
    y = draw_lines(d, deck, mx, y + 8, deck_f, (58, 58, 58), 28)

    # Lead art: night sky over the Gulf, radar dish, missile arcs, burst.
    ax0, ay0, ax1, ay1 = 690, 152, right, 392
    d.rectangle([ax0, ay0, ax1, ay1], fill=(12, 24, 44))
    # stars
    for sx, sy, r in [(716, 176, 2), (760, 164, 2), (812, 182, 2),
                      (880, 168, 2), (940, 190, 2), (700, 210, 1),
                      (845, 205, 1), (968, 168, 1), (790, 160, 1)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=WHITE)
    # moon
    d.ellipse([906, 168, 946, 208], fill=(238, 232, 205))
    d.ellipse([918, 168, 946, 200], fill=(12, 24, 44))
    # missile trails: two diagonal streaks diving toward the burst
    d.line([(706, 196), (782, 292)], fill=ORANGE, width=4)
    d.line([(700, 208), (776, 304)], fill=(255, 176, 32), width=2)
    d.line([(952, 196), (872, 290)], fill=ORANGE, width=4)
    d.line([(958, 208), (878, 302)], fill=(255, 176, 32), width=2)
    # explosion burst low over the skyline (red-orange, spiky, not sun-like)
    bx, by = 830, 312
    for ang in range(0, 360, 24):
        rad = math.radians(ang)
        ln = 40 if (ang // 24) % 2 == 0 else 26
        x2 = bx + ln * math.cos(rad)
        y2 = by + ln * math.sin(rad)
        d.line([(bx, by), (x2, y2)], fill=(255, 120, 20), width=4)
    d.ellipse([bx - 18, by - 18, bx + 18, by + 18], fill=(255, 90, 20))
    d.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(255, 200, 60))
    # skyline silhouettes
    for bx0, bw, bh in [(690, 46, 52), (740, 34, 76), (778, 52, 44),
                        (834, 40, 88), (878, 56, 58), (938, 50, 70)]:
        d.rectangle([bx0, ay1 - bh, bx0 + bw, ay1], fill=(4, 10, 20))
    # radar dish, clear of the burst, on the second tower
    d.line([(757, ay1 - 76), (757, ay1 - 104)], fill=WHITE, width=3)
    d.arc([742, ay1 - 122, 772, ay1 - 92], 180, 360, fill=WHITE, width=4)
    d.line([(757, ay1 - 104), (772, ay1 - 92)], fill=WHITE, width=3)
    # caption
    d.text((ax0, ay1 + 8), "US bases in Bahrain targeted; tankers hit",
           font=SANS(14), fill=GREY)

    rule(d, mx, 420, right, INK, 2)

    # ---- Four-story grid ------------------------------------------------
    stories = [
        ("TRADE", TEAL,
         "EU AND INDONESIA SIGN LANDMARK TRADE DEAL",
         "After ten years of talks, Brussels and Jakarta sign a pact "
         "scrapping tariffs on 98.5% of goods. It still needs "
         "ratification.", "Reuters"),
        ("CLIMATE", GREEN,
         "COP31 TALKS DEADLOCKED IN OVERTIME",
         "Climate negotiators run past their deadline, split over "
         "fossil fuels and finance for poorer nations.", "ABC News"),
        ("UKRAINE", RED,
         "RUSSIAN STRIKE ON LVIV KILLS TWO",
         "A missile hits a building in the western Ukrainian city; "
         "ten people are injured, officials say.", "ANI"),
        ("MEXICO", ORANGE,
         "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
         "Troops seize cartel boss Fausto Isidro Meza Flores in "
         "Sinaloa. Four soldiers and seven suspects are killed "
         "in the raid.", "AFP"),
    ]
    gx, gy = mx, 440
    cw, chh, gap = 470, 188, 12
    for i, (kicker, color, headline, body, source) in enumerate(stories):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (chh + gap)
        d.rectangle([cx, cy, cx + cw, cy + chh], fill=WHITE,
                    outline=(200, 195, 185), width=1)
        d.rectangle([cx, cy, cx + cw, cy + 6], fill=color)
        d.text((cx + 14, cy + 16), kicker, font=SANS_B(15), fill=color)
        hf = SERIF_B(24)
        hl = wrap(d, headline, hf, cw - 28)
        y = draw_lines(d, hl, cx + 14, cy + 40, hf, INK, 28)
        bf = SANS(17)
        bl = wrap(d, body, bf, cw - 28)
        draw_lines(d, bl, cx + 14, y + 4, bf, (58, 58, 58), 22)
        d.text((cx + 14, cy + chh - 24), "Source: " + source,
               font=SANS(13), fill=GREY)

    # ---- Also today strip -----------------------------------------------
    sy = 852
    d.rectangle([mx, sy, right, sy + 96], fill=NAVY_LIGHT)
    d.text((mx + 14, sy + 10), "ALSO TODAY", font=SANS_B(17), fill=GOLD)
    items = [
        "PERU — A 6.7 quake shakes the Andes; no casualties reported.",
        "HONG KONG — Voting opens for the powerful Election Committee.",
        "DENMARK — Russia blamed for a plot to kill a US-Ukrainian citizen.",
    ]
    tf = SANS(16)
    y = sy + 36
    for item in items:
        d.text((mx + 14, y), "•  " + item, font=tf, fill=WHITE)
        y += 20

    # ---- Footer ----------------------------------------------------------
    d.text((W / 2, 968), "All events reported on Sunday 22 November 2026",
           font=SANS_B(14), fill=GREY, anchor="ma")
    d.text((W / 2, 988),
           "Sources: Reuters, Al Jazeera, AFP, Euronews, ANI  •  "
           "One day's news, one image",
           font=SANS(13), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
