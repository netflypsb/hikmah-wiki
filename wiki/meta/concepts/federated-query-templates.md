---
title: Federated Query Templates
created: '2026-06-09'
updated: '2026-06-09'
type: meta
tags: [meta, queries, templates]
---

# Federated Query Templates

> Pre-built query patterns for searching across the LLM Wiki hub.
> Use `python3 ~/.llm-wiki/.tools/federated_query.py "<query>" [options]`

---

## Command Reference

```bash
# Search all wikis for a term
python3 ~/.llm-wiki/.tools/federated_query.py "zakat" --rank

# Search one wiki only
python3 ~/.llm-wiki/.tools/federated_query.py "prayer" --wiki religious/qaradawi-library

# Exact filename match
python3 ~/.llm-wiki/.tools/federated_query.py "concept-zakat" --exact

# Limit results
python3 ~/.llm-wiki/.tools/federated_query.py "tafsir" --rank --top 5
```

---

## Islamic Studies Queries

| Query | Scope | Purpose |
|-------|-------|---------|
| `zakat` | all wikis | Zakah/charity rulings across Quran and fiqh |
| `riba usury interest` | qaradawi-library | Usury/riba positions in Qaradawi's corpus |
| `prayer salah` | all wikis | Prayer rulings and Qur'anic references |
| `halal haram permissibility` | qaradawi-library | Permissibility principles |
| `sunnah hadith methodology` | qaradawi-library | Hadith authentication and application |
| `wasatiyyah moderation middle` | qaradawi-library | Wasatiyyah across all books |
| `tawhid monotheism` | all wikis | Tawhid in Quran and scholarly analysis |
| `marriage divorce family` | qaradawi-library | Family law in Qaradawi's works |
| `economics poverty social security` | qaradawi-library | Islamic economic justice framework |
| `ethics morality character akhlaq` | qaradawi-library | Ethics across Qaradawi's books |

## Medical Queries (Shafira/Hoffbrand)

| Query | Scope | Purpose |
|-------|-------|---------|
| `haemoglobin anaemia` | hoffbrand-9th-edition | Haem pathology |
| `leukaemia ALL AML` | hoffbrand-9th-edition | Acute leukaemias |
| `stem cell transplant HSCT` | all wikis | HSCT across medical wiki |

---

## Cross-Wiki Synthesis Patterns

### Pattern 1: Fiqh + Qur'an
Search for a legal ruling in Qaradawi Library, then find the Qur'anic source verse in Quran Wiki:
```bash
# Step 1: Find the ruling
python3 ~/.llm-wiki/.tools/federated_query.py "zakat nisab threshold" --wiki religious/qaradawi-library --rank

# Step 2: Find the verse
python3 ~/.llm-wiki/.tools/federated_query.py "2:177 2:215" --wiki religious/quran-wiki --rank
```

### Pattern 2: Concept Comparison
Search for a concept across all wikis to find how different corpora treat it:
```bash
python3 ~/.llm-wiki/.tools/federated_query.py "justice adl" --rank --top 20
```

### Pattern 3: Scholar vs Primary Source
Find Qaradawi's position, then verify against the Qur'anic primary text:
```bash
python3 ~/.llm-wiki/.tools/federated_query.py "riba" --wiki religious/qaradawi-library --rank
python3 ~/.llm-wiki/.tools/federated_query.py "riba interest usury" --wiki religious/quran-wiki --rank
```