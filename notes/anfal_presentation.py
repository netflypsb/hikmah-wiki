#!/usr/bin/env python3
"""
Surah Al-Anfal (8) Verses 24-37 — Thematic Study Presentation
Design: Deep green primary, gold accent, parchment surface (Tarbiyyah palette)
Source: Quran Wiki raw corpus (/root/tarbiyyah/quran-wiki/)
"""

import json, re, html
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Design Tokens (Tarbiyyah Palette) ──
C_PRIMARY     = RGBColor(0x1B, 0x4D, 0x3E)
C_PRIMARY_DK  = RGBColor(0x10, 0x33, 0x2B)
C_SECONDARY   = RGBColor(0x6B, 0x90, 0x80)
C_ACCENT      = RGBColor(0xC9, 0xA8, 0x57)
C_ACCENT2     = RGBColor(0xB8, 0x96, 0x4A)
C_SURFACE     = RGBColor(0xFA, 0xF6, 0xF0)
C_SURFACE_R   = RGBColor(0xED, 0xE5, 0xD8)
C_TEXT        = RGBColor(0x1C, 0x19, 0x17)
C_TEXT_MUTED  = RGBColor(0x57, 0x53, 0x4E)
C_WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
C_CARD_BG     = RGBColor(0xF5, 0xEF, 0xE3)

# 16:9 dimensions
W = Inches(13.333)
H = Inches(7.5)

FOOTER_TEXT = 'Quran Wiki Corpus | Tarbiyyah Research | Surah Al-Anfal 8:24-37'

# ── Helpers ──

def add_top_rule(slide):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), W, Inches(0.10))
    shape.fill.solid()
    shape.fill.fore_color.rgb = C_PRIMARY
    shape.line.fill.background()

def add_footer(slide, text=FOOTER_TEXT):
    tx = slide.shapes.add_textbox(Inches(0.5), H - Inches(0.45), W - Inches(1.0), Inches(0.30))
    p = tx.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(9)
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.RIGHT

def add_slide_title(slide, title, subtitle=None):
    add_top_rule(slide)
    tx = slide.shapes.add_textbox(Inches(0.6), Inches(0.25), W - Inches(1.2), Inches(0.55))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p.font.name = 'Georgia'
    ul = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.82), Inches(1.6), Inches(0.04))
    ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
    if subtitle:
        stx = slide.shapes.add_textbox(Inches(0.6), Inches(0.92), W - Inches(1.2), Inches(0.28))
        sp = stx.text_frame.paragraphs[0]
        sp.text = subtitle
        sp.font.size = Pt(14)
        sp.font.color.rgb = C_TEXT_MUTED
        sp.font.italic = True
    return 1.15

def add_verse_badge(slide, verse_ref, y=0.18):
    tx = slide.shapes.add_textbox(Inches(0.6), Inches(y), Inches(1.5), Inches(0.30))
    p = tx.text_frame.paragraphs[0]
    p.text = verse_ref
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT
    p.font.name = 'Georgia'
    ul = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(y + 0.32), Inches(1.5), Inches(0.03))
    ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()

def add_arabic_box(slide, arabic_text, y_inches=0.55, box_h=Inches(0.85)):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(y_inches), W - Inches(1.2), box_h)
    bg.fill.solid(); bg.fill.fore_color.rgb = C_SURFACE_R; bg.line.fill.background()
    lb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(y_inches), Inches(0.05), box_h)
    lb.fill.solid(); lb.fill.fore_color.rgb = C_ACCENT; lb.line.fill.background()
    tx = slide.shapes.add_textbox(Inches(0.8), Inches(y_inches), W - Inches(1.6), box_h)
    tf = tx.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = arabic_text
    p.font.size = Pt(22)
    p.font.color.rgb = C_PRIMARY
    p.alignment = PP_ALIGN.CENTER
    return y_inches + box_h.inches + 0.08

def add_translation(slide, text, y_inches, italic=True, size=13):
    tx = slide.shapes.add_textbox(Inches(0.8), Inches(y_inches), W - Inches(1.6), Inches(0.50))
    tf = tx.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.italic = italic
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER
    return y_inches + 0.52

