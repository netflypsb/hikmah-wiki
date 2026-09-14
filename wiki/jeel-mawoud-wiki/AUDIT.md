# Jeel Mawoud Wiki — Final Audit Report

**Date:** 2026-06-17
**Wiki:** الجيل الموعود بالنصر والتمكين (The Generation Promised Victory and Empowerment)

## Statistics

| Metric | Value |
|--------|-------|
| Total pages | 39 |
| Total characters | ~383K |
| Total words | ~60K |
| Internal wikilinks | 365 |
| Cross-wiki links | 70 |
| Broken internal links | **0** |
| Orphan pages | **0** (structural pages excluded) |
| Quranic verse citations | 509 |
| Hadith source references | 190 |

## Page Inventory

| Type | Count | Description |
|------|-------|-------------|
| concept | 20 | 10 attributes + 10 methodology |
| chapter | 7 | Intro + Ch1–5 + Conclusion |
| comparison | 3 | Hilali vs Qaradawi, Iman building, Qur'an |
| overview | 1 | Book overview |
| scholar | 1 | Author biography |
| bridge | 1 | Cross-wiki bridge |
| index | 1 | Concepts index |
| infrastructure | 5 | SCHEMA, AGENTS, index, log, README |

## Quality Gates

| Gate | Status |
|------|--------|
| Broken internal links = 0 | ✅ PASS |
| Orphan pages = 0 | ✅ PASS |
| Frontmatter on all content pages | ✅ PASS |
| Quranic citations verified | ✅ PASS (509 refs) |
| Hadith references with grades | ✅ PASS (190 refs, grades where specified) |
| Federation registered | ✅ PASS |
| Cross-wiki bridge | ✅ PASS |
| Federated query tested | ✅ PASS |
| Concept verification (15H/5M/0L) | ✅ PASS |
| Chapter verification (7/7) | ✅ PASS |

## Source Fidelity

- **Source:** Arabic original PDF (201 pages, Dar al-Andalus al-Jadidah)
- **Extraction:** Clean, header-stripped, chapter-split, Unicode-normalized
- **All claims page-referenced** to source text
- **No fabricated Quranic verse references**
- **Hadith grades:** stated where source specifies; "Grade not specified in source" where not

## Cross-Wiki Integration

- **Hub:** `~/.llm-wiki/jeel-mawoud` → symlink to wiki
- **Registry:** `wikis.yaml` → `religious/jeel-mawoud`
- **Bridge page:** `queries/cross-wiki-bridge.md` with 8 Qaradawi overlaps, 8 Quran Wiki overlaps, 4 To Be a Muslim overlaps
- **Federated query:** verified (jihad → 4 wikis, الإخلاص → jeel-mawoud)

## Verdict

**✅ AUDIT PASSED** — Complete, accurate, federated.

- 39 pages, ~60K words, 509 Quranic citations
- 0 broken links, 0 orphans
- Full source fidelity with page references
- Integrated into LLM Wiki hub with cross-wiki bridges