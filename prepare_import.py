#!/usr/bin/env python3
"""
prepare_import.py — Clean SplashPads_NEW_ONLY.csv before loading into Airtable.

Clears the following columns so the auto_* scripts can manage them cleanly:
  - description  → auto_descriptions.py --apply --ai
  - type         → auto_type.py --apply
  - features     → auto_features.py --apply
  - age range    → auto_age_range.py --apply

Saves a new file: SplashPads_READY_TO_IMPORT.csv
"""

import pandas as pd
from pathlib import Path

INPUT_FILE  = Path("SplashPads_NEW_ONLY.csv")
OUTPUT_FILE = Path("SplashPads_READY_TO_IMPORT.csv")

COLUMNS_TO_CLEAR = ["description", "type", "features", "age range"]

df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} rows from {INPUT_FILE}\n")

print("Clearing columns:")
for col in COLUMNS_TO_CLEAR:
    if col in df.columns:
        non_empty = df[col].notna().sum()
        df[col] = ""
        print(f"  {col}: cleared {non_empty} values")
    else:
        print(f"  {col}: not found (skipped)")

df.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved: {OUTPUT_FILE} ({len(df)} rows ready to import)")
print("\nNext steps after loading into Airtable:")
print("  1. python3 auto_type.py --apply")
print("  2. python3 auto_age_range.py --apply")
print("  3. python3 auto_features.py --apply")
print("  4. python3 auto_descriptions.py --apply --ai")
print("  5. python3 build.py")
