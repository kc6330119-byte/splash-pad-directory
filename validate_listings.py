#!/usr/bin/env python3
"""
validate_listings.py

Reads the Airtable splash pads CSV export and validates whether each listing
is genuinely a water play facility (splash pad, water park, aquatic center, etc.)
by analyzing CSV fields and website content.

Adapted from holisticvetdirectory validate_animal_practices.py.

Logic:
  1. Pre-score each record from CSV data (name, type, features, description).
  2. High-confidence water facilities (pre-score >= 20) are marked LIKELY WATER
     without hitting their website — skips the majority of records.
  3. Remaining records have their website fetched and scored against
     water vs. non-water keyword lists.
  4. Progress is saved after every web fetch so the script can be safely
     interrupted and resumed.

Outputs:
  data/validation_results.csv   — every record with scores and classification
  data/validation_flagged.csv   — only REVIEW NEEDED and LIKELY NOT WATER records
  data/validation_progress.json — resume checkpoint (delete to start fresh)

Usage:
  python validate_listings.py                # full run (resumable)
  python validate_listings.py --dry-run      # first 20 records only
  python validate_listings.py --reset        # clear progress and restart
"""

import argparse
import csv
import json
import logging
import random
import re
import sys
import time
from pathlib import Path
from typing import Optional, Tuple

import requests
from bs4 import BeautifulSoup

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA_DIR = Path("data")
INPUT_CSV = DATA_DIR / "SplashPads-Grid 2026-03-17.csv"
RESULTS_CSV = DATA_DIR / "validation_results.csv"
FLAGGED_CSV = DATA_DIR / "validation_flagged.csv"
PROGRESS_FILE = DATA_DIR / "validation_progress.json"

# ── Request settings ───────────────────────────────────────────────────────────
REQUEST_TIMEOUT = 10
DELAY_MIN = 1.0
DELAY_MAX = 2.0
MAX_CONTENT_BYTES = 400_000

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

# ── Keyword scoring tables ─────────────────────────────────────────────────────
# (regex_pattern, score_per_match, display_label)
# Score capped at 3x per keyword type to avoid single-word domination.

WATER_KEYWORDS = [
    # Definitive water facility terms
    (r"\bsplash\s*pad\b",                 10, "splash pad"),
    (r"\bspray\s*(park|pad|ground)\b",    10, "spray park/pad"),
    (r"\bsplash\s*park\b",               10, "splash park"),
    (r"\bwater\s*park\b",                10, "water park"),
    (r"\baquatic\s*center\b",            10, "aquatic center"),
    (r"\bwave\s*pool\b",                  8, "wave pool"),
    (r"\blazy\s*river\b",                 8, "lazy river"),
    (r"\bwater\s*slide\b",                8, "water slide"),
    (r"\bwaterslide\b",                   8, "waterslide"),
    # Strong water feature terms
    (r"\bsplash\s*zone\b",                8, "splash zone"),
    (r"\bspray\s*(feature|nozzle|jet)\b", 6, "spray features"),
    (r"\bwading\s*pool\b",                6, "wading pool"),
    (r"\bkiddie\s*pool\b",                6, "kiddie pool"),
    (r"\bdump(ing)?\s*bucket\b",           6, "dumping bucket"),
    (r"\bzero[\s-]*depth\b",              6, "zero-depth"),
    (r"\bswim(ming)?\s*pool\b",           4, "swimming pool"),
    # General water words
    (r"\bsplash\b",                        4, "splash"),
    (r"\bsprinkler\b",                     4, "sprinkler"),
    (r"\baquatic\b",                       4, "aquatic"),
    (r"\bpool\b",                          2, "pool"),
    (r"\bwater\s*play\b",                 6, "water play"),
    (r"\bwater\s*feature\b",              4, "water feature"),
    (r"\bwater\s*fun\b",                  4, "water fun"),
    (r"\bswim\b",                          2, "swim"),
    (r"\bslide\b",                         2, "slide"),
    # Facility types
    (r"\brecreation\s*center\b",          2, "recreation center"),
    (r"\bcommunity\s*pool\b",             4, "community pool"),
    (r"\bpublic\s*pool\b",                4, "public pool"),
    (r"\boutdoor\s*pool\b",               4, "outdoor pool"),
]

