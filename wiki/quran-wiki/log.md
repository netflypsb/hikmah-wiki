---
title: Quran Wiki Log
created: 2026-05-10
updated: 2026-05-10
type: log
---

# Quran Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-07-19] update | Surah 114 (An-Nas) — full enrichment

- Rewrote `surah-114-an-nas.md` from thin stub to comprehensive page (16KB):
  - All 6 verses with Arabic + 5-translation tables (Pickthall, Sahih, Yusuf Ali, Asad, Basmeih)
  - Ibn Kathir (Abridged) — extracted once as surah-level commentary (noted the raw JSONL duplication artifact; presented the full 4,798-char commentary once)
  - Tafsir Muyassar — per-ayah table (Arabic)
  - Fi Zilal companion link to `[[fi-zilal/surah-114-an-nas]]` with key insight summary
  - Structural notes: triple naming of Allah (Rabb/Malik/Ilah) × triple identification of whisperer; 4× repetition of an-nas; saj' rhyme
  - Linguistics section: roots for an-nas, waswas, khannas, sudur, jinnah
  - Full References & Sources (Layer 1 raw, Layer 2 curated themes/concepts, Layer 3 Fi Zilal, secondary-context wikis consulted-and-excluded)
  - Updated frontmatter: added tags (muawwidhatayn, waswas, istiadha, jinn, dhikr), updated sources and date
- Cross-linked to theme pages: protection, shaytan, command; concept page: rhetorical-devices; linguistics: dhikr
- Companion Fi Zilal page built at `/root/tarbiyyah/fi-zilal-wiki/surahs/surah-114-an-nas.md` (5 thematic sections preserved, provenance markers, cross-links)

## [2026-05-10] update | Phase 7 — Linguistics + Translation Comparisons
- 15 Arabic word study pages in linguistics/ (salam, rahmah, huda, sabr, shukr, taqwa, nur, jahannam, jannah, adl, ilm, dhikr, amal, qawm, ummah)
- linguistics/index.md master index
- 20 translation comparison tables in comparisons/ (Ayat al-Kursi, Al-Ikhlas, Al-Fatihah, etc.)
- comparisons/index.md master index
- Cross-linked into main index.md

## [2026-05-10] update | Phase 6 — Rhetorical devices (balagha)
- Created 12 rhetorical device pages in concepts/ (iltifat, tashbeeh, qasam, taqdeem, haal, tamtheel, muzawaja, ijaaz, jawab-al-qasam, kinayah, saj, tashreef-al-sadr)
- Created master index: concepts/rhetorical-devices.md
- Linked into index.md and cross-linked from other concept pages

## [2026-05-10] update | Phase 5 — Tafsir summaries woven into 114 surahs
- Extracted Ibn Kathir (Abridged) + Tafsir Muyassar from raw/tafsir/*.jsonl
- Woven 3-ayah summaries into every surah page
- 114 surahs covered | 0 orphans | 0 broken links | 94 unique tags

## [2026-05-10] verification | Phase 4 — Full lint pass
- 356 total wiki pages | 0 orphans | 0 broken links | 94 unique tags
- All checks PASS

## [2026-05-10] update | Phase 4 — Verse deep-dives + Asbab al-Nuzul
- Created 20 verse deep-dive pages in verses/ (P0 ayahs)
- Created 30 Asbab al-Nuzul pages in entities/asbab-al-nuzul/
- Linked verse pages into surah overviews
- Linked Asbab al-Nuzul into surah overviews
- Updated index.md with new navigation sections

## [2026-05-10] update | Phase 3 — Names of Allah + Juz pages
- Created 99 individual name pages in entities/names-of-allah/
- Created master index: entities/names-of-allah/index.md
- Created 30 juz pages in juz/
- Extracted juz metadata to .ops/juz-metadata.json
- Updated all 114 surah pages with juz cross-links
- Updated index.md with new navigation sections

## [2026-05-10] create | Wiki initialized
- Domain: Quranic Studies — the Holy Qur'an
- Structure created: SCHEMA.md, index.md, log.md
- Raw sources migrated:
  - raw/arabic/ — 6,236 verse Arabic texts (Uthmani rasm, dual-source verified)
  - raw/translations/ — 5 translations × 6,236 ayahs (Pickthall, Sahih, Yusuf Ali, Asad, Basmeih)
  - raw/tafsir/ — 114 surah tafsir files (Ibn Kathir Abridged, Tafsir Muyassar)
  - raw/metadata/ — quran-index.json (114 surahs, 30 ajza, 604 pages, 559 rukus)
  - raw/sources/ — API documentation and source manifests
- Operational files moved to .ops/ and .tools/
- Seed pages created: 114 surah pages, 7 theme pages, 5 prophet pages, 3 story pages, 3 concept pages, 1 comparison page
