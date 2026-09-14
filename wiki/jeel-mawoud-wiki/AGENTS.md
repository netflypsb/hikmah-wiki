---
title: "Jeel Mawoud Wiki — Agent Context"
created: 2026-06-17
updated: 2026-06-17
type: agent-context
tags: [agent-context]
---

# Jeel Mawoud Wiki — Agent Context

## Project Identity

**Name:** Jeel Mawoud Wiki (الجيل الموعود بالنصر والتمكين)
**Domain:** Islamic Tarbiyyah — Complete analysis of Dr. Majdi al-Hilali's book on the promised generation
**Location:** `/root/tarbiyyah/jeel-mawoud-wiki/`
**Type:** Single-book LLM Wiki (Karpathy pattern)
**Agent:** Main Hermes profile (`scholarly-wiki-ops` + `llm-wiki` skills loaded)
**Zone:** Personal project (tarbiyyah) — NEVER mix with Genesis business contexts

## Mission

Build the most comprehensive, accurate, and reliable LLM Wiki from the Arabic original of الجيل الموعود بالنصر والتمكين by Dr. Majdi al-Hilali. Every concept defined with Arabic original + transliteration + English gloss. Every claim traced to source pages. Every Quranic citation verified against Al Quran Cloud API.

## Source

- **Arabic Original PDF:** `raw/pdfs/jeel-mawoud-arabic-original.pdf` (201 pages, 5.3MB)
- **Archive.org ID:** `ozkorallh_20180412`
- **Extracted Text:** `raw/extracted/jeel-mawoud-full-raw.txt` (166,687 chars)
- **Publisher:** Dar al-Andalus al-Jadidah, Egypt
- **ISBN:** 977-6142-96-6
- **Edition:** First, 1429 H / 2008 M
- **Deposit No.:** 27133/2007
- **Malay Translation:** Dewan Pustaka Fajar, 256 pp, ISBN 9789678300902 (purchase only)

## Book Structure

| Section | Pages | Arabic Title |
|---------|-------|-------------|
| Introduction | 5–7 | المقدمة |
| Chapter 1 | 10–23 | لماذا الجيل الموعود؟ |
| Chapter 2 | 24–97 | مع صفات الجيل الموعود (10 attributes) |
| Chapter 3 | 98–145 | كيف تحقق صفات الجيل الموعود؟ |
| Chapter 4 | 146–175 | الجيل الأول وأدوات التغيير |
| Chapter 5 | 175–191 | أين نحن من الجيل الموعود؟ |
| Conclusion | 192–193 | الخاتمة |
| Index | 194–201 | الفهرس |

## Critical Constraints

- **Source fidelity:** Every claim traced to specific pages. No fabrication.
- **Arabic-primary:** All concepts with original Arabic + transliteration + English gloss
- **No cross-contamination:** Never mix with Genesis business data
- **Quranic verification:** Every surah:verse checked against Al Quran Cloud API
- **Hadith attribution:** If grade not in source, write "Grade not specified in source" — never guess

## Context Files (Read These First)

1. **SCHEMA.md** — Wiki conventions, tag taxonomy, frontmatter rules
2. **index.md** — Content catalog
3. **log.md** — Last 30 entries for orientation
4. **.config/books.yaml** — Book registry state
5. **BUILD-PLAN.md** — Full 7-stage build plan

## Cross-Wiki Federation

- **Qaradawi Library** (`/root/qaradawi-library/`) — Shared concepts: ikhlas, sabr, jihad, tarbiyyah, tawadu
- **Quran Wiki** (`/root/tarbiyyah/quran-wiki/`) — Foundation verses for the book's 11 key citations
- **To Be a Muslim** (`~/.llm-wiki/religious/to-be-a-muslim`) — Overlapping tarbiyyah/manhaj themes

## Tooling

- Python 3 + pymupdf (PDF extraction)
- curl (Al Quran Cloud API verification)
- Hermes Agent (wiki page generation, cross-referencing, linting)
- Git (version control)

## Directory Structure

```
/root/tarbiyyah/jeel-mawoud-wiki/
├── .config/              # Book registry
│   └── books.yaml
├── .ops/                 # QA reports, task logs
├── .tools/               # Scripts
├── raw/
│   ├── pdfs/             # Immutable source PDFs
│   └── extracted/        # Extracted + cleaned text
├── entities/             # Book + chapter + author pages
├── concepts/             # Thematic concept pages
├── comparisons/          # Cross-wiki comparisons
├── queries/              # Filed research results
├── SCHEMA.md             # This schema
├── index.md              # Content catalog
├── log.md                # Action log
├── AGENTS.md             # This file
├── README.md             # Human-facing overview
└── BUILD-PLAN.md         # Build plan
```