def add_card(slide, x, y, w, h, title, body_lines, accent_color=C_ACCENT, title_color=None):
    if title_color is None:
        title_color = C_PRIMARY
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    card.fill.solid(); card.fill.fore_color.rgb = C_CARD_BG; card.line.fill.background()
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.06), Inches(h))
    bar.fill.solid(); bar.fill.fore_color.rgb = accent_color; bar.line.fill.background()
    # Title
    tx = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.1), Inches(w - 0.3), Inches(0.35))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = title_color
    # Body
    if body_lines:
        bx = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.45), Inches(w - 0.3), Inches(h - 0.55))
        bf = bx.text_frame; bf.word_wrap = True
        for i, line in enumerate(body_lines):
            if i == 0:
                p = bf.paragraphs[0]
            else:
                p = bf.add_paragraph()
            p.text = line
            p.font.size = Pt(11)
            p.font.color.rgb = C_TEXT
            p.space_after = Pt(3)

def add_bullet_list(slide, x, y, w, h, items, size=12, color=C_TEXT):
    tx = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tx.text_frame; tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(6)

# ── Title Slide (Dark) ──
def make_title_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_PRIMARY_DK
    bb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), H - Inches(0.10), W, Inches(0.10))
    bb.fill.solid(); bb.fill.fore_color.rgb = C_ACCENT; bb.line.fill.background()

    # Surah name
    tx1 = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), W - Inches(1.0), Inches(1.0))
    p = tx1.text_frame.paragraphs[0]
    p.text = "Surah Al-Anfal"
    p.font.size = Pt(44); p.font.bold = True; p.font.color.rgb = C_WHITE; p.font.name = 'Georgia'
    p.alignment = PP_ALIGN.CENTER

    # Arabic name
    tx2 = slide.shapes.add_textbox(Inches(0.5), Inches(2.6), W - Inches(1.0), Inches(0.7))
    p2 = tx2.text_frame.paragraphs[0]
    p2.text = "الأنفال — The Spoils of War"
    p2.font.size = Pt(28); p2.font.color.rgb = C_ACCENT; p2.alignment = PP_ALIGN.CENTER

    # Verse range
    tx3 = slide.shapes.add_textbox(Inches(0.5), Inches(3.5), W - Inches(1.0), Inches(0.5))
    p3 = tx3.text_frame.paragraphs[0]
    p3.text = "Verses 24–37: A Thematic Study"
    p3.font.size = Pt(22); p3.font.italic = True; p3.font.color.rgb = C_SURFACE; p3.alignment = PP_ALIGN.CENTER

    # Subtitle
    tx4 = slide.shapes.add_textbox(Inches(0.5), Inches(4.2), W - Inches(1.0), Inches(0.4))
    p4 = tx4.text_frame.paragraphs[0]
    p4.text = "The Call to Faith, Divine Favour, and the Fate of Disbelievers"
    p4.font.size = Pt(16); p4.font.color.rgb = C_SECONDARY; p4.alignment = PP_ALIGN.CENTER

    # Meta
    tx5 = slide.shapes.add_textbox(Inches(0.5), Inches(5.2), W - Inches(1.0), Inches(0.35))
    p5 = tx5.text_frame.paragraphs[0]
    p5.text = "Medinan Surah | 75 Verses | Juz 9-10 | Tafsir: Ibn Kathir & Muyassar"
    p5.font.size = Pt(14); p5.font.color.rgb = C_TEXT_MUTED; p5.alignment = PP_ALIGN.CENTER

    # Sources
    tx6 = slide.shapes.add_textbox(Inches(0.5), Inches(6.0), W - Inches(1.0), Inches(0.3))
    p6 = tx6.text_frame.paragraphs[0]
    p6.text = "Sources: Quran Wiki Corpus (Al Quran Cloud + Quran.com) | 5 Translations | 2 Tafsirs"
    p6.font.size = Pt(11); p6.font.color.rgb = C_TEXT_MUTED; p6.alignment = PP_ALIGN.CENTER

