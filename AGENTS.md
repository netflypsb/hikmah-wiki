# Hikmah — Agent Operations Guide

## Project Overview

Hikmah is the unified Islamic literature LLM Wiki project. It consolidates all Islamic
source material and curated wiki content that was previously scattered across /root/tarbiyyah/,
/root/qaradawi-library/, and /root/.llm-wiki/religious/.

| Field | Value |
|-------|-------|
| **Location** | `/root/hikmah/` |
| **Engine repo** | `github.com/netflypsb/hikmah-engine` (MIT license) |
| **Content repo** | `github.com/netflypsb/hikmah-wiki` (CC BY-SA 4.0 license) |
| **Source material website** | https://bayt-al-hikmah-nine.vercel.app/ (Bayt al-Hikmah) |

## GitHub Account Rule

**Both hikmah-engine and hikmah-wiki MUST be pushed to the `netflypsb` GitHub account.**
**NEVER push hikmah repos to other GitHub accounts.**

The existing wiki repos on other accounts (quran-wiki, fi-zilal-wiki, jeel-mawoud-wiki,
qaradawi-library) are LEGACY repos from before the hikmah project. They will be archived
after the hikmah-wiki monorepo migration is complete.

## Architecture

Three-layer separation (Karpathy LLM Wiki pattern):

1. **sources/** — Layer 1: Original source material (immutable after ingestion)
   - Quran API corpus (Arabic, 5 translations, Ibn Kathir + Muyassar tafsir) — fetched from Quran.com API, cached locally
   - Fi Zilal al-Qur'an raw text (25 surahs) — PDF extraction
   - Jeel Mawoud PDF + extracted text — Archive.org download
   - Qaradawi Library (10 PDFs + extracted text) — Archive.org download
   - Fathi Yakan books (intimai + kayfa-naduwu) — Archive.org + Tesseract OCR
   - To Be a Muslim source text
   - Aulad Education PDF

2. **wiki/** — Layer 2: Curated wiki content (agent-managed, v1.0 manual curation)
   - quran-wiki/ — 406 pages (114 surahs, 16 concepts, 16 linguistics, 179 entities, 22 comparisons, 30 juz, 21 verses)
   - fi-zilal-wiki/ — 32 pages (22 surahs, 5 concepts)
   - jeel-mawoud-wiki/ — 67 pages (entities, concepts, English translation)
   - qaradawi-library/ — 168 pages (entities, concepts, comparisons)
   - to-be-a-muslim/ — 17 pages
   - meta/ — 10 cross-wiki syntheses and bridges

3. **AGENTS.md + MANIFEST.json** — Layer 3: Rules and processing audit trail

Additional:
- **translations/** — English translations for Bayt al-Hikmah website (not wiki content)
- **tools/** — Python tools (federated query, graph, lint, book pipeline scripts)
- **notes/** — Research deliverables, presentations
- **designs/** — HTML design artifacts

## Versioning

| Version | Description |
|---------|-------------|
| v1.0 | Manual curation workflow (current — per-tafsir-wiki-building skill) |
| v2.0 | hikmah-engine (forked from llm-wiki-newsroom, agent-agnostic CLI) |
| v2.x | Minor improvements (better cascading, new lint rules) |
| v3.0 | Breaking schema change (would require reprocessing) |

All existing content is tagged as v1.0 in MANIFEST.json. The v2.0 engine will:
- Run lint against all v1.0 pages (fix broken links, missing frontmatter)
- Build knowledge graph from existing wikilinks
- Detect contradictions between tafsirs
- NOT overwrite v1.0 curated text without explicit per-page decision
- New content (new surahs, new books) goes through full v2.0 automated pipeline

## Source Authenticity Rules

All content must follow the Tarbiyyah source tier system:

### TIER 1 — Qur'an and Its Exegesis
- Tafsir Ibn Kathir — PRIMARY for Qur'anic interpretation
- Fi Zilal al-Qur'an (Sayyid Qutb) — SECONDARY for thematic/literary tafsir
- Other classical tafasir (al-Tabari, al-Qurtubi, al-Baghawi, al-Sa'di) as supplementary

### TIER 2 — Hadith Collections (Sahih)
- Sahih al-Bukhari, Sahih Muslim, Sunan an-Nasa'i, Sunan Abu Dawud
- Jami' at-Tirmidhi, Sunan Ibn Majah, Muwatta Imam Malik
- Riyad as-Salihin, Forty Hadith (an-Nawawi, Ibn Rajab)

### TIER 3 — Classical Scholars
- Imam al-Ghazali, Ibn Taymiyyah, Ibn al-Qayyim, al-Nawawi, Ibn Rajab
- Imam al-Dhahabi, Ibn Hajar al-Asqalani, al-Bayhaqi

### TIER 4 — Contemporary Authentic Scholars (Verified)
- Sheikh Ibn Baz, Ibn Uthaymeen, al-Albani
- Sheikh al-Qaradawi — ONLY fiqh, NOT political works
- Verified Sunni publishing houses: Darussalam, etc.

### TIER 5 — Islamic History (Authenticated)
- Ibn Hisham/Ibn Ishaq, al-Tabari, Ibn Khaldun

## Prohibited Sources
- Shi'a sources (al-Kafi, Bihar al-Anwar)
- Non-Muslim orientalist sources for theological claims
- Deviant/modernist reinterpretations contradicting classical scholarship
- Unverified websites, anonymous blogs, LLM hallucinations
- Weak (da'if) or fabricated (mawdoo') hadith without explicit labelling

## Citation Rules
1. Every theological claim (aqeedah) must cite Qur'an + authentic hadith
2. Every fiqh ruling must cite source text + classical madhab position
3. Every historical event must cite classical historian
4. Every quote from a scholar must name scholar, work, volume/page
5. Every tafsir reference must specify mufassir and verse range

## Skills

The following Hermes skills are used for this project:

| Skill | Purpose | Location |
|-------|---------|----------|
| `per-tafsir-wiki-building` | Main v1.0 architecture (v1.6.0) | `~/.hermes/skills/religious/` |
| `islamic-literature-wiki-curation` | PDF extraction + cleanup | `~/.hermes/skills/religious/` |
| `islamic-wiki-curation` | Raw text → markdown curation | `~/.hermes/skills/research/` |
| `quran-wiki-reference` | Quran Wiki lookup | `~/.hermes/skills/religious/` |
| `scholarly-wiki-ops` | Book-centric wiki pipeline | `~/.hermes/skills/research/` |
| `llm-wiki-production` | Multi-wiki federation templates | `~/.hermes/skills/research/` |

**Note:** These skills still reference old paths (`/root/tarbiyyah/`, `/root/qaradawi-library/`).
They will be updated to reference `/root/hikmah/` paths in a follow-up step.

## Cross-Project Rules

- **Bayt al-Hikmah** (`/root/projects/bayt-al-hikmah/`) is a SEPARATE project. No workflow connection.
  Both projects share the same source material (original Islamic references). Bayt al-Hikmah is the
  human-facing website; hikmah-wiki is the machine-readable wiki.
- **NEVER** mix hikmah content with Genesis business data.
- **NEVER** push hikmah repos to any GitHub account other than `netflypsb`.
- **NEVER** modify sources/ after ingestion — raw sources are immutable.