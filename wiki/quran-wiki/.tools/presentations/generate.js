const PptxGenJS = require("pptxgenjs");
const fs = require("fs");

// ── Tarbiyyah design tokens (no # prefix for PptxGenJS) ──
const C = {
  primary:     "1B4D3E",
  primaryDark: "164038",
  secondary:   "6B9080",
  accent:      "C9A857",
  surface:     "FAF6F0",
  surfaceRaised:"EDE5D8",
  border:      "D9CFC2",
  text:        "1C1917",
  textMuted:   "57534E",
  white:       "FFFFFF"
};

const W = 10.0, H = 5.625;
const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.12 });

// ── Arabic font ──
const ARABIC_FONT = "Times New Roman"; // Fallback if Amiri not installed
// Try to detect Amiri
const { execSync } = require("child_process");
let arabicFont = "Times New Roman";
try {
  const result = execSync("fc-list | grep -i amiri | head -1", { encoding: "utf-8" });
  if (result.trim().length > 0) arabicFont = "Amiri";
} catch (e) { /* ignore */ }

const pres = new PptxGenJS();
pres.layout = "LAYOUT_16x9";
pres.author = "Tarbiyyah — Quran Wiki Research";
pres.title  = "Surah Al-Muzzammil (73) — Verses 1-19: Divine Orders & Lessons";
pres.subject = "Islamic Scholarly Presentation";

// ──────────────────────────────────────────────────────────────
//  HELPER FUNCTIONS
// ──────────────────────────────────────────────────────────────
function addTopRule(slide) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: W, h: 0.10,
    fill: { color: C.primary }
  });
}

function addVerseBadge(slide, verseNum, y = 0.18) {
  slide.addText(`73:${verseNum}`, {
    x: 0.4, y: y, w: 1.2, h: 0.30,
    fontSize: 16, fontFace: "Georgia", bold: true,
    color: C.accent, align: "left"
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: y + 0.32, w: 1.2, h: 0.03,
    fill: { color: C.accent }
  });
}

function addArabicBox(slide, arabicText, y = 0.60) {
  const boxH = 0.75;
  // Background
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: y, w: W - 0.8, h: boxH,
    fill: { color: C.surfaceRaised }
  });
  // Left gold border
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: y, w: 0.04, h: boxH,
    fill: { color: C.accent }
  });
  // Right gold border
  slide.addShape(pres.shapes.RECTANGLE, {
    x: W - 0.44, y: y, w: 0.04, h: boxH,
    fill: { color: C.accent }
  });
  // Arabic text
  slide.addText(arabicText, {
    x: 0.6, y: y, w: W - 1.2, h: boxH,
    fontSize: 20, fontFace: arabicFont, color: C.primary,
    align: "center", valign: "middle", rtlMode: true
  });
  return y + boxH;
}

function addTranslation(slide, text, y) {
  slide.addText(text, {
    x: 0.6, y: y, w: W - 1.2, h: 0.40,
    fontSize: 14, fontFace: "Calibri", italic: true,
    color: C.textMuted, align: "center"
  });
  return y + 0.42;
}

function addTafsirHeading(slide, heading, y) {
  slide.addText(heading, {
    x: 0.4, y: y, w: W - 0.8, h: 0.30,
    fontSize: 14, fontFace: "Georgia", bold: true,
    color: C.primary, align: "left"
  });
  return y + 0.30;
}

function addBulletText(slide, text, y, opts = {}) {
  slide.addText(text, {
    x: opts.x || 0.5, y: y, w: opts.w || (W - 1.0), h: opts.h || 0.55,
    fontSize: 12, fontFace: "Calibri", color: opts.color || C.text,
    align: "left", valign: "top",
    bullet: opts.bullet !== false,
    paraSpaceAfter: 4
  });
  return y + (opts.h || 0.55) + 0.02;
}

function addFooter(slide, text = "Quran Wiki — Surah Al-Muzzammil (73:1-19) | Tarbiyyah") {
  slide.addText(text, {
    x: 0.4, y: H - 0.40, w: W - 0.8, h: 0.30,
    fontSize: 9, fontFace: "Calibri", color: C.textMuted,
    align: "right"
  });
}

