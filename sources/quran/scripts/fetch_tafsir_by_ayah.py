#!/usr/bin/env python3
"""
Fetch missing tafsir entries for remaining ayahs.
Uses Quran.com API v4: /api/v4/tafsirs/{resource_id}/by_ayah/{surah}:{ayah}
"""
import os
import json
import ssl
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

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

TAFSIR_RESOURCES = [
    {"id": 169, "name": "Ibn Kathir (Abridged)", "author": "Hafiz Ibn Kathir"},
    {"id": 16, "name": "Tafsir Muyassar", "author": "المیسر"},
]

OUTPUT_DIR = "/root/tarbiyyah/quran-wiki/tafsir"
LOG_DIR = "/root/tarbiyyah/quran-wiki/logs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

REQUEST_DELAY = 0.3  # ~3 req/sec to be respectful

def qfetch(url, retries=3):
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": "Hermes-QuranWiki/1.0"})
            data = urlopen(req, context=SSL_CTX, timeout=30).read()
            time.sleep(REQUEST_DELAY)
            return json.loads(data)
        except HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return {"__error__": f"HTTP {e.code}: {e.reason}", "url": url}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return {"__error__": f"Exception: {str(e)}", "url": url}
    return {"__error__": "Max retries exceeded", "url": url}

def load_existing(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def save_jsonl(filepath, records):
    with open(filepath, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def get_missing_ranges():
    """Returns list of (surah, ayah) tuples that need fetching."""
    missing = []
    for surah in range(1, 115):
        fname = os.path.join(OUTPUT_DIR, f"{surah:03d}.jsonl")
        expected = SURAH_AYAH_COUNTS[surah - 1]
        if not os.path.exists(fname):
            for ayah in range(1, expected + 1):
                missing.append((surah, ayah))
        else:
            existing = load_existing(fname)
            existing_ids = {r.get("ayah") for r in existing}
            for ayah in range(1, expected + 1):
                if ayah not in existing_ids:
                    missing.append((surah, ayah))
    return missing

def main():
    missing = get_missing_ranges()
    total_missing = len(missing)
    print(f"Missing ayahs to fetch: {total_missing}")
    if not missing:
        print("Nothing to fetch — all 6236 ayahs already present.")
        return

    # Build lookup: (surah, ayah) -> existing record (when appending to partial file)
    file_cache = {}
    def get_records(surah):
        if surah not in file_cache:
            fname = os.path.join(OUTPUT_DIR, f"{surah:03d}.jsonl")
            file_cache[surah] = load_existing(fname)
        return file_cache[surah]

    errors = []
    unavailable = []
    completed = 0
    start = time.time()

    for surah, ayah in sorted(missing, key=lambda x: (x[0], x[1])):
        verse_key = f"{surah}:{ayah}"
        verse_id = sum(SURAH_AYAH_COUNTS[:surah - 1]) + ayah
        tafsirs = []

        for res in TAFSIR_RESOURCES:
            url = f"https://api.quran.com/api/v4/tafsirs/{res['id']}/by_ayah/{verse_key}"
            resp = qfetch(url)
            if "__error__" in resp:
                errors.append({"surah": surah, "ayah": ayah, "resource_id": res["id"], "error": resp["__error__"], "url": url})
                continue
            tafsir_block = resp.get("tafsir", {})
            text = tafsir_block.get("text", "").strip()
            if not text:
                unavailable.append({"surah": surah, "ayah": ayah, "resource_id": res["id"], "verse_key": verse_key})
                text = ""
            tafsirs.append({
                "name": res["name"],
                "author": res["author"] if text else (res["author"] + " — unavailable"),
                "text": text,
            })

        record = {
            "surah": surah,
            "ayah": ayah,
            "verse_id": verse_id,
            "tafsirs": tafsirs,
        }

        # Append or create
        records = get_records(surah)
        # Remove old record for this ayah if present
        records = [r for r in records if r.get("ayah") != ayah]
        records.append(record)
        file_cache[surah] = records

        # Write back to file periodically (every surah boundary or every 50 ayahs)
        # Just write immediately for simplicity (small files)
        fname = os.path.join(OUTPUT_DIR, f"{surah:03d}.jsonl")
        save_jsonl(fname, sorted(records, key=lambda x: x["ayah"]))

        completed += 1
        if completed % 10 == 0 or completed == total_missing:
            elapsed = time.time() - start
            rate = completed / elapsed if elapsed > 0 else 0
            eta = (total_missing - completed) / rate if rate > 0 else 0
            print(f"  [{completed}/{total_missing}] S{surah}:A{ayah} — rate {rate:.2f}/s — ETA {eta:.0f}s")

    # Final summary
    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.1f}s")
    print(f"Fetched: {completed}/{total_missing}")
    print(f"API errors: {len(errors)}")
    print(f"Unavailable entries: {len(unavailable)}")

    # Save log
    log = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "fetched": completed,
        "total_missing": total_missing,
        "errors": errors,
        "unavailable": unavailable,
    }
    log_path = os.path.join(LOG_DIR, f"tafsir_missing_{time.strftime('%Y%m%d_%H%M%S')}.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f"Log saved: {log_path}")

if __name__ == "__main__":
    main()
