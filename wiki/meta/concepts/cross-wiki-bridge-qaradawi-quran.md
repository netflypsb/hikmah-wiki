---
title: Cross-Wiki Bridge — Quran Wiki ↔ Qaradawi Library
created: '2026-06-09'
updated: '2026-06-09'
type: meta
tags: [meta, cross-wiki, islamic, quran, fiqh]
---

# Cross-Wiki Bridge: Quran Wiki ↔ Qaradawi Library

> This page documents the cross-referencing links between the Quran Wiki and the Qaradawi Library.
> Both are religious knowledge bases under the LLM Wiki hub at `~/.llm-wiki/`.

---

## Linking Convention

When a Qaradawi Library concept or chapter cites a Quranic verse, use this format:

```markdown
[Qur'an 2:177] → consult [[quran-wiki:surah-002-al-baqarah|Al-Baqarah (2)]] for tafsir context
```

The prefix `quran-wiki:` signals a cross-wiki reference. The federated query engine resolves these.

---

## Key Thematic Bridges

### 1. Zakat & Economic Justice
- **Qaradawi Library**: [[concept-zakat]], [[concept-nisab]], [[concept-hawl]], [[concept-usury]], [[comparison-zakat-economic-justice]]
- **Quran Wiki**: Surah Al-Baqarah (2:177, 2:215, 2:261-267, 2:270, 2:280), Surah At-Tawbah (9:60, 9:103), Surah Ar-Rum (30:39)
- **Bridge**: Qaradawi's *Fiqh al-Zakah* is the most comprehensive modern zakah jurisprudence, directly rooted in the Qur'anic verses on zakah, sadaqah, and riba.

### 2. Sunnah Methodology
- **Qaradawi Library**: [[concept-sunnah]], [[concept-hadith]], [[concept-isnad]], [[comparison-sunnah-methodology]]
- **Quran Wiki**: Surah Al-Hashr (59:7), Surah An-Nisa (4:59, 4:65, 4:80)
- **Bridge**: Qaradawi's *Approaching the Sunnah* argues for the Sunnah's legislative authority, rooted in the Qur'anic imperative "obey Allah and obey the Messenger."

### 3. Halal & Haram
- **Qaradawi Library**: [[concept-halal]], [[concept-haram]], [[concept-darurah]], [[comparison-halal-haram-permissibility]]
- **Quran Wiki**: Surah Al-Baqarah (2:168-173), Surah Al-Ma'idah (5:3-5, 5:87-88, 5:96), Surah Al-A'raf (7:157)
- **Bridge**: Qaradawi's *The Lawful and the Prohibited* builds its eleven principles of permissibility on Qur'anic foundations, especially the maxim "He has made lawful all good things" (7:157).

### 4. Ethics & Morality
- **Qaradawi Library**: [[concept-character]], [[concept-justice]], [[concept-sabr]], [[concept-wasatiyyah]]
- **Quran Wiki**: Surah Al-Baqarah (2:177 — comprehensive virtue list), Surah An-Nisa (4:135 — justice), Surah Luqman (31:17-19 — wisdom)
- **Bridge**: Qaradawi's *Ethics in Islam* systematises the Qur'anic moral vision across worship, family, economics, and politics.

### 5. Faith & Spirituality
- **Qaradawi Library**: [[concept-faith]], [[concept-creed]], [[concept-tazkiyah]], [[concept-tawhid]]
- **Quran Wiki**: Surah Al-Baqarah (2:285-286), Surah Al-Anfal (8:2-4), Surah Al-Mu'minun (23:1-11)
- **Bridge**: Qaradawi's *Faith and Life* treats iman as a lived reality, connecting creed to happiness, dignity, and hope — directly echoing the Qur'anic passages on the believers.

---

## Shared Concepts

| Qaradawi Library | Quran Wiki | Arabic | Shared Domain |
|---|---|---|---|
| concept-tawhid | themes/tawhid | توحيد | Aqeedah |
| concept-zakat | surah-002 + surah-009 | زكاة | Fiqh |
| concept-prayer | surah-001 + surah-002 | صلاة | Fiqh |
| concept-fasting | surah-002 | صوم | Fiqh |
| concept-hajj | surah-022 | حج | Fiqh |
| concept-usury | surah-002 + surah-003 | ربا | Fiqh |
| concept-marriage | surah-004 | نكاح | Fiqh |
| concept-divorce | surah-002 + surah-065 | طلاق | Fiqh |
| concept-sabr | surah-002 + surah-103 | صبر | Tazkiyah |
| concept-hadith | concepts/asbab-al-nuzul | حديث | Usul |
| concept-sharia | surah-005 | شريعة | Usul |
| concept-jihad | surah-002 + surah-009 | جهاد | Fiqh |
| concept-wasatiyyah | surah-002:143 | وسطية | Ethics |

---

## How to Use

1. **From Qaradawi Library**: When a concept page references a Qur'anic verse, add a `## Qur'anic References` section linking to the relevant Quran Wiki surah page.
2. **From Quran Wiki**: When a surah page includes tafsir that aligns with Qaradawi's fiqh positions, add a `## Fiqh Elaborations` section linking to the Qaradawi Library concept.
3. **Federated queries**: Use `python3 ~/.llm-wiki/.tools/federated_query.py "zakat" --rank --wiki religious/qaradawi-library` to search one wiki, or omit `--wiki` to search all.