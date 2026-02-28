#!/usr/bin/env python3
"""
auto_type.py — Automatically set the Type field in Airtable based on name keywords.

Usage:
    python3 auto_type.py          # Dry run: shows what would change, writes nothing
    python3 auto_type.py --apply  # Applies changes to Airtable
"""

import sys
import os
from dotenv import load_dotenv
from pyairtable import Api

load_dotenv()

DRY_RUN = "--apply" not in sys.argv

# Keyword rules — first match wins, checked against Name field (case-insensitive)
# Only updates records where Type is blank or "Splash Pad"
TYPE_RULES = [
    # Amusement Parks
    (["six flags", "kings island", "cedar point", "busch gardens", "seaworld",
      "sea world", "hersheypark", "hershey park", "dollywood", "knott's", "knotts",
      "carowinds", "great adventure", "magic mountain", "fiesta texas", "over georgia",
      "over texas", "great america", "worlds of fun", "valleyfair", "michigan's adventure",
      "elitch", "lagoon park", "silverwood", "holiday world", "fun spot", "idlewild",
      "kennywood", "nickelodeon universe", "american dream", "funplex", "enchanted island",
      "wonderland amusement", "amusement park", "fun city", "adventure park"],
     "Amusement Park"),

    # Resort Water Parks
    (["great wolf lodge", "kalahari", "camelback resort", "wilderness resort",
      "avalanche bay", "kartrite", "massanutten", "aquatopia", "soundwaves",
      "splash village", "zehnder", "grand bear", "palm island indoor",
      "split rock resort", "water park resort", "indoor waterpark resort",
      "coconut creek", "water park at wild island"],
     "Resort Water Park"),

    # Dedicated Water Parks
    (["water park", "waterpark", "schlitterbahn", "raging waves", "wet n wild",
      "wet 'n wild", "zoombezi", "water country", "wild waters", "cowabunga",
      "splashdown beach", "typhoon", "noah's ark", "soak city", "hurricane harbor",
      "adventure island", "raging rivers", "whitewater", "white water",
      "oceans of fun", "wild waves", "splash lagoon", "aquaport", "water zoo",
      "water world", "lost island", "volcano island", "dreamworks water",
      "somersplash", "water mine", "wave waterpark", "surf waterpark",
      "the cove waterpark", "splash country", "splashdown waterpark",
      "splash central", "ocean dunes", "splash valley", "open water park",
      "wake nation", "wake island", "margaritaville", "nashville shores",
      "raging waters", "cowabunga bay", "paradise water park", "wave waterpark",
      "mountain creek", "dorney park", "lake compounce", "quassy",
      "frontier town water", "fun city", "bayou splash"],
     "Water Park"),

    # Aquatic Centers
    (["aquatic center", "aquatic centre", "aquatics center", "aquatics complex",
      "swim center", "swimming center", "natatorium", "aquatic complex",
      "family aquatic", "community aquatic", "regional aquatic", "aqua center",
      "swim complex", "aquatic facility", "brooks street swim"],
     "Aquatic Center"),

    # Campground / RV Water Parks
    (["campground", "rv park", "glamping", "camp resort", "indian springs campground"],
     "Campground Water Park"),
]


def get_type_from_name(name):
    """Return the appropriate Type based on keywords in the name, or None if no match."""
    name_lower = name.lower()
    for keywords, type_value in TYPE_RULES:
        if any(kw in name_lower for kw in keywords):
            return type_value
    return None


def main():
    api = Api(os.getenv("AIRTABLE_API_KEY"))
    table = api.table(
        os.getenv("AIRTABLE_BASE_ID"),
        os.getenv("AIRTABLE_TABLE_NAME", "SplashPads")
    )

    print(f"\n{'='*55}")
    print(f"  Auto-Type Script  {'(DRY RUN — no changes written)' if DRY_RUN else '*** APPLYING CHANGES ***'}")
    print(f"{'='*55}\n")

    print("Fetching records from Airtable...")
    records = table.all()
    print(f"Fetched {len(records)} records.\n")

    changes = []

    for record in records:
        fields = record["fields"]
        name = fields.get("Name", "").strip()
        current_type = fields.get("Type", "").strip()

        if not name:
            continue

        # Only update blank or "Splash Pad" — never overwrite manually set types
        if current_type and current_type not in ("", "Splash Pad"):
            continue

        new_type = get_type_from_name(name)
        if new_type and new_type != current_type:
            changes.append({
                "id": record["id"],
                "name": name,
                "current_type": current_type or "(blank)",
                "new_type": new_type,
            })

    if not changes:
        print("No changes to make — all records are already typed correctly.")
        return

    # Print summary grouped by new type
    by_type = {}
    for c in changes:
        by_type.setdefault(c["new_type"], []).append(c["name"])

    print(f"Found {len(changes)} records to update:\n")
    for type_name, names in sorted(by_type.items()):
        print(f"  {type_name} ({len(names)}):")
        for n in sorted(names)[:15]:
            print(f"    - {n}")
        if len(names) > 15:
            print(f"    ... and {len(names) - 15} more")
        print()

    if DRY_RUN:
        print("-" * 55)
        print("DRY RUN complete — nothing was written to Airtable.")
        print("Review the list above, then run with --apply to save changes.")
        print("-" * 55)
        return

    # Apply changes using batch update
    print(f"Applying {len(changes)} updates to Airtable...")
    batch = [{"id": c["id"], "fields": {"Type": c["new_type"]}} for c in changes]

    # pyairtable batch_update handles rate limiting automatically
    chunk_size = 10
    for i in range(0, len(batch), chunk_size):
        chunk = batch[i:i + chunk_size]
        table.batch_update(chunk, typecast=True)
        print(f"  Updated {min(i + chunk_size, len(batch))}/{len(changes)}...")

    print(f"\nDone! Updated {len(changes)} records in Airtable.")
    print("Run python3 build.py to rebuild the site with new types.")


if __name__ == "__main__":
    main()
