import pandas as pd
import re
import json
import os
from datetime import datetime
from difflib import SequenceMatcher

# ==============================
# FORCE FILES TO SCRIPT DIRECTORY
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTSCRAPER_FILE = os.path.join(BASE_DIR, "Outscraper-20260227214450m35_water_park.xlsx")
PREVIOUS_AIRTABLE_FILE = os.path.join(BASE_DIR, "SplashPads-Grid view.csv")

OUTPUT_FILE = os.path.join(BASE_DIR, "SplashPads_NEW_ONLY.csv")
DUPLICATES_FILE = os.path.join(BASE_DIR, "SplashPads_DUPLICATES_SKIPPED.csv")

COORD_TOLERANCE = 0.001
FUZZY_THRESHOLD = 0.90

# ==============================
# LOAD DATA
# ==============================

df = pd.read_excel(OUTSCRAPER_FILE)
previous = pd.read_csv(PREVIOUS_AIRTABLE_FILE)

print(f"Original Outscraper rows: {len(df)}")

df.columns = df.columns.str.strip().str.lower()
previous.columns = previous.columns.str.strip().str.lower()

def normalize(series):
    return series.astype(str).str.strip().str.lower()

# Normalize key fields for dedupe
df["name_clean"] = normalize(df.get("name", ""))
df["street_clean"] = normalize(df.get("address", ""))
df["city_clean"] = normalize(df.get("city", ""))
df["state_clean"] = normalize(df.get("state", ""))
df["location_link_clean"] = normalize(df.get("location_link", ""))

previous["name_clean"] = normalize(previous.get("name", ""))
previous["street_clean"] = normalize(previous.get("address", ""))
previous["city_clean"] = normalize(previous.get("city", ""))
previous["state_clean"] = normalize(previous.get("state", ""))
previous["location_link_clean"] = normalize(previous.get("google maps url", ""))

# ==============================
# INTERNAL DEDUPE
# ==============================

df = df.drop_duplicates(subset=["location_link_clean"])
df = df.drop_duplicates(subset=["name_clean", "street_clean"])
df = df.drop_duplicates(subset=["name_clean", "city_clean", "state_clean"])

print(f"After internal dedupe: {len(df)}")

# ==============================
# DUPLICATE DETECTION
# ==============================

existing_links = set(previous["location_link_clean"])
existing_name_address = set(previous["name_clean"] + "|" + previous["street_clean"])
previous_records = previous.to_dict("records")

def fuzzy_match(a, b):
    return SequenceMatcher(None, a, b).ratio()

def coord_close(lat1, lon1, lat2, lon2):
    if pd.isna(lat1) or pd.isna(lon1) or pd.isna(lat2) or pd.isna(lon2):
        return False
    return abs(lat1 - lat2) <= COORD_TOLERANCE and \
           abs(lon1 - lon2) <= COORD_TOLERANCE

def is_duplicate(row):

    if row["location_link_clean"] in existing_links:
        return True

    key = row["name_clean"] + "|" + row["street_clean"]
    if key in existing_name_address:
        return True

    for prev in previous_records:
        if row["city_clean"] != prev["city_clean"]:
            continue
        if row["state_clean"] != prev["state_clean"]:
            continue

        if coord_close(row.get("latitude"),
                       row.get("longitude"),
                       prev.get("latitude"),
                       prev.get("longitude")):
            return True

        if fuzzy_match(row["name_clean"], prev["name_clean"]) >= FUZZY_THRESHOLD:
            return True

    return False

df["is_duplicate"] = df.apply(is_duplicate, axis=1).fillna(False)

duplicates = df[df["is_duplicate"]]
new_records = df[~df["is_duplicate"]]

print(f"Removed existing records: {len(duplicates)}")
print(f"New records to import: {len(new_records)}")

duplicates.to_csv(DUPLICATES_FILE, index=False)

df = new_records.reset_index(drop=True)

print(f"DF rows before building output: {len(df)}")

# ==============================
# FIELD HELPERS
# ==============================

def clean_field(val):
    """Convert a field value to a clean string, returning '' for nan/empty."""
    s = str(val).strip()
    return "" if s.lower() == "nan" or s == "" else s

def combine_description(row):
    parts = [
        clean_field(row.get("website_description", "")),
        clean_field(row.get("description", "")),
        clean_field(row.get("company_insights.description", "")),
    ]
    # Use the longest non-empty part as the primary description
    parts = [p for p in parts if p]
    if not parts:
        return ""
    # Return the longest one — it's usually the most informative
    return max(parts, key=len)

def format_phone(phone):
    if pd.isna(phone):
        return ""
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return ""

