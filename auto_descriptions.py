#!/usr/bin/env python3
"""
auto_descriptions.py — Two-pass description cleanup for Airtable SplashPads.

Pass 1 (all records):
  Strips embedded 'nan' values and normalizes whitespace. Safe and free.

Pass 2 (records still lacking a useful description after Pass 1):
  1. Matches against Outscraper-Clean-Descriptions.xlsx by website URL
  2. Falls back to Claude AI (Haiku) for any remaining records

Usage:
    python3 auto_descriptions.py                 # Dry run — shows what would change
    python3 auto_descriptions.py --apply         # Apply Pass 1 cleanup only (free)
    python3 auto_descriptions.py --apply --ai    # Apply Pass 1 + Excel + AI generation

Requirements:
    - Outscraper-Clean-Descriptions.xlsx must be in the project root
    - For --ai: add ANTHROPIC_API_KEY to your .env file
"""

import sys
import os
import re
import time
from pathlib import Path
from dotenv import load_dotenv
from pyairtable import Api

load_dotenv()

DRY_RUN = "--apply" not in sys.argv
USE_AI  = "--ai" in sys.argv

EXCEL_PATH      = Path("Outscraper-Clean-Descriptions.xlsx")
MIN_DESC_LENGTH = 60   # Descriptions shorter than this (after cleaning) need replacement
CHUNK_SIZE      = 10   # Airtable batch size

