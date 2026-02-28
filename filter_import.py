#!/usr/bin/env python3
"""
filter_import.py — Remove non-water-attraction records from SplashPads_READY_TO_IMPORT.csv

Removes records that have no water-related keyword in their name AND match
known non-water attraction patterns (fun centers, amusement parks without
water, go-karts, animal attractions, boat tours, plazas, etc.)

Saves:
  SplashPads_FILTERED.csv        — clean records ready to load
  SplashPads_REMOVED.csv         — removed records for your review
"""

import pandas as pd
from pathlib import Path

INPUT_FILE   = Path("SplashPads_READY_TO_IMPORT.csv")
OUTPUT_FILE  = Path("SplashPads_FILTERED.csv")
REMOVED_FILE = Path("SplashPads_REMOVED.csv")

# Keywords that indicate a legitimate water attraction
WATER_WORDS = [
    "splash", "spray", "aquatic", "pool", "water", "swim", "wave",
    "slide", "lagoon", "bay", "creek", "river", "lake", "shore",
    "oasis", "cove", "island", "beach", "surf", "tide", "fountain",
    "wet", "hydro", "marine", "sea", "ocean", "tropical", "resort",
    "jellystone", "koa ", "schlitterbahn", "typhoon", "whitewater",
]

# Keywords that flag a non-water attraction (only applied when no water keyword found)
NOT_WATER = [
    "amusement park", "theme park",
    "go-kart", "go kart", "gokart",
    "mini golf", "mini-golf",
    "trampoline", "bounce",
    "bowling",
    "laser tag",
    "escape room",
    "snake", "animal farm", "dinosaur",
    "axe throw",
    "arcade",
    "fun center", "fun zone", "fun park",
    "kayak", "canoe", "paddleboard",
    "speedboat", "sightseeing cruise", "boat ride", "boat tour",
    "zipline", "zip line",
    "rock climbing",
    "batting cage",
    "bumper car",
    "haunted",
    "sky zone",
    "kids empire",
    "catch air",
    "magic sky",
    "jumpin", "jumping",
    "indoor play",
    "play place",
    "square",           # city plazas e.g. Abingdon Square, Jackson Square
    "circle line",
    "picnic grounds",
    "mb2 entertainment",
]

df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} rows from {INPUT_FILE}\n")


def should_remove(name):
    name_lower = str(name).lower()

    # Keep anything with a water keyword in the name
    if any(w in name_lower for w in WATER_WORDS):
        return False

    # No water keyword — check for known non-water patterns
    return any(kw in name_lower for kw in NOT_WATER)


mask_remove = df["name"].apply(should_remove)
removed  = df[mask_remove].copy()
filtered = df[~mask_remove].copy()

print(f"Records kept:    {len(filtered)}")
print(f"Records removed: {len(removed)}")

print("\nRemoved records:")
for _, row in removed.iterrows():
    print(f"  {row['name']} | {row['city']}, {row['state']}")

filtered.to_csv(OUTPUT_FILE, index=False)
removed.to_csv(REMOVED_FILE, index=False)

print(f"\nSaved: {OUTPUT_FILE}  ({len(filtered)} rows)")
print(f"Saved: {REMOVED_FILE} ({len(removed)} rows — review if needed)")
