# QA Review: Surah Ash-Shams (091) Curated Page

**File reviewed:** `surahs/surah-091-ash-shams.md`  
**Raw source:** `raw/surah-091-ash-shams.md`  
**Review date:** 2026-07-20  
**Status:** Needs cleanup before publication

---

## 1. Frontmatter — VERIFIED

Lines 1–13 are well-formed YAML with required fields:

- `title`, `type`, `surah_number: 091`, `surah_name: ash-shams`, `revelation: makki`, `verse_count: 15` — all correct.
- `sources: [raw/surah-091-ash-shams.md]` — present.
- `confidence: high` — **recommend lowering to `medium`** because of the PDF garbage and transcription errors below.

## 2. Verse Text — VERIFIED BUT UNMARKED

Lines 28–42 contain all 15 verses in the correct order and the English translation matches the raw source. **Issue:** the clean verse block carries **no provenance marker**, while the rest of the article uses `^[raw/surah-091-ash-shams.md]`. Add markers to each verse or a single block-level marker.

## 3. PDF Garbage Tokens

A duplicate, corrupted verse fragment block appears at lines 48–80 and should be removed entirely. It contains ASCII garble after each verse:

| Line | Garbage token(s) | Context |
|------|------------------|---------|
| 48 | `91_` | Stray chapter number |
| 50 | `**Ash-Shams**` | Redundant heading |
| 52 | `### Al-Shams` | Stray sub-heading before real sections |
| 54 | `y8ptu` | After v.1 |
| 56 | `ys)9u` | After v.2 |
| 58 | `p]9u` | After v.3 |
| 60 | `y8tt` | After v.4 |
| 62 | `y9tt/ tu u9u` | After v.5 |
| 64 | `y8yss tu F{u` | After v.6 |
| 66 | `y1y tu` | After v.7 |
| 68 | `y1u)s?u yug yyo;r's` | After v.8 |
| 70 | `y8.y` | After v.9 |
| 72 | `y9y` | After v.10 |
| 74 | `y1us/ rO Mt/x` | After v.11 |
| 76 | `y]yt7/` | After v.12 |
| 78 | `yu)u ts)s`, `tyys ys)ys` | After v.13–14 |
| 80 | `yt6 ss` | After v.15 |

These are corrupted Arabic transliteration fragments left over from `pdftotext` extraction.

## 4. Garbled / Corrupted Text

Systematic diacritic loss and transcription errors throughout the commentary:

| Line | Curated text | Should be | Issue |
|------|--------------|-----------|-------|
| 74 | `Thamd` | `Thamūd` | Missing macron |
| 84 | `srah` (×1) | `sūrah` | Missing macron |
| 96 | `srah` / `srahs` (×3) | `sūrah` / `sūrahs` | Missing macron |
| 100 | `srah` (×1) | `sūrah` | Missing macron |
| 106 | `srah`, `Srah 76`, `Srah 38` | `sūrah`, `Sūrah 76`, `Sūrah 38` | Missing macron |
| 110 | `Srah 74`, `Srah 13` | `Sūrah 74`, `Sūrah 13` | Missing macron |
| 110 | `am creating man from clay` | `'I am creating man from clay` | Missing opening quote |
| 110 | `peoples lot` | `people's lot` | Missing apostrophe |
| 114 | `ha made` | `has made` | Missing `'s` |
| 114 | `peoples lot` | `people's lot` | Missing apostrophe |
| 120 | `Thamd` | `Thamūd` | Missing macron |
| 120 | `li` | `Şāliĥ` | Prophet's name corrupted |
| 120 | `Srah 89` | `Sūrah 89` | Missing macron |
| 124 | `Thamds` | `Thamūd's` | Missing macron and apostrophe |

Also, many inline Qur’anic snippets lack quotation marks (e.g., lines 106, 110, 114, 120, 124), making them hard to distinguish from Qutb’s prose.

## 5. Broken Markdown

Stray PDF page headers are inserted mid-section, breaking the narrative flow:

| Line | Problem |
|------|---------|
| 52 | `### Al-Shams` — orphan heading in the garbage block |
| 92 | `### Al-Shams (The Sun)` — splits the *God’s Solemn Oath* paragraph |
| 98 | `### Al-Shams (The Sun)` — splits the *God’s Solemn Oath* paragraph |
| 108 | `### Al-Shams (The Sun)` — splits the *A Look into the Human Soul* paragraph |
| 112 | `### Al-Shams (The Sun)` — splits the *A Look into the Human Soul* paragraph |
| 122 | `### Al-Shams (The Sun)` — splits the *Historical Example* paragraph |

**Required section headers are present** (`Overview`, `God's Solemn Oath`, `A Look into the Human Soul`, `Historical Example`, `References & Sources`), but the first three sections are interrupted by the stray headings above.

## 6. Missing Provenance Markers

- **Lines 28–42 (clean verse block):** no `^[raw/…]` markers.
- **Lines 88–94 (*God’s Solemn Oath* opening verse quote):** the quote is partly at line 90 and partly at line 94, with a stray heading in between; only the second half has a marker. The whole quote should be contiguous and marked once.

## 7. References & Sources — VERIFIED

Lines 128–152 contain a structured `## References & Sources` section with Layer 1–3 sources, secondary wiki notes, related surahs, and cross-cutting concept links. All entries are valid markdown and point to existing raw/cross-reference paths.

---

## Summary & Recommendation

The curated page has the correct **structure** and **content**, but it still carries a significant amount of **PDF extraction debris** and **transcription errors**. Before it can be considered publication-ready:

1. **Delete** the entire garbage block at lines 48–80.
2. **Restore diacritics:** `srah` → `sūrah`, `Thamd` → `Thamūd`, `li` → `Şāliĥ`.
3. **Fix apostrophe/quote errors:** `peoples` → `people's`, `ha made` → `has made`, `am creating` → `'I am creating`, add quotes around inline verse snippets.
4. **Remove** the six stray `### Al-Shams (The Sun)` mid-paragraph headers.
5. **Add provenance markers** to the clean verse block and consolidate the opening verse quote under *God’s Solemn Oath*.
6. **Lower `confidence:` to `medium`** until the cleanup is completed.