NOT_WATER_KEYWORDS = [
    # Definitive non-water terms
    (r"\btrampoline\s*(park)?\b",        -10, "trampoline"),
    (r"\bgo[\s-]*kart\b",               -10, "go-kart"),
    (r"\bbowling\b",                      -8, "bowling"),
    (r"\blaser\s*tag\b",                  -8, "laser tag"),
    (r"\bescape\s*room\b",               -8, "escape room"),
    (r"\baxe\s*throw\b",                  -8, "axe throwing"),
    (r"\bbatting\s*cage\b",               -8, "batting cage"),
    (r"\brock\s*climb\b",                 -6, "rock climbing"),
    (r"\bskate\s*park\b",                 -8, "skatepark"),
    (r"\bdog\s*park\b",                   -8, "dog park"),
    (r"\bdog\s*water\s*park\b",           -8, "dog water park"),
    # Non-water businesses
    (r"\bplumbing\b",                    -10, "plumbing"),
    (r"\bcinema\b",                      -10, "cinema"),
    (r"\bmovie\s*theater\b",             -10, "movie theater"),
    (r"\brestaurant\b",                   -6, "restaurant"),
    (r"\bbar\s*(&|and)\s*grill\b",        -6, "bar & grill"),
    (r"\bgrocery\b",                     -10, "grocery"),
    (r"\bhardware\s*store\b",            -10, "hardware store"),
    (r"\breal\s*estate\b",              -10, "real estate"),
    (r"\bdentist\b",                     -10, "dentist"),
    (r"\bchurch\b",                       -8, "church"),
    (r"\bfuneral\b",                     -10, "funeral"),
    (r"\bcemetery\b",                    -10, "cemetery"),
    # Rental/service companies (not facilities)
    (r"\brental\s*(company|service)\b",   -6, "rental company"),
    (r"\bbounce\s*house\s*rental\b",      -8, "bounce house rental"),
    (r"\bparty\s*rental\b",               -6, "party rental"),
    # Abandoned/closed
    (r"\babandoned\b",                    -8, "abandoned"),
    (r"\bpermanently\s*closed\b",        -10, "permanently closed"),
    # Pet-specific facilities (not for families)
    (r"\bpet\s*massage\b",               -8, "pet massage"),
    (r"\bdog\s*grooming\b",              -8, "dog grooming"),
    (r"\bkennel\b",                       -6, "kennel"),
    (r"\bveterinar\b",                    -6, "veterinary"),
    # RV/camping without water context
    (r"\brv\s*(park|resort)\b",           -3, "RV park"),
    (r"\bcampground\b",                   -3, "campground"),
]

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ── Progress helpers ───────────────────────────────────────────────────────────
def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"processed": {}}


def save_progress(progress: dict) -> None:
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


