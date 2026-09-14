#!/usr/bin/env python3
"""
Surah Al-Muzzammil (73) — Tafseer Presentation
Perspective: A Da'ie (Caller to Islam)
Design: Tarbiyyah aesthetic — deep green, gold accent, parchment surface
Data source: Quran Wiki verified corpus (Al Quran Cloud API + Quran.com API)
Tafsir: Ibn Kathir (Abridged) + Tafsir Muyassar
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import nsmap
from pptx.oxml import parse_xml
import json, re, html
from pathlib import Path

# ── Design Tokens ──
C_PRIMARY     = RGBColor(0x1B, 0x4D, 0x3E)   # Deep green
C_PRIMARY_DK  = RGBColor(0x16, 0x40, 0x38)   # Darker green
C_SECONDARY   = RGBColor(0x6B, 0x90, 0x80)   # Sage
C_ACCENT      = RGBColor(0xC9, 0xA8, 0x57)   # Gold
C_SURFACE     = RGBColor(0xFA, 0xF6, 0xF0)   # Parchment
C_SURFACE_R   = RGBColor(0xED, 0xE5, 0xD8)   # Raised parchment
C_BORDER      = RGBColor(0xD9, 0xCF, 0xC2)   # Border
C_TEXT        = RGBColor(0x1C, 0x19, 0x17)   # Near-black
C_TEXT_MUTED  = RGBColor(0x57, 0x53, 0x4E)   # Muted
C_WHITE       = RGBColor(0xFF, 0xFF, 0xFF)

W = Inches(10.0)
H = Inches(5.625)

# ── Load Quran Wiki Data ──
QURAN = Path("/root/tarbiyyah/quran-wiki")

# Arabic
verses_ar = {}
for f in sorted((QURAN / "raw/arabic").glob("073-*.md")):
    _, ayah_str = f.stem.split("-")
    ayah_num = int(ayah_str)
    text = f.read_text(encoding="utf-8")
    m = re.search(r'## Arabic Text \(Quran\.com.*?```text\n(.*?)\n```', text, re.DOTALL)
    if m:
        verses_ar[ayah_num] = m.group(1).strip()
    else:
        m2 = re.search(r'```text\n(.*?)\n```', text, re.DOTALL)
        verses_ar[ayah_num] = m2.group(1).strip() if m2 else ""

# Translations
verses_trans = {}
for f in sorted((QURAN / "raw/translations/surah_073").glob("ayah_*.json")):
    with open(f) as fh:
        d = json.load(fh)
    ayah_num = int(d["ayah"])
    trans = {}
    for t in d.get("translations", []):
        key = t.get("edition", t.get("translator", "unknown"))
        trans[key] = t["text"]
    verses_trans[ayah_num] = trans

# Tafsir Ibn Kathir (cleaned)
tafsirs = {}
with open(QURAN / "raw/tafsir/073.jsonl") as fh:
    for line in fh:
        try:
            d = json.loads(line)
        except:
            continue
        ayah = d.get("ayah", d.get("verse_id"))
        for t in d.get("tafsirs", []):
            if "Ibn Kathir" in t.get("name", ""):
                text = re.sub(r'<[^>]+>', ' ', t.get("text", ""))
                text = html.unescape(text)
                text = re.sub(r'\s+', ' ', text).strip()
                tafsirs[ayah] = text

# ── Helpers ──
def add_top_rule(slide):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), W, Inches(0.10))
    shape.fill.solid()
    shape.fill.fore_color.rgb = C_PRIMARY
    shape.line.fill.background()

def add_footer(slide, text="Quran Wiki — Surah Al-Muzzammil (73) | Tarbiyyah"):
    tx = slide.shapes.add_textbox(Inches(0.4), H - Inches(0.40), W - Inches(0.8), Inches(0.30))
    p = tx.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(9)
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.RIGHT

def add_arabic_box(slide, arabic_text, y_inches=0.55, box_h=Inches(0.75)):
    # Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(y_inches), W - Inches(0.8), box_h)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_SURFACE_R
    bg.line.fill.background()
    # Left gold border
    lb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(y_inches), Inches(0.04), box_h)
    lb.fill.solid()
    lb.fill.fore_color.rgb = C_ACCENT
    lb.line.fill.background()
    # Right gold border
    rb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, W - Inches(0.44), Inches(y_inches), Inches(0.04), box_h)
    rb.fill.solid()
    rb.fill.fore_color.rgb = C_ACCENT
    rb.line.fill.background()
    # Text
    tx = slide.shapes.add_textbox(Inches(0.6), Inches(y_inches), W - Inches(1.2), box_h)
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = arabic_text
    p.font.size = Pt(20)
    p.font.color.rgb = C_PRIMARY
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Times New Roman"  # Fallback; RTL handled by PPT
    return y_inches + box_h.inches + 0.05

def add_translation(slide, text, y_inches):
    tx = slide.shapes.add_textbox(Inches(0.6), Inches(y_inches), W - Inches(1.2), Inches(0.40))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(13)
    p.font.italic = True
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER
    return y_inches + 0.42

def add_tafsir_heading(slide, heading, y_inches):
    tx = slide.shapes.add_textbox(Inches(0.4), Inches(y_inches), W - Inches(0.8), Inches(0.30))
    p = tx.text_frame.paragraphs[0]
    p.text = heading
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p.font.name = "Georgia"
    return y_inches + 0.30

def add_bullet(slide, text, y_inches, h=Inches(0.50), color=C_TEXT):
    tx = slide.shapes.add_textbox(Inches(0.5), Inches(y_inches), W - Inches(1.0), h)
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• " + text
    p.font.size = Pt(12)
    p.font.color.rgb = color
    p.space_after = Pt(4)
    return y_inches + h.inches + 0.02

def add_slide_title(slide, title, subtitle=None):
    add_top_rule(slide)
    tx = slide.shapes.add_textbox(Inches(0.4), Inches(0.25), W - Inches(0.8), Inches(0.45))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p.font.name = "Georgia"
    # Gold underline
    ul = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.75), Inches(1.4), Inches(0.04))
    ul.fill.solid()
    ul.fill.fore_color.rgb = C_ACCENT
    ul.line.fill.background()
    if subtitle:
        stx = slide.shapes.add_textbox(Inches(0.4), Inches(0.85), W - Inches(0.8), Inches(0.25))
        sp = stx.text_frame.paragraphs[0]
        sp.text = subtitle
        sp.font.size = Pt(12)
        sp.font.color.rgb = C_TEXT_MUTED
        sp.font.italic = True
    return 1.0

# ── Presentation ──
prs = Presentation()
prs.slide_width = W
prs.slide_height = H
prs.core_properties.author = "Tarbiyyah — Quran Wiki Research"
prs.core_properties.title = "Surah Al-Muzzammil (73) — Tafseer for the Da'ie"
prs.core_properties.subject = "Islamic Scholarly Presentation"

blank_layout = prs.slide_layouts[6]  # Blank

# ── SLIDE 1: Title ──
s1 = prs.slides.add_slide(blank_layout)
s1.background.fill.solid()
s1.background.fill.fore_color.rgb = C_PRIMARY
# Gold bottom bar
bb = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), H - Inches(0.08), W, Inches(0.08))
bb.fill.solid()
bb.fill.fore_color.rgb = C_ACCENT
bb.line.fill.background()
# Title
tx1 = s1.shapes.add_textbox(Inches(0.5), Inches(1.2), W - Inches(1.0), Inches(0.9))
p = tx1.text_frame.paragraphs[0]
p.text = "Surah Al-Muzzammil"
p.font.size = Pt(40)
p.font.bold = True
p.font.color.rgb = C_WHITE
p.font.name = "Georgia"
p.alignment = PP_ALIGN.CENTER
# Arabic subtitle
tx2 = s1.shapes.add_textbox(Inches(0.5), Inches(2.1), W - Inches(1.0), Inches(0.5))
p2 = tx2.text_frame.paragraphs[0]
p2.text = "المزمل — The Enwrapped One"
p2.font.size = Pt(24)
p2.font.color.rgb = C_ACCENT
p2.alignment = PP_ALIGN.CENTER
# Subtitle
tx3 = s1.shapes.add_textbox(Inches(0.5), Inches(2.8), W - Inches(1.0), Inches(0.4))
p3 = tx3.text_frame.paragraphs[0]
p3.text = "Tafseer from the Perspective of a Da'ie"
p3.font.size = Pt(18)
p3.font.italic = True
p3.font.color.rgb = C_SURFACE
p3.alignment = PP_ALIGN.CENTER
# Meta
tx4 = s1.shapes.add_textbox(Inches(0.5), Inches(3.5), W - Inches(1.0), Inches(0.3))
p4 = tx4.text_frame.paragraphs[0]
p4.text = "Meccan Surah | 20 Verses | Juz 29 | Tafsir: Ibn Kathir & Muyassar"
p4.font.size = Pt(13)
p4.font.color.rgb = C_SECONDARY
p4.alignment = PP_ALIGN.CENTER

# ── SLIDE 2: Why This Surah Matters to a Da'ie ──
s2 = prs.slides.add_slide(blank_layout)
s2.background.fill.solid()
s2.background.fill.fore_color.rgb = C_SURFACE
add_slide_title(s2, "Why This Surah Matters to a Da'ie", "Spiritual foundation for the caller to Islam")
y = 1.0
y = add_bullet(s2, "It was revealed in the early Makkan period — the era of da'wah under persecution, exactly the context many da'ies face today.", y)
y = add_bullet(s2, "It contains the divine command for night prayer (Tahajjud) — the spiritual engine that sustains prophetic stamina.", y)
y = add_bullet(s2, "It teaches how to handle rejection with patience (Sabr) and gracious avoidance (Hijr Jamil) — essential skills for every caller.", y)
y = add_bullet(s2, "It warns with the parable of Pharaoh — a universal case study in what happens when a society rejects its messenger.", y)
y = add_bullet(s2, "It ends with human free will: 'Whoever wills may take a path to his Lord' — the very invitation every da'ie extends.", y)
add_footer(s2)

# ── SLIDE 3: Introduction ──
s3 = prs.slides.add_slide(blank_layout)
s3.background.fill.solid()
s3.background.fill.fore_color.rgb = C_SURFACE
add_slide_title(s3, "Introduction to Surah Al-Muzzammil", "Structure, context, and themes")
y = 1.0
y = add_bullet(s3, "Revealed in Makkah during the first phase of Prophethood — before the Hijrah, when opposition was intensifying.", y)
y = add_bullet(s3, "The first 19 verses contain two major sections:", y)
y = add_bullet(s3, "    (1) Spiritual Preparation (verses 1-9): Night prayer, Quranic recitation, and exclusive devotion", y, color=C_TEXT_MUTED)
y = add_bullet(s3, "    (2) Prophetic Conduct & Warning (verses 10-19): Patience, divine justice, and the Day of Judgment", y, color=C_TEXT_MUTED)
y = add_bullet(s3, "Verse 20 (not covered here) abrogates the obligation of half-night prayer and mentions charity — a transition to Madinan legislation.", y)
y = add_bullet(s3, "Sources: Tafsir Ibn Kathir (Abridged) & Tafsir Muyassar — Quran Wiki verified corpus", y, color=C_TEXT_MUTED)
add_footer(s3)

# ── SLIDE 4: Verse 1-2 — The Command to Rise ──
s4 = prs.slides.add_slide(blank_layout)
s4.background.fill.solid()
s4.background.fill.fore_color.rgb = C_SURFACE
add_top_rule(s4)
# Verse badge
vb = s4.shapes.add_textbox(Inches(0.4), Inches(0.18), Inches(1.2), Inches(0.30))
vp = vb.text_frame.paragraphs[0]
vp.text = "73:1-2"
vp.font.size = Pt(16)
vp.font.bold = True
vp.font.color.rgb = C_ACCENT
vp.font.name = "Georgia"
ul = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.50), Inches(1.2), Inches(0.03))
ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
# Arabic
y = add_arabic_box(s4, verses_ar.get(1, "") + " ۝ " + verses_ar.get(2, ""), 0.55)
# Translation
y = add_translation(s4, verses_trans.get(1, {}).get("en.pickthall", "") + " " + verses_trans.get(2, {}).get("en.pickthall", ""), y)
# Tafsir
y = add_tafsir_heading(s4, "Tafsir Ibn Kathir — The Command to Stand at Night", y)
y = add_bullet(s4, '"Al-Muzzammil" — one wrapped in garments, asleep. Allah commands the Prophet to cease rest and stand in prayer.', y)
y = add_bullet(s4, 'This command was initially obligatory for the Prophet alone (17:79), establishing Tahajjud as a foundational spiritual practice.', y)
y = add_bullet(s4, 'The command extends to believers: "Their sides forsake their beds, to invoke their Lord in fear and hope" (32:16).', y)
add_footer(s4)

# ── SLIDE 5: Verse 3-4 — Duration & Tartil ──
s5 = prs.slides.add_slide(blank_layout)
s5.background.fill.solid()
s5.background.fill.fore_color.rgb = C_SURFACE
add_top_rule(s5)
vb = s5.shapes.add_textbox(Inches(0.4), Inches(0.18), Inches(1.2), Inches(0.30))
vp = vb.text_frame.paragraphs[0]
vp.text = "73:3-4"
vp.font.size = Pt(16); vp.font.bold = True; vp.font.color.rgb = C_ACCENT; vp.font.name = "Georgia"
ul = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.50), Inches(1.2), Inches(0.03))
ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
y = add_arabic_box(s5, verses_ar.get(3, "") + " ۝ " + verses_ar.get(4, ""), 0.55)
y = add_translation(s5, verses_trans.get(3, {}).get("en.pickthall", "") + " — " + verses_trans.get(4, {}).get("en.pickthall", ""), y)
y = add_tafsir_heading(s5, "Divine Flexibility & The Art of Tartil", y)
y = add_bullet(s5, "The prescribed duration: half the night, or slightly less (reaching one-third), or slightly more (reaching two-thirds).", y)
y = add_bullet(s5, '"No hardship on you concerning that slight increase or decrease" — ease within the command.', y)
y = add_bullet(s5, "Tartil (ترتيل): reciting slowly, clearly, and with contemplation. A'ishah reported the Prophet recited with measured, distinct pronunciation.", y)
y = add_bullet(s5, "The purpose: understanding, reflection, and heartfelt connection — not mere mechanical reading.", y)
add_footer(s5)

# ── SLIDE 6: Verse 5 — The Heavy Word ──
s6 = prs.slides.add_slide(blank_layout)
s6.background.fill.solid()
s6.background.fill.fore_color.rgb = C_SURFACE
add_top_rule(s6)
vb = s6.shapes.add_textbox(Inches(0.4), Inches(0.18), Inches(1.2), Inches(0.30))
vp = vb.text_frame.paragraphs[0]
vp.text = "73:5"
vp.font.size = Pt(16); vp.font.bold = True; vp.font.color.rgb = C_ACCENT; vp.font.name = "Georgia"
ul = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.50), Inches(1.2), Inches(0.03))
ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
y = add_arabic_box(s6, verses_ar.get(5, ""), 0.55)
y = add_translation(s6, verses_trans.get(5, {}).get("en.pickthall", ""), y)
y = add_tafsir_heading(s6, "Tafsir Muyassar — The Weight of Revelation", y)
y = add_bullet(s6, '"Qawlan thaqilan" — a heavy, weighty word: the Quran containing commands, prohibitions, and divine legislation.', y)
y = add_bullet(s6, "The revelation is 'heavy' because it demands commitment, transforms character, and confronts falsehood.", y)
y = add_bullet(s6, "This weightiness requires spiritual preparation — hence the preceding command to stand at night in prayer.", y)
y = add_bullet(s6, "For the da'ie: the message you carry is not light. It requires your own soul to be prepared before you can prepare others.", y)
add_footer(s6)

# ── SLIDE 7: Verse 6 — The Power of Night Prayer ──
s7 = prs.slides.add_slide(blank_layout)
s7.background.fill.solid()
s7.background.fill.fore_color.rgb = C_SURFACE
add_top_rule(s7)
vb = s7.shapes.add_textbox(Inches(0.4), Inches(0.18), Inches(1.2), Inches(0.30))
vp = vb.text_frame.paragraphs[0]
vp.text = "73:6"
vp.font.size = Pt(16); vp.font.bold = True; vp.font.color.rgb = C_ACCENT; vp.font.name = "Georgia"
ul = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.50), Inches(1.2), Inches(0.03))
ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
y = add_arabic_box(s7, verses_ar.get(6, ""), 0.55)
y = add_translation(s7, verses_trans.get(6, {}).get("en.pickthall", ""), y)
y = add_tafsir_heading(s7, "Tafsir Muyassar — Why the Night is Superior", y)
y = add_bullet(s7, "Night worship has stronger impact on the heart because worldly distractions are absent.", y)
y = add_bullet(s7, '"Aqwamu qilan" — speech is more upright and accurate because the heart is free from daytime preoccupations.', y)
y = add_bullet(s7, "The stillness of night creates the optimal psychological and spiritual conditions for deep connection with Allah.", y)
y = add_bullet(s7, "For the da'ie: your night prayer is your secret weapon. It is where you recharge, gain clarity, and receive fortitude for the day's challenges.", y)
add_footer(s7)

# ── SLIDE 8: Verses 7-9 — Day, Night, and Total Devotion ──
s8 = prs.slides.add_slide(blank_layout)
s8.background.fill.solid()
s8.background.fill.fore_color.rgb = C_SURFACE
add_top_rule(s8)
vb = s8.shapes.add_textbox(Inches(0.4), Inches(0.18), Inches(1.2), Inches(0.30))
vp = vb.text_frame.paragraphs[0]
vp.text = "73:7-9"
vp.font.size = Pt(16); vp.font.bold = True; vp.font.color.rgb = C_ACCENT; vp.font.name = "Georgia"
ul = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.50), Inches(1.2), Inches(0.03))
ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
y = add_arabic_box(s8, verses_ar.get(7, "") + " ۝ " + verses_ar.get(8, "") + " ۝ " + verses_ar.get(9, ""), 0.55, box_h=Inches(0.90))
y = add_translation(s8, verses_trans.get(7, {}).get("en.pickthall", "") + " " + verses_trans.get(8, {}).get("en.pickthall", "") + " " + verses_trans.get(9, {}).get("en.pickthall", ""), y)
y = add_tafsir_heading(s8, "Balance of Day & Night | Total Devotion (Tabattul)", y)
y = add_bullet(s8, "Verse 7: Daytime is for worldly duties and propagation. Night is reserved for exclusive communion with Allah.", y)
y = add_bullet(s8, "Verse 8: 'Tabattul' — total, exclusive devotion. Cut all attachments and dedicate worship solely to Allah.", y)
y = add_bullet(s8, "Verse 9: Tawhid declaration — Allah is Lord of East and West, the sole deity. Take Him as Wakil (Disposer of Affairs).", y)
add_footer(s8)

# ── SLIDE 9: Verses 10-11 — Sabr & Hijr Jamil ──
s9 = prs.slides.add_slide(blank_layout)
s9.background.fill.solid()
s9.background.fill.fore_color.rgb = C_SURFACE
add_top_rule(s9)
vb = s9.shapes.add_textbox(Inches(0.4), Inches(0.18), Inches(1.2), Inches(0.30))
vp = vb.text_frame.paragraphs[0]
vp.text = "73:10-11"
vp.font.size = Pt(16); vp.font.bold = True; vp.font.color.rgb = C_ACCENT; vp.font.name = "Georgia"
ul = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.50), Inches(1.2), Inches(0.03))
ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
y = add_arabic_box(s9, verses_ar.get(10, "") + " ۝ " + verses_ar.get(11, ""), 0.55)
y = add_translation(s9, verses_trans.get(10, {}).get("en.pickthall", "") + " " + verses_trans.get(11, {}).get("en.pickthall", ""), y)
y = add_tafsir_heading(s9, "Prophetic Conduct: Sabr & Hijr Jamil", y)
y = add_bullet(s9, '"Sabr" — patient endurance of mockery, slander, and rejection from the disbelievers.', y)
y = add_bullet(s9, '"Hijran jamilan" — gracious avoidance: do not retaliate, do not seek revenge. Maintain dignity and noble character.', y)
y = add_bullet(s9, '"Watharnee" — leave the rejectors to Me. The Prophet\'s task is delivery (balagh); Allah handles reckoning.', y)
y = add_bullet(s9, "For the da'ie: you will face insults, mockery, and rejection. Your response is patience and dignified distance — never hatred, never retaliation.", y)
add_footer(s9)

# ── SLIDE 10: Verses 12-14 — Warning of the Hereafter ──
s10 = prs.slides.add_slide(blank_layout)
s10.background.fill.solid()
s10.background.fill.fore_color.rgb = C_SURFACE
add_top_rule(s10)
vb = s10.shapes.add_textbox(Inches(0.4), Inches(0.18), Inches(1.2), Inches(0.30))
vp = vb.text_frame.paragraphs[0]
vp.text = "73:12-14"
vp.font.size = Pt(16); vp.font.bold = True; vp.font.color.rgb = C_ACCENT; vp.font.name = "Georgia"
ul = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.50), Inches(1.2), Inches(0.03))
ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
y = add_arabic_box(s10, verses_ar.get(12, "") + " ۝ " + verses_ar.get(13, "") + " ۝ " + verses_ar.get(14, ""), 0.55, box_h=Inches(0.90))
y = add_translation(s10, verses_trans.get(12, {}).get("en.pickthall", "") + " " + verses_trans.get(13, {}).get("en.pickthall", "") + " " + verses_trans.get(14, {}).get("en.pickthall", ""), y)
y = add_tafsir_heading(s10, "The Four Punishments of the Rejectors", y)
y = add_bullet(s10, "Ankal (أنكال) — Heavy fetters and chains binding the disbelievers in Hellfire.", y)
y = add_bullet(s10, "Jahim (جحيم) — A blazing, all-consuming fire of punishment.", y)
y = add_bullet(s10, "Ta'am dhu ghussah — Food that chokes, stuck in the throat, neither entering nor exiting.", y)
y = add_bullet(s10, "Adhabun aleem — Painful torment on the Day when earth and mountains convulse, and mountains become like flowing sand.", y)
add_footer(s10)

# ── SLIDE 11: Verses 15-16 — The Lesson from Pharaoh ──
s11 = prs.slides.add_slide(blank_layout)
s11.background.fill.solid()
s11.background.fill.fore_color.rgb = C_SURFACE
add_top_rule(s11)
vb = s11.shapes.add_textbox(Inches(0.4), Inches(0.18), Inches(1.2), Inches(0.30))
vp = vb.text_frame.paragraphs[0]
vp.text = "73:15-16"
vp.font.size = Pt(16); vp.font.bold = True; vp.font.color.rgb = C_ACCENT; vp.font.name = "Georgia"
ul = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.50), Inches(1.2), Inches(0.03))
ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
y = add_arabic_box(s11, verses_ar.get(15, "") + " ۝ " + verses_ar.get(16, ""), 0.55)
y = add_translation(s11, verses_trans.get(15, {}).get("en.pickthall", "") + " " + verses_trans.get(16, {}).get("en.pickthall", ""), y)
y = add_tafsir_heading(s11, "The Parable of Pharaoh — A Stern Warning", y)
y = add_bullet(s11, "The Prophet Muhammad is a 'shahid' (witness) over his Ummah — his testimony will be presented on Judgment Day.", y)
y = add_bullet(s11, "Pharaoh was sent Musa (AS) as a messenger; he denied, rebelled, and was seized by Allah with crushing punishment.", y)
y = add_bullet(s11, '"Akhdhan wabeelan" — a severe, ruinous seizure. The parallel is explicit: reject the messenger, face the consequence.', y)
y = add_bullet(s11, "For the da'ie: when people reject your call, remember Pharaoh. The message is true; the consequence of rejection is real.", y)
add_footer(s11)

# ── SLIDE 12: Verses 17-18 — The Day of Resurrection ──
s12 = prs.slides.add_slide(blank_layout)
s12.background.fill.solid()
s12.background.fill.fore_color.rgb = C_SURFACE
add_top_rule(s12)
vb = s12.shapes.add_textbox(Inches(0.4), Inches(0.18), Inches(1.2), Inches(0.30))
vp = vb.text_frame.paragraphs[0]
vp.text = "73:17-18"
vp.font.size = Pt(16); vp.font.bold = True; vp.font.color.rgb = C_ACCENT; vp.font.name = "Georgia"
ul = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.50), Inches(1.2), Inches(0.03))
ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
y = add_arabic_box(s12, verses_ar.get(17, "") + " ۝ " + verses_ar.get(18, ""), 0.55)
y = add_translation(s12, verses_trans.get(17, {}).get("en.pickthall", "") + " " + verses_trans.get(18, {}).get("en.pickthall", ""), y)
y = add_tafsir_heading(s12, "Tafsir Muyassar — The Unimaginable Terror", y)
y = add_bullet(s12, "A Day so terrifying that children will turn white-haired from sheer horror and dread.", y)
y = add_bullet(s12, "The sky itself will be rent asunder — the cosmic order will collapse before the power of Allah.", y)
y = add_bullet(s12, '"Kana wa\'duhu maf\'oolan" — His promise is certainly fulfilled. The resurrection is not conjecture; it is guaranteed reality.', y)
y = add_bullet(s12, "The rhetorical question: if you deny Allah now, what defense will you have on that Day?", y)
add_footer(s12)

# ── SLIDE 13: Verse 19 — A Reminder & Free Will ──
s13 = prs.slides.add_slide(blank_layout)
s13.background.fill.solid()
s13.background.fill.fore_color.rgb = C_SURFACE
add_top_rule(s13)
vb = s13.shapes.add_textbox(Inches(0.4), Inches(0.18), Inches(1.2), Inches(0.30))
vp = vb.text_frame.paragraphs[0]
vp.text = "73:19"
vp.font.size = Pt(16); vp.font.bold = True; vp.font.color.rgb = C_ACCENT; vp.font.name = "Georgia"
ul = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.50), Inches(1.2), Inches(0.03))
ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
y = add_arabic_box(s13, verses_ar.get(19, ""), 0.55)
y = add_translation(s13, verses_trans.get(19, {}).get("en.pickthall", ""), y)
y = add_tafsir_heading(s13, "Tafsir Ibn Kathir — Admonition & Divine Will", y)
y = add_bullet(s13, '"Hadhihi tathkirah" — This surah is an admonition, a reminder for those of sound understanding.', y)
y = add_bullet(s13, '"Faman shaa attakhadha ila rabbihi sabeelan" — Whoever wills may take a path to his Lord.', y)
y = add_bullet(s13, 'The will is ultimately subject to Allah\'s will: "But you cannot will, unless Allah wills" (76:30).', y)
y = add_bullet(s13, "This verse balances human responsibility with divine sovereignty — a cornerstone of Ahl al-Sunnah theology.", y)
add_footer(s13)

# ── SLIDE 14: Major Divine Orders (Summary) ──
s14 = prs.slides.add_slide(blank_layout)
s14.background.fill.solid()
s14.background.fill.fore_color.rgb = C_SURFACE
add_slide_title(s14, "Major Divine Orders (Verses 1-19)", "The commands every da'ie must internalize")
y = 1.0
orders = [
    ("1-4", "Qiyam al-Lail — Stand in night prayer (Tahajjud) for half the night or near it"),
    ("4", "Tartil — Recite the Quran slowly, distinctly, with contemplation"),
    ("8", "Dhikr & Tabattul — Remember Allah's name with complete, exclusive devotion"),
    ("9", "Tawhid & Tawakkul — Affirm Allah as sole deity; take Him as Wakil"),
    ("10", "Sabr — Exercise patient endurance against mockery and rejection"),
    ("10", "Hijr Jamil — Avoid opponents with gracious, noble conduct"),
    ("11", "Tafweedh — Leave the rejectors to Allah; focus on delivery (balagh)"),
    ("19", "Ikhtiyar — Choose the path to Allah; exercise free will within divine decree")
]
for v, text in orders:
    badge = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(y), Inches(0.35), Inches(0.28))
    badge.fill.solid(); badge.fill.fore_color.rgb = C_PRIMARY; badge.line.fill.background()
    btx = s14.shapes.add_textbox(Inches(0.4), Inches(y), Inches(0.35), Inches(0.28))
    bp = btx.text_frame.paragraphs[0]
    bp.text = v; bp.font.size = Pt(11); bp.font.bold = True; bp.font.color.rgb = C_WHITE
    bp.alignment = PP_ALIGN.CENTER
    tx = s14.shapes.add_textbox(Inches(0.85), Inches(y), W - Inches(1.3), Inches(0.28))
    tp = tx.text_frame.paragraphs[0]
    tp.text = text; tp.font.size = Pt(12); tp.font.color.rgb = C_TEXT
    tp.alignment = PP_ALIGN.LEFT
    y += 0.34
add_footer(s14)

# ── SLIDE 15: Major Lessons for the Da'ie ──
s15 = prs.slides.add_slide(blank_layout)
s15.background.fill.solid()
s15.background.fill.fore_color.rgb = C_SURFACE
add_slide_title(s15, "Major Lessons for the Da'ie", "Practical takeaways from Surah Al-Muzzammil")
y = 1.0
lessons = [
    "Spiritual preparation precedes prophetic duty — night prayer is the foundation of revelation-bearing.",
    "The Quran demands weighty commitment; it is not light reading but life-transforming legislation.",
    "Night prayer creates the optimal conditions for deep reflection and sincere supplication.",
    "The prophetic model requires balance: active daytime engagement + deep nighttime devotion.",
    "Patience and gracious avoidance are superior to retaliation when facing opposition.",
    "Divine justice is certain; worldly respite for rejectors is temporary and deceptive.",
    "The fate of Pharaoh serves as a universal warning to all who reject Allah's messengers.",
    "Human will operates within divine decree — we choose, but Allah ultimately enables and guides."
]
for i, l in enumerate(lessons):
    oval = s15.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.45), Inches(y + 0.04), Inches(0.18), Inches(0.18))
    oval.fill.solid(); oval.fill.fore_color.rgb = C_ACCENT; oval.line.fill.background()
    ntx = s15.shapes.add_textbox(Inches(0.45), Inches(y + 0.04), Inches(0.18), Inches(0.18))
    np = ntx.text_frame.paragraphs[0]
    np.text = str(i + 1); np.font.size = Pt(10); np.font.bold = True; np.font.color.rgb = C_WHITE
    np.alignment = PP_ALIGN.CENTER
    tx = s15.shapes.add_textbox(Inches(0.75), Inches(y), W - Inches(1.2), Inches(0.50))
    tp = tx.text_frame; tp.word_wrap = True
    tp.paragraphs[0].text = l
    tp.paragraphs[0].font.size = Pt(12)
    tp.paragraphs[0].font.color.rgb = C_TEXT
    y += 0.52
add_footer(s15)

# ── SLIDE 16: Conclusion ──
s16 = prs.slides.add_slide(blank_layout)
s16.background.fill.solid()
s16.background.fill.fore_color.rgb = C_PRIMARY
bb = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), H - Inches(0.08), W, Inches(0.08))
bb.fill.solid(); bb.fill.fore_color.rgb = C_ACCENT; bb.line.fill.background()
tx = s16.shapes.add_textbox(Inches(0.5), Inches(0.5), W - Inches(1.0), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "Conclusion"
p.font.size = Pt(32); p.font.bold = True; p.font.color.rgb = C_WHITE; p.font.name = "Georgia"
p.alignment = PP_ALIGN.CENTER
tx2 = s16.shapes.add_textbox(Inches(0.5), Inches(1.3), W - Inches(1.0), Inches(0.5))
p2 = tx2.text_frame.paragraphs[0]
p2.text = "رَبَّنَا تَقَبَّلْ مِنَّا إِنَّكَ أَنْتَ السَّمِيعُ الْعَلِيمُ"
p2.font.size = Pt(22); p2.font.color.rgb = C_ACCENT; p2.alignment = PP_ALIGN.CENTER
tx3 = s16.shapes.add_textbox(Inches(0.5), Inches(1.9), W - Inches(1.0), Inches(0.35))
p3 = tx3.text_frame.paragraphs[0]
p3.text = "Our Lord, accept from us; indeed, You are the All-Hearing, the All-Knowing."
p3.font.size = Pt(14); p3.font.italic = True; p3.font.color.rgb = C_SURFACE; p3.alignment = PP_ALIGN.CENTER
tx4 = s16.shapes.add_textbox(Inches(0.5), Inches(2.6), W - Inches(1.0), Inches(0.9))
p4 = tx4.text_frame; p4.word_wrap = True
p4.paragraphs[0].text = "Surah Al-Muzzammil teaches us that spiritual elevation requires night devotion, patient conduct, unwavering tawhid, and trust in divine justice. The path to Allah is open to whoever wills — may we be among those who choose it."
p4.paragraphs[0].font.size = Pt(14); p4.paragraphs[0].font.color.rgb = C_SURFACE; p4.paragraphs[0].alignment = PP_ALIGN.CENTER
tx5 = s16.shapes.add_textbox(Inches(0.5), Inches(3.8), W - Inches(1.0), Inches(0.3))
p5 = tx5.text_frame.paragraphs[0]
p5.text = "Sources: Quran Wiki (verified against Al Quran Cloud API & Quran.com API) | Tafsir Ibn Kathir (Abridged) | Tafsir Muyassar"
p5.font.size = Pt(10); p5.font.color.rgb = C_SECONDARY; p5.alignment = PP_ALIGN.CENTER

# ── WRITE ──
out_path = "/root/tarbiyyah/quran-wiki/.tools/presentations/surah-muzzammil-73-tafseer-daie.pptx"
prs.save(out_path)
print(f"Presentation saved: {out_path}")
