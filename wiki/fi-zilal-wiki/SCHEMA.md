---
name: Fi Zilal al-Qur'an Wiki Schema
domain: Quranic Exegesis — Tafsir Fi Zilal al-Qur'an by Sayyid Qutb (في ظلال القرآن)
created: 2026-07-19
version: 1.0.0
---

# Wiki Schema — Fi Zilal al-Qur'an

## Domain
This wiki covers **Tafsir Fi Zilal al-Qur'an** (في ظلال القرآن, "In the Shade of the Qur'an") by Sayyid Qutb (1906–1966), the complete thematic-literary tafsir of all 114 surahs.

Fi Zilal is a **Tier 1 secondary tafsir** (per Tarbiyyah CLAUDE.md): thematic and literary in character, not per-ayah. Its flowing essay sections — "Overview", "Faith and Its Significance", "Need for Righteous Deeds", "Profit and Loss" — treat each surah as a unified whole, weaving together theology, social critique, and literary analysis.

## Relationship to Other Wikis
- **quran-wiki** (`/root/tarbiyyah/quran-wiki/`) — primary Quran wiki (Uthmani text, per-ayah Ibn Kathir + Muyassar tafsir, themes, prophets, linguistics). Fi Zilal is a *companion* tafsir, cited alongside but not merged into quran-wiki.
- **qaradawi-library** — Qaradawi draws on Fi Zilal; cross-link where concepts overlap.
- **meta-wiki** — cross-domain syntheses bridge.

Each surah page in this wiki cross-links to the matching `[[quran-wiki/surah-NNN-*]]` page so the two tafasir can be consulted together.

## Conventions

### File Naming
- Raw sources: `raw/surah-NNN-[english-name].md` (verbatim ingestion)
- Surah pages: `surahs/surah-NNN-[english-name].md` (curated wiki page)
- Concept pages: `concepts/[concept-name].md` (cross-cutting themes Fi Zilal develops across surahs)
- All lowercase, hyphens, no spaces or diacritics in filenames.

### Frontmatter (every wiki page)
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: surah | concept | comparison | query
surah_number: 103
surah_name: al-asr
revelation: makki | madani
verse_count: 3
tags: [from taxonomy below]
sources: [raw/surah-103-al-asr.md]
confidence: high
---
```

### Provenance
- The `raw/` directory holds verbatim source text. Never edit raw files after ingestion.
- The `surahs/` directory holds curated pages that preserve the original's thematic section headings as `##` headers.
- Provenance markers: `^[raw/surah-NNN-*.md]` appended to paragraphs whose claims come from a specific source section.

### Arabic Terms
Always include Arabic in original script with diacritics for precision:
*sūrah* (سُورَة), *īmān* (إِيمَان), *ṣabr* (صَبْر), *jāhiliyyah* (جَاهِلِيَّة), *khusr* (خُسْر).

## Tag Taxonomy

### Tafsir-Specific
- `fi-zilal` — pages in this wiki
- `thematic-tafsir` — literary/thematic exegesis (vs per-ayah)
- `literary-analysis` — rhetorical, stylistic, structural observations
- `social-critique` — Qutb's critique of jahiliyyah and modernity
- `tarbiyyah-spiritual` — spiritual/educational cultivation themes

### Quranic (shared with quran-wiki)
- `tawhid`, `risalah`, `akhirah`, `iman`, `amal-salih`, `haqq`, `sabr`, `tawasi`
- `jahiliyyah`, `khusr`, `khilafah`, `ummah`, `dawah`
- `makki`, `madani`, `qasam`, `nasr`

### Source
- `sayyid-qutb` — author attribution
- `fi-zilal-eng` — English translation source

## Page Types

### Surah Page (`type: surah`)
- YAML frontmatter (surah_number, surah_name, revelation, verse_count)
- Arabic title + transliteration
- Verse text (from quran-wiki cross-reference)
- Each thematic section from the source preserved as `##` heading:
  - `## Overview`
  - `## Faith and Its Significance`
  - `## Need for Righteous Deeds`
  - `## Profit and Loss`
  - (section names vary per surah — preserve the original)
- Cross-links: `[[quran-wiki/surah-103-al-asr]]`, concept pages, related surahs
- References & Sources section at bottom

### Concept Page (`type: concept`)
- Cross-cutting themes Fi Zilal develops across multiple surahs
- e.g., `concepts/iman-and-dignified-humanity.md` — the faith-as-human-dignity motif Qutb builds across Al-Asr and elsewhere
- Links back to every surah page that develops the concept

## Quality Gates
- Every new page must have YAML frontmatter
- Every new surah page must link to its quran-wiki counterpart
- Every new page must be added to `index.md`
- Every action must be appended to `log.md`
- Arabic terms must include original script with diacritics
- Local-only git commits — never push to GitHub without explicit instruction