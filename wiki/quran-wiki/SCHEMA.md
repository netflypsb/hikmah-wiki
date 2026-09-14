---
name: Quran Wiki Schema
domain: Quranic Studies — the Holy Qur'an as revelation, text, exegesis, and thematic universe
created: 2026-05-10
version: 1.0.0
---

# Wiki Schema — Quranic Studies

## Domain
This wiki covers the Holy Qur'an in its full dimension:
- **Textual**: Uthmani rasm, verse divisions, surah structure, linguistic features
- **Thematic**: Major themes (tawhid, risalah, akhirah, divine attributes)
- **Narrative**: Stories of prophets, nations, parables
- **Exegetical**: Tafsir, asbab al-nuzul, qiraat variations
- **Structural**: Makki/Madani classification, juz/hizb/page mappings
- **Comparative**: Translations, scholarly approaches, cross-surah analysis

## Conventions

### File Naming
- Surah pages: `surah-NNN-[english-name].md` (e.g., `surah-002-al-baqarah.md`)
- Verse pages: `surahs/[surah-slug]/verse-NNN.md` (created on-demand when content exists)
- Theme pages: `entities/themes/[theme-name].md`
- Prophet pages: `entities/prophets/[prophet-name].md`
- Story pages: `entities/stories/[story-name].md`
- Concept pages: `concepts/[concept-name].md`
- Comparison pages: `comparisons/[comparison-name].md`
- Query pages: `queries/[query-name].md`
- All lowercase, hyphens, no spaces or diacritics in filenames.

### Frontmatter (every wiki page)
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: surah | verse | theme | prophet | story | concept | comparison | query | name
tags: [from taxonomy below]
sources: [raw/metadata/quran-index.json, raw/translations/surah_NNN/ayah_NNN.json, raw/tafsir/NNN.jsonl]
confidence: high | medium | low
contested: true           # set when scholars differ
contradictions: [page-slug]
---
```

### Cross-References
- **Minimum 2 outbound ``wikilinks`` per page** (except index.md and log.md)
- Every surah page links to at least 2 themes + 2 related surahs
- Every theme page links to all surahs where it appears prominently
- Every prophet page links to all surahs where they are mentioned
- Use short wikilinks for intra-wiki: `surah-002-al-baqarah`
- Use full paths for clarity: `Tawhid`

### Arabic Text
- Include original Arabic with tashkeel (تَشْكِيل) for precision
- Use code blocks for verse text to preserve RTL rendering
- Transliterate key terms when helpful: *tawhid* (تَوْحِيد)

### Provenance
- Pages synthesizing 3+ sources append `^[raw/tafsir/NNN.jsonl]` markers
- Translation comparisons cite edition IDs: `en.pickthall`, `en.sahih`, `en.asad`, `en.yusufali`, `ms.basmeih`
- Tafsir citations name the mufassir: Ibn Kathir, Tafsir Muyassar

### Update Policy
- When new tafsir or translation is added, bump `updated` date
- Contradictions between tafasir are noted with dates and sources
- Mark `contested: true` and list `contradictions:` when scholars differ

## Tag Taxonomy

### Structural Tags
- `surah` — Surah overview pages
- `verse` — Individual verse deep-dives
- `juz` — Juz (para) boundaries and themes
- `ruku` — Ruku groupings
- `page` — Mushaf page references (604-page Madani)
- `makki` — Meccan revelation
- `madani` — Medinan revelation

### Content Tags
- `command` — Divine command (amr)
- `prohibition` — Divine prohibition (nahy)
- `promise` — Promise of reward (wa'd)
- `warning` — Warning of punishment (wa'id)
- `story` — Narrative of prophets/nations
- `parable` — Mathal (metaphor/parable)
- `oath` — Qasam (divine oath)
- `rhetorical-device` — Iltifat, tashbeeh, etc.
- `dialogue` — Conversational passages
- `law` — Legal/legislative verse

### Thematic Tags
- `tawhid` — Divine Oneness
- `risalah` — Prophethood and messengership
- `akhirah` — Afterlife, resurrection, judgement
- `jannah` — Paradise
- `jahannam` — Hellfire
- `iman` — Faith, belief
- `kufr` — Disbelief
- `shirk` — Polytheism
- `salah` — Prayer
- `sawm` — Fasting
- `zakat` — Charity
- `hajj` — Pilgrimage
- `jihad` — Struggle/striving
- `adl` — Justice
- `rahma` — Mercy
- `qadr` — Divine Decree
- `shukr` — Gratitude
- `sabr` — Patience
- `taqwa` — God-consciousness
- `ilm` — Knowledge
- `dua` — Supplication
- `dhikr` — Remembrance of Allah

### Entity Tags
- `prophet` — Prophet biography/mentions
- `angel` — Angelic beings
- `nation` — Historical nations (Bani Israel, Thamud, etc.)
- `battle` — Military events mentioned
- `miracle` — Miraculous events
- `name-of-allah` — Divine Name/Attribute

### Meta Tags
- `translation` — Translation analysis
- `tafsir` — Exegetical commentary
- `asbab-al-nuzul` — Occasions of revelation
- `qiraat` — Reading variants
- `comparison` — Side-by-side analysis
- `query` — Research question result

## Page Thresholds
- **Create a surah page** — always; all 114 exist
- **Create a verse page** — when the verse has tafsir, thematic significance, or is referenced in 2+ other pages
- **Create a theme page** — when the theme appears in 3+ surahs
- **Create a prophet page** — when the prophet is mentioned in 2+ surahs
- **Create a story page** — when the narrative spans 2+ surahs or has multi-verse detail
- **Create a concept page** — when the concept is central to understanding 2+ surahs
- **DON'T create** pages for passing mentions, minor details, or single-verse trivia
- **Split a page** when it exceeds 200 lines

## Surah Pages
Every surah page includes:
- Overview (name meaning, revelation context, structural place)
- Key statistics (verses, juz, pages, rukus)
- Thematic summary (primary themes as ```wikilinks```)
- Key verses (ayahs with significance)
- Related surahs (at least 2 ```wikilinks```)
- Source references (raw/ entries)

## Theme Pages
Every theme page includes:
- Definition and Arabic root meaning
- Qur'anic basis (verses where it appears)
- Related themes (```wikilinks```)
- Tafsir perspectives
- Fiqh implications (brief, with link to future fiqh-wiki)

## Prophet Pages
Every prophet page includes:
- Qur'anic mentions (surah + verse references)
- Key narrative events
- Lessons from their story
- Related themes and stories (```wikilinks```)

## Concept Pages
Every concept page includes:
- Definition and scholarly context
- Qur'anic evidence
- Related concepts (```wikilinks```)
- Open questions or scholarly debates

## Comparison Pages
Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison
- Verdict or synthesis
- Sources

## Raw Sources
All files in `raw/` are **immutable**. The agent reads but never modifies them.
Raw frontmatter:
```yaml
---
source_url: https://api.alquran.cloud/v1/ayah/...
ingested: YYYY-MM-DD
sha256: <hex digest of body>
---
```

## Update Policy
When new information conflicts:
1. Check dates — newer tafasir generally don't supersede classical ones
2. For genuinely contradictory tafsir views, note both with dates and sources
3. Mark `contradictions:` in frontmatter
4. Flag for review in lint report
