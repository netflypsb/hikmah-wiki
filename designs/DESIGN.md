# Tarbiyyah Design System — Islamic Scholarly Aesthetic

Brand tokens for all HTML presentations, articles, and visual assets produced by the Tarbiyyah project.

---

## Brand Philosophy

Tarbiyyah designs must feel like the intersection of a classical Islamic manuscript and a modern digital publication. Every design should evoke:
- **Reverence** — through typography and space
- **Clarity** — through clean layouts and high contrast
- **Timelessness** — through restrained palettes and classical proportions
- **Scholarly authority** — through structured hierarchies and generous margins

---

## Colour Tokens

| Token | Hex | Usage |
|---|---|---|
| `--ink` | `#1C1917` | Primary text — like the ink of a classical manuscript |
| `--ink-light` | `#57534E` | Secondary text, captions, metadata |
| `--parchment` | `#FAF6F0` | Page background — warm, aged paper feel |
| `--parchment-dark` | `#EDE5D8` | Alternating section backgrounds, cards, subtle panels |
| `--green-deep` | `#1B4D3E` | Primary accent — the colour of paradise in Islamic tradition |
| `--green-muted` | `#6B9080` | Secondary accent, borders, secondary buttons |
| `--gold-rich` | `#C9A857` | Highlights for Arabic text, key terms, decorative elements |
| `--gold-pale` | `#E8D5A3` | Subtle gold for background accents, hover states |
| `--terracotta` | `#A0522D` | Tertiary accent for warnings, editorial markers |

### Background Patterns
Use a **subtle geometric Islamic pattern** as a very faint watermark (~3–5% opacity) on:
- Hero sections
- Section dividers between chapters
- Title card backgrounds

Implement as:
```css
background-image: url("data:image/svg+xml,...");
background-repeat: repeat;
background-size: 40px 40px;
opacity: 0.04;
```

---

## Typography

| Role | Font | Weight | Notes |
|---|---|---|---|
| Arabic script | **Amiri** (Google Fonts) | 400, 700 | Classical Arabic typeface. Use for: Qur'anic verses, hadith Arabic text, Arabic terminology, du'a |
| Latin headings | **Crimson Pro** (Google Fonts) | 400, 500, 700 | Scholarly serif. Feels like a traditional book. Use for article titles, section headings, chapter numbers |
| Latin body | **Source Sans 3** (Google Fonts) | 400, 600 | Humanist sans. Highly readable for long-form text. Use for body, explanations, citations |
| Code / metadata | **IBM Plex Mono** | 400 | Optional for technical metadata, hadith reference numbers |

### Type Scale
| Level | Size | Font | Usage |
|---|---|---|---|
| Display | 48–64px | Crimson Pro 700 | Hero titles |
| H1 | 40px | Crimson Pro 700 | Chapter / article title |
| H2 | 32px | Crimson Pro 500 | Section headings |
| H3 | 24px | Crimson Pro 500 | Sub-section headings |
| H4 | 20px | Crimson Pro 400 | Sub-sub headings |
| Arabic quote | 22px | Amiri 400 | Qur'anic verses and hadith |
| Body | 18px | Source Sans 3 400 | Paragraphs |
| Body-sm | 16px | Source Sans 3 400 | Long explanations |
| Caption | 14px | Source Sans 3 400 | Metadata, footnotes, hadith chains |
| Reference | 13px | Source Sans 3 600 | In-text citations |

### Qur'anic Verse Styling
```css
.arabic-ayah {
  font-family: 'Amiri', serif;
  font-size: 22px;
  font-style: italic;
  color: var(--green-deep);
  text-align: center;
  padding: 24px 40px;
  border-right: 3px solid var(--gold-rich);
  border-left: 3px solid var(--gold-rich);
  background: var(--parchment-dark);
  margin: 32px 0;
}
.ayah-reference {
  font-family: 'Source Sans 3', sans-serif;
  font-size: 13px;
  color: var(--gold-rich);
  text-align: center;
  margin-top: 8px;
}
```

### Hadith Block Styling
```css
.hadith-block {
  font-family: 'Amiri', serif;
  font-size: 20px;
  color: var(--ink);
  background: var(--parchment-dark);
  padding: 24px 32px;
  border-radius: 8px;
  border-top: 4px solid var(--green-deep);
  margin: 28px 0;
}
.hadith-chain {
  font-family: 'Source Sans 3', sans-serif;
  font-size: 13px;
  color: var(--ink-light);
  margin-top: 12px;
  font-style: italic;
}
```

---

## Layout Principles

1. **Generous margins** — minimum 64px on desktop sections. Content should breathe.
2. **Single-column reading** — maximum content width 720px for articles (optimal line length).
3. **Cards** — use only when comparing multiple items. Default is open flowing text.
4. **Section dividers** — use subtle decorative Islamic geometric dividers (SVG) between major sections.
5. **Footnotes** — superscript numbers in gold. References panel at the bottom of every article.

---

## Component Styles

### Buttons
```css
.btn-primary {
  background: var(--green-deep);
  color: #fff;
  padding: 12px 28px;
  border: none;
  border-radius: 4px;
  font-family: 'Source Sans 3', sans-serif;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-primary:hover {
  background: #164038;
}
.btn-secondary {
  background: transparent;
  color: var(--green-deep);
  border: 2px solid var(--green-muted);
  padding: 10px 26px;
  border-radius: 4px;
}
```

### Reference Callout
```css
.reference-callout {
  background: var(--parchment-dark);
  border-left: 4px solid var(--gold-rich);
  padding: 16px 20px;
  margin: 20px 0;
  font-family: 'Source Sans 3', sans-serif;
  font-size: 14px;
  color: var(--ink);
}
.reference-callout strong {
  color: var(--terracotta);
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.05em;
}
```

### Numbered List (for scholarly arguments)
```css
.scholarly-list {
  list-style: none;
  counter-reset: argument;
}
.scholarly-list li {
  counter-increment: argument;
  margin-bottom: 16px;
  padding-left: 40px;
  position: relative;
}
.scholarly-list li::before {
  content: counter(argument);
  position: absolute;
  left: 0;
  top: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--green-deep);
  color: #fff;
  font-family: 'Crimson Pro', serif;
  font-size: 15px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

---

## Animation Rules

- **NO infinite animations** (religious reverence + no distraction)
- Allowed: subtle scroll-reveal fade-ins (single pass, no loop)
- Allowed: hover colour transitions (smooth, ≤0.3s)
- Prohibited: spinning, bouncing, pulsing, music, anything cartoonish
- Decorative geometric SVG elements may have slow, one-off entrance animations

---

## Google Fonts Import

Always load these three:
```html
<link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Crimson+Pro:wght@400;500;600;700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
```

---

## Export Scripts

Available in `.claude/skills/design/scripts/`:
- `preview.sh` — open the design in browser
- `export-pdf.sh` — generate PDF from HTML
- `export-pptx.js` — generate PowerPoint from slide deck HTML

Use these for distributing articles as PDFs or presentations as PPTX.

---

*This design system reflects the scholarly dignity of the Islamic tradition while delivering modern, accessible digital content.*
