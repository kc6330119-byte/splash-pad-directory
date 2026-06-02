#!/usr/bin/env python3
"""
scan_false_positive_pads.py

Local review-surface scan for Splash Pad Locator false positives.

This does not write to Airtable and does not change the generated site. It scans
the latest available Airtable-style CSV plus the generated dist/ review surface
and flags listings that look weak or off-topic for a splash pad / spray pad
directory.

Outputs:
  data/false_positive_scan_YYYYMMDD_HHMMSS.csv
  data/false_positive_scan_YYYYMMDD_HHMMSS.md

Usage:
  python3 scan_false_positive_pads.py
  python3 scan_false_positive_pads.py --csv "DGL Files/SplashPads-Grid view-20260529.csv"
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DIST_DIR = BASE_DIR / "dist"
SITE_URL = "https://splashpadlocator.com"

DEFAULT_CSV_CANDIDATES = [
    BASE_DIR / "DGL Files" / "SplashPads-Grid view-20260529.csv",
    DATA_DIR / "SplashPads-Grid view-20260529.csv",
    DATA_DIR / "SplashPads-Grid 2026-03-17.csv",
]


DIRECT_WATER_PATTERNS = [
    (r"\bsplash\s*pad\b", "splash pad"),
    (r"\bsplashpad\b", "splashpad"),
    (r"\bsplash\s*(park|zone|house)\b", "splash park/zone"),
    (r"\bspray\s*(pad|park|ground|deck|zone)\b", "spray pad/park"),
    (r"\bsprayground\b", "sprayground"),
    (r"\bwater\s*park\b", "water park"),
    (r"\bwaterpark\b", "waterpark"),
    (r"\baquatic\s*(center|centre|complex|facility|park)\b", "aquatic facility"),
    (r"\baquatics\s*(center|centre|complex)\b", "aquatics facility"),
    (r"\bwater\s*play(ground| area| feature| zone)?\b", "water play"),
    (r"\bwater\s*playground\b", "water playground"),
    (r"\bwave\s*pool\b", "wave pool"),
    (r"\blazy\s*river\b", "lazy river"),
    (r"\bwater\s*slide\b", "water slide"),
    (r"\bwaterslide\b", "waterslide"),
    (r"\bswim(ming)?\s*(pool|center|centre|complex|school)?\b", "swim/pool"),
    (r"\bpool\b", "pool"),
    (r"\bnatatorium\b", "natatorium"),
]

BROAD_WATER_PATTERNS = [
    (r"\blake\b", "lake"),
    (r"\briver\b", "river"),
    (r"\bcreek\b", "creek"),
    (r"\bbeach\b", "beach"),
    (r"\bbay\b", "bay"),
    (r"\bcove\b", "cove"),
    (r"\bisland\b", "island"),
    (r"\bshore\b", "shore"),
    (r"\bwaterfront\b", "waterfront"),
    (r"\bwhitewater\b", "whitewater"),
]

NEGATIVE_PATTERNS = [
    (r"\b(pizza|cafe|deli|restaurant|bar\s*(?:&|and)?\s*grill|saloon|pub)\b", 8, "restaurant/food business"),
    (r"\b(whitewater\s*rafting|rafting|zip\s*line|zipline|mountain\s*coaster|aerial|ropes\s*course)\b", 8, "adventure/rafting/coaster"),
    (r"\b(trampoline|bounce|inflatable|ninja|action\s*park|indoor\s*play|play\s*place)\b", 7, "indoor action/play venue"),
    (r"\b(arcade|bowling|laser\s*tag|escape\s*room|mini[\s-]*golf|go[\s-]*kart|bumper\s*car)\b", 7, "dry entertainment venue"),
    (r"\b(hotel|inn|lodge|casino|resort|rv\s*park|campground|camping|koa)\b", 5, "lodging/campground/pool-only risk"),
    (r"\b(boat|boathouse|ferry|cruise|jet\s*ski|kayak|canoe|marina|paddleboard|wake\s*park)\b", 6, "boating/water-sports not splash"),
    (r"\b(zoo|aquarium|museum|lighthouse|cavern|cave|theater|cinema|mall|store|grocery|hardware)\b", 8, "off-topic attraction/business"),
    (r"\b(water\s*supplier|water\s*soften|water\s*treatment|pool\s*contractor|pool\s*service)\b", 9, "water business, not public venue"),
    (r"\b(gym|fitness|physical\s*therapy|spa|sauna|bathhouse|massage)\b", 7, "fitness/spa/therapy venue"),
    (r"\b(church|funeral|cemetery|public\s*works|association|subdivision|apartment)\b", 8, "non-recreation organization"),
    (r"\b(playground|play\s*ground)\b", 1, "playground without proven spray feature"),
]

AI_GENERIC_PATTERNS = [
    (r"\bfamilies in [^.,]{0,80} looking for water fun\b", "generic water-fun template"),
    (r"\bprovides water play activities\b", "generic water-play claim"),
    (r"\bwater play areas cater to\b", "generic water-play audience claim"),
    (r"\bsummer staple for outdoor water play\b", "generic summer-staple claim"),
    (r"\blocal splash facilities offer cooling relief\b", "state-template filler"),
    (r"\bpack sunscreen, water shoes, and a towel\b", "template packing advice"),
    (r"\bworth adding to your summer lineup\b", "template recommendation"),
    (r"\bgentler water features\b", "generic gentle-water claim"),
    (r"\bthe water features are designed\b", "generic water-feature claim"),
]

WATER_TYPES = {
    "Splash Pad",
    "Water Park",
    "Aquatic Center",
    "Campground Water Park",
    "Resort Water Park",
    "Indoor Water Play",
    "Indoor Splash Pad",
    "Spray Park",
    "Amusement Park",
}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-{2,}", "-", value)


def first_existing_csv(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit)
        if not path.exists():
            raise SystemExit(f"CSV not found: {path}")
        return path
    for path in DEFAULT_CSV_CANDIDATES:
        if path.exists():
            return path
    raise SystemExit("No CSV found. Pass --csv /path/to/export.csv")


def load_sitemap_urls() -> set[str]:
    path = DIST_DIR / "sitemap.xml"
    if not path.exists():
        return set()
    text = path.read_text(errors="ignore")
    return set(re.findall(r"<loc>(.*?)</loc>", text))


def load_search_index() -> dict[tuple[str, str, str], str]:
    path = DIST_DIR / "search-index.json"
    if not path.exists():
        return {}
    rows = json.loads(path.read_text())
    index = {}
    for row in rows:
        key = (
            str(row.get("name", "")).casefold(),
            str(row.get("city", "")).casefold(),
            str(row.get("state", "")).casefold(),
        )
        index[key] = row.get("slug", "")
    return index


def html_index_state(slug: str) -> str:
    path = DIST_DIR / "pad" / f"{slug}.html"
    if not path.exists():
        return "not_generated"
    text = path.read_text(errors="ignore").lower()
    if re.search(r"<meta[^>]+name=[\"']robots[\"'][^>]+noindex", text):
        return "noindex"
    return "indexable"


def hits(patterns: list[tuple[str, str]], text: str) -> list[str]:
    found = []
    for pattern, label in patterns:
        if re.search(pattern, text, re.I):
            found.append(label)
    return found


def negative_hits(text: str) -> list[tuple[str, int]]:
    found = []
    for pattern, score, label in NEGATIVE_PATTERNS:
        if re.search(pattern, text, re.I):
            found.append((label, score))
    return found


def classify(score: int) -> str:
    if score >= 14:
        return "HIGH"
    if score >= 8:
        return "MEDIUM"
    if score >= 5:
        return "LOW"
    return "WATCH"


def reason_text(parts: list[str]) -> str:
    return "; ".join(dict.fromkeys(p for p in parts if p))


def public_exposure(page_state: str, in_sitemap: bool) -> str:
    if page_state == "indexable" and in_sitemap:
        return "indexable + in sitemap"
    if page_state == "indexable":
        return "indexable, not in sitemap"
    if page_state == "noindex":
        return "noindex"
    return "not generated"


def suggested_action(priority: str, exposure: str) -> str:
    if priority == "HIGH" and exposure == "indexable + in sitemap":
        return "Review now: exclude/noindex unless source proof confirms this is a splash/spray/water-play venue"
    if priority == "HIGH":
        return "Review before publishing: likely false positive or over-classified record"
    if priority == "MEDIUM" and exposure == "indexable + in sitemap":
        return "Verify before keeping indexable: require source proof and useful operating metadata"
    if priority == "MEDIUM":
        return "Backlog review: keep out of public review surface until verified"
    return "Watchlist: spot-check if it appears in sitemap or search index"


def scan_row(row: dict, search_index: dict, sitemap_urls: set[str]) -> dict | None:
    name = row.get("Name", "").strip()
    city = row.get("City", "").strip()
    state = row.get("State", "").strip()
    if not name:
        return None

    type_value = row.get("Type", "").strip()
    desc = row.get("Description", "").strip()
    website = row.get("Website URL", "").strip()
    features = row.get("Features", "").strip()
    admission = row.get("Admission", "").strip()
    hours = row.get("Hours", "").strip()
    maps_url = row.get("Google Maps URL", "").strip()

    key = (name.casefold(), city.casefold(), state.casefold())
    slug = search_index.get(key) or slugify(f"{name}-{city}")
    public_url = f"{SITE_URL}/pad/{slug}"
    in_sitemap = public_url in sitemap_urls
    page_state = html_index_state(slug)

    combined = " ".join([name, type_value, desc, website, maps_url]).lower()
    # Do not include transformed Type or generated description here. This scan is
    # looking for source evidence, not whether the pipeline already labeled it.
    sourceish = " ".join([name, website, maps_url]).lower()

    direct_water = hits(DIRECT_WATER_PATTERNS, sourceish)
    broad_water = hits(BROAD_WATER_PATTERNS, sourceish)
    neg = negative_hits(combined)
    generic = hits(AI_GENERIC_PATTERNS, desc.lower())

    score = 0
    reasons = []

    if neg:
        neg_score = sum(s for _, s in neg)
        score += min(neg_score, 18)
        reasons.append("negative venue signal: " + ", ".join(label for label, _ in neg[:4]))

    if not direct_water:
        score += 2
        reasons.append("no direct splash/spray/aquatic/pool signal in source fields")
        if broad_water:
            score += 1
            reasons.append("only broad water/location terms: " + ", ".join(broad_water[:4]))
    elif any(label for label, _ in neg):
        score += 2
        reasons.append("water signal exists but conflicts with off-topic signal")

    if generic and not direct_water:
        score += 6
        reasons.append("generic AI water-play description: " + ", ".join(generic[:3]))
    elif generic:
        score += 2
        reasons.append("generic AI water-play description")

    if type_value in WATER_TYPES and not direct_water and neg:
        score += 3
        reasons.append(f"current Type '{type_value}' may be over-trusting generated classification")

    missing = []
    for label, value in (("Type", type_value), ("Admission", admission), ("Features", features), ("Hours", hours)):
        if not value:
            missing.append(label)
    if len(missing) >= 2 and not direct_water:
        score += min(len(missing), 3)
        reasons.append("missing/blank operating fields: " + ", ".join(missing))

    if page_state == "indexable" and in_sitemap and score >= 5:
        score += 1
        reasons.append("currently indexable and emitted in sitemap")

    has_strong_negative = any(s >= 5 for _, s in neg)
    has_unsupported_ai_water = bool(generic and not direct_water)
    has_blank_profile = len(missing) >= 3 and not direct_water
    if score < 7 or not (has_strong_negative or has_unsupported_ai_water or has_blank_profile):
        return None

    priority = classify(score)
    exposure = public_exposure(page_state, in_sitemap)
    parsed = urlparse(website if website.startswith(("http://", "https://")) else f"https://{website}") if website else None
    domain = parsed.netloc.replace("www.", "") if parsed else ""

    return {
        "Priority": priority,
        "Score": score,
        "Public Exposure": exposure,
        "Suggested Action": suggested_action(priority, exposure),
        "Name": name,
        "City": city,
        "State": state,
        "Type": type_value,
        "Slug": slug,
        "Public URL": public_url,
        "In Sitemap": "yes" if in_sitemap else "no",
        "Page State": page_state,
        "Website Domain": domain,
        "Reasons": reason_text(reasons),
        "Source Water Signals": ", ".join(direct_water) or "(none)",
        "Broad Water Signals": ", ".join(broad_water) or "(none)",
        "Negative Signals": ", ".join(label for label, _ in neg) or "(none)",
        "Description Snippet": desc[:220].replace("\n", " "),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = [
        "Priority",
        "Score",
        "Public Exposure",
        "Suggested Action",
        "Name",
        "City",
        "State",
        "Type",
        "Slug",
        "Public URL",
        "In Sitemap",
        "Page State",
        "Website Domain",
        "Reasons",
        "Source Water Signals",
        "Broad Water Signals",
        "Negative Signals",
        "Description Snippet",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict], source_csv: Path) -> None:
    counts = Counter(r["Priority"] for r in rows)
    page_counts = Counter(r["Page State"] for r in rows)
    sitemap_count = sum(1 for r in rows if r["In Sitemap"] == "yes")
    public_surface_count = sum(1 for r in rows if r["Public Exposure"] == "indexable + in sitemap")
    high_public_count = sum(1 for r in rows if r["Priority"] == "HIGH" and r["Public Exposure"] == "indexable + in sitemap")
    medium_public_count = sum(1 for r in rows if r["Priority"] == "MEDIUM" and r["Public Exposure"] == "indexable + in sitemap")
    lines = [
        "# False Positive Pad Scan",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Source CSV: `{source_csv}`",
        "",
        "This is a non-destructive review queue. It flags pages that may be off-topic, "
        "over-classified, or relying on generated water-play copy without strong source evidence.",
        "",
        "## Summary",
        "",
        f"- Total flagged: {len(rows)}",
        f"- HIGH: {counts.get('HIGH', 0)}",
        f"- MEDIUM: {counts.get('MEDIUM', 0)}",
        f"- LOW: {counts.get('LOW', 0)}",
        f"- Indexable flagged pages: {page_counts.get('indexable', 0)}",
        f"- Flagged pages in sitemap: {sitemap_count}",
        f"- Public review-surface flags: {public_surface_count}",
        f"- HIGH public review-surface flags: {high_public_count}",
        f"- MEDIUM public review-surface flags: {medium_public_count}",
        "",
        "## Highest Priority",
        "",
    ]
    for row in rows[:75]:
        lines.extend([
            f"### {row['Priority']} · score {row['Score']} · {row['Name']} ({row['City']}, {row['State']})",
            "",
            f"- URL: {row['Public URL']}",
            f"- Type: {row['Type'] or '(blank)'}",
            f"- Page state: {row['Page State']} | In sitemap: {row['In Sitemap']}",
            f"- Suggested action: {row['Suggested Action']}",
            f"- Reasons: {row['Reasons']}",
            f"- Source water signals: {row['Source Water Signals']}",
            f"- Negative signals: {row['Negative Signals']}",
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan SPL pad pages for likely non-splash-pad false positives.")
    parser.add_argument("--csv", help="Airtable-style CSV export to scan")
    args = parser.parse_args()

    source_csv = first_existing_csv(args.csv)
    DATA_DIR.mkdir(exist_ok=True)

    search_index = load_search_index()
    sitemap_urls = load_sitemap_urls()

    with source_csv.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    flagged = []
    for row in rows:
        result = scan_row(row, search_index, sitemap_urls)
        if result:
            flagged.append(result)

    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "WATCH": 3}
    flagged.sort(key=lambda r: (priority_order.get(r["Priority"], 9), -int(r["Score"]), r["State"], r["Name"]))

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = DATA_DIR / f"false_positive_scan_{stamp}.csv"
    md_path = DATA_DIR / f"false_positive_scan_{stamp}.md"
    write_csv(csv_path, flagged)
    write_markdown(md_path, flagged, source_csv)

    counts = Counter(r["Priority"] for r in flagged)
    print(f"Scanned {len(rows)} rows from {source_csv}")
    print(f"Flagged {len(flagged)} possible false positives")
    for label in ("HIGH", "MEDIUM", "LOW", "WATCH"):
        if counts.get(label):
            print(f"  {label}: {counts[label]}")
    print(f"CSV: {csv_path}")
    print(f"MD:  {md_path}")


if __name__ == "__main__":
    main()