WATER_KEYWORDS = [
    "water", "splash", "aquatic", "pool", "spray", "swim", "wave",
    "slide", "lazy river", "waterpark", "water park", "sprayground",
    "recreation", "family fun", "fountain", "spray pad", "waterslide",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def clean_description(raw):
    """Remove 'nan' lines and normalize whitespace. Returns cleaned string."""
    if not raw:
        return ""
    lines = str(raw).splitlines()
    kept = [ln.strip() for ln in lines if ln.strip().lower() != "nan" and ln.strip()]
    return " ".join(kept).strip()


def is_useful(desc):
    """True if description is long enough to display on the site."""
    return len(clean_description(desc)) >= MIN_DESC_LENGTH


def norm_url(url):
    """Normalize a URL to a bare domain+path key for matching."""
    if not url or str(url).strip() in ("", "nan"):
        return ""
    u = str(url).lower().strip().rstrip("/")
    return re.sub(r"^https?://(www\.)?", "", u)


def excel_desc_quality(desc):
    """Return True if an Excel description is worth using."""
    if not desc or "nan" in str(desc).lower():
        return False
    d = str(desc).strip()
    if len(d) < 80:
        return False
    return any(kw in d.lower() for kw in WATER_KEYWORDS)


# ── Excel lookup ──────────────────────────────────────────────────────────────

def load_excel_lookup():
    """Build {normalized_url: description} from the Excel file."""
    if not EXCEL_PATH.exists():
        print(f"  Warning: {EXCEL_PATH} not found — skipping Excel matching.")
        return {}

    import pandas as pd
    df = pd.read_excel(EXCEL_PATH)
    has_desc = (
        df["company_insights.description"].notna()
        & (df["company_insights.description"].str.strip() != "")
    )
    df_clean = df[has_desc].copy()
    df_clean["url_key"] = df_clean["website"].apply(norm_url)

    lookup = {}
    for _, row in df_clean.iterrows():
        key  = row["url_key"]
        desc = str(row["company_insights.description"])
        if key and key not in lookup and excel_desc_quality(desc):
            lookup[key] = desc

    print(f"  Loaded {len(lookup)} quality descriptions from Excel.")
    return lookup


# ── AI generation ─────────────────────────────────────────────────────────────

def generate_ai_description(pad):
    """Call Claude Haiku to write a 2-3 sentence description for a pad."""
    import anthropic

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    features  = ", ".join(pad.get("features",  [])) or "not specified"
    age_range = ", ".join(pad.get("age_range", [])) or "not specified"
    admission = pad.get("admission", "") or "unknown"

    prompt = (
        f"Write a 2-3 sentence description for a water attraction listing. "
        f"Be factual and specific. Do not invent details not provided. "
        f"Do not use filler phrases like 'nestled' or 'boasting'.\n\n"
        f"Name: {pad['name']}\n"
        f"Location: {pad['city']}, {pad['state']}\n"
        f"Type: {pad['type']}\n"
        f"Admission: {admission}\n"
        f"Features: {features}\n"
        f"Age Range: {age_range}\n\n"
        f"Write only the description text."
    )

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=160,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    api   = Api(os.getenv("AIRTABLE_API_KEY"))
    table = api.table(
        os.getenv("AIRTABLE_BASE_ID"),
        os.getenv("AIRTABLE_TABLE_NAME", "SplashPads"),
    )

    mode_label = "DRY RUN" if DRY_RUN else ("APPLY + AI" if USE_AI else "APPLY — Pass 1 only")
    print(f"\n{'='*62}")
    print(f"  Auto-Descriptions  [{mode_label}]")
    print(f"{'='*62}\n")

    print("Fetching records from Airtable...")
    records = table.all()
    print(f"Fetched {len(records)} records.\n")

    # ── Categorise every record ───────────────────────────────────────────────
    pass1_changes  = []   # cleaning changes the value (nan stripped / whitespace)
    still_needs    = []   # even after cleaning, description is too short

    for rec in records:
        fields  = rec["fields"]
        name    = fields.get("Name", "").strip()
        if not name:
            continue

        original = fields.get("Description", "")
        cleaned  = clean_description(original)

        if cleaned != original.strip():
            pass1_changes.append({
                "id":       rec["id"],
                "name":     name,
                "original": original,
                "cleaned":  cleaned,
            })

        if not is_useful(cleaned):
            still_needs.append({
                "id":     rec["id"],
                "name":   name,
                "fields": fields,
                "cleaned": cleaned,
            })

    print(f"── Pass 1: nan/whitespace cleanup ──────────────────────────")
    print(f"  Records to clean:                    {len(pass1_changes)}")
    print(f"  Still need a description after clean: {len(still_needs)}\n")

    # ── Pass 2: Excel match + AI ──────────────────────────────────────────────
    print("── Pass 2: Fill missing descriptions ──────────────────────")
    excel_lookup = load_excel_lookup() if still_needs else {}

    pass2_excel = []
    pass2_ai    = []

    for rec in still_needs:
        url_key = norm_url(rec["fields"].get("Website URL", ""))
        if url_key and url_key in excel_lookup:
            pass2_excel.append({
                "id":       rec["id"],
                "name":     rec["name"],
                "new_desc": excel_lookup[url_key],
            })
        else:
            pass2_ai.append(rec)

    est_cost = len(pass2_ai) * 0.004
    print(f"  Matched from Excel (good quality):   {len(pass2_excel)}")
    print(f"  Require AI generation:               {len(pass2_ai)}")
    print(f"  Estimated AI cost:                   ~${est_cost:.2f}\n")

    # ── Dry run output ────────────────────────────────────────────────────────
    if DRY_RUN:
        print("─" * 62)
        print("PASS 1 SAMPLES (before → after):\n")
        for c in pass1_changes[:5]:
            print(f"  {c['name']}")
            print(f"    Before: {repr(c['original'].strip()[:90])}")
            print(f"    After:  {repr(c['cleaned'][:90])}")
            print()

        if pass2_excel:
            print("─" * 62)
            print("PASS 2 EXCEL SAMPLES:\n")
            for c in pass2_excel[:3]:
                print(f"  {c['name']}")
                print(f"    {c['new_desc'][:130]}")
                print()

        if pass2_ai:
            print("─" * 62)
            print(f"PASS 2 AI: {len(pass2_ai)} records would be sent to Claude Haiku\n")
            print("  Sample records:")
            for r in pass2_ai[:8]:
                city  = r["fields"].get("City", "")
                state = r["fields"].get("State", "")
                print(f"    - {r['name']} ({city}, {state})")

        print("\n" + "─" * 62)
        print("DRY RUN complete — nothing written to Airtable.")
        print("  --apply         Apply Pass 1 cleanup (free, safe)")
        print("  --apply --ai    Apply Pass 1 + Excel + AI generation")
        print("─" * 62)
        return

    # ── Build update map (Pass 1 + Excel) ────────────────────────────────────
    # IDs that will get AI descriptions — don't pre-write a short cleaned value
    ai_ids = {r["id"] for r in pass2_ai}

    updates = {}
    for c in pass1_changes:
        if c["id"] not in ai_ids:
            updates[c["id"]] = c["cleaned"]
    for c in pass2_excel:
        updates[c["id"]] = c["new_desc"]   # Excel wins over cleaned

    print(f"Applying {len(updates)} Pass 1 + Excel updates...")
    batch = [{"id": rid, "fields": {"Description": desc}} for rid, desc in updates.items()]
    for i in range(0, len(batch), CHUNK_SIZE):
        table.batch_update(batch[i:i + CHUNK_SIZE])
        print(f"  Updated {min(i + CHUNK_SIZE, len(batch))}/{len(batch)}...")

    # ── AI generation ─────────────────────────────────────────────────────────
    if not USE_AI:
        if pass2_ai:
            print(f"\nSkipped AI generation for {len(pass2_ai)} records.")
            print("Re-run with --apply --ai to generate those descriptions.")
        total = len(updates)
        print(f"\nDone! Updated {total} records.")
        return

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\nError: ANTHROPIC_API_KEY not found in .env — skipping AI generation.")
        print("Add it and re-run with --apply --ai.")
        return

    try:
        import anthropic  # noqa: F401
    except ImportError:
        print("\nError: anthropic package not installed.")
        print("Run: pip install anthropic")
        return

    print(f"\nGenerating AI descriptions for {len(pass2_ai)} records...")
    ai_batch = []
    errors   = 0

    for i, rec in enumerate(pass2_ai):
        try:
            pad_data = {
                "name":      rec["name"],
                "city":      rec["fields"].get("City", ""),
                "state":     rec["fields"].get("State", ""),
                "type":      rec["fields"].get("Type", "Splash Pad"),
                "admission": rec["fields"].get("Admission", ""),
                "features":  rec["fields"].get("Features", []),
                "age_range": rec["fields"].get("Age Range", []),
            }
            new_desc = generate_ai_description(pad_data)
            ai_batch.append({"id": rec["id"], "fields": {"Description": new_desc}})
            print(f"  [{i+1}/{len(pass2_ai)}] {rec['name'][:50]}: {new_desc[:70]}...")
            time.sleep(0.25)   # gentle rate limiting
        except Exception as e:
            print(f"  [{i+1}/{len(pass2_ai)}] Error — {rec['name']}: {e}")
            errors += 1

    print(f"\nWriting {len(ai_batch)} AI descriptions to Airtable...")
    for i in range(0, len(ai_batch), CHUNK_SIZE):
        table.batch_update(ai_batch[i:i + CHUNK_SIZE])
        print(f"  Updated {min(i + CHUNK_SIZE, len(ai_batch))}/{len(ai_batch)}...")

    total = len(updates) + len(ai_batch)
    print(f"\nDone! Total records updated: {total}")
    if errors:
        print(f"  ({errors} records skipped due to errors — re-run to retry)")
    print("Run python3 build.py to rebuild the site with updated descriptions.")


if __name__ == "__main__":
    main()
