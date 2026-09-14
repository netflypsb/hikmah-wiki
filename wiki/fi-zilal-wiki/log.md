# Fi Zilal al-Qur'an Wiki — Action Log

## 2026-07-19

- Wiki scaffolded at `/root/tarbiyyah/fi-zilal-wiki/` (SCHEMA.md, index.md, log.md, raw/, surahs/, concepts/)
- Raw source ingested: `raw/surah-103-al-asr.md` (from /mnt/c/Users/netfl/Downloads/asr-eng.md)
- Curated page generated: `surahs/surah-103-al-asr.md` — 4 thematic sections preserved (Overview, Faith and Its Significance, Faith in Human Life, Need for Righteous Deeds, Profit and Loss), provenance markers added, cross-linked to quran-wiki
- Symlink created: `~/.llm-wiki/religious/fi-zilal/` → `/root/tarbiyyah/fi-zilal-wiki/`
- Registered in `~/.llm-wiki/.config/wikis.yaml` under `religious:`
- Git initialized, initial commit

### Batch ingest: Surahs 101, 102, 104, 105

- Extracted text from 4 PDFs via pdftotext: Al-Takāthur (102), Al-Qāri'ah (101), Al-Humazah (104), Al-Fīl (105)
- Cleaned OCR artifacts (page numbers, form feeds, Arabic glyph fragments, line-break fragmentation)
- Raw sources written:
  - `raw/surah-101-al-qariah.md` (5,498 chars) — 2 sections: Overview, Determination of People's Fates
  - `raw/surah-102-al-takathur.md` (4,832 chars) — 1 section: Greedy Preoccupations
  - `raw/surah-104-al-humazah.md` (5,593 chars) — 1 section: Despicable Character
  - `raw/surah-105-al-fil.md` (22,293 chars) — 5 sections: Historical Background, A Rationalist View, Natural Phenomena and God's Power, A Momentous Event, The Arabs and Islam
- Curated surah pages generated with YAML frontmatter, verse text, thematic sections, provenance markers, cross-links to quran-wiki
- Concept pages built for cross-cutting themes across surahs 101–105:
  - `concepts/akhirah-and-the-fleeting-world.md` — triptych theme across 101/102/103
  - `concepts/jahiliyyah-and-wealth.md` — wealth-worship as jāhiliyyah hallmark across 102/104/105
  - `concepts/divine-protection-of-the-house.md` — God's sovereign protection of the Ka'bah across 103/105
  - `concepts/iman-and-dignified-humanity.md` — faith as human dignity and its loss across 103/104
- Index updated with 5 surahs + 4 concept pages
- Git commit pending

### Ingest: Surah 93 — Ad-Duha