# ── Section Divider Slide (Dark) ──
def make_section_slide(prs, theme_num, theme_title, verse_range):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_PRIMARY
    bb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), H - Inches(0.08), W, Inches(0.08))
    bb.fill.solid(); bb.fill.fore_color.rgb = C_ACCENT; bb.line.fill.background()

    # Theme number
    tx1 = slide.shapes.add_textbox(Inches(0.5), Inches(2.0), W - Inches(1.0), Inches(0.5))
    p = tx1.text_frame.paragraphs[0]
    p.text = f"Theme {theme_num}"
    p.font.size = Pt(20); p.font.color.rgb = C_ACCENT; p.alignment = PP_ALIGN.CENTER
    p.font.name = 'Georgia'

    # Theme title
    tx2 = slide.shapes.add_textbox(Inches(0.5), Inches(2.7), W - Inches(1.0), Inches(1.0))
    p2 = tx2.text_frame.paragraphs[0]
    p2.text = theme_title
    p2.font.size = Pt(36); p2.font.bold = True; p2.font.color.rgb = C_WHITE; p2.font.name = 'Georgia'
    p2.alignment = PP_ALIGN.CENTER

    # Verse range
    tx3 = slide.shapes.add_textbox(Inches(0.5), Inches(4.0), W - Inches(1.0), Inches(0.4))
    p3 = tx3.text_frame.paragraphs[0]
    p3.text = f"Qur'an 8:{verse_range}"
    p3.font.size = Pt(18); p3.font.italic = True; p3.font.color.rgb = C_SURFACE; p3.alignment = PP_ALIGN.CENTER

# ── Verse Slide ──
def make_verse_slide(prs, verse_ref, arabic, translation, tafsir_summary, theme_label):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE

    add_verse_badge(slide, verse_ref)
    y = add_slide_title(slide, f"Verse {verse_ref}", theme_label)

    # Arabic verse
    y = add_arabic_box(slide, arabic, y_inches=y, box_h=Inches(0.80))

    # Translation (Sahih International)
    tx_trans = slide.shapes.add_textbox(Inches(0.8), Inches(y), W - Inches(1.6), Inches(0.7))
    tf = tx_trans.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Sahih International:"
    p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_ACCENT2
    p2 = tf.add_paragraph()
    p2.text = translation
    p2.font.size = Pt(13); p2.font.italic = True; p2.font.color.rgb = C_TEXT_MUTED
    y += 0.85

    # Tafsir card
    if tafsir_summary:
        # Truncate if too long
        if len(tafsir_summary) > 350:
            tafsir_summary = tafsir_summary[:340] + " [...]"
        add_card(slide, 0.6, y, W.inches - 1.2, 2.2,
                 "Tafsir Ibn Kathir (Key Points)", [tafsir_summary],
                 accent_color=C_PRIMARY)

    add_footer(slide)

# ── Lesson Slide ──
def make_lesson_slide(prs, title, lessons, theme_label):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE

    y = add_slide_title(slide, title, theme_label)

    for i, (lesson_title, lesson_body) in enumerate(lessons):
        row_y = y + i * 1.4
        add_card(slide, 0.6, row_y, W.inches - 1.2, 1.25,
                 lesson_title, [lesson_body],
                 accent_color=C_ACCENT)

    add_footer(slide)

