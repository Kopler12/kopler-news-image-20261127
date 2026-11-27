#!/usr/bin/env python3
"""Render THE WORLD TODAY - Friday 27 November 2026.

Draws a 1024x1024 newspaper front page with the six world-news stories
first reported on Friday 27 November 2026, using only Pillow and the
system fonts. Deterministic: no network, no clock, no randomness.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
CARD = (255, 253, 246)
INK = (20, 20, 20)
GREY = (90, 86, 76)
RED = (178, 34, 26)
NAVY = (31, 58, 95)
TEAL = (14, 107, 107)
GOLD = (176, 124, 0)
SLATE = (70, 80, 95)
LIGHT_LINE = (205, 198, 184)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def font(path, size):
    return ImageFont.truetype(path, size)


SERIF_B = lambda s: font(f"{FL}/LiberationSerif-Bold.ttf", s)
SERIF_I = lambda s: font(f"{FL}/LiberationSerif-Italic.ttf", s)
SANS_B = lambda s: font(f"{FL}/LiberationSans-Bold.ttf", s)
SANS = lambda s: font(f"{FL}/LiberationSans-Regular.ttf", s)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label, color):
    draw.text((x, y), label, font=SANS_B(19), fill=color)


def scene_frame(draw, x, y, w, h, bg):
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw_gaza_scene(draw, x, y, w, h):
    scene_frame(draw, x, y, w, h, (232, 224, 208))
    # skyline silhouette
    base = y + h
    heights = [58, 92, 70, 110, 84, 66, 98, 74]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw + 3
        draw.rectangle([bx, base - hh, bx + bw - 6, base], fill=NAVY)
        for wy in range(int(base - hh + 10), int(base - 8), 16):
            draw.rectangle([bx + 5, wy, bx + 9, wy + 7], fill=(240, 210, 90))
    # red warning triangle
    cx, cy = x + w - 78, y + 58
    draw.polygon([(cx, cy - 44), (cx + 46, cy + 34), (cx - 46, cy + 34)],
                 fill=RED, outline=INK)
    draw.text((cx - 7, cy - 22), "!", font=SANS_B(40), fill=(255, 255, 255))
    draw.text((x + 16, y + 12), "1,000,000", font=SANS_B(46), fill=RED)


def draw_ukraine_scene(draw, x, y, w, h):
    scene_frame(draw, x, y, w, h, (214, 226, 238))
    # cooling tower
    tx = x + 24
    draw.polygon([(tx, y + h - 6), (tx + 26, y + 18), (tx + 86, y + 18),
                  (tx + 112, y + h - 6)], fill=(150, 158, 170), outline=INK)
    draw.rectangle([tx + 22, y + 12, tx + 90, y + 22], fill=(120, 128, 142))
    # lightning bolt
    bx, by = x + w - 118, y + 16
    draw.polygon([(bx + 34, by), (bx + 6, by + 52), (bx + 28, by + 52),
                  (bx + 16, by + 96), (bx + 58, by + 38), (bx + 34, by + 38)],
                 fill=(240, 190, 20), outline=INK)
    # drone
    dx, dy = x + w - 210, y + 22
    draw.ellipse([dx - 16, dy - 6, dx + 16, dy + 6], fill=INK)
    draw.rectangle([dx - 34, dy - 16, dx + 34, dy - 12], fill=INK)
    draw.ellipse([dx - 46, dy - 22, dx - 22, dy - 10], outline=INK, width=2)
    draw.ellipse([dx + 22, dy - 22, dx + 46, dy - 10], outline=INK, width=2)
    draw.rectangle([dx - 3, dy + 4, dx + 3, dy + 26], fill=INK)


def draw_korea_scene(draw, x, y, w, h):
    scene_frame(draw, x, y, w, h, (24, 32, 54))
    # red starburst
    cx, cy = x + w - 66, y + 52
    for k in range(12):
        import math
        a = math.pi * k / 6
        x2, y2 = cx + 44 * math.cos(a), cy + 44 * math.sin(a)
        draw.line([cx, cy, x2, y2], fill=(220, 60, 50), width=4)
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=RED)
    draw.text((cx - 13, cy - 19), "*", font=SANS_B(44), fill=(255, 255, 255))
    # rocket
    rx, ry = x + 30, y + h - 92
    draw.polygon([(rx + 22, ry), (rx + 44, ry + 34), (rx, ry + 34)], fill=RED)
    draw.rectangle([rx, ry + 34, rx + 44, ry + 78], fill=(240, 240, 235),
                   outline=INK)
    draw.polygon([(rx - 12, ry + 78), (rx, ry + 58), (rx, ry + 78)],
                 fill=RED)
    draw.polygon([(rx + 56, ry + 78), (rx + 44, ry + 58), (rx + 44, ry + 78)],
                 fill=RED)
    draw.polygon([(rx + 14, ry + 78), (rx + 30, ry + 78), (rx + 22, ry + 96)],
                 fill=(240, 160, 20))
    draw.ellipse([rx + 14, ry + 46, rx + 30, ry + 62], fill=NAVY)


def draw_hk_scene(draw, x, y, w, h):
    scene_frame(draw, x, y, w, h, (226, 222, 214))
    base = y + h
    # three towers, middle one scorched
    draw.rectangle([x + 18, base - 78, x + 74, base], fill=(140, 146, 158),
                   outline=INK)
    draw.rectangle([x + 84, base - 104, x + 150, base], fill=(52, 52, 52),
                   outline=INK)
    draw.rectangle([x + 160, base - 66, x + 212, base], fill=(140, 146, 158),
                   outline=INK)
    for wx in (28, 48, 94, 114, 134, 170, 190):
        for wy in range(int(base - 70), int(base - 8), 18):
            draw.rectangle([x + wx, wy, x + wx + 8, wy + 8],
                           fill=(240, 210, 90))
    # memorial candle
    cx = x + w - 62
    draw.rectangle([cx - 12, base - 34, cx + 12, base - 6], fill=(245, 240, 225),
                   outline=INK)
    draw.polygon([(cx, base - 58), (cx - 9, base - 38), (cx + 9, base - 38)],
                 fill=(240, 160, 20))


def draw_bangladesh_scene(draw, x, y, w, h):
    scene_frame(draw, x, y, w, h, (208, 228, 222))
    # factory with sawtooth roof
    fx, fy = x + 16, y + h - 64
    draw.polygon([(fx, fy), (fx + 34, fy - 26), (fx + 68, fy),
                  (fx + 102, fy - 26), (fx + 136, fy), (fx + 136, fy + 64),
                  (fx, fy + 64)], fill=TEAL, outline=INK)
    for wx in (12, 44, 76, 108):
        draw.rectangle([fx + wx, fy + 18, fx + wx + 16, fy + 34],
                       fill=(255, 250, 230))
    # tear-gas cloud
    cx, cy = x + w - 84, y + 44
    for ox, oy, r in ((-22, 8, 20), (0, -6, 24), (22, 8, 20), (-8, 16, 18),
                      (12, 18, 16)):
        draw.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                     fill=(168, 168, 160), outline=(120, 120, 112))


def draw_usa_scene(draw, x, y, w, h):
    scene_frame(draw, x, y, w, h, (210, 220, 232))
    # storm cloud
    cx, cy = x + 66, y + 42
    for ox, oy, r in ((-24, 10, 22), (0, -8, 28), (26, 8, 22), (-10, 18, 20),
                      (16, 18, 18)):
        draw.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                     fill=(74, 82, 96))
    # lightning
    bx, by = cx - 8, cy + 22
    draw.polygon([(bx + 12, by), (bx, by + 18), (bx + 9, by + 18),
                  (bx + 3, by + 34), (bx + 19, by + 13), (bx + 9, by + 13)],
                 fill=(240, 190, 20))
    # plane
    px, py = x + w - 130, y + 26
    draw.polygon([(px, py + 10), (px + 96, py + 10), (px + 110, py + 16),
                  (px + 96, py + 22), (px, py + 22)], fill=NAVY)
    draw.polygon([(px + 30, py + 10), (px + 44, py - 12), (px + 58, py + 10)],
                 fill=NAVY)
    draw.polygon([(px + 78, py + 22), (px + 88, py + 38), (px + 96, py + 22)],
                 fill=NAVY)
    # rain
    for rx in range(x + 16, x + w - 12, 26):
        draw.line([rx, y + h - 26, rx - 6, y + h - 10], fill=NAVY, width=2)


def story_cell(draw, x, y, w, h, kicker_label, color, headline, summary,
               scene_fn, head_size=29, scene_h=104):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)
    sh = scene_h
    scene_fn(draw, x + 10, y + 10, w - 20, sh)
    ty = y + 10 + sh + 12
    kicker(draw, x + 14, ty, kicker_label, color)
    ty += 26
    lines = wrap(draw, headline, SERIF_B(head_size), w - 28)
    ty = text_block(draw, x + 14, ty, lines, SERIF_B(head_size), INK,
                    head_size + 4)
    ty += 4
    lines = wrap(draw, summary, SANS(18), w - 28)
    text_block(draw, x + 14, ty, lines, SANS(18), (52, 48, 42), 23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer double frame
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)
    d.rectangle([14, 14, W - 15, H - 15], outline=LIGHT_LINE, width=1)

    # masthead
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=SERIF_B(86))
    d.text(((W - tw) / 2, 26), title, font=SERIF_B(86), fill=INK)
    d.line([32, 128, W - 32, 128], fill=INK, width=3)
    d.line([32, 133, W - 32, 133], fill=INK, width=1)
    date = "FRIDAY  ·  27 NOVEMBER 2026"
    dw = d.textlength(date, font=SANS_B(26))
    d.text(((W - dw) / 2, 142), date, font=SANS_B(26), fill=RED)
    sub = "The day's world news in one picture"
    sw = d.textlength(sub, font=SERIF_I(22))
    d.text(((W - sw) / 2, 176), sub, font=SERIF_I(22), fill=GREY)

    # ---- LEAD: Gaza ----
    lx, ly, lw, lh = 32, 208, 960, 202
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=INK, width=2)
    kicker(d, lx + 20, ly + 14, "MIDDLE EAST  ·  GAZA", RED)
    head = "A MILLION AT RISK"
    d.text((lx + 20, ly + 44), head, font=SERIF_B(52), fill=INK)
    lead_sum = ("Defence Minister Israel Katz warns a new Gaza operation is "
                "coming — one that could displace a million Palestinians, "
                "aid agencies fear, as the ceasefire frays.")
    lines = wrap(d, lead_sum, SANS(21), 560)
    text_block(d, lx + 20, ly + 112, lines, SANS(21), (52, 48, 42), 27)
    draw_gaza_scene(d, lx + 620, ly + 14, 320, 182)

    # ---- Row 1: Ukraine + North Korea ----
    y1 = 424
    story_cell(d, 32, y1, 472, 250, "EUROPE  ·  UKRAINE", NAVY,
               "Drones strike deep inside Russia",
               "Ukrainian drones hit a power plant at Nevinnomyssk — and a "
               "fertiliser plant in Stavropol too.",
               draw_ukraine_scene, scene_h=96)
    story_cell(d, 520, y1, 472, 250, "ASIA  ·  NORTH KOREA", RED,
               "Kim vows more nuclear weapons",
               "Kim Jong Un promises an “irreversible” expansion of the "
               "nuclear arsenal and blames American hostility.",
               draw_korea_scene, scene_h=96)

    # ---- Row 2: Hong Kong + Bangladesh + USA ----
    y2 = 688
    story_cell(d, 32, y2, 309, 250, "ASIA  ·  HONG KONG", GOLD,
               "A year after the tower fire",
               "Hong Kong marks a year since the Tai Po tower fire killed "
               "159 people.",
               draw_hk_scene, head_size=26, scene_h=88)
    story_cell(d, 357, y2, 310, 250, "ASIA  ·  BANGLADESH", TEAL,
               "Tear gas at pay protest",
               "A day after a 36% wage rise, workers say it falls short "
               "and march again.",
               draw_bangladesh_scene, head_size=26, scene_h=88)
    story_cell(d, 683, y2, 309, 250, "AMERICAS  ·  USA", SLATE,
               "Storms hit Thanksgiving",
               "Wild weather delays flights and clogs highways as Americans "
               "head home.",
               draw_usa_scene, head_size=26, scene_h=88)

    # ---- Footer ticker ----
    fy = 952
    d.line([32, fy, W - 32, fy], fill=INK, width=2)
    tick = ("ALSO TODAY — UN backs Palestine’s economy  ·  Iraq jails 8 "
            "French IS fighters for life  ·  Thai refinery blast injures 7")
    d.text((32, fy + 8), tick, font=SANS(14), fill=GREY)
    credit = "Drawn from wire reports first published Friday 27 November 2026"
    cw = d.textlength(credit, font=SERIF_I(15))
    d.text((W - 32 - cw, fy + 28), credit, font=SERIF_I(15), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
