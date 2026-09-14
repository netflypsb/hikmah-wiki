#!/usr/bin/env python3
"""Split the Arabic OCR text into chapter files using content search on cleaned text."""
import re
import os

SOURCE = "/root/tarbiyyah/fathi-yakan-intimai/madha-yaani-intimaii-full-text-clean.txt"
OUTDIR = "/root/tarbiyyah/fathi-yakan-intimai/translation/chapters_ar"

os.makedirs(OUTDIR, exist_ok=True)

with open(SOURCE, 'r', encoding='utf-8') as f:
    raw = f.read()

# Remove page markers
text = re.sub(r'--- Page \d+ ---', '', raw)
text = re.sub(r'\n{3,}', '\n\n', text).strip()

# Find positions in the cleaned text using find_all
def find_all(pattern, text):
    positions = []
    start = 0
    while True:
        match = re.search(re.escape(pattern), text[start:])
        if match:
            pos = start + match.start()
            positions.append(pos)
            start = pos + 1
        else:
            break
    return positions

# For each chapter, find the correct content position (skip TOC entries)
# Key insight: TOC entries are around position 4500-5000 (Part 1) and 45300-45700 (Part 2)
# We want content positions AFTER the TOC

def find_after_toc(pattern, text, min_pos=5000):
    """Find the first occurrence of pattern after min_pos."""
    positions = find_all(pattern, text)
    for p in positions:
        if p >= min_pos:
            return p
    return -1

# Introduction
intro_pos = text.find('الحمد لله والصلاة والسلام على رسوله وبعد')

# Part 1 chapters - content starts after intro and Part 1 TOC
# Part 1 TOC is around position 4500-5000
part1_start = 5000  # After Part 1 TOC

ch1_pos = find_after_toc('أن أكون مسلماً في عقيدتي', text, part1_start)
if ch1_pos == -1:
    ch1_pos = find_after_toc('في عقيدتي', text, part1_start)

ch2_pos = find_after_toc('ان اكون مسلماً في عبادتي', text, part1_start)
if ch2_pos == -1:
    ch2_pos = find_after_toc('في عبادتي', text, part1_start)

ch3_pos = find_after_toc('في اخلاتي', text, part1_start)
if ch3_pos == -1:
    ch3_pos = find_after_toc('في أخلاقي', text, part1_start)

ch4_pos = find_after_toc('في أهلي وبي', text, part1_start)

ch5_pos = find_after_toc('أن أنتصر على نفسي', text, part1_start)

# Chapter 6 - OCR variant
ch6_pos = find_after_toc('أن أكون مؤمناً بأن المبتقبل', text, part1_start)
if ch6_pos == -1:
    ch6_pos = find_after_toc('المبتقبل', text, 40000)  # After ch5

# Part 2 starts after chapter 6
part2_toc_end = 46000  # Part 2 TOC is around 45300-46000

# Part 2 intro (author's note)
part2_intro_pos = find_after_toc('الى الاسلام هو الآساس', text, part2_toc_end)
if part2_intro_pos == -1:
    part2_intro_pos = 46000

# Chapter 7 - living for Islam (content, not TOC)
ch7_pos = find_after_toc('ان أعيش للاسلام', text, part2_toc_end)
if ch7_pos == -1:
    ch7_pos = find_after_toc('أن أعيش للاسلام', text, part2_toc_end)
if ch7_pos == -1:
    ch7_pos = 47400  # Fallback

# Chapter 8 - obligation to work
ch8_pos = find_after_toc('ان اكون مؤمناً بوجوب العمل للاسلام', text, ch7_pos + 100)
if ch8_pos == -1:
    ch8_pos = find_after_toc('ان العمل للاسلام', text, ch7_pos + 100)
if ch8_pos == -1:
    ch8_pos = 55400  # Fallback to known position

# Chapter 9 - Islamic movement
# Look for content heading after ch8
ch9_pos = find_after_toc('القاعدة الأساسية', text, ch8_pos + 100)
if ch9_pos == -1:
    ch9_pos = 65500

# Chapter 10 - methods
ch10_pos = find_after_toc('أن يكون هذا الانتماء أبعاد', text, ch9_pos + 100)
if ch10_pos == -1:
    ch10_pos = find_after_toc('أبعاد تتجاوز', text, ch9_pos + 100)
if ch10_pos == -1:
    ch10_pos = 87000

# Chapter 11 - dimensions
ch11_pos = find_after_toc('هجرته الى ما هاجر اليه', text, ch10_pos + 100)
if ch11_pos == -1:
    ch11_pos = 89000

# Chapter 12 - pillars
ch12_pos = find_after_toc('أعوذ بك من الحبن', text, ch11_pos + 100)
if ch12_pos == -1:
    ch12_pos = 105000

# Chapter 13 - conditions
ch13_pos = find_after_toc('باط الرباني', text, ch12_pos + 100)
if ch13_pos == -1:
    ch13_pos = 115000

# Chapter 14 - the bond's litany
ch14_pos = find_after_toc('ورد الرابطة', text, ch13_pos + 100)
if ch14_pos == -1:
    ch14_pos = 123358

# Assemble positions
positions = [
    (intro_pos, "00-introduction"),
    (ch1_pos, "01-being-muslim-in-belief"),
    (ch2_pos, "02-being-muslim-in-worship"),
    (ch3_pos, "03-being-muslim-in-character"),
    (ch4_pos, "04-being-muslim-in-family"),
    (ch5_pos, "05-overcoming-the-ego"),
    (ch6_pos, "06-certainty-future-islam"),
    (part2_intro_pos, "06b-part2-intro"),
    (ch7_pos, "07-living-for-islam"),
    (ch8_pos, "08-obligation-to-work"),
    (ch9_pos, "09-islamic-movement"),
    (ch10_pos, "10-methods-islamic-work"),
    (ch11_pos, "11-dimensions-of-belonging"),
    (ch12_pos, "12-pillars-islamic-work"),
    (ch13_pos, "13-conditions-brotherhood"),
    (ch14_pos, "14-the-bonds-litany"),
]

# Sort by position
positions.sort(key=lambda x: x[0])

# Extract
total_words = 0
for i, (start, filename) in enumerate(positions):
    if i + 1 < len(positions):
        end = positions[i+1][0]
    else:
        end = len(text)
    
    chapter_text = text[start:end].strip()
    outpath = os.path.join(OUTDIR, f"{filename}.txt")
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(chapter_text)
    
    word_count = len(chapter_text.split())
    total_words += word_count
    preview = chapter_text[:100].replace('\n', ' ')
    print(f"{filename}: pos={start}, {word_count} words | {preview}...")

print(f"\nTotal words: {total_words}")
print("Done.")