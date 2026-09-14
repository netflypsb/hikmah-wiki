# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-06-08] create | Wiki initialized
- Domain: Islamic theology and activism — "To Be a Muslim" by Fathi Yakan
- Structure created with SCHEMA.md, index.md, log.md
- Source: `/mnt/c/Users/netfl/Downloads/to_be_a_muslim.pdf` (37 pages, two-column layout)
- Extraction: pymupdf block-level with column separation, ligature cleanup, hyphen rejoin

## [2026-06-08] create | Entity page: hasan-al-banna
- Created `/entities/hasan-al-banna.md` with full content from book source
- Covers: Muslim Brotherhood founder role, three types of people, five tools of movement, stages of da'wah (Risalat Ta'alim), ten principles of bai'ah, 30+ duties from Educational Discourse, movement vs. organizations, trials, strength
- Wikilinks to: fathi-yakan, baiah, islamic-movement, man-vs-materialism, brotherhood, syed-qutb, islamic-activism, strategic-planning

## [2026-06-08] ingest | "To Be a Muslim" by Fathi Yakan
- Raw source: `raw/book.md` (~175K chars, ~30K words, 1623 lines)
- Created 3 entity pages: fathi-yakan, hasan-al-banna, syed-qutb
- Created 11 concept pages: aqidah, ibadah, morals, family-life, self-control, man-vs-materialism, islamic-activism, islamic-movement, strategic-planning, baiah, brotherhood
- Total pages: 14

## [2026-06-08] create | entities/syed-qutb.md
- Entity page for Syed Qutb with full YAML frontmatter
- Covers psychological isolation concept (Book §2.3.5), Qutb's quote on vanguard isolation, and the principle of vigilance against Satanic traps where Islamic work is active
- Wikilinks to fathi-yakan, islamic-movement, self-control, hasan-al-banna