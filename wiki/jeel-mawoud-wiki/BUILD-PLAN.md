# Jeel Mawoud LLM Wiki — Build Plan

> الجيل الموعود بالنصر والتمكين by Dr. Majdi al-Hilali
> Full-stage plan for creating a comprehensive, accurate, and reliable LLM Wiki

## Guiding Principles

1. **Source fidelity above all** — Every claim traced back to a specific page/chapter of the Arabic original
2. **Arabic-primary** — All concepts defined with original Arabic terms + transliteration + Malay/English gloss
3. **Cross-wiki integration** — Link to Quran Wiki (foundation verses), Qaradawi Library (shared Islamic concepts), To Be a Muslim (overlapping tarbiyyah themes)
4. **No hallucination** — If the source text is ambiguous, say so. Never fabricate hadith grades or verse references
5. **Scholarly rigor** — Follow Tarbiyyah CLAUDE.md source tiers; cite Qur'an with surah:verse, hadith with source

## Wiki Location

```
/root/tarbiyyah/jeel-mawoud-wiki/
```

Will be symlinked into the LLM Wiki hub at `~/.llm-wiki/religious/jeel-mawoud/` and registered in `wikis.yaml`.

---

## Stage 0: Scaffold & Schema (Foundation)

**Goal:** Create the wiki skeleton with conventions locked down before any content generation.

### Deliverables
- [ ] `SCHEMA.md` — Domain conventions, tag taxonomy, frontmatter spec, page types
- [ ] `index.md` — Empty catalog with sectioned header
- [ ] `log.md` — Creation entry
- [ ] `AGENTS.md` — Project identity for agent sessions
- [ ] `.config/books.yaml` — Book registry (1 book: jeel-mawoud)
- [ ] Directory structure: `raw/`, `entities/`, `concepts/`, `comparisons/`, `queries/`
- [ ] `raw/pdfs/` — Move Arabic PDF here as immutable source
- [ ] `raw/extracted/` — Move cleaned extracted text here

### Tag Taxonomy (Domain-Specific)

| Category | Tags |
|----------|------|
| Structural | `chapter`, `overview`, `introduction`, `conclusion`, `index` |
| Core Concepts | `jeel-mawoud`, `nasr`, `tamkin`, `iman`, `ikhlas`, `mahabbah`, `khawf`, `ibadah`, `tawadu`, `zuhd`, `jihad`, `sabr`, `itidal`, `ukhuwwah` |
| Methodology | `tarbiyyah`, `dakwah`, `kaderisasi`, `manhaj`, `asbab`, `qa-idah` |
| Quranic | `ayah`, `tafsir`, `quranic-promise` |
| Historical | `sahabah`, `first-generation`, `seerah`, `islamic-history` |
| Meta | `comparison`, `cross-wiki`, `concept-definition`, `scholar-biography` |

### Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
| `chapter` | `entities/` | One per chapter — detailed summary with source lines |
| `overview` | `entities/` | Book overview page |
| `scholar` | `entities/` | Author biography |
| `concept` | `concepts/` | Thematic concept pages (10 core + derived) |
| `comparison` | `comparisons/` | Cross-wiki thematic comparisons |
| `query` | `queries/` | Filed research results |

### Frontmatter Spec

```yaml
---
title: "Page Title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: chapter | overview | scholar | concept | comparison | query
tags: [from taxonomy above]
sources: ["raw/extracted/jeel-mawoud-full.txt:page_start-page_end"]
confidence: high | medium | low
# Chapter pages only:
chapter: 1-5
pages: "10-23"
# Concept pages only:
arabic: "الإخلاص"
transliteration: "al-Ikhlas"
---
```

### Verification
- All directories exist
- SCHEMA.md references no broken wikilinks (escape examples with backticks)
- books.yaml has correct metadata (ISBN, publisher, page count, Archive.org ID)

---

## Stage 1: Raw Source Preparation (Text Cleaning & Chapter Splitting)

