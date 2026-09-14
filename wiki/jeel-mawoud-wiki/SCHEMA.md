# Jeel Mawoud Wiki — Schema

## Identity

**Wiki Name:** Jeel Mawoud Wiki (الجيل الموعود بالنصر والتمكين)
**Domain:** Islamic tarbiyyah — Attributes of the promised generation
**Source:** الجيل الموعود بالنصر والتمكين by Dr. Majdi al-Hilali (مجدي الهلالي)
**Location:** `/root/tarbiyyah/jeel-mawoud-wiki/`
**Type:** Single-book LLM Wiki (Karpathy pattern)
**Language:** English with Arabic terms in original script + transliteration
**Hub:** Registered in `~/.llm-wiki/.config/wikis.yaml` under `religious.jeel-mawoud`

## Page Types

| Type | Directory | Filename Pattern | Purpose |
|------|-----------|-----------------|---------|
| `overview` | `entities/` | `overview-jeel-mawoud.md` | Book synopsis + metadata |
| `scholar` | `entities/` | `scholar-majdi-al-hilali.md` | Author biography |
| `chapter` | `entities/` | `ch-NN-slug.md` | Chapter summary + citations |
| `concept` | `concepts/` | `concept-slug.md` | Thematic concept definition |
| `comparison` | `comparisons/` | `comparison-slug.md` | Cross-wiki thematic analysis |
| `query` | `queries/` | `query-slug.md` | Filed research results |
| `index` | root | `index.md` | Content catalog |
| `log` | root | `log.md` | Chronological action log |

## Frontmatter Spec

All pages must have YAML frontmatter:

```yaml
---
title: "Page Title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: overview | scholar | chapter | concept | comparison | query
tags: [tag1, tag2, ...]  # from taxonomy below
sources: ["raw/extracted/file.txt:pages XX-YY"]  # traceable to source
confidence: high | medium | low
---
```

**Chapter pages add:**
```yaml
chapter: 0-6  # 0=intro, 1-5=chapters, 6=conclusion
pages: "NN-MM"  # book page numbers
```

**Concept pages add:**
```yaml
arabic: "Arabic term"
transliteration: "transliteration"
```

**Comparison pages add:**
```yaml
wikis: [jeel-mawoud, qaradawi-library, quran-wiki, to-be-a-muslim]
```

## Tag Taxonomy

### Structural
`chapter`, `overview`, `scholar`, `concept`, `comparison`, `query`, `introduction`, `conclusion`

### Core Concepts (10 Attributes)
`jeel-mawoud`, `ikhlas`, `mahabbah`, `khawf`, `ibadah`, `tawadu`, `zuhd`, `jihad`, `sabr`, `itidal`, `ukhuwwah`

### Methodology
`tarbiyyah`, `dakwah`, `manhaj`, `asbab`, `qa-idah`, `marifah`, `tazkiyah`, `hikmah`

### Theological
`nasr`, `tamkin`, `iman`, `quranic-promise`, `akhirah`, `tawhid`

### Historical
`sahabah`, `first-generation`, `seerah`, `islamic-history`

### Meta
`cross-wiki`, `concept-definition`, `scholar-biography`, `verification`

## Wikilink Conventions

- **Internal:** `[[entities/ch-01-limadha]]`, `[[concepts/concept-ikhlas]]`
- **Cross-wiki:** `[[qaradawi-library/concept-ikhlas|Qaradawi on Ikhlas]]`, `[[quran-wiki/surah-002-al-baqarah|Al-Baqarah]]`
- **Directory links:** NEVER use `[[concepts/concepts-index|Concepts Index]]` — always use `[[concepts/concepts-index|Concepts Index]]`
- **Pipe syntax:** `[[concepts/concept-nasr-tamkin|display text]]` when display text differs from slug

## Raw Source Conventions

- `raw/pdfs/` — Immutable. Never modify after creation.
- `raw/extracted/` — Machine-extracted text. Corrections go in wiki pages, not here.
- `.ops/` — Operational artifacts (QA reports, task logs). Excluded from page counts.
- `.tools/` — Scripts. Excluded from page counts.
- `.config/` — Registry and configuration.

## Quality Rules

1. Every claim must have a source page reference
2. Every Quranic verse must be in `surah:verse` format and verified
3. Every hadith must have source attribution; if grade is unknown in source, write "Grade not specified in source"
4. No fabricated content — if uncertain, state it explicitly
5. Arabic terms: always provide original script + transliteration + English gloss
6. Cross-wiki links must use stable slugs, not page titles

## Quranic Citation Format

```
| Verse | Context | Page |
|-------|---------|------|
| 2:257 | Allah is the ally of believers | p15 |
```

Arabic verification via Al Quran Cloud API: `api.alquran.cloud/v1/ayah/{surah}:{verse}`