// ──────────────────────────────────────────────────────────────
//  SLIDE 1 — TITLE (DARK)
// ──────────────────────────────────────────────────────────────
let s1 = pres.addSlide();
s1.background = { color: C.primary };
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.08, w: W, h: 0.08,
  fill: { color: C.accent }
});
s1.addText("Surah Al-Muzzammil", {
  x: 0.5, y: 1.2, w: W - 1.0, h: 0.9,
  fontSize: 40, fontFace: "Georgia", bold: true,
  color: C.white, align: "center"
});
s1.addText("المزمل — The Enwrapped One", {
  x: 0.5, y: 2.1, w: W - 1.0, h: 0.5,
  fontSize: 24, fontFace: arabicFont,
  color: C.accent, align: "center"
});
s1.addText("Divine Orders & Major Lessons — Verses 1 to 19", {
  x: 0.5, y: 2.8, w: W - 1.0, h: 0.4,
  fontSize: 18, fontFace: "Calibri", italic: true,
  color: C.surface, align: "center"
});
s1.addText("Meccan Surah | Juz 29 | Pages 574–575 | 20 Verses", {
  x: 0.5, y: 3.5, w: W - 1.0, h: 0.3,
  fontSize: 13, fontFace: "Calibri",
  color: C.secondary, align: "center"
});

// ──────────────────────────────────────────────────────────────
//  SLIDE 2 — INTRODUCTION
// ──────────────────────────────────────────────────────────────
let s2 = pres.addSlide();
s2.background = { color: C.surface };
addTopRule(s2);
s2.addText("Introduction to Surah Al-Muzzammil", {
  x: 0.4, y: 0.25, w: W - 0.8, h: 0.45,
  fontSize: 28, fontFace: "Georgia", bold: true, color: C.primary, align: "left"
});
s2.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.75, w: 1.4, h: 0.04,
  fill: { color: C.accent }
});

let introY = 1.0;
addBulletText(s2, "Revealed in Makkah during the early period of Prophethood", introY);
introY = addBulletText(s2, "The first 19 verses contain fundamental divine commands establishing the spiritual framework of the Prophet's mission", introY + 0.05);
introY = addBulletText(s2, "The surah transitions from intense night prayer obligations to patience in the face of opposition, culminating in warnings of the Hereafter", introY + 0.05);
introY = addBulletText(s2, "Two major thematic sections: (1) Spiritual preparation (verses 1-9), (2) Prophetic conduct & eschatological warning (verses 10-19)", introY + 0.05);
introY = addBulletText(s2, "Sources: Tafsir Ibn Kathir (Abridged) & Tafsir Muyassar — Quran Wiki verified corpus", introY + 0.05, { color: C.textMuted, bullet: false });
addFooter(s2);

// ──────────────────────────────────────────────────────────────
//  SLIDE 3 — VERSES 1-2: THE COMMAND TO RISE AT NIGHT
// ──────────────────────────────────────────────────────────────
let s3 = pres.addSlide();
s3.background = { color: C.surface };
addTopRule(s3);
addVerseBadge(s3, "1-2");
let y3 = addArabicBox(s3, "يَـٰٓأَيُّهَا ٱلْمُزَّمِّلُ ۝ قُمِ ٱلَّيْلَ إِلَّا قَلِيلًا", 0.55);
y3 = addTranslation(s3, "O thou wrapped up in thy raiment! Keep vigil the night long, save a little —", y3 + 0.05);
y3 = addTafsirHeading(s3, "Tafsir Ibn Kathir — The Command to Stand at Night", y3 + 0.05);
addBulletText(s3, "\"Al-Muzzammil\" — one wrapped in garments, asleep. Allah commands the Prophet to cease rest and stand in prayer.", y3);
addBulletText(s3, "This command was initially obligatory for the Prophet alone (17:79), establishing Tahajjud as a foundational spiritual practice.", y3 + 0.55);
addBulletText(s3, "The command extends to believers: \"Their sides forsake their beds, to invoke their Lord in fear and hope\" (32:16).", y3 + 1.10);
addFooter(s3);

