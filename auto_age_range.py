#!/usr/bin/env python3
"""
auto_age_range.py — Automatically set the Age Range field in Airtable
based on Type and name keywords.

Usage:
    python3 auto_age_range.py          # Dry run: shows what would change, writes nothing
    python3 auto_age_range.py --apply  # Applies changes to Airtable
"""

import sys
import os
from dotenv import load_dotenv
from pyairtable import Api

load_dotenv()

DRY_RUN = "--apply" not in sys.argv

# Age ranges assigned by Type
TYPE_AGE_RANGES = {
    "Splash Pad":              ["Families", "Kids", "Toddlers"],
    "Spray Park":              ["Families", "Kids", "Toddlers"],
    "Indoor Splash Pad":       ["Families", "Kids", "Toddlers"],
    "Indoor Water Play":       ["Families", "Kids", "Toddlers"],
    "Aquatic Center":          ["Families", "Kids", "All Ages"],
    "Water Park":              ["Families", "Kids", "All Ages"],
    "Resort Water Park":       ["Families", "Kids", "All Ages"],
    "Amusement Park":          ["Families", "Kids"],
    "Campground Water Park":   ["Families", "Kids"],
}

# If the name contains any of these keywords, always include Toddlers
TODDLER_KEYWORDS = [
    "toddler", "tot ", "tiny tot", "little ones", "baby pool",
    "wading pool", "wader", "zero depth", "zero-depth", "splash zone",
    "spray zone", "spray pad", "spray park", "splash pad"
]


def get_age_ranges(name, type_value):
    """Return appropriate age ranges based on type and name keywords."""
    # Start with type-based assignment, defaulting to Splash Pad ranges
    ranges = set(TYPE_AGE_RANGES.get(type_value, ["Families", "Kids", "Toddlers"]))

    # Add Toddlers if name contains relevant keywords
    name_lower = name.lower()
    if any(kw in name_lower for kw in TODDLER_KEYWORDS):
        ranges.add("Toddlers")

    return sorted(ranges)


def main():
    api = Api(os.getenv("AIRTABLE_API_KEY"))
    table = api.table(
        os.getenv("AIRTABLE_BASE_ID"),
        os.getenv("AIRTABLE_TABLE_NAME", "SplashPads")
    )

    print(f"\n{'='*55}")
    print(f"  Auto-Age-Range Script  {'(DRY RUN — no changes written)' if DRY_RUN else '*** APPLYING CHANGES ***'}")
    print(f"{'='*55}\n")

    print("Fetching records from Airtable...")
    records = table.all()
    print(f"Fetched {len(records)} records.\n")

    changes = []

    for record in records:
        fields = record["fields"]
        name = fields.get("Name", "").strip()
        current_age_range = fields.get("Age Range", [])
        type_value = fields.get("Type", "Splash Pad").strip()

        if not name:
            continue

        # Only update blank records — never overwrite existing age ranges
        if current_age_range:
            continue

        new_ranges = get_age_ranges(name, type_value)

        changes.append({
            "id": record["id"],
            "name": name,
            "type": type_value,
            "new_ranges": new_ranges,
        })

    if not changes:
        print("No changes to make — all records already have Age Range set.")
        return

    # Print summary grouped by assigned ranges
    by_ranges = {}
    for c in changes:
        key = ", ".join(c["new_ranges"])
        by_ranges.setdefault(key, []).append(c["name"])

    print(f"Found {len(changes)} records to update:\n")
    for ranges_label, names in sorted(by_ranges.items()):
        print(f"  [{ranges_label}] ({len(names)}):")
        for n in sorted(names)[:10]:
            print(f"    - {n}")
        if len(names) > 10:
            print(f"    ... and {len(names) - 10} more")
        print()

    if DRY_RUN:
        print("-" * 55)
        print("DRY RUN complete — nothing was written to Airtable.")
        print("Review the list above, then run with --apply to save changes.")
        print("-" * 55)
        return

    # Apply changes using batch update
    print(f"Applying {len(changes)} updates to Airtable...")
    batch = [{"id": c["id"], "fields": {"Age Range": c["new_ranges"]}} for c in changes]

    chunk_size = 10
    for i in range(0, len(batch), chunk_size):
        chunk = batch[i:i + chunk_size]
        table.batch_update(chunk, typecast=True)
        print(f"  Updated {min(i + chunk_size, len(changes))}/{len(changes)}...")

    print(f"\nDone! Updated {len(changes)} records in Airtable.")
    print("Run python3 build.py to rebuild the site with updated age ranges.")


if __name__ == "__main__":
    main()