**Goal:** Produce clean, chapter-separated source files that are the immutable ground truth for all subsequent wiki pages.

### 1.1 Full Text Re-Extraction
- Re-extract from PDF with improved pipeline:
  - Strip repeated headers (title + author lines on every page)
  - Strip page numbers
  - Preserve Quranic diacritical marks (tashkeel)
  - Mark page boundaries clearly: `--- PAGE N ---`
  - Output: `raw/extracted/jeel-mawoud-full.txt`

### 1.2 Chapter Splitting
Split the full text into per-chapter files using the verified page boundaries:

| Chapter | File | Pages | Notes |
|---------|------|-------|-------|
| Introduction | `ch-00-introduction.txt` | 5–7 | المقدمة |
| Chapter 1 | `ch-01-limadha-al-jil-al-mawud.txt` | 10–23 | لماذا الجيل الموعود؟ |
| Chapter 2 | `ch-02-sifat-al-jil-al-mawud.txt` | 24–97 | مع صفات الجيل الموعود |
| Chapter 3 | `ch-03-kayfa-tuhaqqaq.txt` | 98–145 | كيف تحقق صفات الجيل الموعود؟ |
| Chapter 4 | `ch-04-al-jil-al-awwal.txt` | 146–175 | الجيل الأول وأدوات التغيير |
| Chapter 5 | `ch-05-ayna-nahnu.txt` | 175–191 | أين نحن من الجيل الموعود؟ |
| Conclusion | `ch-06-conclusion.txt` | 192–193 | الخاتمة |

Divider pages (8, 9, 23, 96, 97, 145, 173, 174, 191) are blank in the original — skip them.
TOC pages (194–201) are index, not content — store separately as `raw/extracted/toc.txt`.

### 1.3 Unicode Normalization
- Normalize presentation forms (FB50-FDFF) to standard Arabic (0600-06FF) for search consistency
- Preserve Uthmani Quranic characters (ٱ, ـ) — do NOT strip these
- Verify: normalized text should have higher Arabic ratio (>85%) after header stripping

### 1.4 Quality Gate
- [ ] Each chapter file starts with the correct chapter title
- [ ] Each chapter file ends at the correct boundary (no overlap with next chapter)
- [ ] No garbled text in any chapter file
- [ ] Total character count per chapter is reasonable (no empty or trivial files)
- [ ] Quranic verses with tashkeel are intact

---

## Stage 2: Entity Pages (Book Overview + Author + Chapters)

**Goal:** Create structured entity pages for the book itself, the author, and each chapter.

### 2.1 Book Overview Page
`entities/overview-jeel-mawoud.md`
- Full metadata (Arabic/English/Malay titles, author, publisher, ISBN, editions)
- Central thesis: Allah's promise of victory is conditional on a generation fulfilling specific attributes
- Chapter index with wikilinks to each chapter page
- Cross-references: `[[qaradawi-library/...]]` for shared themes, `[[quran-wiki/...]]` for foundation verses

### 2.2 Author Biography Page
`entities/scholar-majdi-al-hilali.md`
- Full biography with Arabic name (مجدي الهلالي)
- Intellectual context: da'wah movement, tarbiyyah focus, medical background
- Bibliography: 30+ books with brief descriptions
- Distinctive contributions: practical tarbiyyah, iman-building, youth-oriented
- Cross-references to Qaradawi Library where themes overlap

### 2.3 Chapter Pages (7 pages)
One per chapter + introduction + conclusion, each containing:

**Template:**
```markdown
---
title: "Chapter N — Arabic Title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: chapter
tags: [chapter, ...relevant domain tags]
sources: ["raw/extracted/ch-NN-slug.txt"]
chapter: N
pages: "NN-MM"
---

## Summary
[150-250 word scholarly summary from source text]

## Key Arguments
[Bullet list of the chapter's main arguments, each traced to source pages]

## Quranic Evidence
[Table: Verse | Context in Chapter | Page Reference]

## Hadith Evidence
[Table: Hadith | Source | Grade (if known) | Page Reference]

## Key Concepts Introduced
[Wikilinks to concept pages: [[concept-ikhlas]], [[concept-mahabbah]], etc.]

## Sahabah Examples
[Key companion stories cited in this chapter with page references]

## Cross-References
- Related chapters: [[ch-NN-slug]]
- Related concepts: [[concept-xxx]]
- Cross-wiki: [[quran-wiki/surah-...]] | [[qaradawi-library/concept-xxx]]
```

**Execution:** Delegate in batches of 2-3 chapters per subagent. Each subagent receives:
- The chapter's full extracted text as context
- The template above
- A list of concept slugs to use for wikilinks
- Cross-wiki link targets (Quran surahs, Qaradawi concepts)

### 2.4 Quality Gate
- [ ] 7 chapter pages created with correct frontmatter
- [ ] Every chapter page has ≥2 outbound wikilinks
- [ ] Every chapter page references source pages in `sources:` field
- [ ] Book overview page links to all chapter pages
- [ ] Author page links to overview page

---

## Stage 3: Concept Pages (Core Knowledge Graph)

**Goal:** Create concept pages for all key Islamic concepts discussed in the book. These are the wiki's highest-value pages — they synthesize the book's treatment of each concept with cross-references to other wikis.

### 3.1 Core Concepts (10 — from Chapter 2's 10 attributes)

| # | Arabic | Transliteration | English | File |
|---|--------|----------------|---------|------|
| 1 | الإخلاص | al-Ikhlas | Sincerity to Allah | `concepts/concept-ikhlas.md` |
| 2 | محبة الله | Mahabbatullah | Love of Allah | `concepts/concept-mahabbah.md` |
| 3 | الخوف من الله | Khawfullah | Fear of Allah | `concepts/concept-khawf.md` |
| 4 | العبادة | al-Ibadah | Worship (Monks of the Night) | `concepts/concept-ibadah.md` |
| 5 | التواضع | at-Tawadu' | Humility | `concepts/concept-tawadu.md` |
| 6 | الزهد | az-Zuhd | Asceticism/Worldly Detachment | `concepts/concept-zuhd.md` |
| 7 | الجهاد | al-Jihad | Striving/Struggle | `concepts/concept-jihad.md` |
| 8 | الصبر والثبات | as-Sabr wa ath-Thabat | Patience & Steadfastness | `concepts/concept-sabr.md` |
| 9 | الاعتدال والتوازن | al-I'tidal wa at-Tawazun | Moderation & Balance | `concepts/concept-itidal.md` |
| 10 | الترابط والأخوة | at-Tarabut wa al-Ukhuwwah | Cohesion & Brotherhood | `concepts/concept-ukhuwwah.md` |

### 3.2 Methodology Concepts (from Chapters 1, 3, 5)

| Arabic | Transliteration | English | File |
|--------|----------------|---------|------|
| الجيل الموعود | al-Jil al-Maw'ud | The Promised Generation | `concepts/concept-jeel-mawoud.md` |
| النصر والتمكين | an-Nasr wa at-Tamkin | Victory & Empowerment | `concepts/concept-nasr-tamkin.md` |
| الأخذ بالأسباب | al-Akhdhu bil Asbab | Taking All Necessary Causes | `concepts/concept-asbab.md` |
| القاعدة الصلبة | al-Qa'idah as-Salbah | Solid Foundation | `concepts/concept-qa-idah.md` |
| المعرفة بالله | al-Ma'rifah billah | Knowledge of Allah | `concepts/concept-marifah.md` |
| المعرفة بالنفس | Ma'rifat an-Nafs | Knowledge of Self | `concepts/concept-ma-rifat-an-nafs.md` |
| الإيمان بالآخرة | al-Iman bil Akhirah | Faith in the Hereafter | `concepts/concept-iman-al-akhirah.md` |
| الحكمة | al-Hikmah | Wisdom | `concepts/concept-hikmah.md` |
| التربية | at-Tarbiyyah | Education/Nurturing | `concepts/concept-tarbiyyah.md` |
| تزكية النفس | Tazkiyat an-Nafs | Soul Purification | `concepts/concept-tazkiyah.md` |