// ──────────────────────────────────────────────────────────────
//  SLIDE 4 — VERSES 3-4: DURATION & QURANIC RECITATION
// ──────────────────────────────────────────────────────────────
let s4 = pres.addSlide();
s4.background = { color: C.surface };
addTopRule(s4);
addVerseBadge(s4, "3-4");
let y4 = addArabicBox(s4, "نِّصْفَهُۥٓ أَوِ ٱنقُصْ مِنْهُ قَلِيلًا ۝ أَوْ زِدْ عَلَيْهِ وَرَتِّلِ ٱلْقُرْءَانَ تَرْتِيلًا", 0.55);
y4 = addTranslation(s4, "A half thereof, or abate a little thereof, or add (a little) thereto — and chant the Qur'an in measure,", y4 + 0.05);
y4 = addTafsirHeading(s4, "Divine Flexibility & The Art of Tartil", y4 + 0.05);
addBulletText(s4, "The prescribed duration: half the night, or slightly less (reaching one-third), or slightly more (reaching two-thirds).", y4);
addBulletText(s4, "\"No hardship on you concerning that slight increase or decrease\" — ease within the command.", y4 + 0.55);
addBulletText(s4, "Tartil (ترتيل): reciting slowly, clearly, and with contemplation. A'ishah reported the Prophet recited with measured, distinct pronunciation.", y4 + 1.10);
addBulletText(s4, "The purpose: understanding, reflection, and heartfelt connection — not mere mechanical reading.", y4 + 1.65);
addFooter(s4);

// ──────────────────────────────────────────────────────────────
//  SLIDE 5 — VERSE 5: THE HEAVY WORD
// ──────────────────────────────────────────────────────────────
let s5 = pres.addSlide();
s5.background = { color: C.surface };
addTopRule(s5);
addVerseBadge(s5, "5");
let y5 = addArabicBox(s5, "إِنَّا سَنُلْقِي عَلَيْكَ قَوْلًا ثَقِيلًا", 0.55);
y5 = addTranslation(s5, "For we shall charge thee with a word of weight.", y5 + 0.05);
y5 = addTafsirHeading(s5, "Tafsir Muyassar — The Weight of Revelation", y5 + 0.05);
addBulletText(s5, "\"Qawlan thaqilan\" — a heavy, weighty word: the Quran containing commands, prohibitions, and divine legislation.", y5);
addBulletText(s5, "The revelation is \"heavy\" because it demands commitment, transforms character, and confronts falsehood.", y5 + 0.55);
addBulletText(s5, "This weightiness requires spiritual preparation — hence the preceding command to stand at night in prayer.", y5 + 1.10);
addBulletText(s5, "The Quran is not light entertainment; it is a profound responsibility that reshapes the soul and society.", y5 + 1.65);
addFooter(s5);

// ──────────────────────────────────────────────────────────────
//  SLIDE 6 — VERSE 6: THE POWER OF NIGHT PRAYER
// ──────────────────────────────────────────────────────────────
let s6 = pres.addSlide();
s6.background = { color: C.surface };
addTopRule(s6);
addVerseBadge(s6, "6");
let y6 = addArabicBox(s6, "إِنَّ نَاشِئَةَ ٱلَّيْلِ هِيَ أَشَدُّ وَطْـًٔا وَأَقْوَمُ قِيلًا", 0.55);
y6 = addTranslation(s6, "Lo! the vigil of the night is (a time) when impression is more keen and speech more certain.", y6 + 0.05);
y6 = addTafsirHeading(s6, "Tafsir Muyassar — Why the Night is Superior", y6 + 0.05);
addBulletText(s6, "Night worship has stronger impact on the heart because worldly distractions are absent.", y6);
addBulletText(s6, "\"Aqwamu qilan\" — speech is more upright and accurate because the heart is free from daytime preoccupations.", y6 + 0.55);
addBulletText(s6, "The stillness of night creates the optimal psychological and spiritual conditions for deep connection with Allah.", y6 + 1.10);
addBulletText(s6, "Scientific corroboration: reduced cortisol, heightened prefrontal engagement — the quiet hours enable peak reflection.", y6 + 1.65);
addFooter(s6);

