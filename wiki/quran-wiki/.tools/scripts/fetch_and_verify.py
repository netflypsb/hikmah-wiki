#!/usr/bin/env python3
"""
Fetch all 6236 ayahs from Al Quran Cloud and Quran.com APIs.
Cross-verify character-by-character.
Save each ayah as individual markdown file.
Log discrepancies.
"""
import asyncio
import json
import os
import ssl
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from collections import defaultdict

# Surah -> ayah count mapping (source: Al Quran Cloud /surah endpoint as canonical)
SURAH_AYAH_COUNTS = [
    7, 286, 200, 176, 120, 165, 206, 75, 129, 109,
    123, 111, 43, 52, 99, 128, 111, 110, 98, 135,
    112, 78, 118, 64, 77, 227, 93, 88, 69, 60,
    34, 30, 73, 54, 45, 83, 182, 88, 75, 85,
    54, 53, 89, 59, 37, 35, 38, 29, 18, 45,
    60, 49, 62, 55, 78, 96, 29, 22, 24, 13,
    14, 11, 11, 18, 12, 12, 30, 52, 52, 44,
    28, 28, 20, 56, 40, 31, 50, 40, 46, 42,
    29, 19, 36, 25, 22, 17, 19, 26, 30, 20,
    15, 21, 11, 8, 8, 19, 5, 8, 8, 11,
    11, 8, 3, 9, 5, 4, 7, 3, 6, 3,
    5, 4, 5, 6
]

TOTAL_AYAHS = sum(SURAH_AYAH_COUNTS)  # 6236

OUTPUT_DIR = "/root/tarbiyyah/quran-wiki/arabic"
DISCREPANCY_DIR = "/root/tarbiyyah/quran-wiki/discrepancies"
LOG_DIR = "/root/tarbiyyah/quran-wiki/logs"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DISCREPANCY_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# SSL context that doesn't verify certs (some WSL setups need this)
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

MAX_CONCURRENT = 8
REQUEST_DELAY = 0.15  # ~6-7 req/sec, well within generous limits


async def fetch_url(url, semaphore, retries=3):
    """Fetch a URL with retry logic."""
    async with semaphore:
        for attempt in range(retries):
            try:
                req = Request(url, headers={"User-Agent": "Hermes-QuranWiki/1.0"})
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: urlopen(req, context=SSL_CTX, timeout=30).read())
                await asyncio.sleep(REQUEST_DELAY)
                return json.loads(data)
            except HTTPError as e:
                if e.code == 429 and attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return {"__error__": f"HTTP {e.code}: {e.reason}", "url": url}
            except URLError as e:
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return {"__error__": f"URLError: {e.reason}", "url": url}
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return {"__error__": f"Exception: {str(e)}", "url": url}
        return {"__error__": "Max retries exceeded", "url": url}


def extract_text_aq(response):
    """Extract Arabic text from Al Quran Cloud response."""
    try:
        return response["data"]["text"].strip()
    except (KeyError, TypeError):
        return None


def extract_text_qc(response):
    """Extract Arabic text from Quran.com response."""
    try:
        verse = response["verse"]
        if isinstance(verse, dict):
            return verse.get("text_uthmani", "").strip()
        if isinstance(verse, list) and len(verse) > 0:
            return verse[0].get("text_uthmani", "").strip()
        return None
    except (KeyError, TypeError):
        return None


def normalize_arabic(text):
    """Normalize Arabic text for comparison: strip leading Bismillah if present (for surah > 1), normalize whitespace."""
    if not text:
        return ""
    text = text.replace("\u0640", "")  # Remove tatweel/kashida for comparison
    text = " ".join(text.split())  # Normalize whitespace
    return text.strip()


def build_markdown(surah, ayah, text_aq, text_qc, match):
    """Build the markdown content for an ayah."""
    lines = [
        f"# Surah {surah:03d}, Ayah {ayah:03d}",
        "",
        "> **Status:** " + ("VERIFIED " if match else "**DISCREPANCY DETECTED** "),
        f"> **Sources:** Al Quran Cloud (`quran-uthmani-quran-academy`) | Quran.com (`text_uthmani`)",
        "",
        "## Arabic Text (Al Quran Cloud — Primary)",
        "",
        f"```text",
        f"{text_aq}",
        f"```",
        "",
        "## Arabic Text (Quran.com — Cross-reference)",
        "",
        f"```text",
        f"{text_qc}",
        f"```",
        "",
    ]
    if not match:
        lines.extend([
            "## ⚠️ Discrepancy Details",
            "",
            f"- **Al Quran Cloud length:** {len(text_aq)} characters",
            f"- **Quran.com length:** {len(text_qc)} characters",
            "",
            "## Character Diff (first 20 differing positions)",
            "",
        ])
        diffs = []
        max_len = max(len(text_aq), len(text_qc))
        for i in range(max_len):
            c1 = text_aq[i] if i < len(text_aq) else "<EOF>"
            c2 = text_qc[i] if i < len(text_qc) else "<EOF>"
            if c1 != c2:
                diffs.append(f"| Position {i} | `{repr(c1)}` | `{repr(c2)}` |")
                if len(diffs) >= 20:
                    diffs.append("| ... | ... | ... |")
                    break
        lines.append("| Position | Al Quran Cloud | Quran.com |")
        lines.append("|----------|---------------|-----------|")
        lines.extend(diffs)
        lines.append("")
    lines.extend([
        "---",
        f"*Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}*",
    ])
    return "\n".join(lines)


