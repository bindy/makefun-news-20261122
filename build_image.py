#!/usr/bin/env python3
"""Render the 22 Nov 2026 world-news image: 30 stories in a 5x6 grid.

The layout is drawn with Pillow so every headline stays legible. Each card
carries a region tag, a short headline and one supporting detail line. The
stories are the ones reported on 22 Nov 2026 (Reuters/AP and other roundups
checked 23 Nov 2026); stories already used in the 21 Nov entry are not
repeated except where 22 Nov brought a new development (COP31 collapse).
"""
from PIL import Image, ImageDraw, ImageFont

PAGE = (1024, 1024)
PAPER = "#ffffff"
TEXT = "#111827"
FAINT = "#4b5563"
HEADER_H = 88
FOOT_H = 28
MARGIN = 12
GAP = 8
COLS = 5
ROWS = 6
CARD_FILL = "#f8fafc"
CARD_EDGE = "#e2e8f0"

PALETTE = {
    "EUROPE": "#2563eb",
    "UKRAINE": "#ca8a04",
    "MIDDLE EAST": "#be185d",
    "ASIA": "#059669",
    "MARKETS": "#7c3aed",
    "SPACE": "#0d9488",
    "TECH": "#0284c7",
    "AFRICA": "#d97706",
    "AMERICAS": "#dc2626",
    "CLIMATE": "#16a34a",
    "WORLD": "#475569",
    "HEALTH": "#db2777",
    "SPORTS": "#0f766e",
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


def typeface(size, bold=False):
    """Load a DejaVu face at the given size."""
    stem = "DejaVuSans-Bold" if bold else "DejaVuSans"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + stem + ".ttf", size)


def split_lines(canvas, text, face, max_width):
    """Split text into as many lines as fit within max_width."""
    out = []
    current = ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if canvas.textlength(candidate, font=face) <= max_width:
            current = candidate
        elif current:
            out.append(current)
            current = word
        else:
            current = word
    if current:
        out.append(current)
    return out


def draw_card(canvas, number, region, head, detail, x, y, cw, ch):
    """Draw one story card at (x, y) with size cw x ch."""
    color = PALETTE[region]
    canvas.rounded_rectangle((x, y, x + cw, y + ch), radius=8, fill=CARD_FILL, outline=CARD_EDGE)
    canvas.rounded_rectangle((x, y, x + cw, y + 5), radius=3, fill=color)
    canvas.text((x + 8, y + 11), region, font=typeface(10, True), fill=color)
    canvas.text((x + cw - 8, y + 11), "%02d" % number, font=typeface(10, True), fill=color, anchor="ra")
    canvas.line(((x + 8, y + 26), (x + cw - 8, y + 26)), fill=CARD_EDGE)
    head_lines = split_lines(canvas, head, typeface(14, True), cw - 16)[:3]
    text_y = y + 30
    for line in head_lines:
        canvas.text((x + 8, text_y), line, font=typeface(14, True), fill=TEXT)
        text_y += 18
    detail_lines = split_lines(canvas, detail, typeface(11), cw - 16)[:2]
    for line in detail_lines:
        canvas.text((x + 8, text_y + 2), line, font=typeface(11), fill=FAINT)
        text_y += 14


def main():
    assert len(STORIES) == 30
    img = Image.new("RGB", PAGE, PAPER)
    canvas = ImageDraw.Draw(img)
    canvas.rectangle((0, 0, PAGE[0], HEADER_H), fill="#0f172a")
    canvas.text((16, 12), "THE WORLD IN ONE PICTURE", font=typeface(30, True), fill="#ffffff")
    canvas.text((16, 52), "SUNDAY, 22 NOVEMBER 2026  •  30 STORIES  •  9 SECTIONS", font=typeface(17), fill="#bfdbfe")
    canvas.text((PAGE[0] - 16, 52), "make.fun", font=typeface(17, True), fill="#93c5fd", anchor="ra")
    cw = (PAGE[0] - 2 * MARGIN - (COLS - 1) * GAP) // COLS
    ch = (PAGE[1] - HEADER_H - FOOT_H - MARGIN - (ROWS - 1) * GAP) // ROWS
    top = HEADER_H + 10
    for number, (region, head, detail) in enumerate(STORIES, start=1):
        row, col = divmod(number - 1, COLS)
        draw_card(canvas, number, region, head, detail,
                  MARGIN + col * (cw + GAP), top + row * (ch + GAP), cw, ch)
    canvas.text((16, PAGE[1] - 22), "Sources: Reuters, AP, AFP, Al Jazeera  •  Headlines as reported on 22 Nov 2026", font=typeface(11), fill=FAINT)
    out_path = "/home/hatch/workspace/makefun-news-20261122/entry.png"
    img.save(out_path, "PNG")
    print("saved", out_path, img.size)


if __name__ == "__main__":
    main()
