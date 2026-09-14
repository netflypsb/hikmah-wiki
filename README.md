# Hikmah — Islamic Literature LLM Wiki

## What This Is

Hikmah (حكمة, "wisdom") is an open-source project to create a machine-readable, auditable LLM Wiki of Islamic literature. It has two parts:

1. **hikmah-engine** — The software engine that processes Islamic source material into a cross-linked wiki. Forked from [llm-wiki-newsroom](https://github.com/alfadur7/llm-wiki-newsroom), adapted for Arabic/English Islamic scholarship. Published at `github.com/netflypsb/hikmah-engine`.

2. **hikmah-wiki** — The content: the actual wiki pages, knowledge graph, and processing manifest. All curated content is versioned and auditable. Published at `github.com/netflypsb/hikmah-wiki`.

## Source Material

Original Islamic reference texts (Qur'an, Hadith, tafsir works, scholarly books) are published and maintained on **Bayt al-Hikmah** — a project to bring Islamic references into website format for easy consumption, and to translate original works into as many languages as possible.

Website: https://bayt-al-hikmah-nine.vercel.app/

Note: not all source material is currently available on Bayt al-Hikmah. New references are added gradually. This wiki references the original works by title, author, and chapter/verse — refer to Bayt al-Hikmah to read the full original texts as they become available.

## Directory Structure

```
/root/hikmah/
├── sources/                    # Layer 1: original source material (immutable)
│   ├── quran/                  # Quran API corpus (Arabic, translations, tafsir, metadata)
│   ├── fi-zilal/               # Fi Zilal al-Qur'an raw text (25 surahs)
│   ├── jeel-mawoud/            # Jeel Mawoud PDF + extracted text
│   ├── qaradawi/               # Qaradawi Library PDFs + extracted text
│   ├── fathi-yakan/            # Fathi Yakan books (intimai + kayfa-naduwu)
│   ├── to-be-a-muslim/         # To Be a Muslim source text
│   └── aulad-education/        # Prophetic Child Education PDF
├── wiki/                       # Layer 2: curated wiki content (agent-managed)
│   ├── quran-wiki/             # 406 pages (114 surahs, concepts, linguistics, entities)
│   ├── fi-zilal-wiki/          # 32 pages (22 surahs, 5 concepts)
│   ├── jeel-mawoud-wiki/       # 67 pages (entities, concepts, translations)
│   ├── qaradawi-library/       # 168 pages (entities, concepts, comparisons)
│   ├── to-be-a-muslim/         # 17 pages
│   └── meta/                   # 10 cross-wiki syntheses and bridges
├── translations/               # English translations (for Bayt al-Hikmah website)
│   ├── fathi-yakan-intimai/    # 20 chapters
│   ├── fathi-yakan-kayfa-naduwu/ # 18 chapters
│   └── jeel-mawoud/            # 26 files
├── tools/                      # Python tools (federated query, graph, lint, scripts)
├── notes/                      # Research deliverables, presentations
├── designs/                    # HTML design artifacts
├── MANIFEST.json               # Per-page processing audit trail
├── AGENTS.md                   # Agent context and rules (this file's companion)
├── BAYT_AL_HIKMAH.md           # Reference to Bayt al-Hikmah (single source of truth)
└── README.md                   # This file
```

## Versioning

- **v1.0** — Current manual curation workflow (per-tafsir-wiki-building, islamic-wiki-curation skills). All existing content is v1.0.
- **v2.0** — hikmah-engine (forked from newsroom). Enriches existing content without overwriting. New content goes through automated pipeline.
- See MANIFEST.json for per-page provenance tracking.

## Related Projects

- **Bayt al-Hikmah** (`/root/projects/bayt-al-hikmah/`) — Separate project. Human-facing website for Islamic references. No workflow connection to hikmah. Both projects share the same source material (original Islamic references).
- **Existing wiki repos** (legacy) — Legacy repos being superseded by hikmah-wiki monorepo.

## Skills

The following Hermes skills are used for v1.0 manual curation:
- `per-tafsir-wiki-building` — Main architecture (v1.6.0)
- `islamic-literature-wiki-curation` — PDF extraction + cleanup
- `islamic-wiki-curation` — Raw text → markdown curation
- `quran-wiki-reference` — Quran Wiki lookup
- `scholarly-wiki-ops` — Book-centric wiki pipeline
- `llm-wiki-production` — Multi-wiki federation templates

These skills will be updated to reference the new `/root/hikmah/` paths. The future `hikmah-engine` skill will govern the v2.0+ automated pipeline.