def derive_features(row):
    """
    Derives Airtable multi-select 'features' field
    based on structured and free-text Outscraper data.
    """

    VALID_FEATURES = {
        "restroom",
        "shade",
        "parking",
        "playground",
        "snack bar",
        "accessibility"
    }

    features = set()

    text = " ".join([
        clean_field(row.get("about", "")),
        clean_field(row.get("description", "")),
        clean_field(row.get("website_description", "")),
        clean_field(row.get("subtypes", "")),
        clean_field(row.get("company_insights.description", "")),
    ]).lower()

    # Restroom
    if any(word in text for word in ["restroom", "bathroom", "toilet"]):
        features.add("restroom")

    # Shade
    if any(word in text for word in [
        "shade structure",
        "shaded area",
        "covered pavilion",
        "canopy"
    ]):
        features.add("shade")

    # Parking
    if any(word in text for word in [
        "parking lot",
        "free parking",
        "paid parking"
    ]):
        features.add("parking")

    # Playground
    if "playground" in text:
        features.add("playground")

    # Snack Bar
    if any(word in text for word in [
        "snack bar",
        "concessions",
        "food stand"
    ]):
        features.add("snack bar")

    # Accessibility
    if any(word in text for word in [
        "wheelchair",
        "ada accessible",
        "accessible entrance"
    ]):
        features.add("accessibility")

    # Convert to Title Case for Airtable
    formatted = [f.title() for f in sorted(features) if f in VALID_FEATURES]

    return ", ".join(formatted)

def derive_type(subtypes):
    if pd.isna(subtypes):
        return ""
    subtypes = str(subtypes).lower()
    if "indoor" in subtypes:
        return "Indoor Water Play"
    if "water playground" in subtypes:
        return "Water Playground"
    if "spray park" in subtypes:
        return "Spray Park"
    if "splash pad" in subtypes:
        return "Splash Pad"
    return ""

def derive_admission(row):
    text = " ".join([
        clean_field(row.get("prices", "")),
        clean_field(row.get("about", "")),
        clean_field(row.get("description", "")),
        clean_field(row.get("website_description", "")),
        clean_field(row.get("company_insights.description", "")),
    ]).lower()

    place_type = derive_type(row.get("subtypes", ""))

    if any(x in text for x in ["season pass", "seasonal pass", "annual pass", "membership"]):
        return "Seasonal Pass"

    if re.search(r"\$\s*\d+", text):
        return "Paid"

    if "free" in text:
        return "Free"

    if place_type in ["Splash Pad", "Spray Park"]:
        return "Free"

    return ""

def derive_age_range(row):
    text = str(row.get("about", "")).lower()
    ages = set()
    if "good for kids" in text:
        ages.update(["Kids", "Families"])
    if "toddler" in text:
        ages.add("Toddlers")
    if "tween" in text:
        ages.add("Tweens")
    if "all ages" in text:
        ages.add("All Ages")
    return ", ".join(sorted(ages))

def format_hours(hours_raw):
    if pd.isna(hours_raw):
        return ""
    try:
        hours_dict = json.loads(hours_raw.replace("'", '"')) \
            if isinstance(hours_raw, str) else hours_raw
    except:
        return str(hours_raw)

    formatted = []
    all_times = set()
    for day, times in hours_dict.items():
        if times:
            time_str = " & ".join(times).replace("-", "–")
            formatted.append(f"{day}: {time_str}")
            all_times.add(time_str)

    if len(all_times) == 1:
        return f"Daily: {list(all_times)[0]}"
    return "\n".join(formatted)

def col(name):
    return df[name] if name in df.columns else pd.Series([""] * len(df))

# ==============================
# BUILD OUTPUT (LOCKED ORDER)
# ==============================

output = pd.DataFrame()

output["name"] = col("name")
output["description"] = df.apply(combine_description, axis=1)
output["address"] = col("address")
output["city"] = col("city")
output["state"] = col("state")
output["zip"] = col("postal_code")
output["phone"] = col("phone").apply(format_phone)
output["website url"] = col("website")
output["google maps url"] = col("location_link")
output["photo url"] = col("photo")
output["hours"] = col("working_hours").apply(format_hours)
output["admission"] = df.apply(derive_admission, axis=1)
output["price"] = col("prices")
output["age range"] = df.apply(derive_age_range, axis=1)
output["features"] = df.apply(derive_features, axis=1)
output["type"] = col("subtypes").apply(derive_type)
output["date added"] = datetime.today().strftime("%Y-%m-%d")
output["rating"] = col("rating")
output["review count"] = col("reviews")
output["latitude"] = col("latitude")
output["longitude"] = col("longitude")
output["logo"] = col("logo")

FINAL_COLUMNS = [
    "name",
    "description",
    "address",
    "city",
    "state",
    "zip",
    "phone",
    "website url",
    "google maps url",
    "photo url",
    "hours",
    "admission",
    "price",
    "age range",
    "features",
    "type",
    "date added",   # ← comma here
    "rating",
    "review count",
    "latitude",
    "longitude",
    "logo"
]

for col_name in FINAL_COLUMNS:
    if col_name not in output.columns:
        output[col_name] = ""

output = output[FINAL_COLUMNS]

print("Final output row count:", len(output))

output.to_csv(OUTPUT_FILE, index=False)

print(f"✅ New-only file saved: {OUTPUT_FILE}")
print(f"🗂 Duplicate report saved: {DUPLICATES_FILE}")