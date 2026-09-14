#!/usr/bin/env python3
"""Assemble and clean OCR text from individual page files."""
import os
import re
import sys

OCR_DIR = "/root/tarbiyyah/fathi-yakan-intimai/ocr_text"
OUTPUT = "/root/tarbiyyah/fathi-yakan-intimai/madha-yaani-intimaii-full-text.txt"

def clean_line(line):
    """Clean common OCR artifacts."""
    # Remove empty lines
    line = line.strip()
    if not line:
        return ""
    # Remove standalone page numbers (just digits)
    if re.match(r'^\d{1,3}$', line):
        return ""
    # Remove lines that are just footnote markers like "(1)" or "1)"
    if re.match(r'^[\(\d\)]+$', line):
        return ""
    # Remove very short lines (likely OCR noise)
    if len(line) < 3:
        return ""
    return line

def assemble():
    pages = sorted([f for f in os.listdir(OCR_DIR) if f.startswith("page-") and f.endswith(".txt")])
    
    output_lines = []
    total_words = 0
    total_chars = 0
    non_empty_pages = 0
    empty_pages = []
    
    for page_file in pages:
        page_path = os.path.join(OCR_DIR, page_file)
        page_num = int(re.search(r'page-(\d+)', page_file).group(1))
        
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        cleaned = []
        for line in lines:
            cl = clean_line(line)
            if cl:
                cleaned.append(cl)
        
        if cleaned:
            non_empty_pages += 1
            # Add page marker for reference
            output_lines.append(f"\n--- Page {page_num} ---\n")
            output_lines.extend(cleaned)
            # Count words (Arabic word = sequence of Arabic chars)
            text = ' '.join(cleaned)
            words = len(text.split())
            total_words += words
            total_chars += len(text)
        else:
            empty_pages.append(page_num)
    
    # Write assembled text
    full_text = '\n'.join(output_lines)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    # Also write a clean version without page markers
    clean_output = OUTPUT.replace('.txt', '-clean.txt')
    clean_lines = [l for l in output_lines if not l.startswith('--- Page')]
    clean_text = '\n'.join(clean_lines)
    with open(clean_output, 'w', encoding='utf-8') as f:
        f.write(clean_text)
    
    # Stats
    print(f"Total pages: {len(pages)}")
    print(f"Non-empty pages: {non_empty_pages}")
    print(f"Empty/blank pages: {len(empty_pages)} -> {empty_pages}")
    print(f"Total words: {total_words:,}")
    print(f"Total characters: {total_chars:,}")
    print(f"Output: {OUTPUT}")
    print(f"Clean output: {clean_output}")
    print(f"File size: {os.path.getsize(OUTPUT):,} bytes")

if __name__ == "__main__":
    assemble()