- Source PDF: `/mnt/c/Users/netfl/Downloads/dhuha-eng.pdf` (5 pages, pp. 181–185 of the printed edition)
- Extracted via `pdftotext -layout`; raw source already ingested at `raw/surah-093-ad-duha.md` (12,130 chars, 231 lines) — Arabic verse text did not extract cleanly (embedded font issue); cross-reference to quran-wiki/raw/arabic/093-* noted in raw file
- Two thematic sections preserved: Overview, Unfailing Favours
- Curated page generated at `surahs/surah-093-ad-duha.md` (12,482 chars) with:
  - YAML frontmatter (surah_number 93, makki, 11 verses, 19 tags)
  - Verse text (all 11 verses, blockquote form)
  - Provenance markers `^[raw/surah-093-ad-duha.md]` on every sourced paragraph
  - Cross-link to [[quran-wiki/surah-093-ad-duha]]
  - Sub-sections added under each thematic section to surface key movements: *fatrat al-waḥy*, past favours as proof, the oath as frame, direct reassurance, three favours, transition to social instruction
  - References section with companion tafsir, Quran Wiki themes, related surahs (Al-Qadr 097 — the night of revelation as counterpart to Ad-Duha's pause in revelation)
- Index updated (row 93 inserted between 1 and 97)
- Git commit pending

### Batch ingest: Surahs 109, 112, 113 — Al-Kafirun, Al-Ikhlas, Al-Falaq

- Three PDFs already extracted; raw sources pre-existing:
  - `raw/surah-109-al-kafirun.md` (12,484 chars, pp. 273–277) — 1 thematic section: No Meeting of the Ways
  - `raw/surah-112-al-ikhlas.md` (12,354 chars, pp. 288–292) — 2 thematic sections: God's Absolute Oneness, A Complete Way of Life
  - `raw/surah-113-al-falaq.md` (12,287 chars, pp. 293–297) — 2 thematic sections: Overview, Protection against Evil
- Curated pages generated with full YAML frontmatter, verse text, provenance markers, cross-links to quran-wiki counterparts
- **Bidirectional cross-links surfaced** (Qutb's explicit theological pairings):
  - 109 ↔ 112: Al-Kafirun (negative demarcation of *tawḥīd* vs. *shirk*) + Al-Ikhlas (positive affirmation of *tawḥīd*); Prophet recited both in *sunnah* before *fajr*
  - 112 ↔ 113: the `Ā'ishah/Bukhārī bedtime *ḥadīth* ties Al-Ikhlas + Al-Falaq + An-Nas as a three-sūrah litany
  - 113 ↔ 114: the *mu'awwidhatayn* (two seeking-refuge *sūrahs*) — paired divine invitation to shelter
- Notable doctrinal positions preserved: Qutb's dismissal of the Labīd ibn al-A`ṣam magic-on-Prophet story (113) on `isma/qur'anic-arbitration/chronology grounds; *aḥad* vs. *wāḥid* semantic precision (112); *ghāsiq/waqab* linguistic analysis (113); critique of Sufi isolationism (112)
- Index updated (rows 109, 112, 113 inserted in numeric order between 97 and 114)
- Git commit pending

### Concept page: Tawḥīd as Complete Way of Life — Not Abstract Doctrine

- **Trigger:** user identified the recurring theme of *tawḥīd* as complete way of life across the Meccan *sūrahs* (especially 109, 112, 113, 114 + the existing 103/104 batch) and requested a dedicated, VERY THOROUGH and VERY ACCURATE concept page — "this is the CORE of Islam and is VERY CRUCIAL"
- **Full-source-utilisation audit executed** per skill protocol:
  - Layer 1 (quran-wiki raw): Ibn Kathir + Muyassar per-ayah for surahs 109, 112, 113, 114; curated surah pages for all 9 surahs
  - Layer 2 (quran-wiki curated): theme pages (tawhid.md, iman.md, shirk.md); concept pages (qasam, jawab-al-qasam, makki-vs-madani)
  - Layer 3 (Fi Zilal): raw + curated pages for surahs 1, 93, 97, 103, 104, 109, 112, 113, 114
  - Secondary wikis: Qaradawi Library (concept-tawhid, concept-faith, concept-ikhlas — corroborating); Jeel Mawoud (concept-ikhlas, concept-ibadah — corroborating); Meta-wiki (tawhid-in-creed-and-exegesis — framing); To-Be-a-Muslim (not found at expected path — documented as consulted-and-excluded)
- **Concept page generated:** `concepts/tawhid-as-complete-way-of-life.md` (42,659 chars) — the largest concept page in the wiki
  - Five-dimensional framework (creed, existential explanation, values/laws/ethics, liberation, community/protection) with Qutb's own words for each
  - Progressive unfolding table across 9 Meccan *sūrahs* (foundation → consolation → cosmic → human condition → inversion → demarcation → affirmation → daily refuge)
  - Critical distinction section: abstract doctrine vs. complete way of life — three reductions identified (Sufi deviation, *jāhiliyyah* compromise, scholarly reduction)
  - Cross-tafsir corroboration table: Qutb (existential/social), Qaradawi (legislative), al-Hilali (inner/political), Ibn Kathir (textual/creedal) — four traditions converging without contradiction
  - Prophetic pairing finding: Al-Kafirun + Al-Ikhlas as the daily *fajr* declaration (negative demarcation + positive affirmation); bedtime litany (Al-Ikhlas + Al-Falaq + An-Nas) — the full daily cycle framed by *tawḥīd*
  - *Tawḥīd* of causality (Qutb's epistemological dimension), *da'wah* implication (separation before invitation), protection dimension, social dimension
  - Eight-point summary: creed → existential explanation → values → liberation → daily practice → community → boundary → protection
  - 25+ Qur'anic cross-references and 10+ *aḥādīth* catalogued
- **Relationship to existing concept:** `iman-and-dignified-humanity` is the sub-theme (what faith does to the human being); this new page is the umbrella (what faith itself is). Cross-link added to iman-and-dignified-humanity page.
- **Cross-wiki links:** Qaradawi (concept-tawhid, concept-faith, concept-ikhlas), Jeel Mawoud (concept-ikhlas, concept-ibadah), Meta-wiki (tawhid-in-creed-and-exegesis)
- Index updated: new concept row added as umbrella (bolded) above iman-and-dignified-humanity
- Git commit pending

### Ingest: Surah 1 — Al-Fātiḥah

- Source PDF: `/mnt/c/Users/netfl/Downloads/al-fatihah-eng.pdf` (8 pages, A4, Nitro Pro, 322KB)
- Extracted via `pdftotext -layout` → 336 lines, 19,843 chars
- Arabic verse text did not extract cleanly from PDF (embedded Arabic font rendering issue); English commentary extracted perfectly. Noted in raw file with cross-reference to quran-wiki/raw/arabic/001-*.md for verified Uthmani Arabic.
- Raw source written: `raw/surah-001-al-fatihah.md` (18,588 chars) — 7 thematic sections preserved:
  - Overview (the surah as the seven oft-repeated verses, 15:87)
  - Verse 1: Basmalah — invocation of God's name, al-Raḥmān/al-Raḥīm
  - Verse 2: Praise and Lordship — `Umar narration, Lord of all the worlds, correction of polytheism
  - Verse 3: Mercy as the Creator-creation link — contrast with Greek mythology and Old Testament
  - Verse 4: Belief in the hereafter — the hereafter as balance
  - Verse 5: Liberation through worship — two categories of power, the Muslim and nature, Mount Uḥud
  - Verses 6–7: Guidance and the straight path
  - The ḥadīth of the fruits of prayer (the divine response to each verse)
- Curated page generated: `surahs/surah-001-al-fatihah.md` (11,252 chars) — structured as the seven fundamental principles (one per verse), provenance markers, cross-links to quran-wiki, Qur'anic cross-reference list
- Page numbers preserved from printed edition (pp. 1–8)
- Index updated with Surah 1 entry
- Git commit pending

### Batch ingest: 17 surah raw files (text extraction)

Source: 17 PDFs from `/mnt/c/Users/netfl/Downloads/`. Extracted via `pdftotext -layout`. 15 of 17 had text layers; 2 (Ar-Rahman, Ghafir) were image-based and required OCR (running separately).

Text-extracted surahs (15):

| Surah | # | Pages | Chars | Raw file |
|-------|---|-------|-------|----------|
| Ash-Shams | 91 | 7 | 18,185 | surah-091-ash-shams.md |
| Ya-Sin | 36 | 38 | 105,688 | surah-036-ya-sin.md |
| As-Sajdah | 32 | 24 | 65,436 | surah-032-as-sajdah.md |
| Luqman | 31 | 35 | 94,245 | surah-031-luqman.md |
| Ar-Rum | 30 | 42 | 120,032 | surah-030-ar-rum.md |
| Al-Furqan | 25 | 65 | 185,649 | surah-025-al-furqan.md |
| Al-Kahf | 18 | 72 | 202,326 | surah-018-al-kahf.md |
| Al-Alaq | 96 | 14 | 37,868 | surah-096-al-alaq.md |
| Al-Qadr | 97 | 4 | 9,149 | surah-097-al-qadr.md |
| Al-Kafirun | 109 | 5 | 11,912 | surah-109-al-kafirun.md |
| Al-Ikhlas | 112 | 5 | 11,847 | surah-112-al-ikhlas.md |
| Al-Falaq | 113 | 5 | 11,641 | surah-113-al-falaq.md |
| An-Nas | 114 | 4 | 8,408 | surah-114-an-nas.md |
| Ad-Duha | 93 | 5 | 11,476 | surah-093-ad-duha.md |
| Al-Layl | 92 | 7 | 17,526 | surah-092-al-layl.md |

OCR-required surahs (2, running in background):

| Surah | # | Pages | Status |
|-------|---|-------|--------|
| Ar-Rahman | 55 | 30 | OCR in progress (tesseract, 300 DPI) |
| Ghafir | 40 | 78 | OCR in progress (tesseract, 300 DPI) |

- Each raw file has a header with surah number, name, source PDF, extraction method, and a note directing to quran-wiki for verified Uthmani Arabic
- No curated surah pages created yet (per user instruction — some are very long)
- Index not yet updated (will update when curated pages are built)
- Git commit pending

### Ingest: Surah 97 — Al-Qadr (curated page)

- Raw source already extracted in the 17-surah batch: `raw/surah-097-al-qadr.md` (9,149 chars, 4 pages from qadr-eng.pdf, pp. 207–210)
- Curated page generated: `surahs/surah-097-al-qadr.md` — single thematic section preserved from the source:
  - A Most Distinguished Night (the Night of Power as cosmic communion; the three lights — Qur'ān, angels/Spirit, dawn; the blessed night in the Qur'anic constellation via 44:3-6 and 2:185; the name *Laylat al-Qadr* as both planning and rank; "better than a thousand months"; beyond human perception; humanity's loss when it overlooks the Night; Prophetic guidance on commemorating it in the last ten nights of Ramaḍān; worship linked with faith as the Islamic method of *tarbiyyah*)
- Subsections added to organize the single source section into navigable subthemes (the blessed night in the Qur'anic constellation, the name *Laylat al-Qadr*, beyond human perception, humanity's loss, the Prophetic guidance, worship linked with faith)
- Provenance markers `^[raw/surah-097-al-qadr.md]` on every subsection
- Cross-links: quran-wiki/surah-097-al-qadr (companion), quran-wiki entities/themes/qadr, rahma, command; related surahs Al-`Alaq (96) and Al-Fātiḥah (1)
- Qur'anic cross-references cited: 2:185, 44:3-6, 96 (first revelation)
- Two aḥādīth cited (Bukhārī & Muslim) on seeking the Night in the last ten nights and the reward of devoted worship
- Index updated with Surah 97 entry
- Git commit pending

**Cross-cutting concept note:** Al-Qadr (97) develops two themes that may eventually form concept pages: (1) *laylat-al-qadr* as cosmic-communion event — the Night as the moment when heaven and earth meet, with angels/Jibrīl descending; this recurs in the Ad-Dukhān 44:3-6 cross-reference and may link to a broader "revelation as cosmic event" concept if other relevant surahs are curated (e.g., Al-`Alaq 96). (2) *tarbiyyah-spiritual* — Qutb's emphasis on worship linked with faith as the Islamic educational method. This second theme already appears implicitly in Al-Asr (103)'s "faith as constitutive of human dignity" and An-Nas (114)'s "dhikr as the believer's weapon"; revisit when more surahs are curated to build a `concepts/tarbiyyah-worship-and-faith.md` page.

### Ingest: Surah 114 — An-Nas (curated page)

- Raw source already extracted in the 17-surah batch above: `raw/surah-114-an-nas.md` (8,692 chars, 4 pages from an-nas-eng.pdf)
- Curated page generated: `surahs/surah-114-an-nas.md` — 5 thematic sections preserved from the source:
  - The Lord of Mankind (the three divine attributes: Lord, Sovereign, God; mankind singled out for closeness to God's protection)
  - The Ancient Battle Between Man and Satan (Adam-Iblīs war; faith and dhikr as the believer's weapons; Ibn `Abbās ḥadīth)
  - Human Whisperers More Devilish Than the Devil (four types of human whisperer; the 'slinking' nature as intrinsic feebleness when confronted)
  - The Everlasting War (war till end of time; Qur'ānic scene 17:61-65 of Iblīs's challenge and God's response)
  - The Most Perfect Concept of the Battle (righteousness backed by God's power vs evil backed by a timid, retreating whisperer)
- Provenance markers `^[raw/surah-114-an-nas.md]` on every section; cross-links to quran-wiki counterpart, Al-Falaq (companion mu'awwidhatayn), and Quran Wiki theme pages
- Index updated with Surah 114 entry
- This completes the raw→curated pipeline for An-Nas; raw was ingested in the earlier batch, only the curated page was missing

**Cross-cutting concept note:** An-Nas introduces the theme "the battle between good and evil" — Qutb explicitly calls it "the most perfect concept of the battle between good and evil." This theme (spiritual warfare, dhikr as the believer's weapon, the whisperer's intrinsic feebleness) does NOT yet have a concept page because it currently appears in only 1 ingested surah. When Al-Falaq (113) or Al-Ikhlas (112) receives a curated page, revisit and create `concepts/battle-of-good-and-evil.md` linking back to An-Nas.

### Ingest: Surah 18 — Al-Kahf (curated page)

- Raw source already extracted in the 17-surah batch: `raw/surah-018-al-kahf.md` (202,326 chars, 72 pages from al-kahfi-eng.pdf, pp. 182–253 of the printed edition)
- **The largest surah in the wiki** — 110 verses, 5 major narrative sections, 27 subsections, ~174K chars of formatted commentary
- Curated page generated: `surahs/surah-018-al-kahf.md` (180,447 chars) with:
  - YAML frontmatter (surah_number 18, makki, 110 verses, 18 tags)
  - Key verse text at top (vv. 1-8 opening, v. 110 closing — the *tawḥīd* frame), with pointer to quran-wiki for full 110-verse text
  - **Prologue** — Qutb's overview: the surah's central theme is purging faith of all alien concepts, establishing correct thought/reasoning and sound values on the basis of faith; five-stage structure outlined
  - **Section 1: A Distinctive System of Values** (vv. 1-27) — opening declaration of *tawḥīd* and the Qur'an's purity; the Sleepers in the Cave (*Aṣḥāb al-Kahf*): young men who chose faith over society, God's grace in the cave, the sun's deliberate movement away, their awakening, debate over their number, reliance on God and the eternal word
  - **Section 2: Faith Based on Free Choice** (vv. 28-46) — the Prophet commanded to remain with the believers, not seek the wealthy; the parable of the two gardens: the arrogant owner vs. the believer who values faith above wealth; the transience of earthly life (water-plants-stubble simile); "wealth and children are the adornment of the life of this world"
  - **Section 3: Heedless of Divine Warnings** (vv. 47-59) — the Day of Judgement: mountains moving, earth bare, records laid open; Adam and Iblīs; the unbridgeable gulf between false deities and their worshippers; man's contentiousness despite the Qur'an's many-faceted lessons; God's mercy and respite vs. the appointed term
  - **Section 4: A Special Lesson for Moses** (vv. 60-82) — Moses' journey to the meeting of the two seas; the pious sage (Khidr); three seemingly unjust actions (scuttling the boat, killing the boy, raising the wall) and their divine rationale; the limits of human knowledge vs. divine wisdom
  - **Section 5: Accurate Historical Accounts** (vv. 83-110) — Dhu'l-Qarnayn's three journeys (west, east, between the two mountains); the barrier against Gog and Magog; the Day of Judgement scene; the sea-as-ink analogy for God's infinite knowledge; the closing verse (110) — *tawḥīd* and righteous action as the passport to meeting the Lord
  - Provenance markers `^[raw/surah-018-al-kahf.md]` on every sourced paragraph
  - Cross-links to [[quran-wiki/surah-018-al-kahf]] and three concept pages (tawhid-as-complete-way-of-life, akhirah-and-the-fleeting-world, jahiliyyah-and-wealth)
  - Related surahs: Al-Isra' (17) as thematic pair (same revelation context — Quraysh/Madinah rabbis three questions), Al-Fatihah (1) as straight-path foundation, An-Nahl (16) as preceding sovereignty declaration
  - Secondary wikis consulted-and-excluded: Qaradawi Library, Jeel Mawoud, Meta-wiki
- Index updated with Surah 18 entry
- Git commit pending

### Batch ingest: Surahs 91, 92, 96 -- Ash-Shams, Al-Layl, Al-`Alaq (curated pages)

- Raw sources already extracted in the 17-surah batch:
  - `raw/surah-091-ash-shams.md` (18,185 chars, 7 pages from syams-eng.pdf, pp. 167-173)
  - `raw/surah-092-al-layl.md` (17,526 chars, 7 pages from layl-eng.pdf, pp. 174-180)
  - `raw/surah-096-al-alaq.md` (37,868 chars, 14 pages from alaq-eng.pdf, pp. 193-206)
- Curated pages generated with YAML frontmatter, verse text, thematic sections, provenance markers, cross-links:
  - `surahs/surah-091-ash-shams.md` (19,946 chars) -- 4 sections: Overview, God's Solemn Oath, A Look into the Human Soul, Historical Example. 15 verses, 26 provenance markers. Tags: qasam, nafs, tazkiyah, fitrah, thamud, divine-oath. Related: Al-Layl (92) as cosmic pair, Al-Asr (103).
  - `surahs/surah-092-al-layl.md` (19,159 chars) -- 4 sections: Overview, An Oath by Universal Phenomena, A Journey with Divergent Ends, And Different Ends. 21 verses, 33 provenance markers. Tags: qasam, sadaqah, iman, akhirah, divine-oath, human-choice, divergent-paths. Related: Ash-Shams (91) as cosmic pair, Al-Asr (103).
  - `surahs/surah-096-al-alaq.md` (37,284 chars) -- 4 sections: The First Revelation, A Momentous Event, A Special Type of Education, Arrogance and Ingratitude. 19 verses, 46 provenance markers. Tags: wahy, ilm, qalam, fatrat-al-wahy, first-revelation, arrogance, abu-jahl, sajdah. Related: Al-Qadr (97) as revelation pair, Ad-Duha (93) for fatrat al-wahy.
- Al-Kafirun (109) curated page reviewed -- no issues found (already clean from previous build)
- All pages cleaned of PDF artifacts (Arabic glyph fragments, stray digits, garbage tokens)
- Index updated with 3 new surah entries
- Git commit pending

### Cleanup: Surah 18 — Al-Kahf curated page (PDF garbage removal + structural fixes)

- Comprehensive 4-pass cleanup of `surahs/surah-018-al-kahf.md` (171K chars, 655 lines)
- **Pass 1**: Removed 81+ Arabic glyph fragments from PDF interleaving (tokens like `ygs`, `xsB uu`, `teu;u`, `Ztqy`, `Moymu`, `yzyu`, `ytGn@`, `Lym`, `yyy`u`, etc.)
- **Pass 2**: Removed 28 additional garbage tokens (`ygrB`, `ttooKt`, `MtGn@`, `VtGo`, `JtrB`, `WsW`, `ftFy`, `yytG`, `yKt`, `tFtrB`, `tFo`, `tyzF`, etc.)
- **Pass 3**: Removed remaining mixed-case fragments (`Iu ftFy`, `yh t/r's`, `n@`, `DhuI` → `Dhu'l`)
- **Pass 4**: Cleaned verse text corruptions identified by 3 parallel review subagents (missing quotation marks, remaining inline tokens `n<`, `yr`, `ys nu`, `Wut`, `y)ym`)
- **Structural fixes**:
  - Fixed malformed verse header (all 110 verses were stuffed into a `###` header line) → clean `### Verses` header
  - Fixed `### How Many Were in the Again the scene...` → `### How Many Were in the Cave?` with body text separated
  - Fixed `### Wt gs` garbage header → removed (was duplicate Overview)
  - Fixed `### Why Reject God's They could certainly...` → `### Why Reject God's Guidance?` with body text separated
  - Restructured `## References & Sources` from single-line header into proper multi-section markdown (Layer 1/2/3, Secondary Wikis, Related Surahs, Cross-Cutting Concepts)
- **Verification**: All 25 expected subsections from raw source confirmed present. 257 provenance markers intact. 0 remaining garbage tokens.
- 3 parallel review subagents (lines 1-205, 206-410, 411-655) confirmed all issues addressed
- Git commit pending

### Ingest: Surah 25 — Al-Furqan (curated page)

- Raw source already extracted in the 17-surah batch: `raw/surah-025-al-furqan.md` (193,296 chars, 65 pages from al-furqan-eng.pdf, pp. 284-348 of the printed edition)
- **A large surah** — 77 verses, 4 parts, 32 sections (including 3 "Overview" subsections), ~165K chars of formatted commentary
- Curated page generated: `surahs/surah-025-al-furqan.md` (164,792 chars, 2,530 lines) with:
  - YAML frontmatter (surah_number 25, makki, 77 verses, 17 tags)
  - Cross-reference to [[quran-wiki/surah-025-al-furqan]] for Uthmani text, Ibn Kathir, and Muyassar
  - **Prologue** — Qutb's overview: the surah aims at comforting the Prophet against Quraysh rejection, portraying divine kindness and the battle against arrogant mortals
  - **Part 1: To Distinguish Right from False** (vv. 1-9) — blessed is He who revealed the Criterion; the unbelievers' accusations against the Qur'an; the Purpose of Qur'anic Revelations (gradual revelation for contemplation); Accusations without Basis (fables of ancient times); Honouring Mankind (human messenger as mercy, not angel); Denying Resurrection (blazing fire, those who deny the Last Hour); Entrusting God's Message to Man (messengers who ate food and walked in markets)
  - **Part 2: Below Animal Level** (vv. 10-44) — the unbelievers' objections (no angels sent, no treasure); Overview; Ominous Prospects for the Unbelievers (those gathered to hell on their faces); What Use is Regret? (the wrongdoer bites his hands); A Complaint by God's Messenger (my people have regarded this Qur'an as a thing to be forsaken); The Time Span of Qur'anic Revelations (We never sent messengers other than men); The Fate of Earlier Unbelievers (Noah, `Ād, Thamūd, people of al-Rass); Ridiculing God's Messenger (al-Walīd ibn al-Mughīrah's plotting); When Desire is Worshipped (the one who takes his desire as deity, worse than cattle)
  - **Part 3: Raising Support Against God** (vv. 45-60) — Overview; Moving Shadows, Still Night (God's signs in shadows, night, day); Jihad by Means of the Qur'an (the Qur'an's irresistible power, al-Akhnas ibn Sharīq and Abū Sufyān secretly listening); Separating Types of Water (fresh and salt water, the barrier between them); The Great Miracle of Life (A.C. Morrison quote on genes and chromosomes); In League Against God (the unbeliever always gives support against his Lord); In Whom to Trust (place your trust in the Living One); Setting the Universe to Order (all glory belongs to God, the universe as ordered system)
  - **Part 4: God's True Servants** (vv. 63-77) — Overview; The Distinctive Features of Faith (the `ibād al-Raḥmān: walk gently, pray at night); Steering Away from Sin (avoid killing without right, avoid fornication); Erasing Sin Through Repentance (the door of repentance is always open); Further Qualities of True Believers (avoid false testimony, avoid vain talk); Destined for the Finest Abode (paradise as reward, the finest abode)
  - Provenance markers `^[raw/surah-025-al-furqan.md]` on every section (32 markers)
  - Cross-links to [[quran-wiki/surah-025-al-furqan]] and concept page [[concepts/tawhid-as-complete-way-of-life]]
  - Related surahs: Al-Kahf (18) — trials of faith and divine protection; Al-Anbiya (21) — prophethood and rejection; Maryam (19) — divine mercy and resurrection
  - 3 parallel review subagents verified the page (lines 1-840, 841-1680, 1681-2530) — issues addressed
- Index updated with Surah 25 entry
- Git commit pending

### Ingest: Surah 30 — Ar-Rum (curated page)

- Raw source already extracted in the 17-surah batch: `raw/surah-030-ar-rum.md` (126,327 chars, 42 pages from ar-rum-eng.pdf, pp. 274-315 of the printed edition)
- 60 verses, 2 parts, 17 sections (including Prologue + Overview), ~101K chars of formatted commentary
- Curated page generated: `surahs/surah-030-ar-rum.md` (100,742 chars, 1,646 lines) with:
  - YAML frontmatter (surah_number 30, makki, 60 verses, 17 tags)
  - Cross-reference to [[quran-wiki/surah-030-ar-rum]] for Uthmani text, Ibn Kathir, and Muyassar
  - **Prologue** — Qutb's overview: the surah opens with the Byzantine-Persian conflict, uses the event to establish links between believers and the universe, God's rule, and human nature; two interlinked sections
  - **Part 1: Signs to Reflect Upon** (vv. 1-32) — the Byzantine victory prophecy; The Natural Bond of Faith (fitrah and divine guidance); To Whom Power Belongs (God's sovereignty over history); An Invitation to Reflect (cosmic signs); Two Divergent Ways (believers vs unbelievers); The Cycle of Life and Death (resurrection from dead earth); Man and the Universe (diversity of languages and colours); An Analogy Drawn from Human Life (the spider's web); Concluding Directive (steadfastness in faith)
  - **Part 2: Bringing Life out of the Dead** (vv. 33-60) — Overview; Vacillating Conditions (human ingratitude in hardship vs ease); Corruption and Pollution (corruption on land and sea); Aspects of God's Grace (rain, winds, clouds); The Different Stages of Man's Life (creation from dust, seed, blood clot); No Change of Position (God's inevitable decree, the Day of Judgement)
  - Provenance markers `^[raw/surah-030-ar-rum.md]` on every section (17 markers)
  - Cross-links to [[quran-wiki/surah-030-ar-rum]] and concept page [[concepts/tawhid-as-complete-way-of-life]]
  - Related surahs: Al-Furqan (25) — divine criterion and rejection of prophecy; Al-Kahf (18) — trials of faith; Al-Anbiya (21) — prophethood and universal message
  - 3 parallel review subagents verified the page
- Index updated with Surah 30 entry
- Git commit pending

## 2026-07-24

- Raw source already extracted: `raw/surah-036-ya-sin.md` (111,483 chars, 38 pages from yasin-eng.pdf, pp. 192-229 of the printed edition)
- 83 verses, 3 parts, 14 sections (including Prologue + 2 Overview sections), ~84K chars of formatted commentary
- Curated page generated: `surahs/surah-036-ya-sin.md` (84,111 chars, 209 lines) with:
  - YAML frontmatter (surah_number 36, makki, 83 verses, 18 tags)
  - Cross-reference to [[quran-wiki/surah-036-ya-sin]] for Uthmani text, Ibn Kathir, and Muyassar
  - **Prologue** — Qutb's overview: Makkan surah with short verses and fast rhythm; three parts covering revelation/truth of message, cosmic signs + resurrection, and a final summation (poetry denial, God's oneness, resurrection)
  - **Part 1: Appeal to Reason** (vv. 1-29) — A Book Full of Wisdom (oath by the Qur'an, divine wisdom); A Historical Case (the township that rejected three messengers); Welcome Support (the believer from the farthest end of town); Killing an Innocent Man (the believer's martyrdom and divine retribution)
  - **Part 2: Signs Galore** (vv. 30-68) — Overview (transition to cosmic signs); A Sorrowful Condition (denial of messengers, destruction of past nations); Only Look Around (dead earth, night/day, sun/moon, ships, cattle, pairs); What Opens Sealed Hearts (human ingratitude, charity refusal); Mercy: the Essential Quality (the Trumpet, paradise, the guilty ones, divine power over human faculties)
  - **Part 3: What Prevents Resurrection?** (vv. 69-83) — Overview (final review of themes); No Place for Poetry (Qur'an is not poetry); Just the One God (cattle as divine provision, idolatry critique); A Second Life for All (resurrection from gamete, green tree fire, heavens/earth creation, "Be, and it is")
  - Provenance markers `^[raw/surah-036-ya-sin.md]` on every section (14 markers)
  - Cross-links to [[quran-wiki/surah-036-ya-sin]] and concept page [[concepts/tawhid-as-complete-way-of-life]]
  - Related surahs: An-Naba (78) — resurrection imagery; Al-Waqi'ah (56) — paradise scenes; Al-Furqan (25) — idolatry critique
  - 3 parallel review subagents verified the page (lines 1-73, 74-146, 147-219)
  - Multi-pass cleanup: removed 113 math operator verse separators (∩⊇∪), Arabic Unicode glyphs, romanized Arabic tokens (0xC0-0xFF), page numbers (41), running headers (26 "Yā sīn | ..."), garbage blockquote lines
  - Text corrections applied: "Yd Sin"→"Ya Sin", "All of wisdom"→"full of wisdom", "will he"→"will be", "God- fearing"→"God-fearing", bracket corruptions, missing verse numbers restored (83, 45), wikilink path fixes
- Index updated with Surah 36 entry
- Git commit pending

## 2026-08-15

### Ingest: Surah 8 — Al-Anfal (raw + curated page)

- Source PDF: `/mnt/c/Users/netfl/Downloads/al-anfal-eng.pdf` (~130 pages of the printed edition)
- Extracted via `pdftotext -layout` → 8,715 lines, 565,402 chars
- Arabic verse text did not extract from PDF (embedded font issue); cross-reference to quran-wiki/raw/arabic/008-*.md for verified Uthmani Arabic (75 verse files already present)
- Raw source written: `raw/surah-008-al-anfal.md` (526,763 chars, 7,384 lines) — cleaned of page headers, form feeds, Arabic verse markers
- **The first Madinan surah in the wiki** — 75 verses, 5 major parts, 69 thematic sections, ~510K chars of formatted commentary
- Curated page generated: `surahs/surah-008-al-anfal.md` (509,551 chars, 1,917 lines) with:
  - YAML frontmatter (surah_number 8, madani, 75 verses, 22 tags)
  - Cross-reference to [[quran-wiki/surah-008-al-anfal]] for Uthmani text, Ibn Kathir, and Muyassar
  - **Part 1: Prologue — The Islamic Approach and the Battle of Badr** (20 sections) — the most extensive prologue in the entire tafsir:
    - Prologue (revelation context, chronology)
    - Characteristics of the Islamic Approach (serious realism, progressive stages, definitive principles, legal framework)
    - The Liberation of Mankind (jihad as declaration of human liberation from servitude to creatures)
    - How Defensive Is Jihad? (Qutb's rejection of "defensive jihad only" as defeatist misreading)
    - A Stage of No Fighting (Makkan period strategy — 6 reasons for restraint)
    - What Justification for Jihad? (inherent justification in the nature of Islam)
    - A Gulf Too Wide! (the gap between human planning and divine will)
    - A Further Point of View (Mawdudi's perspective on jihad)
    - Misgivings about Jihad (Western misunderstandings of jihad)
    - The Essence of Jihad (Islam as revolutionary concept, not mere religion)
    - For God's Cause (fī sabīlillāh — the pure intention requirement)
    - Islam's Revolutionary Message (worship God alone, no human masters)
    - Characteristics of the Call for an Islamic Change (prophetic methodology)
    - The Need for Jihad and Its Objective (removing oppression, establishing justice)
    - The Universal Revolution (global scope, not nationalistic)
    - The Battle of Badr (detailed historical account — Ibn Ishaq, Ibn Hisham sources)
    - Rejecting Wise Counsel (the incident of `Abdullah ibn Jahsh)
    - Qur'anic Comments (surah structure overview — 6 thematic areas)
    - Why Believers Fight (faith as the basis of all jihad commands)
    - To Sum Up (the surah's educational method, Badr as divine test)
  - **Part 2: Different Types of Victory (Verses 1-29)** (13 sections) — spoils of war ruling, qualities of true believers, the battle events, divine support, tactical withdrawal, God's planning, response to God's call, victory through hardship, the reassuring criterion (discernment/furqan)
  - **Part 3: In Defiance of the Truth (Verses 30-40)** (7 sections) — Quraysh's plot against the Prophet, feeble manoeuvres, sophisticated ploys, human folly, separating good from bad, the positive approach (fight until no oppression)
  - **Part 4: God's Will at Work (Verses 41-54)** (10 sections) — the one-fifth rule, fighting after victory, true belief, the criterion of distinction, clear evidence, God's purpose, eliminating failure, deception, divine justice, what changes God's blessings (the unchanging divine law)
  - **Part 5: Delineation of Loyalties (Verses 55-75)** (19 sections) — treaty breaches, the worst of creatures, striking terror, military readiness, peace prospect, trust in God, uniting hearts, matching forces, captive rulings, God's preferred option, deceiving God, definition of relations, loyalty in Muslim community, practical manifestation of Islamic theory, demarcation of loyalties, true believers, nature of Islamic society, community of mankind
  - Provenance markers `^[raw/surah-008-al-anfal.md]` on every sourced paragraph
  - Cross-links to [[quran-wiki/surah-008-al-anfal]] and concept pages (tawhid-as-complete-way-of-life, jahiliyyah-and-wealth)
  - Related surahs: Al-Baqarah (2), At-Tawbah (9), Al-Hajj (22), An-Nisa (4)
  - References section with key themes and notable doctrinal positions
- 5 parallel subagents dispatched for initial processing (3+2), Part 1 reprocessed manually after subagent hit tool-call limit
- Index updated with Surah 8 entry
- Git commit pending

## 2026-08-15

### Ingest: Surah 9 — At-Tawbah (The Repentance)

- **Source:** `at-taubah-eng.pdf` (252 pages, 1.15 MB) — Fi Zilal al-Qur'an, English translation by Sayyid Qutb
- **Extraction:** `pdftotext -layout` → 760K chars raw text, 12K lines
- **Cleaning:** Removed page numbers, form feeds, running headers (7 unique), Arabic glyph fragments (gentle word-level cleaning), verse markers (∩⊇∪). Diacritic batch fixes applied (Qur'ān, sūrah, Muḥammad, Muhājirīn, Anşār, jāhiliyyah, jihād, ḥadīth, Imām, Aḥmad, Bukhārī, Ṭabarī, etc.)
- **Raw file:** `raw/surah-009-at-tawbah.md` — 672K chars, 10.3K lines
- **Curated page:** `surahs/surah-009-at-tawbah.md` — 676K chars, 10.5K lines
  - **7 major thematic sections** (preserved as `##` headings):
    1. **Prologue** (7 sub-sections) — historical context, revelation stages, jihād rulings overview
    2. **The Basis of Inter-Communal Relations** (19 sub-sections) — treaties with idolaters, the four sacred months, international relations principles, asylum, the Tabūk expedition context
    3. **Relations with Other Religions** (15 sub-sections) — People of the Book, Jewish attitudes, Christian Trinity critique, jizyah, hoarding wealth
    4. **A Higher Degree of Unbelief** (3 sub-sections) — the sacred months manipulation, mobilization reluctance
    5. **The Supreme Word of God** (2 sub-sections) — the call to jihād, distinguishing true believers from liars
    6. **Manifestations of Hypocrisy** (26 sub-sections) — the hypocrites exposed, zakāt distribution, the mosque of dissension, false excuses, believers vs. hypocrites
    7. **The Earth's Suffocating Expanse** (18 sub-sections) — the divine covenant with believers, repentance, the three who stayed behind, Islamic war ethics, conclusion
  - **80+ sub-sections** preserved as `###` headings
  - Provenance markers `^[raw/surah-009-at-tawbah.md]`
  - Cross-links to [[quran-wiki/surah-009-at-tawbah]] and concept pages (tawhid-as-complete-way-of-life, jahiliyyah-and-wealth, iman-and-dignified-humanity)
  - Related surahs: Al-Anfal (8) — predecessor with provisional rulings amended by At-Tawbah; Muhammad (47); Al-Ma'idah (5)
- **Largest surah ingested to date** (252 pages, 672K chars raw — surpassing Al-Kahf at 202K chars)
- Index updated with Surah 9 entry
- Git commit pending