// ──────────────────────────────────────────────────────────────
//  SLIDE 7 — VERSES 7-9: DAYTIME OCCUPATION & COMPLETE DEVOTION
// ──────────────────────────────────────────────────────────────
let s7 = pres.addSlide();
s7.background = { color: C.surface };
addTopRule(s7);
addVerseBadge(s7, "7-9");
let y7 = addArabicBox(s7, "إِنَّ لَكَ فِي ٱلنَّهَارِ سَبْحًا طَوِيلًا ۝ وَٱذْكُرِ ٱسْمَ رَبِّكَ وَتَبَتَّلْ إِلَيْهِ تَبْتِيلًا ۝ رَّبُّ ٱلْمَشْرِقِ وَٱلْمَغْرِبِ لَآ إِلَـٰهَ إِلَّا هُوَ فَٱتَّخِذْهُ وَكِيلًا", 0.55);
y7 = addTranslation(s7, "Lo! thou hast by day a chain of business. So remember the name of thy Lord and devote thyself with a complete devotion — Lord of the East and the West; there is no Allah save Him; so choose thou Him alone for thy defender —", y7 + 0.05);
y7 = addTafsirHeading(s7, "Balance of Day & Night | Total Devotion (Tabattul)", y7 + 0.05);
addBulletText(s7, "Verse 7: Daytime is for worldly duties and propagation. Night is reserved for exclusive communion with Allah.", y7);
addBulletText(s7, "Verse 8: \"Tabattul\" — total, exclusive devotion. Cut all attachments and dedicate worship solely to Allah.", y7 + 0.55);
addBulletText(s7, "Verse 9: Tawhid declaration — Allah is Lord of East and West, the sole deity. Take Him as Wakil (Disposer of Affairs).", y7 + 1.10);
addBulletText(s7, "This is the prophetic balance: active engagement by day, deep devotion by night, tawhid as the constant anchor.", y7 + 1.65);
addFooter(s7);

// ──────────────────────────────────────────────────────────────
//  SLIDE 8 — VERSES 10-11: PATIENCE & RELIANCE ON ALLAH
// ──────────────────────────────────────────────────────────────
let s8 = pres.addSlide();
s8.background = { color: C.surface };
addTopRule(s8);
addVerseBadge(s8, "10-11");
let y8 = addArabicBox(s8, "وَٱصْبِرْ عَلَىٰ مَا يَقُولُونَ وَٱهْجُرْهُمْ هَجْرًا جَمِيلًا ۝ وَذَرْنِي وَٱلْمُكَذِّبِينَ أُو۟لِي ٱلنَّعْمَةِ وَمَهِّلْهُمْ قَلِيلًا", 0.55);
y8 = addTranslation(s8, "And bear with patience what they utter, and part from them with a fair leave-taking. Leave Me to deal with the deniers, lords of ease and comfort; and do thou respite them awhile.", y8 + 0.05);
y8 = addTafsirHeading(s8, "Prophetic Conduct: Sabr & Hijr Jamil", y8 + 0.05);
addBulletText(s8, "\"Sabr\" — patient endurance of mockery, slander, and rejection from the disbelievers.", y8);
addBulletText(s8, "\"Hijran jamilan\" — gracious avoidance: do not retaliate, do not seek revenge. Maintain dignity and noble character.", y8 + 0.55);
addBulletText(s8, "\"Watharnee\" — leave the rejectors to Me. The Prophet's task is delivery (balagh); Allah handles reckoning.", y8 + 1.10);
addBulletText(s8, "\"Wa mahhilhum qaleelan\" — grant them brief respite. Worldly enjoyment is temporary; divine justice is certain.", y8 + 1.65);
addFooter(s8);