# ── Conclusion Slide (Dark) ──
def make_conclusion_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_PRIMARY_DK
    bb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), H - Inches(0.10), W, Inches(0.10))
    bb.fill.solid(); bb.fill.fore_color.rgb = C_ACCENT; bb.line.fill.background()

    tx = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), W - Inches(1.0), Inches(0.6))
    p = tx.text_frame.paragraphs[0]
    p.text = "Key Takeaways"
    p.font.size = Pt(32); p.font.bold = True; p.font.color.rgb = C_WHITE; p.font.name = 'Georgia'
    p.alignment = PP_ALIGN.CENTER

    takeaways = [
        "1. Respond to Allah's call — it gives life to the heart and orders your affairs",
        "2. Fitnah strikes all when evil is tolerated — communal responsibility is real",
        "3. Remember past weakness → gratitude → continued favour",
        "4. Wealth and children are tests, not rewards — the real prize is with Allah",
        "5. Taqwa yields furqan: the ability to distinguish truth from falsehood",
        "6. Allah's plan supersedes every human plot — He is the best of planners",
        "7. The Prophet's presence and istighfar are shields against punishment",
        "8. Wealth spent against truth becomes regret — the wicked will be separated",
    ]

    tx2 = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), W - Inches(2.0), Inches(4.5))
    tf = tx2.text_frame; tf.word_wrap = True
    for i, t in enumerate(takeaways):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = t
        p.font.size = Pt(15); p.font.color.rgb = C_SURFACE; p.space_after = Pt(8)

    # Sources
    tx3 = slide.shapes.add_textbox(Inches(0.5), Inches(6.3), W - Inches(1.0), Inches(0.5))
    p3 = tx3.text_frame.paragraphs[0]
    p3.text = "Sources: Quran Wiki Corpus | Arabic: Al Quran Cloud + Quran.com | Tafsir: Ibn Kathir & Muyassar | 5 Translations"
    p3.font.size = Pt(10); p3.font.color.rgb = C_TEXT_MUTED; p3.alignment = PP_ALIGN.CENTER