### 3.3 Cross-Wiki Integration Concepts (shared with existing wikis)

These concepts already exist in Qaradawi Library or Quran Wiki. Create Jeel Mawoud-specific pages that **add the book's unique perspective**, then link across:

| Concept | Exists In | Jeel Mawoud Addition | File |
|---------|-----------|----------------------|------|
| الإخلاص (Ikhlas) | Qaradawi Library | Hilali's focus on ikhlas as the FIRST attribute of the promised generation | `concept-ikhlas.md` |
| الصبر (Sabr) | Qaradawi Library | Hilali's treatment of sabr as path of dakwah carriers | `concept-sabr.md` |
| الجهاد (Jihad) | Qaradawi Library | Hilali's emphasis on jihad with clarity of purpose (وضوح الهدف) | `concept-jihad.md` |
| التربية (Tarbiyyah) | Qaradawi Library | Hilali's practical tarbiyyah methodology (educator + environment + curriculum) | `concept-tarbiyyah.md` |
| التواضع (Tawadu') | Qaradawi Library (as humility) | Hilali's three-dimension: with Allah, self, people | `concept-tawadu.md` |

### 3.4 Concept Page Template

```markdown
---
title: "Concept Name (Arabic)"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept
tags: [concept, ...domain tags]
sources: ["raw/extracted/ch-NN-slug.txt:pages XX-YY"]
arabic: "Arabic term"
transliteration: "transliteration"
confidence: high
---

## Definition
[200-400 word scholarly definition with Arabic root meaning]

## Al-Hilali's Treatment
[The book's specific arguments and evidence — with page references]

## Quranic Evidence
[Table: Verse | How the book uses it | Page]

## Hadith & Sahabah Examples
[Key narrations and companion stories cited]

## Related Concepts
- [[concept-xxx]] — brief relationship
- [[concept-yyy]] — brief relationship

## Cross-Wiki References
- [[qaradawi-library/concept-xxx|Qaradawi on XXX]] — comparison point
- [[quran-wiki/surah-NNN-xxx|Surah XXX]] — foundation verse
- [[to-be-muslim/...|To Be a Muslim on XXX]] — overlapping theme
```

### 3.5 Quality Gate
- [ ] All 20 concept pages created with full frontmatter
- [ ] Every concept page has `arabic:` and `transliteration:` fields
- [ ] Every concept page has ≥3 outbound wikilinks
- [ ] Every concept page has ≥1 cross-wiki reference
- [ ] No concept page is a stub — all have substantive definitions
- [ ] Quranic verse references verified against Quran Wiki (surah:verse format)

---

## Stage 4: Cross-Reference & Link Graph (Connectivity)

**Goal:** Build the wikilink graph so pages connect to each other and to the broader wiki federation.

### 4.1 Internal Cross-References
- Chapter pages → concept pages (each attribute linked)
- Concept pages → chapter pages (where the concept is discussed)
- Overview page → all chapters and concepts
- Author page → overview page

### 4.2 Cross-Wiki Bridge Pages
Create `comparisons/` pages for themes spanning multiple wikis:

| Comparison | Wikis Involved | File |
|------------|---------------|------|
| Tarbiyyah Methodology: Hilali vs Qaradawi | Jeel Mawoud + Qaradawi Library | `comparisons/comparison-tarbiyyah-methodology.md` |
| Iman Building: Practical vs Theoretical | Jeel Mawoud + To Be a Muslim | `comparisons/comparison-iman-building.md` |
| The Promised Generation in Qur'an | Jeel Mawoud + Quran Wiki | `comparisons/comparison-promised-generation-quran.md` |

### 4.3 Quranic Verse Verification
For every Quranic verse cited in the book (11 foundation verses identified):
- Cross-check surah:verse against Quran Wiki
- Verify Arabic text matches (using Al Quran Cloud API)
- Add wikilinks from chapter pages to specific Quran Wiki surah pages

### 4.4 Link Integrity Check
- Run lint: no broken wikilinks
- Run lint: no orphan pages
- Ensure every page has ≥2 inbound links

### 4.5 Quality Gate
- [ ] All internal wikilinks resolve to existing pages
- [ ] All cross-wiki wikilinks resolve to verified pages in target wikis
- [ ] Orphan rate <10%
- [ ] 3 comparison pages created
- [ ] All 11 foundation verses cross-checked and linked

---

## Stage 5: Deep Content Pass (Accuracy & Depth)

**Goal:** Transform summaries into scholarly-grade content. Every claim verified, every citation traced.

### 5.1 Chapter Deep-Dives
Re-read each chapter's full source text and enrich:
- Expand summaries from 150→400 words
- Add detailed argument structure (premises → conclusions)
- Extract ALL Quranic citations with exact verse references
- Extract ALL hadith citations with source attribution
- Extract ALL sahabah stories with narrator names
- Add footnotes for page-specific references

### 5.2 Concept Deep-Dives
Re-read relevant chapter sections and enrich:
- Expand definitions from 200→500 words
- Add Arabic root etymology (e.g., خ-ل-ص for ikhlas)
- Add classical scholarly context (Ibn Taymiyyah, al-Ghazali, al-Nawawi where the book references them)
- Add the book's distinctive positions vs. general scholarly consensus
- Add practical implications section (what does this mean for the reader?)

### 5.3 Quranic Citation Audit
- Extract every surah:verse reference from the text
- Verify each against Al Quran Cloud API
- For each, create a mini-entry: verse text (Arabic) + book's usage + page reference
- Flag any discrepancies (misattributed verse numbers, etc.)

### 5.4 Quality Gate
- [ ] All chapter summaries ≥400 words
- [ ] All concept definitions ≥500 words
- [ ] Every Quranic citation has surah:verse verified
- [ ] Every hadith citation has source attributed (or flagged if source unclear in original)
- [ ] No unverified claims in any page

---

## Stage 6: Federation & Navigation (Hub Integration)

**Goal:** Register the wiki in the LLM Wiki hub and enable cross-wiki search.

### 6.1 Hub Registration
- Add entry to `~/.llm-wiki/.config/wikis.yaml` under `religious:`
- Create symlink: `~/.llm-wiki/religious/jeel-mawoud → /root/tarbiyyah/jeel-mawoud-wiki`
- Update hub `index.md` with Jeel Mawoud entry

### 6.2 Cross-Wiki Bridge Page
Create/update `meta/concepts/cross-wiki-bridge-jeel-mawoud.md` in the hub:
- Map shared concepts between Jeel Mawoud ↔ Qaradawi Library
- Map shared concepts between Jeel Mawoud ↔ Quran Wiki
- Map shared concepts between Jeel Mawoud ↔ To Be a Muslim
- Provide federated query templates

### 6.3 Federated Query Test
- Verify `python3 ~/.llm-wiki/.tools/federated_query.py "ikhlas" --rank` returns results from Jeel Mawoud
- Verify `python3 ~/.llm-wiki/.tools/federated_query.py "tarbiyyah" --rank` returns results from multiple wikis

### 6.4 Quality Gate
- [ ] Wiki registered in `wikis.yaml`
- [ ] Symlink working: `ls ~/.llm-wiki/religious/jeel-mawoud/SCHEMA.md`
- [ ] Federated queries return Jeel Mawoud results
- [ ] Hub index.md updated

---

## Stage 7: Final Audit & Polish

**Goal:** Zero-defect delivery. Lint-clean, cross-referenced, ready for production use.

### 7.1 Full Lint Run
- Frontmatter validation (all required fields present)
- Tag audit (all tags in SCHEMA.md taxonomy)
- Broken wikilink scan (internal + cross-wiki)
- Orphan page scan (0 acceptable)
- Page size audit (no page >200 lines without splitting)
- Stale content audit (all `updated` dates current)

### 7.2 Content Accuracy Review
- Spot-check 10 random claims against source text
- Spot-check all Quranic verse references
- Verify author biography dates from web search
- Verify book metadata (ISBN, publisher, page count)

### 7.3 Navigation Polish
- `index.md` has every page listed with one-line summary
- `log.md` has all actions chronologically
- `SCHEMA.md` reflects actual state

### 7.4 Final Stats Report
```
Total pages: N
  - Entity pages: N (1 overview + 1 scholar + 7 chapters)
  - Concept pages: N (20)
  - Comparison pages: N (3)
  - Navigation pages: 3 (index, log, SCHEMA)
Total wikilinks: N
Orphan rate: X%
Cross-wiki links: N
Quranic citations verified: N/N
```

### 7.5 Quality Gate
- [ ] Lint: 0 critical issues, 0 broken links, 0 orphans
- [ ] Accuracy: 100% Quranic citations verified
- [ ] Completeness: every chapter + concept + comparison page created
- [ ] Federation: hub registered, federated queries working

---

## Execution Strategy

### Parallelism Model

| Stage | Parallelizable? | Delegation Pattern |
|-------|----------------|-------------------|
| 0: Scaffold | No | Single agent (sequential setup) |
| 1: Source Prep | Partial | Text extraction = single; chapter split = script |
| 2: Entity Pages | Yes | 2-3 chapters per subagent (3 batches) |
| 3: Concept Pages | Yes | 5 concepts per subagent (4 batches) |
| 4: Cross-References | Partial | Bridge pages = delegated; verification = single |
| 5: Deep Content | Yes | 2 chapters per subagent (4 batches) |
| 6: Federation | No | Single agent (hub operations) |
| 7: Final Audit | No | Single agent (lint + report) |

### Subagent Prompt Template (for Stages 2, 3, 5)

Every delegated subagent receives:
1. **Source text** — The relevant chapter/concept's full extracted text
2. **Template** — The page template with required sections
3. **Cross-reference targets** — Concept slugs and cross-wiki links to include
4. **Quality rules** — "Every claim must have a page reference. Every Quranic verse must have surah:verse. No fabricated content."
5. **Language** — "Write in English with Arabic terms in original script + transliteration."

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Arabic text quality issues | Stage 1 includes Unicode normalization + manual spot-check |
| Subagent fabricates hadith grades | Template requires: "If grade not stated in source, write 'Grade not specified in source' — never guess" |
| Cross-wiki links break when other wikis change | Use stable slugs (surah-NNN-name, concept-xxx) not page titles |
| Orphan explosion after batch creation | Stage 4 includes mandatory link integrity check + orphan resolution |
| Concept duplication with Qaradawi Library | Stage 3.3 explicitly maps overlap; each wiki gets its own perspective page |

---

## Estimated Timeline

| Stage | Duration | Cumulative |
|-------|----------|------------|
| 0: Scaffold | 15 min | 15 min |
| 1: Source Prep | 30 min | 45 min |
| 2: Entity Pages | 45 min | 1.5 hr |
| 3: Concept Pages | 60 min | 2.5 hr |
| 4: Cross-References | 30 min | 3 hr |
| 5: Deep Content | 60 min | 4 hr |
| 6: Federation | 20 min | 4.3 hr |
| 7: Final Audit | 20 min | ~4.5 hr |

**Total: ~4.5 hours of active agent work across 7 stages.**