// ──────────────────────────────────────────────────────────────
//  SLIDE 9 — VERSES 12-14: WARNING OF THE HEREAFTER
// ──────────────────────────────────────────────────────────────
let s9 = pres.addSlide();
s9.background = { color: C.surface };
addTopRule(s9);
addVerseBadge(s9, "12-14");
let y9 = addArabicBox(s9, "إِنَّ لَدَيْنَآ أَنكَالًا وَجَحِيمًا ۝ وَطَعَامًا ذَا غُصَّةٍ وَعَذَابًا أَلِيمًا ۝ يَوْمَ تَرْجُفُ ٱلْأَرْضُ وَٱلْجِبَالُ وَكَانَتِ ٱلْجِبَالُ كَثِيبًا مَّهِيلًا", 0.55);
y9 = addTranslation(s9, "Lo! with Us are heavy fetters and a raging fire, and food which choketh, and a painful doom — On the day when the earth and the hills rock, and the hills become a heap of running sand.", y9 + 0.05);
y9 = addTafsirHeading(s9, "The Four Punishments of the Rejectors", y9 + 0.05);
addBulletText(s9, "Ankal (أنكال) — Heavy fetters and chains binding the disbelievers in Hellfire.", y9);
addBulletText(s9, "Jahim (جحيم) — A blazing, all-consuming fire of punishment.", y9 + 0.55);
addBulletText(s9, "Ta'am dhu ghussah — Food that chokes, stuck in the throat, neither entering nor exiting.", y9 + 1.10);
addBulletText(s9, "Adhabun aleem — Painful torment on the Day when earth and mountains convulse, and mountains become like flowing sand.", y9 + 1.65);
addFooter(s9);

// ──────────────────────────────────────────────────────────────
//  SLIDE 10 — VERSES 15-16: THE LESSON FROM PHARAOH
// ──────────────────────────────────────────────────────────────
let s10 = pres.addSlide();
s10.background = { color: C.surface };
addTopRule(s10);
addVerseBadge(s10, "15-16");
let y10 = addArabicBox(s10, "إِنَّآ أَرْسَلْنَآ إِلَيْكُمْ رَسُولًا شَـٰهِدًا عَلَيْكُمْ كَمَآ أَرْسَلْنَآ إِلَىٰ فِرْعَوْنَ رَسُولًا ۝ فَعَصَىٰ فِرْعَوْنُ ٱلرَّسُولَ فَأَخَذْنَـٰهُ أَخْذًا وَبِيلًا", 0.55);
y10 = addTranslation(s10, "Lo! We have sent unto you a messenger as witness against you, even as We sent unto Pharaoh a messenger. But Pharaoh rebelled against the messenger, whereupon We seized him with no gentle grip.", y10 + 0.05);
y10 = addTafsirHeading(s10, "The Parable of Pharaoh — A Stern Warning", y10 + 0.05);
addBulletText(s10, "The Prophet Muhammad is a \"shahid\" (witness) over his Ummah — his testimony will be presented on Judgment Day.", y10);
addBulletText(s10, "Pharaoh was sent Musa (AS) as a messenger; he denied, rebelled, and was seized by Allah with crushing punishment.", y10 + 0.55);
addBulletText(s10, "\"Akhdhan wabeelan\" — a severe, ruinous seizure. The parallel is explicit: reject the messenger, face the consequence.", y10 + 1.10);
addBulletText(s10, "This is a warning to the Makkan Quraysh: the fate of Pharaoh awaits those who persist in denial.", y10 + 1.65);
addFooter(s10);

// ──────────────────────────────────────────────────────────────
//  SLIDE 11 — VERSES 17-18: THE DAY OF RESURRECTION
// ──────────────────────────────────────────────────────────────
let s11 = pres.addSlide();
s11.background = { color: C.surface };
addTopRule(s11);
addVerseBadge(s11, "17-18");
let y11 = addArabicBox(s11, "فَكَيْفَ تَتَّقُونَ إِن كَفَرْتُمْ يَوْمًا يَجْعَلُ ٱلْوِلْدَ ٰ⁠نَ شِيبًا ۝ ٱلسَّمَآءُ مُنفَطِرُۢ بِهِۦۚ كَانَ وَعْدُهُۥ مَفْعُولًا", 0.55);
y11 = addTranslation(s11, "Then how, if ye disbelieve, will ye protect yourselves upon the day which will turn children grey, the very heaven being then rent asunder. His promise is to be fulfilled.", y11 + 0.05);
y11 = addTafsirHeading(s11, "Tafsir Muyassar — The Unimaginable Terror", y11 + 0.05);
addBulletText(s11, "A Day so terrifying that children will turn white-haired from sheer horror and dread.", y11);
addBulletText(s11, "The sky itself will be rent asunder — the cosmic order will collapse before the power of Allah.", y11 + 0.55);
addBulletText(s11, "\"Kana wa'duhu maf'oolan\" — His promise is certainly fulfilled. The resurrection is not conjecture; it is guaranteed reality.", y11 + 1.10);
addBulletText(s11, "The rhetorical question: if you deny Allah now, what defense will you have on that Day?", y11 + 1.65);
addFooter(s11);