async def process_ayah(surah, ayah, semaphore, stats):
    """Process a single ayah: fetch both APIs, compare, save."""
    key = f"{surah:03d}-{ayah:03d}"
    url_aq = f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/quran-uthmani-quran-academy"
    url_qc = f"https://api.quran.com/api/v4/verses/by_key/{surah}:{ayah}?fields=text_uthmani"

    # Fetch both
    resp_aq, resp_qc = await asyncio.gather(
        fetch_url(url_aq, semaphore),
        fetch_url(url_qc, semaphore),
    )

    text_aq_raw = extract_text_aq(resp_aq)
    text_qc_raw = extract_text_qc(resp_qc)

    error_aq = "__error__" in str(resp_aq)
    error_qc = "__error__" in str(resp_qc)

    if text_aq_raw is None:
        stats["missing_aq"].append(key)
    if text_qc_raw is None:
        stats["missing_qc"].append(key)

    # Use whichever source is available
    if text_aq_raw:
        text_aq = text_aq_raw
    else:
        text_aq = text_qc_raw or ""

    if text_qc_raw:
        text_qc = text_qc_raw
    else:
        text_qc = text_aq_raw or ""

    norm_aq = normalize_arabic(text_aq)
    norm_qc = normalize_arabic(text_qc)

    match = (norm_aq == norm_qc) and not (error_aq or error_qc)

    if not match and text_aq and text_qc:
        stats["discrepancies"].append(key)

    markdown = build_markdown(surah, ayah, text_aq, text_qc, match)

    filepath = os.path.join(OUTPUT_DIR, f"{key}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)

    stats["processed"] += 1
    return key, match


async def main():
    stats = {
        "processed": 0,
        "discrepancies": [],
        "missing_aq": [],
        "missing_qc": [],
        "start_time": time.time(),
    }

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    tasks = []

    print(f"Starting fetch of {TOTAL_AYAHS} ayahs...")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"Max concurrent: {MAX_CONCURRENT}, delay: {REQUEST_DELAY}s")
    print()

    for surah in range(1, 115):
        for ayah in range(1, SURAH_AYAH_COUNTS[surah - 1] + 1):
            tasks.append(process_ayah(surah, ayah, semaphore, stats))

    # Process with periodic status updates
    completed = 0
    report_interval = 500
    next_report = report_interval

    for coro in asyncio.as_completed(tasks):
        key, match = await coro
        completed += 1
        if completed >= next_report:
            elapsed = time.time() - stats["start_time"]
            rate = completed / elapsed if elapsed > 0 else 0
            eta = (TOTAL_AYAHS - completed) / rate if rate > 0 else 0
            print(f"  [{completed}/{TOTAL_AYAHS}] {key} — rate: {rate:.1f}/s — ETA: {eta/60:.1f}min")
            next_report += report_interval

    elapsed = time.time() - stats["start_time"]
    print(f"\n{'='*60}")
    print(f"DONE in {elapsed/60:.1f} minutes")
    print(f"Total processed: {stats['processed']}/{TOTAL_AYAHS}")
    print(f"Discrepancies: {len(stats['discrepancies'])}")
    print(f"Missing from Al Quran Cloud: {len(stats['missing_aq'])}")
    print(f"Missing from Quran.com: {len(stats['missing_qc'])}")

    # Write discrepancy report
    discrepancy_path = os.path.join(DISCREPANCY_DIR, "discrepancy_report.json")
    with open(discrepancy_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    # Write summary log
    log_path = os.path.join(LOG_DIR, f"fetch_{time.strftime('%Y%m%d_%H%M%S')}.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Quran Wiki Fetch & Verify\n")
        f.write(f"{'='*60}\n")
        f.write(f"Total ayahs: {TOTAL_AYAHS}\n")
        f.write(f"Processed:   {stats['processed']}\n")
        f.write(f"Elapsed:     {elapsed/60:.1f} minutes\n")
        f.write(f"Rate:        {stats['processed']/elapsed:.1f} ayahs/sec\n")
        f.write(f"Discrepancies: {len(stats['discrepancies'])}\n")
        f.write(f"Missing AQ:  {len(stats['missing_aq'])}\n")
        f.write(f"Missing QC:  {len(stats['missing_qc'])}\n")
        if stats["discrepancies"]:
            f.write(f"\nDiscrepancy list ({len(stats['discrepancies'])}):\n")
            for d in stats["discrepancies"]:
                f.write(f"  - {d}\n")
        if stats["missing_aq"]:
            f.write(f"\nMissing from Al Quran Cloud ({len(stats['missing_aq'])}):\n")
            for d in stats["missing_aq"]:
                f.write(f"  - {d}\n")
        if stats["missing_qc"]:
            f.write(f"\nMissing from Quran.com ({len(stats['missing_qc'])}):\n")
            for d in stats["missing_qc"]:
                f.write(f"  - {d}\n")

    print(f"\nFiles written:")
    print(f"  Discrepancy report: {discrepancy_path}")
    print(f"  Summary log:        {log_path}")

    # Also write a simple discrepancy CSV
    if stats["discrepancies"]:
        csv_path = os.path.join(DISCREPANCY_DIR, "discrepancies.csv")
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("surah,ayah\n")
            for d in stats["discrepancies"]:
                s, a = d.split("-")
                f.write(f"{int(s)},{int(a)}\n")
        print(f"  Discrepancy CSV:    {csv_path}")

    return stats


if __name__ == "__main__":
    result = asyncio.run(main())
    print("\nAll done.")
