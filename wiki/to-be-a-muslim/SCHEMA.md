# Wiki Schema

## Domain
Islamic theology and activism — the book "To Be a Muslim" by Fathi Yakan. Covers creed (aqidah), worship (ibadah), morals, family life, self-control, the Islamic Movement, dawah, strategic planning, bai'ah, and brotherhood.

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `islamic-movement.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Cross-wiki references:** Use `[[quran-wiki/surah-002-al-baqarah|Al-Baqarah]]` format to reference pages in other federation wikis
- **Provenance markers:** Since this wiki is derived from a single source (the book), provenance is implicit via `sources:` in frontmatter. No inline `^[raw/...]` markers needed.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query
tags: [from taxonomy below]
sources: [raw/book.md]
---
```

## Tag Taxonomy
### Theology
- `aqidah`, `tawhid`, `akhirah`, `revelation`, `charity`, `prayer`, `dhikr`
- `ibadah`, `fiqh`, `shariah`, `ijtehad`

### Ethics & Practice
- `morals`, `wara`, `modesty`, `honesty`, `fortitude`, `humility`, `grace`
- `self-control`, `jihad-an-nafs`, `satantic-traps`

### Social & Political
- `family`, `marriage`, `parenting`, `brotherhood`
- `dawah`, `islamic-movement`, `activism`, `baiah`
- `strategic-planning`, `gradualism`, `jihad`

### Historical Figures
- `prophet-muhammad`, `hasan-al-banna`, `syed-qutb`, `fathi-yakan`

### Meta
- `quran-verse`, `hadith`, `book-excerpt`

## Page Thresholds
- **Create a page** when a concept or entity is central to the book or appears across multiple sections
- **Add to existing page** when new information supplements what's already covered
- **DON'T create a page** for passing mentions or minor details
- **Split a page** when it exceeds ~200 lines

## Entity Pages
One page per notable person or entity. Include:
- Overview / who they are
- Key contributions referenced in the book
- Relationships to other entities (`[[wikilinks]]`)
- Source references

## Concept Pages
One page per major concept. Include:
- Definition / explanation from the book
- Qur'an and hadith evidence cited
- Practical implications
- Related concepts (`[[wikilinks]]`)

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report