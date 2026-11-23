#!/usr/bin/env python3
"""Build the 22 Nov 2026 world-news image: a dense 5x6 grid of 30 stories.

Programmatic Pillow layout, so every headline stays legible. Each card has a
region tag, a short headline and one supporting detail line.
Stories are those reported on 22 Nov 2026 (Reuters/AP and other roundups
checked 23 Nov 2026); stories already used in the 21 Nov entry are not
repeated except where 22 Nov brought a new development (COP31 collapse).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (255, 255, 255)
INK = (17, 24, 39)
MUTED = (75, 85, 99)

REGION_COLORS = {
    "EUROPE": (37, 99, 235),
    "UKRAINE": (202, 138, 4),
    "MIDDLE EAST": (190, 24, 93),
    "ASIA": (5, 150, 105),
    "MARKETS": (124, 58, 237),
    "SPACE": (13, 148, 136),
    "TECH": (2, 132, 199),
    "AFRICA": (217, 119, 6),
    "AMERICAS": (220, 38, 38),
    "CLIMATE": (22, 163, 74),
    "WORLD": (71, 85, 105),
    "HEALTH": (219, 39, 119),
    "SPORTS": (15, 118, 110),
}

STORIES = [
    ("CLIMATE", "COP31 collapses in Antalya", "No deal at all; EU objects to a text with no fossil-fuel mention"),
    ("MIDDLE EAST", "Iran strikes US bases in Bahrain", "Missiles and drones; civilian facility hit, two people injured"),
    ("MIDDLE EAST", "Iran hits oil tankers near Hormuz", "At least three tankers struck or damaged, shipping at risk"),
    ("UKRAINE", "Russian missile hits Kryvyi Rih", "A 7-year-old boy and a 20-year-old woman killed; 60 wounded"),
    ("UKRAINE", "Russian cargo ship burns in the Baltic", "Fire after a suspected Ukrainian drone strike"),
    ("AMERICAS", "Mexico captures 'El Chapo Isidro'", "11 killed in Sinaloa raid, including four soldiers"),
    ("AMERICAS", "Peru hit by a 6.7 earthquake", "Near Junin: 1 dead, 16 injured, 853 people displaced"),
    ("ASIA", "Fire at an Indonesian candy factory", "3 workers killed in Cikande; 36 still missing"),
    ("EUROPE", "EU and Indonesia sign trade deal", "Tariffs scrapped on up to 98.5% of goods after ~10 years"),
    ("AMERICAS", "Democrats win a historic midterm", "AP: at least 258 House seats, strongest result in decades"),
    ("AMERICAS", "Trump vows a 10% credit-card cap", "Says he will work with Democrats on the rate cap"),
    ("TECH", "Amazon nears a $7.5bn Decart deal", "Israeli AI startup buy to boost Trainium chips"),
    ("TECH", "Trump confirms an FBI database breach", "NCIC hit: fingerprints, wanted and missing-person records"),
    ("TECH", "IBM unveils a 520-qubit Nighthawk r3", "Targets real workloads, not breaking RSA"),
    ("SPORTS", "Verstappen wins the Las Vegas GP", "Third win in four years; Norris 2nd, Piastri 3rd by 0.639s"),
    ("ASIA", "South Korea minister quits over AI cheating", "Education minister resigns in exam-cheating scandal"),
    ("EUROPE", "Italian jeweller Paolo Bulgari dies", "Dies aged 89"),
    ("MIDDLE EAST", "Houthis strike after Saudi operation", "Retaliation in Yemen after a coalition raid in Hodeida"),
    ("MIDDLE EAST", "Israeli strikes in Gaza go on", "Drone strike kills three in Gaza City despite ceasefire"),
    ("ASIA", "China-Japan ties sour over Taiwan", "Row deepens over Taiwan and critical minerals"),
    ("AMERICAS", "Arrests at Seattle airport", "Immigration officers detain travellers; a flight delayed"),
    ("AMERICAS", "Storm kills at least three in Brazil", "Severe storm hits the south"),
    ("WORLD", "Ukraine peace talks resume in Abu Dhabi", "Prisoner exchange agreed; no comprehensive settlement yet"),
    ("SPORTS", "F1 presses on to Qatar and Abu Dhabi", "Finale goes ahead despite rising Middle East tensions"),
    ("AMERICAS", "Republicans debate the midterm loss", "Party asks why it lost, and whether Trump is to blame"),
    ("WORLD", "Hunt for a formula to keep AI in check", "Researchers seek maths to stop an AI apocalypse"),
    ("ASIA", "China easier to visit, harder to leave", "Visitors report tougher exits despite easier entry"),
    ("MIDDLE EAST", "Settler arson attacks in West Bank", "Condemned by Israel's opposition leader"),
    ("UKRAINE", "Kyiv restaurants brace for a hard winter", "War pressures mount as the cold sets in"),
    ("EUROPE", "UK public turns against Brexit", "Polls indicate opinion shifting away from Brexit"),
]

def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

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

def main():
    assert len(STORIES) == 30, len(STORIES)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # Header
    d.rectangle([0, 0, W, 88], fill=(15, 23, 42))
    d.text((16, 12), "THE WORLD IN ONE PICTURE", font=font(30, True), fill=(255, 255, 255))
    d.text((16, 52), "SUNDAY, 22 NOVEMBER 2026  •  30 STORIES  •  9 SECTIONS", font=font(17), fill=(191, 219, 254))
    d.text((W - 16, 52), "make.fun", font=font(17, True), fill=(147, 197, 253), anchor="ra")
    # Grid: 5 cols x 6 rows
    margin, gap = 12, 8
    cols, rows = 5, 6
    cw = (W - 2 * margin - (cols - 1) * gap) // cols
    ch = (H - 88 - 28 - margin - (rows - 1) * gap) // rows
    top = 88 + 10
    for i, (region, head, detail) in enumerate(STORIES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = top + r * (ch + gap)
        color = REGION_COLORS[region]
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=8, fill=(248, 250, 252), outline=(226, 232, 240))
        d.rounded_rectangle([x, y, x + cw, y + 5], radius=3, fill=color)
        d.text((x + 8, y + 11), region, font=font(10, True), fill=color)
        d.text((x + cw - 8, y + 11), f"{i + 1:02d}", font=font(10, True), fill=color, anchor="ra")
        d.line([(x + 8, y + 26), (x + cw - 8, y + 26)], fill=(226, 232, 240))
        lines = wrap(d, head, font(14, True), cw - 16)[:3]
        ly = y + 30
        for ln in lines:
            d.text((x + 8, ly), ln, font=font(14, True), fill=INK)
            ly += 18
        dlines = wrap(d, detail, font(11), cw - 16)[:2]
        for ln in dlines:
            d.text((x + 8, ly + 2), ln, font=font(11), fill=MUTED)
            ly += 14
    d.text((16, H - 22), "Sources: Reuters, AP, AFP, Al Jazeera  •  Headlines as reported on 22 Nov 2026", font=font(11), fill=MUTED)
    img.save("/home/hatch/workspace/makefun-news-20261122/entry.png", "PNG")
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