// ──────────────────────────────────────────────────────────────
//  SLIDE 12 — VERSE 19: A REMINDER & FREE WILL
// ──────────────────────────────────────────────────────────────
let s12 = pres.addSlide();
s12.background = { color: C.surface };
addTopRule(s12);
addVerseBadge(s12, "19");
let y12 = addArabicBox(s12, "إِنَّ هَـٰذِهِۦ تَذْكِرَةٌۖ فَمَن شَآءَ ٱتَّخَذَ إِلَىٰ رَبِّهِۦ سَبِيلًا", 0.55);
y12 = addTranslation(s12, "Lo! This is a Reminder. Let him who will, then, choose a way unto his Lord.", y12 + 0.05);
y12 = addTafsirHeading(s12, "Tafsir Ibn Kathir — Admonition & Divine Will", y12 + 0.05);
addBulletText(s12, "\"Hadhihi tathkirah\" — This surah is an admonition, a reminder for those of sound understanding.", y12);
addBulletText(s12, "\"Faman shaa attakhadha ila rabbihi sabeelan\" — Whoever wills may take a path to his Lord.", y12 + 0.55);
addBulletText(s12, "The will is ultimately subject to Allah's will: \"But you cannot will, unless Allah wills\" (76:30).", y12 + 1.10);
addBulletText(s12, "This verse balances human responsibility with divine sovereignty — a cornerstone of Ahl al-Sunnah theology.", y12 + 1.65);
addFooter(s12);

// ──────────────────────────────────────────────────────────────
//  SLIDE 13 — MAJOR DIVINE ORDERS (SUMMARY)
// ──────────────────────────────────────────────────────────────
let s13 = pres.addSlide();
s13.background = { color: C.surface };
addTopRule(s13);
s13.addText("Major Divine Orders (Verses 1-19)", {
  x: 0.4, y: 0.25, w: W - 0.8, h: 0.45,
  fontSize: 28, fontFace: "Georgia", bold: true, color: C.primary, align: "left"
});
s13.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.75, w: 1.4, h: 0.04,
  fill: { color: C.accent }
});

let orders = [
  { v: "1-4", text: "Qiyam al-Lail — Stand in night prayer (Tahajjud) for half the night or near it" },
  { v: "4", text: "Tartil — Recite the Quran slowly, distinctly, with contemplation" },
  { v: "8", text: "Dhikr & Tabattul — Remember Allah's name with complete, exclusive devotion" },
  { v: "9", text: "Tawhid & Tawakkul — Affirm Allah as sole deity; take Him as Wakil" },
  { v: "10", text: "Sabr — Exercise patient endurance against mockery and rejection" },
  { v: "10", text: "Hijr Jamil — Avoid opponents with gracious, noble conduct" },
  { v: "11", text: "Tafweedh — Leave the rejectors to Allah; focus on delivery (balagh)" },
  { v: "19", text: "Ikhtiyar — Choose the path to Allah; exercise free will within divine decree" }
];

let oy = 1.0;
orders.forEach((o, i) => {
  s13.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: oy, w: 0.35, h: 0.28,
    fill: { color: C.primary }
  });
  s13.addText(o.v, {
    x: 0.4, y: oy, w: 0.35, h: 0.28,
    fontSize: 11, fontFace: "Calibri", bold: true,
    color: C.white, align: "center", valign: "middle"
  });
  s13.addText(o.text, {
    x: 0.85, y: oy, w: W - 1.3, h: 0.28,
    fontSize: 12, fontFace: "Calibri",
    color: C.text, align: "left", valign: "middle"
  });
  oy += 0.34;
});
addFooter(s13);

