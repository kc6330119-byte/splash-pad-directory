#!/usr/bin/env python3
"""
auto_features.py — Conservatively assign Features field values in Airtable.

Adds Restrooms, Picnic Area, and/or Shade to records that don't already have them.
Never removes or overwrites existing features.

Rules (conservative):
  Restrooms  — added to: Water Park, Resort Water Park, Aquatic Center,
                          Amusement Park, Campground Water Park (by Type)
  Picnic Area — added when name contains park/recreation keywords,
                or Type is Water Park, Resort Water Park, Amusement Park,
                or Campground Water Park
  Shade       — added only when Type is Indoor Splash Pad / Indoor Water Play,
                or name contains "indoor", "pavilion", "covered", "shelter",
                "rec center", "recreation center", "community center"

Usage:
    python3 auto_features.py          # Dry run — shows what would change
    python3 auto_features.py --apply  # Applies changes to Airtable
"""

import sys
import os
from dotenv import load_dotenv
from pyairtable import Api

load_dotenv()

DRY_RUN = "--apply" not in sys.argv

# ── Restrooms ────────────────────────────────────────────────────────────────
# Types that reliably have restrooms on-site
RESTROOMS_TYPES = {
    "Water Park",
    "Resort Water Park",
    "Aquatic Center",
    "Amusement Park",
    "Campground Water Park",
}

# ── Picnic Area ───────────────────────────────────────────────────────────────
# Types that reliably have picnic areas
PICNIC_TYPES = {
    "Water Park",
    "Resort Water Park",
    "Amusement Park",
    "Campground Water Park",
}

# Name keywords that strongly suggest picnic infrastructure
PICNIC_KEYWORDS = [
    "county park",
    "city park",
    "regional park",
    "state park",
    "recreation area",
    "recreational area",
    "recreation park",
    "rec park",
    "campground",
    "camp resort",
    "picnic",
    "pavilion",
    "fairgrounds",
    "fairground",
]

# ── Shade ─────────────────────────────────────────────────────────────────────
# Types that are always indoor (shade = covered)
SHADE_TYPES = {
    "Indoor Splash Pad",
    "Indoor Water Play",
}

# Name keywords that strongly suggest covered/shaded areas
SHADE_KEYWORDS = [
    "indoor",
    "inside",
    "pavilion",
    "covered",
    "shelter",
    "rec center",
    "recreation center",
    "community center",
    "community rec",
    "ymca",
    "y.m.c.a",
    "natatorium",
]


def features_to_add(name: str, type_value: str, current_features: list) -> list:
    """Return a list of feature strings that should be added to this record."""
    name_lower = name.lower()
    current_set = set(current_features)
    to_add = []

    # Restrooms
    if "Restrooms" not in current_set:
        if type_value in RESTROOMS_TYPES:
            to_add.append("Restrooms")

    # Picnic Area
    if "Picnic Area" not in current_set:
        if type_value in PICNIC_TYPES or any(kw in name_lower for kw in PICNIC_KEYWORDS):
            to_add.append("Picnic Area")

    # Shade
    if "Shade" not in current_set:
        if type_value in SHADE_TYPES or any(kw in name_lower for kw in SHADE_KEYWORDS):
            to_add.append("Shade")

    return to_add


def main():
    api = Api(os.getenv("AIRTABLE_API_KEY"))
    table = api.table(
        os.getenv("AIRTABLE_BASE_ID"),
        os.getenv("AIRTABLE_TABLE_NAME", "SplashPads")
    )

    print(f"\n{'='*58}")
    print(f"  Auto-Features Script  {'(DRY RUN — no changes written)' if DRY_RUN else '*** APPLYING CHANGES ***'}")
    print(f"{'='*58}\n")

    print("Fetching records from Airtable...")
    records = table.all()
    print(f"Fetched {len(records)} records.\n")

    changes = []

    for record in records:
        fields = record["fields"]
        name = fields.get("Name", "").strip()
        if not name:
            continue

        type_value = fields.get("Type", "Splash Pad").strip()
        current_features = fields.get("Features", [])

        additions = features_to_add(name, type_value, current_features)
        if not additions:
            continue

        changes.append({
            "id": record["id"],
            "name": name,
            "type": type_value,
            "current_features": current_features,
            "additions": additions,
            "new_features": sorted(set(current_features) | set(additions)),
        })

    if not changes:
        print("No changes to make — all records already have the relevant features set.")
        return

    # Summary grouped by what's being added
    by_additions = {}
    for c in changes:
        key = " + ".join(sorted(c["additions"]))
        by_additions.setdefault(key, []).append(c["name"])

    print(f"Found {len(changes)} records to update:\n")
    for label, names in sorted(by_additions.items()):
        print(f"  Adding [{label}] to {len(names)} records:")
        for n in sorted(names)[:10]:
            print(f"    - {n}")
        if len(names) > 10:
            print(f"    ... and {len(names) - 10} more")
        print()

    if DRY_RUN:
        print("-" * 58)
        print("DRY RUN complete — nothing was written to Airtable.")
        print("Review the list above, then run with --apply to save changes.")
        print("-" * 58)
        return

    # Apply changes in batches of 10
    print(f"Applying {len(changes)} updates to Airtable...")
    batch = [{"id": c["id"], "fields": {"Features": c["new_features"]}} for c in changes]

    chunk_size = 10
    for i in range(0, len(batch), chunk_size):
        chunk = batch[i:i + chunk_size]
        table.batch_update(chunk, typecast=True)
        print(f"  Updated {min(i + chunk_size, len(changes))}/{len(changes)}...")

    print(f"\nDone! Updated {len(changes)} records in Airtable.")
    print("Run python3 build.py to rebuild the site with updated features.")


if __name__ == "__main__":
    main()