# ── Web fetching ───────────────────────────────────────────────────────────────
def fetch_text(url: str) -> Optional[str]:
    """Fetch a URL and return visible text, or None on failure."""
    try:
        resp = requests.get(
            url, headers=HEADERS, timeout=REQUEST_TIMEOUT,
            allow_redirects=True, stream=True
        )
        resp.raise_for_status()

        chunks = []
        total = 0
        for chunk in resp.iter_content(chunk_size=8192):
            chunks.append(chunk)
            total += len(chunk)
            if total >= MAX_CONTENT_BYTES:
                break

        soup = BeautifulSoup(b"".join(chunks), "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return re.sub(r"\s+", " ", text)
    except Exception:
        return None


def normalise_url(raw: str) -> str:
    raw = raw.strip().rstrip("/")
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    return raw


def fetch_site_text(website: str) -> Tuple[str, str]:
    """Fetch homepage. If water signals are weak, also try /about."""
    base = normalise_url(website)
    home = fetch_text(base) or ""
    pages = "homepage"

    strong_water = any(
        re.search(pat, home, re.IGNORECASE)
        for pat, score, _ in WATER_KEYWORDS
        if score >= 8
    )

    if not strong_water or len(home) < 300:
        for path in ("/about", "/about-us", "/attractions"):
            extra = fetch_text(base + path) or ""
            if extra:
                home = home + " " + extra
                pages += f" + {path}"
                break

    return home, pages


# ── Scoring ────────────────────────────────────────────────────────────────────
def score_text(text: str) -> Tuple[int, list, list]:
    """Score text for water vs. non-water signals."""
    water_hits = []
    not_water_hits = []
    score = 0

    for pattern, pts, label in WATER_KEYWORDS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            contribution = min(pts * len(matches), pts * 3)
            score += contribution
            water_hits.append(f"{label}({len(matches)})")

    for pattern, pts, label in NOT_WATER_KEYWORDS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            contribution = max(pts * len(matches), pts * 3)
            score += contribution
            not_water_hits.append(f"{label}({len(matches)})")

    return score, water_hits, not_water_hits


def pre_score_from_csv(row: dict) -> Tuple[int, list]:
    """Quick score from Airtable CSV fields only — no web request."""
    score = 0
    signals = []

    name = row.get("Name", "").lower()
    pad_type = row.get("Type", "").strip()
    features = row.get("Features", "")
    description = row.get("Description", "")
    admission = row.get("Admission", "")

    # Type field — strong signal
    WATER_TYPES = {
        "Splash Pad": 15, "Spray Park": 15, "Water Park": 12,
        "Aquatic Center": 12, "Indoor Splash Pad": 15,
        "Indoor Water Play": 12, "Resort Water Park": 10,
        "Campground Water Park": 8,
    }
    if pad_type in WATER_TYPES:
        score += WATER_TYPES[pad_type]
        signals.append(f"type: {pad_type}")

    # Name keywords
    water_name_words = [
        "splash", "spray", "aquatic", "water park", "waterpark",
        "pool", "swim", "wave", "slide", "lagoon",
    ]
    for w in water_name_words:
        if w in name:
            score += 8
            signals.append(f"name: '{w}'")
            break

    not_water_name_words = [
        "trampoline", "go-kart", "bowling", "laser tag", "cinema",
        "plumbing", "restaurant", "dog park", "skate park", "batting",
        "rental", "church", "funeral", "cemetery", "abandoned",
        "pet massage", "dog grooming", "kennel",
    ]
    for w in not_water_name_words:
        if w in name:
            score -= 15
            signals.append(f"name: '{w}' (negative)")
            break

    # Features — water-related features are a signal
    water_features = ["Water park", "Restrooms", "Picnic Area", "Shade", "Playground"]
    if features:
        feat_count = sum(1 for f in water_features if f in features)
        if feat_count >= 2:
            score += 5
            signals.append(f"features: {feat_count} water-related")

    # Description keywords
    if description and len(description) > 50:
        desc_score, water_hits, _ = score_text(description)
        score += desc_score // 2  # half-weight
        if water_hits:
            signals.append(f"desc: {','.join(water_hits[:3])}")

    # Admission set — suggests a real facility
    if admission in ("Free", "Paid"):
        score += 3
        signals.append(f"admission: {admission}")

    return score, signals


def classify(score: int) -> str:
    if score >= 8:
        return "LIKELY WATER"
    elif score >= 0:
        return "REVIEW NEEDED"
    else:
        return "LIKELY NOT WATER"


# ── CSV output ─────────────────────────────────────────────────────────────────
FIELDNAMES = [
    "Classification", "Name", "City", "State", "Type",
    "Website", "Pre-Score", "Web Score", "Total Score",
    "Water Signals", "Non-Water Signals", "Pages Checked",
]

CLASSIFICATION_ORDER = {
    "LIKELY NOT WATER": 0,
    "REVIEW NEEDED": 1,
    "NO WEBSITE": 2,
    "LIKELY WATER": 3,
}


def write_csv(path: Path, rows: list) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


# ── Main ───────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Validate splash pad listings")
    parser.add_argument("--dry-run", action="store_true",
                        help="Process only the first 20 records")
    parser.add_argument("--reset", action="store_true",
                        help="Delete progress file and start fresh")
    args = parser.parse_args()

    DATA_DIR.mkdir(exist_ok=True)

    if args.reset and PROGRESS_FILE.exists():
        PROGRESS_FILE.unlink()
        log.info("Progress file cleared — starting fresh.")

    if not INPUT_CSV.exists():
        log.error(f"CSV not found: {INPUT_CSV}")
        sys.exit(1)

    with open(INPUT_CSV, encoding="utf-8-sig") as f:
        all_rows = list(csv.DictReader(f))
    log.info(f"Loaded {len(all_rows)} records from CSV")

    if args.dry_run:
        all_rows = all_rows[:20]
        log.info("DRY RUN — processing first 20 records only")

    progress = load_progress()
    processed = progress.get("processed", {})

    results = []
    web_fetches = 0
    HIGH_CONFIDENCE_THRESHOLD = 20

    for i, row in enumerate(all_rows, 1):
        name = row.get("Name", "").strip()
        website = row.get("Website URL", "").strip()
        city = row.get("City", "")
        state = row.get("State", "")
        pad_type = row.get("Type", "")
        key = f"{name}|{city}|{state}"

        # ── No website ────────────────────────────────────────────────────
        if not website or website.lower() == "nan":
            # Still pre-score from CSV fields
            pre_score, pre_signals = pre_score_from_csv(row)
            classification = classify(pre_score) if pre_score != 0 else "NO WEBSITE"
            results.append({
                "Name": name, "City": city, "State": state, "Type": pad_type,
                "Website": "", "Pre-Score": pre_score, "Web Score": 0,
                "Total Score": pre_score,
                "Water Signals": ", ".join(pre_signals),
                "Non-Water Signals": "",
                "Pages Checked": "no website — CSV only",
                "Classification": classification,
            })
            continue

        # ── Already in progress cache ─────────────────────────────────────
        if key in processed and not args.dry_run:
            results.append(processed[key])
            continue

        # ── Pre-score from CSV fields ─────────────────────────────────────
        pre_score, pre_signals = pre_score_from_csv(row)

        # ── Skip web fetch for high-confidence water facilities ───────────
        if pre_score >= HIGH_CONFIDENCE_THRESHOLD:
            result = {
                "Name": name, "City": city, "State": state, "Type": pad_type,
                "Website": website, "Pre-Score": pre_score, "Web Score": 0,
                "Total Score": pre_score,
                "Water Signals": ", ".join(pre_signals),
                "Non-Water Signals": "",
                "Pages Checked": "skipped — high pre-score",
                "Classification": "LIKELY WATER",
            }
            results.append(result)
            if not args.dry_run:
                processed[key] = result
            if i % 500 == 0:
                log.info(f"  [{i}/{len(all_rows)}] high-confidence skip: {name}")
            continue

        # ── Fetch and analyse website ─────────────────────────────────────
        log.info(f"[{i}/{len(all_rows)}] Checking: {name} | {city}, {state} — {website[:60]}")
        site_text, pages_checked = fetch_site_text(website)
        web_fetches += 1

        if site_text:
            web_score, water_matches, not_water_matches = score_text(site_text)
        else:
            web_score, water_matches, not_water_matches = 0, [], []
            pages_checked = "unreachable"

        total_score = pre_score + web_score
        classification = classify(total_score)

        if classification != "LIKELY WATER":
            log.warning(
                f"  *** FLAGGED [{classification}] score={total_score}: "
                f"{name} | {city}, {state}"
            )

        result = {
            "Name": name, "City": city, "State": state, "Type": pad_type,
            "Website": website, "Pre-Score": pre_score, "Web Score": web_score,
            "Total Score": total_score,
            "Water Signals": ", ".join(pre_signals + water_matches),
            "Non-Water Signals": ", ".join(not_water_matches),
            "Pages Checked": pages_checked,
            "Classification": classification,
        }

        results.append(result)

        if not args.dry_run:
            processed[key] = result
            save_progress({"processed": processed})

        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

    # ── Sort and write output ─────────────────────────────────────────────
    results.sort(key=lambda r: (
        CLASSIFICATION_ORDER.get(r["Classification"], 4),
        r.get("Total Score", 0)
    ))

    if not args.dry_run:
        write_csv(RESULTS_CSV, results)
        flagged = [r for r in results
                   if r["Classification"] in ("LIKELY NOT WATER", "REVIEW NEEDED")]
        write_csv(FLAGGED_CSV, flagged)

    # ── Summary ───────────────────────────────────────────────────────────
    counts = {}
    for r in results:
        counts[r["Classification"]] = counts.get(r["Classification"], 0) + 1

    log.info("\n=== VALIDATION SUMMARY ===")
    for label in ["LIKELY NOT WATER", "REVIEW NEEDED", "NO WEBSITE", "LIKELY WATER"]:
        if label in counts:
            log.info(f"  {label}: {counts[label]}")
    log.info(f"  Web fetches performed: {web_fetches}")

    if not args.dry_run:
        flagged_count = counts.get("LIKELY NOT WATER", 0) + counts.get("REVIEW NEEDED", 0)
        log.info(f"\nAll results  → {RESULTS_CSV}")
        log.info(f"Flagged only → {FLAGGED_CSV}  ({flagged_count} records to review)")


if __name__ == "__main__":
    main()