// ──────────────────────────────────────────────────────────────
//  SLIDE 14 — MAJOR LESSONS (SUMMARY)
// ──────────────────────────────────────────────────────────────
let s14 = pres.addSlide();
s14.background = { color: C.surface };
addTopRule(s14);
s14.addText("Major Lessons from Surah Al-Muzzammil", {
  x: 0.4, y: 0.25, w: W - 0.8, h: 0.45,
  fontSize: 28, fontFace: "Georgia", bold: true, color: C.primary, align: "left"
});
s14.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.75, w: 1.4, h: 0.04,
  fill: { color: C.accent }
});

let lessons = [
  "Spiritual preparation precedes prophetic duty — night prayer is the foundation of revelation-bearing.",
  "The Quran demands weighty commitment; it is not light reading but life-transforming legislation.",
  "Night prayer creates the optimal conditions for deep reflection and sincere supplication.",
  "The prophetic model requires balance: active daytime engagement + deep nighttime devotion.",
  "Patience and gracious avoidance are superior to retaliation when facing opposition.",
  "Divine justice is certain; worldly respite for rejectors is temporary and deceptive.",
  "The fate of Pharaoh serves as a universal warning to all who reject Allah's messengers.",
  "Human will operates within divine decree — we choose, but Allah ultimately enables and guides."
];

let ly = 1.0;
lessons.forEach((l, i) => {
  s14.addShape(pres.shapes.OVAL, {
    x: 0.45, y: ly + 0.04, w: 0.18, h: 0.18,
    fill: { color: C.accent }
  });
  s14.addText(String(i + 1), {
    x: 0.45, y: ly + 0.04, w: 0.18, h: 0.18,
    fontSize: 10, fontFace: "Calibri", bold: true,
    color: C.white, align: "center", valign: "middle"
  });
  s14.addText(l, {
    x: 0.75, y: ly, w: W - 1.2, h: 0.50,
    fontSize: 12, fontFace: "Calibri",
    color: C.text, align: "left", valign: "top",
    paraSpaceAfter: 2
  });
  ly += 0.52;
});
addFooter(s14);

// ──────────────────────────────────────────────────────────────
//  SLIDE 15 — CONCLUSION (DARK)
// ──────────────────────────────────────────────────────────────
let s15 = pres.addSlide();
s15.background = { color: C.primary };
s15.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.08, w: W, h: 0.08,
  fill: { color: C.accent }
});
s15.addText("Conclusion", {
  x: 0.5, y: 0.5, w: W - 1.0, h: 0.5,
  fontSize: 32, fontFace: "Georgia", bold: true,
  color: C.white, align: "center"
});
s15.addText("رَبَّنَا تَقَبَّلْ مِنَّا إِنَّكَ أَنْتَ السَّمِيعُ الْعَلِيمُ", {
  x: 0.5, y: 1.3, w: W - 1.0, h: 0.5,
  fontSize: 22, fontFace: arabicFont,
  color: C.accent, align: "center"
});
s15.addText("Our Lord, accept from us; indeed, You are the All-Hearing, the All-Knowing.", {
  x: 0.5, y: 1.9, w: W - 1.0, h: 0.35,
  fontSize: 14, fontFace: "Calibri", italic: true,
  color: C.surface, align: "center"
});
s15.addText("Surah Al-Muzzammil teaches us that spiritual elevation requires night devotion, patient conduct, unwavering tawhid, and trust in divine justice. The path to Allah is open to whoever wills — may we be among those who choose it.", {
  x: 0.5, y: 2.6, w: W - 1.0, h: 0.9,
  fontSize: 14, fontFace: "Calibri",
  color: C.surface, align: "center"
});
s15.addText("Sources: Quran Wiki (verified against Al Quran Cloud API & Quran.com API) | Tafsir Ibn Kathir (Abridged) | Tafsir Muyassar", {
  x: 0.5, y: 3.8, w: W - 1.0, h: 0.3,
  fontSize: 10, fontFace: "Calibri",
  color: C.secondary, align: "center"
});

// ── WRITE ──
pres.writeFile({ fileName: "surah-muzzammil-73-v1-19.pptx" });
console.log("Presentation saved: surah-muzzammil-73-v1-19.pptx");
