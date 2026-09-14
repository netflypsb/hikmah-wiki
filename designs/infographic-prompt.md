# Hikmah Project — Image Generation Prompt

Use with: Midjourney / DALL-E 3 / Ideogram / Flux (tested structure works across all).
Output target: GitHub repository README banners.

---

## MASTER PROMPT (recommended primary)

A clean, professional infographic in flat modern vector illustration style, warm paper
background color #f8f6f2, deep navy #0a2540 accents, terracotta #c45c3e highlights,
soft sage green secondary accents, generous white space, thin elegant line work,
wide horizontal banner format 1600x800 pixels, 16:8 aspect ratio.

Title at top center in large elegant serif typography: "THE HIKMAH PROJECT"
with subtitle in smaller sans-serif: "Bringing Islamic Literature to the World —
for Humans and for AI". A small decorative geometric Islamic star motif in terracotta
sits left and right of the title.

The infographic is organized as THREE connected sections arranged horizontally
like a flowing pipeline from left to right, connected by elegant thin arrows
with subtle terracotta gradient:

**LEFT SECTION — "SOURCES" (label at top in navy):**
A stack of stylized book and document icons in muted navy and sage: an open Quran
manuscript with gold illumination border, classical Arabic books stacked, a digital
document icon. Small caption underneath: "Qur'an · Tafsir · Classical & Contemporary
Scholarship". A thin dotted line flows from this stack toward the center.

**CENTER SECTION — "THE ENGINE" (largest visual weight, slightly elevated):**
A prominent glowing gear-workflow diagram in navy and terracotta showing the engine
as a rounded rectangular hub labeled "HIKMAH ENGINE" with five small connected
module chips arranged around it labeled: "Extract", "Validate", "Lint", "Graph",
"Gates". Beneath the hub, three small checkmark badges in sage green labeled
"Quality Gates", "Provenance", "Source Tiers". Caption: "Open-source pipeline
(MIT) — turns raw sources into auditable knowledge. Works with any AI agent."

**RIGHT SECTION — "TWO OUTPUTS":**
Two rounded panels side by side:
(a) A panel labeled "LLM WIKI" showing a stylized network graph of connected
nodes (small circles connected by lines, like a knowledge graph) in navy with
a few terracotta and sage nodes highlighted, small caption: "1,000+ interlinked
pages · 6 wikis · every claim traced to source".
(b) A panel labeled "BAYT AL-HIKMAH" showing a simplified elegant website mockup
(books on a shelf icon, Arabic calligraphy flourish), caption: "Human-readable
digital library · free for everyone".

**BOTTOM STRIP — "WHO THIS SERVES / HOW TO HELP":**
A single row of five small icon-and-label groups separated by thin vertical
dividers, evenly spaced:
1. Scholar icon (book + magnifier) — "Verify & cite — every claim auditable"
2. Developer icon (terminal + gear) — "Build with the engine — MIT licensed"
3. Islamic app builder icon (phone + Quran) — "Free structured content — CC BY-SA"
4. AI researcher icon (neural network nodes) — "Clean grounded data for Islamic AI"
5. Contributor icon (hands + plus sign) — "Add sources, review, translate — open to all"

Bottom right corner, small text: "github.com/netflypsb/hikmah-engine ·
github.com/netflypsb/hikmah-wiki". Small CC BY-SA + MIT license badges bottom left.

Overall mood: scholarly, calm, trustworthy, modern Islamic aesthetics — geometric
patterns used sparingly as borders and dividers, NO photographic elements, no
people, no photorealism, flat vector style, crisp edges, high contrast text,
generous negative space, professional open-source project banner quality.

---

## ALTERNATE VERSION A — Vertical (GitHub social preview / README side placement)

Same content and palette as above, but portrait format 1200x1500 pixels, 4:5 aspect.
Layout: title top, three sections stacked vertically (Sources → Engine → Outputs),
stakeholder strip at bottom. The Engine section is visually the largest block in
the middle of the composition.

---

## ALTERNATE VERSION B — Minimal wide banner (README top)

Ultra-wide 1600x500 pixels, 16:5 aspect. Only: title + one-line subtitle,
three compact icon blocks (Sources stack → Engine gear → two output panels),
single-line stakeholder strip. Fewer words, larger icons. Use when the README
already explains details in text.

---

## SIZING GUIDANCE FOR GITHUB

| Placement | Dimensions | Aspect | Notes |
|---|---|---|---|
| README top banner | 1600x800 (2x for retina: 1280x640 logical) | 2:1 | Sweet spot — GitHub renders up to ~830px wide in content column; upload 1600px wide and it scales down sharp |
| Social preview (repo settings) | 1280x640 | 2:1 | GitHub crops to this for link cards |
| README side float | 800x1000 | 4:5 | Vertical alternate A |
| Compact top banner | 1600x500 | 16:5 | Alternate B |

Rules:
- Generate at 2x the display size (retina crispness).
- Keep total text <150 words in the image; GitHub compresses PNGs and small text
  blurs. Every label must remain readable at 50% scale.
- Export as PNG (lossless) under 300KB; avoid JPEG (text artifacts).
- Test readability by viewing the README on a phone before committing.

---

## NEGATIVE PROMPT (if the generator supports it)

photorealistic, 3D render, people, faces, photographic texture, clutter, dense text
walls, watermarks, logos of real companies, dark background, neon colors, gradients
everywhere, drop shadows everywhere, stock-photo look, hands, religious icons
outside the specified manuscript/book style, Arabic script rendered incorrectly
or as gibberish

NOTE ON ARABIC TEXT: image generators frequently mangle Arabic calligraphy.
If the output renders broken Arabic, regenerate with this line removed:
"Arabic calligraphy flourish" — keep only the geometric star motif, which
generates reliably.

---

## TEXT SAFEGUARD

Image models misspell words. If any generated text is garbled, prefer this
two-step approach: (1) generate the illustration WITHOUT any text/labels, (2)
overlay the real text with a design tool (Figma/Canva/HTML+CSS) using the exact
labels above. This guarantees perfect spelling and lets you update numbers
(1,074 pages → 1,500 pages) without regenerating the art.