# ── MAIN ──
def main():
    # Load research data
    with open('/tmp/anfal_research_data.json', 'r', encoding='utf-8') as f:
        verses = json.load(f)

    # Helper to get tafsir summary (first 300 chars of Ibn Kathir, cleaned)
    def get_tafsir_summary(ayah):
        ik = verses[str(ayah)]["tafsir"]["ibn_kathir"]
        # Clean up: remove extra spaces
        ik = re.sub(r'\s+', ' ', ik).strip()
        return ik

    # Tafsir summaries for key verses (curated for slides)
    tafsir_summaries = {
        24: "Al-Bukhari narrates: Abu Sa'id bin Al-Mu'alla was praying when the Prophet called him. He didn't answer until he finished. The Prophet asked: 'What prevented you from answering me? Has not Allah said: O you who believe! Answer Allah and His Messenger when he calls you to that which will give you life?' The Prophet then taught him the greatest Surah (Al-Fatihah). 'That which gives you life' means that which makes your affairs good — interpreted as Jihad, faith, and obedience.",
        25: "Allah warns of a fitnah (trial) that is not restricted to the wrongdoers alone. When sins are not stopped, the consequences reach everyone. Ibn Kathir cites the battle of Al-Jamal: even those who didn't instigate it were engulfed. Az-Zubayr was asked why he participated — he cited this verse. Communal responsibility: silence in the face of evil brings collective punishment.",
        26: "Allah reminds the believers: when they were few and oppressed in Makkah, fearing abduction by pagans, fire worshippers, or Romans, Allah gave them refuge in Madinah, strengthened them with victory at Badr, and fed them from good things (including the spoils of war). Qatadah: 'Arabs were the weakest of the weak, had the toughest life, the emptiest stomachs.' This is a call to gratitude.",
        27: "Revealed about Hatib bin Abi Balta'ah, who wrote to the Quraysh warning them of the Prophet's march on Makkah. Allah revealed the letter's location. When confronted, Hatib said he did it to protect his family in Makkah. Umar sought permission to execute him, but the Prophet said: 'He has participated in Badr, and perhaps Allah has looked at the people of Badr and said: Do what you wish, for I have forgiven you.' Betrayal is not just material — it is spiritual allegiance.",
        28: "Wealth and children are a fitnah (trial/test). Allah tests: do these blessings draw the believer closer to Him or become a distraction? The 'great reward' with Allah is the real goal. This verse was connected to the Hatib story — his concern for his family in Makkah led him to betray the Prophet. Family ties can become a trial when they conflict with faith.",
        29: "Taqwa yields furqan (criterion). Ibn Abbas, Mujahid, Qatadah, and others gave multiple meanings: 'a way out,' 'salvation,' 'aid,' or 'criterion between truth and falsehood.' Ibn Ishaq's interpretation is most general: furqan is the discernment that comes from God-consciousness. Three gifts of taqwa: (1) furqan — the criterion, (2) expiation of evil deeds, (3) forgiveness. Allah is the possessor of great bounty.",
        30: "The Quraysh plotted at Dar An-Nadwah: to imprison, kill, or expel the Prophet. Ibn Kathir narrates that Iblis appeared as an old man and guided them to choose expulsion. This led to the Hijra — the founding of the Islamic state in Madinah. Allah's plan (makr) turned their plot into the very means of Islam's triumph. 'Allah is the best of planners' — His wisdom supersedes all human scheming.",
        31: "The Quraysh claimed: 'If we wished, we could say the like of this.' Ibn Kathir identifies An-Nadr bin Al-Harith as the speaker — he visited Persia, learned tales of Rustum and Isphandiyar, and presented them as an alternative to the Qur'an. He was captured at Badr and executed. Their boast was empty: they were challenged repeatedly to produce even one chapter like the Qur'an and never could. They called it 'tales of the ancients.'",
        32: "The Quraysh defiantly prayed: 'O Allah, if this is the truth from You, rain down stones on us or bring a painful punishment.' This is the peak of arrogance — daring Allah to punish them, confident He would not. Ibn Kathir notes that Allah did send punishment later — at Badr — but not the stones from the sky they challenged Him to send. Their defiance was met with defeat in battle, not cosmic destruction.",
        33: "Two reasons Allah withheld punishment: (1) the Prophet was among them, and (2) they sought forgiveness. The Prophet's presence was a shield for the entire community. After he migrated, the punishment came at Badr. Ibn Kathir adds: if not for weak, oppressed Muslims living among the Makkans who invoked Allah's forgiveness, the torment would have come even before the migration. Istighfar (seeking forgiveness) is a communal shield.",
        34: "Why should Allah not punish them? They obstruct believers from al-Masjid al-Haram and are not its rightful guardians. 'Its true guardians are not but the righteous.' This redefines religious authority: it belongs to the God-conscious, not to those who merely control the building. The Quraysh claimed custodianship of the Ka'bah, but their actions disqualified them.",
        35: "Their 'prayer' at the Ka'bah was nothing but whistling and handclapping — empty ritual devoid of devotion. 'Taste the punishment for what you disbelieved.' This is a powerful critique of ritual without meaning, worship without sincerity. The Quraysh maintained the form of worship at the Sacred House but had replaced its substance with noise.",
        36: "The disbelievers spend their wealth to hinder people from Allah's path. After Badr, the Quraysh spent vast wealth on the Uhud campaign — only to be defeated again. Their spending becomes a source of regret, then they are overcome, then gathered to Hell. The prophecy was fulfilled in history: their wealth could not stop Islam's advance.",
        37: "Allah will distinguish the wicked from the good, heap the wicked together, and cast them into Hell. The cosmic battle between truth and falsehood ends with definitive separation — not mutual annihilation, but sorting and judgment. 'They are the losers' — those who spent against truth and rejected faith lose both this world and the Hereafter.",
    }

    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    prs.core_properties.author = "Tarbiyyah — Quran Wiki Research"
    prs.core_properties.title = "Surah Al-Anfal (8) Verses 24-37 — Thematic Study"
    prs.core_properties.subject = "Quranic Studies, Tafsir Ibn Kathir, Tafsir Muyassar"

    # ── Slide 1: Title ──
    make_title_slide(prs)

    # ── Slide 2: Overview / Thematic Structure ──
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    y = add_slide_title(slide, "Thematic Structure", "Surah Al-Anfal 8:24-37 — Five Interconnected Themes")

    themes = [
        ("Theme 1", "The Call to Life & Warning of Fitnah", "8:24-25"),
        ("Theme 2", "Divine Favour & Warning against Betrayal", "8:26-28"),
        ("Theme 3", "Taqwa and the Criterion (Furqan)", "8:29"),
        ("Theme 4", "Quraysh's Plots & Allah's Protection", "8:30-33"),
        ("Theme 5", "Deserved Punishment & Futile Spending", "8:34-37"),
    ]

    for i, (num, title, vr) in enumerate(themes):
        row_y = y + i * 1.05
        # Card
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(row_y), W.inches - 1.2, 0.90)
        card.fill.solid(); card.fill.fore_color.rgb = C_CARD_BG; card.line.fill.background()
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(row_y), Inches(0.06), Inches(0.90))
        bar.fill.solid(); bar.fill.fore_color.rgb = C_ACCENT; bar.line.fill.background()

        # Theme number
        tx1 = slide.shapes.add_textbox(Inches(0.8), Inches(row_y + 0.08), Inches(1.2), Inches(0.3))
        p = tx1.text_frame.paragraphs[0]
        p.text = num; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = C_ACCENT; p.font.name = 'Georgia'

        # Title
        tx2 = slide.shapes.add_textbox(Inches(2.0), Inches(row_y + 0.08), Inches(7.0), Inches(0.4))
        p2 = tx2.text_frame.paragraphs[0]
        p2.text = title; p2.font.size = Pt(16); p2.font.bold = True; p2.font.color.rgb = C_PRIMARY

        # Verse range
        tx3 = slide.shapes.add_textbox(Inches(2.0), Inches(row_y + 0.48), Inches(7.0), Inches(0.3))
        p3 = tx3.text_frame.paragraphs[0]
        p3.text = f"Qur'an 8:{vr}"; p3.font.size = Pt(12); p3.font.italic = True; p3.font.color.rgb = C_TEXT_MUTED

    add_footer(slide)

    # ── Theme 1 Section Divider ──
    make_section_slide(prs, 1, "The Call to Life & Warning of Fitnah", "24-25")

    # ── Verse 8:24 ──
    v = verses["24"]
    make_verse_slide(prs, "8:24", v["arabic"], v["translations"]["en.sahih"],
                     tafsir_summaries[24], "Theme 1: The Call to Life (8:24-25)")

    # ── Verse 8:25 ──
    v = verses["25"]
    make_verse_slide(prs, "8:25", v["arabic"], v["translations"]["en.sahih"],
                     tafsir_summaries[25], "Theme 1: The Call to Life (8:24-25)")

    # ── Theme 1 Lessons ──
    make_lesson_slide(prs, "Theme 1: Key Lessons", [
        ("Respond to What Gives Life",
         "The call to respond to Allah and His Messenger is a call to spiritual vitality. Al-Bukhari interpreted 'that which gives you life' as 'that which makes your affairs good.' The Prophet taught that this response takes priority even over prayer."),
        ("Allah Intervenes Between Man and His Heart",
         "Allah is intimately involved in the human heart. He can turn a person's heart, and the believer must recognise that the heart is not solely in human control — it belongs to Allah."),
        ("Fitnah Is Not Selective",
         "A trial 'will not strike those who have wronged exclusively.' When evil is tolerated, consequences reach the innocent. Communal responsibility: silence in the face of wrongdoing brings collective consequences."),
    ], "Theme 1: The Call to Life (8:24-25)")

    # ── Theme 2 Section Divider ──
    make_section_slide(prs, 2, "Divine Favour & Warning against Betrayal", "26-28")

    # ── Verses 8:26-28 ──
    for ayah in [26, 27, 28]:
        v = verses[str(ayah)]
        make_verse_slide(prs, f"8:{ayah}", v["arabic"], v["translations"]["en.sahih"],
                         tafsir_summaries[ayah], "Theme 2: Divine Favour & Betrayal (8:26-28)")

    # ── Theme 2 Lessons ──
    make_lesson_slide(prs, "Theme 2: Key Lessons", [
        ("Remember Your Past Weakness",
         "The believers were few and oppressed, fearing abduction. Allah gave refuge, victory, and sustenance. Gratitude for Allah's blessings is a religious obligation — forgetfulness leads to betrayal."),
        ("Do Not Betray Your Trusts",
         "Revealed about Hatib bin Abi Balta'ah, who warned the Quraysh of the Prophet's march. Betrayal is not merely material — it is spiritual allegiance. The Prophet forgave him for his past service at Badr."),
        ("Wealth and Children Are a Trial",
         "Possessions and progeny are tests: do they draw the believer closer to Allah or become a distraction? Hatib's concern for his family led to his betrayal. The 'great reward' with Allah is the real goal."),
    ], "Theme 2: Divine Favour & Betrayal (8:26-28)")

    # ── Theme 3 Section Divider ──
    make_section_slide(prs, 3, "Taqwa and the Criterion (Furqan)", "29")

    # ── Verse 8:29 ──
    v = verses["29"]
    make_verse_slide(prs, "8:29", v["arabic"], v["translations"]["en.sahih"],
                     tafsir_summaries[29], "Theme 3: Taqwa and the Criterion (8:29)")

    # ── Theme 3 Lessons ──
    make_lesson_slide(prs, "Theme 3: Key Lessons", [
        ("Taqwa Yields Furqan",
         "God-consciousness produces the ability to distinguish truth from falsehood. Ibn Abbas, Mujahid, Qatadah gave meanings: 'a way out,' 'salvation,' 'aid,' 'criterion.' Ibn Ishaq: furqan is the discernment from living in awareness of Allah."),
        ("Three Gifts of Taqwa",
         "(1) Furqan — the criterion between truth and falsehood. (2) Expiation of evil deeds — Allah removes your misdeeds. (3) Forgiveness — Allah pardons you. A comprehensive spiritual programme: discernment, purification, and pardon."),
    ], "Theme 3: Taqwa and the Criterion (8:29)")

    # ── Theme 4 Section Divider ──
    make_section_slide(prs, 4, "Quraysh's Plots & Allah's Protection", "30-33")

    # ── Verses 8:30-33 ──
    for ayah in [30, 31, 32, 33]:
        v = verses[str(ayah)]
        make_verse_slide(prs, f"8:{ayah}", v["arabic"], v["translations"]["en.sahih"],
                         tafsir_summaries[ayah], "Theme 4: Quraysh's Plots & Allah's Protection (8:30-33)")

    # ── Theme 4 Lessons ──
    make_lesson_slide(prs, "Theme 4: Key Lessons", [
        ("The Makkan Plot Backfired",
         "At Dar An-Nadwah, the Quraysh chose to expel the Prophet. Iblis appeared as an old man guiding this decision. The expulsion led to the Hijra — the founding of the Islamic state. Allah's plan turned their plot into Islam's triumph."),
        ("The Defiant Prayer for Punishment",
         "The Quraysh dared Allah to rain stones on them if the Qur'an was true. An-Nadr bin Al-Harith boasted he could rival the Qur'an — he was executed at Badr. Their arrogance was empty; they never produced even one chapter."),
        ("Two Shields Against Punishment",
         "(1) The Prophet's presence among them. (2) Seeking forgiveness (istighfar). After the Prophet migrated, punishment came at Badr. Istighfar is a communal shield — even a few seekers of forgiveness can protect a community."),
    ], "Theme 4: Quraysh's Plots & Allah's Protection (8:30-33)")

    # ── Theme 5 Section Divider ──
    make_section_slide(prs, 5, "Deserved Punishment & Futile Spending", "34-37")

    # ── Verses 8:34-37 ──
    for ayah in [34, 35, 36, 37]:
        v = verses[str(ayah)]
        make_verse_slide(prs, f"8:{ayah}", v["arabic"], v["translations"]["en.sahih"],
                         tafsir_summaries[ayah], "Theme 5: Deserved Punishment & Futile Spending (8:34-37)")

    # ── Theme 5 Lessons ──
    make_lesson_slide(prs, "Theme 5: Key Lessons", [
        ("Obstructing the Sacred Mosque",
         "The Quraysh's sin was not just disbelief but actively preventing believers from al-Masjid al-Haram. 'Its true guardians are not but the righteous.' Religious authority belongs to the God-conscious, not to those who control the building."),
        ("Ritual Without Meaning",
         "Their 'prayer' at the Ka'bah was whistling and handclapping — empty ritual devoid of devotion. A powerful critique of worship without sincerity: form without substance is no worship at all."),
        ("Wealth Against Truth Becomes Regret",
         "The Quraysh spent vast wealth after Badr to fight Islam at Uhud — only to be defeated again. Their spending brought grief, not victory. Allah will separate the wicked from the good and heap them into Hell. The losers lose both worlds."),
    ], "Theme 5: Deserved Punishment & Futile Spending (8:34-37)")

    # ── Cross-Thematic Reflections Slide ──
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    y = add_slide_title(slide, "Cross-Thematic Reflections", "The Architecture of the Passage 8:24-37")

    # Two columns: Believers vs Disbelievers
    add_card(slide, 0.6, y, 5.8, 3.0, "Believers (8:24-29)", [
        "• Called to life — respond to Allah and His Messenger",
        "• Warned of fitnah that strikes all who tolerate evil",
        "• Reminded of past weakness and divine favour",
        "• Warned against betraying trusts (spiritual allegiance)",
        "• Wealth and children are tests, not rewards",
        "• Promised furqan (criterion) through taqwa",
        "• Three gifts: discernment, purification, forgiveness",
    ], accent_color=C_PRIMARY)

    add_card(slide, 6.9, y, 5.8, 3.0, "Disbelievers (8:30-37)", [
        "• Plotted to imprison, kill, or expel the Prophet",
        "• Boasted they could rival the Qur'an (empty claim)",
        "• Dared Allah to punish them (peak of arrogance)",
        "• Obstructed believers from the Sacred Mosque",
        "• Replaced worship with whistling and handclapping",
        "• Spent wealth against Islam → regret → defeat → Hell",
        "• Allah separates the wicked from the good",
    ], accent_color=C_ACCENT2)

    # Pivot note
    y += 3.2
    tx = slide.shapes.add_textbox(Inches(0.6), Inches(y), W.inches - 1.2, Inches(0.8))
    tf = tx.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "The Pivot: Verse 8:29 — Taqwa yields Furqan"
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_ACCENT; p.font.name = 'Georgia'
    p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = "This is the criterion by which the two paths are distinguished — the very principle that verse 8:37 enacts cosmically."
    p2.font.size = Pt(13); p2.font.italic = True; p2.font.color.rgb = C_TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

    add_footer(slide)

    # ── References Slide ──
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    y = add_slide_title(slide, "References and Sources", "Verified from the Quran Wiki Corpus")

    add_card(slide, 0.6, y, 5.8, 2.5, "Primary Sources", [
        "• The Holy Qur'an — Surah Al-Anfal (8), vv. 24-37",
        "  Arabic: Uthmani script (Al Quran Cloud + Quran.com)",
        "• Tafsir Ibn Kathir (Abridged)",
        "  Imam Ibn Kathir (d. 774 AH / 1373 CE)",
        "• Tafsir Muyassar",
        "  King Fahd Complex for the Printing of the Holy Qur'an",
    ], accent_color=C_PRIMARY)

    add_card(slide, 6.9, y, 5.8, 2.5, "Translations (5 editions)", [
        "• Sahih International (English) — primary",
        "• Marmaduke Pickthall (English)",
        "• Abdullah Yusuf Ali (English)",
        "• Muhammad Asad (English)",
        "• Abdullah Muhammad Basmeih (Malay)",
    ], accent_color=C_ACCENT2)

    y += 2.7
    add_card(slide, 0.6, y, 12.1, 1.8, "Hadith Collections Cited Within Tafsir", [
        "Sahih al-Bukhari (d. 256 AH) | Sahih Muslim (d. 261 AH) | Musnad Ahmad (d. 241 AH) | Sunan at-Tirmidhi (d. 279 AH) | Sunan an-Nasa'i (d. 303 AH) | Sunan Abu Dawud (d. 275 AH) | Sunan Ibn Majah (d. 273 AH)",
    ], accent_color=C_SECONDARY)

    add_footer(slide)

    # ── Conclusion Slide ──
    make_conclusion_slide(prs)

    # Save
    out_path = "/root/tarbiyyah/notes/anfal-8-24-37-presentation.pptx"
    prs.save(out_path)
    print(f"Saved: {out_path}")
    print(f"Total slides: {len(prs.slides)}")

if __name__ == "__main__":
    main()