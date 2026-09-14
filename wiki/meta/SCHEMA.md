---
name: Tarbiyyah Meta-Wiki Schema
domain: Islamic Knowledge — cross-disciplinary synthesis and navigation
subdomains: [quranic-studies, fiqh, hadith, seerah, aqeedah, tazkiyah, scholars, arabic]
created: 2026-05-10
version: 1.0.0
---

# Meta-Wiki Schema — Tarbiyyah Knowledge Federation

## Purpose
This meta-wiki is the **sole bridge** between all Islamic knowledge domains under Tarbiyyah. It does not duplicate content from sub-wikis — it synthesizes, cross-references, and navigates across them.

## Architecture

```
tarbiyyah/
├── quran-wiki/          ← Quranic studies (SOVEREIGN — never referenced from below)
├── fiqh-wiki/           ← Jurisprudence (future)
├── hadith-wiki/         ← Hadith sciences (future)
├── seerah-wiki/         ← Prophetic biography (future)
├── aqeedah-wiki/        ← Theology (future)
├── scholars-wiki/       ← Ulama biographies (future)
└── meta-wiki/           ← THIS WIKI — cross-domain synthesis only
    ├── SCHEMA.md
    ├── index.md
    ├── log.md
    ├── cross-syntheses/   ← Pages linking 2+ wikis
    └── domain-indexes/    ← Per-domain quick-reference cards
```

## Rules
1. **No content duplication** — meta-wiki never quotes Quranic verses directly; it links to quran-wiki/.
2. **No downward authority** — meta-wiki can read all sub-wikis; sub-wikis cannot write into meta-wiki/.
3. **Cross-wiki links use full syntax** — `[[quran-wiki/surah-002-al-baqarah|Al-Baqarah]]` not `[[Al-Baqarah]]`.
4. **Every cross-synthesis must touch 2+ domains** — a page about "salat in the Quran and fiqh" is valid; a page about "salat in the Quran" belongs in quran-wiki/.
5. **Global tag taxonomy is SSOT** — all sub-wikis use the same tags defined here.

## Global Tag Taxonomy

### Revelation & Sources
- `quran` — Quranic text, tafsir, translation
- `hadith` — Prophetic narration, chain, grade
- `sunnah` — Practice of the Prophet (broader than hadith)
- `ijma` — Scholarly consensus
- `qiyas` — Analogical reasoning
- `usul` — Principles of jurisprudence/theology

### Disciplines
- `tafsir` — Quranic exegesis
- `fiqh` — Islamic jurisprudence
- `aqeedah` — Theology / creed
- `seerah` — Prophetic biography
- `hadith-science` — Mustalah, jarh wa ta'dil, etc.
- `tazkiyah` — Spirituality / purification of soul
- `arabic` — Grammar, rhetoric, morphology
- `history` — Islamic civilization, caliphates, battles

### Theological Themes (from quran-wiki)
- `tawhid` — Divine Oneness
- `risalah` — Messengership
- `akhirah` — Afterlife
- `iman` — Faith
- `kufr` — Disbelief
- `shirk` — Polytheism
- `qadr` — Divine Decree

### Worship & Law
- `salah` — Prayer
- `sawm` — Fasting
- `zakat` — Charity
- `hajj` — Pilgrimage
- `jihad` — Striving
- `muamalat` — Transactions
- `munakahat` — Family law
- `jinayat` — Criminal law

### Spiritual & Ethical
- `sabr` — Patience
- `shukr` — Gratitude
- `taqwa` — God-consciousness
- `ikhlas` — Sincerity
- `adab` — Etiquette
- `dhikr` — Remembrance
- `dua` — Supplication

### Meta
- `cross-synthesis` — Links 2+ domains
- `comparison` — Side-by-side analysis across domains
- `methodology` — How knowledge is derived
- `controversy` — Scholarly disputes
- `timeline` — Chronological ordering
- `biography` — Person-focused

## Cross-Wiki Link Syntax

```markdown
<!-- Full syntax — creates federated edges in graph engine -->
See [[quran-wiki/surah-002-al-baqarah|Al-Baqarah]] for the Quranic basis.

<!-- Domain index quick links -->
For the legal ruling, see [[fiqh-wiki/index|Fiqh Wiki]] (future).

<!-- Cross-synthesis internal link -->
This is explored in [[cross-syntheses/prayer-in-quran-and-fiqh|Prayer in Quran and Fiqh]].
```

## Page Thresholds
- **Create a cross-synthesis** when a topic genuinely spans 2+ domains AND the synthesis adds value beyond what each domain wiki already contains.
- **Create a domain-index** when a new wiki is scaffolded — it serves as a quick-reference card.
- **DON'T create** pages that duplicate sub-wiki content.
- **DON'T create** pages that only reference one domain.

## Update Policy
- When sub-wiki content changes, meta-wiki cross-syntheses are **not automatically updated** — they are reviewed quarterly or on-demand.
- When a new wiki is added, update `index.md` and create its `domain-indexes/` card.
