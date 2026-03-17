#!/usr/bin/env python3
"""
enrich_descriptions.py — Deterministic description enrichment for thin pad listings.

Replaces thin (<100 char) or irrelevant descriptions with varied, informative text
built from available data fields. Uses MD5 hash of the slug for deterministic
template selection so descriptions rebuild identically every time.

Approach adapted from holisticvetdirectory generate_site.py Action 4.

Usage:
  python enrich_descriptions.py              # dry run — preview changes
  python enrich_descriptions.py --apply      # write to Airtable
"""

import argparse
import hashlib
import os
from pathlib import Path

from dotenv import load_dotenv
from pyairtable import Api
from slugify import slugify

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "SplashPads")

MIN_DESC_LENGTH = 100  # descriptions shorter than this get enriched

# ── Known irrelevant description patterns ─────────────────────────────────────
# These are city/county website meta tags that have nothing to do with the facility.
IRRELEVANT_PHRASES = [
    "official website",
    "utility bill",
    "fire department",
    "sign up for programs",
    "senior center",
    "contact information",
    "parks and recreation department",
    "hope to see you soon",
    "demographics, history",
    "sandhill crane capital",
]


def is_irrelevant(desc: str) -> bool:
    """Check if a description is a generic city website meta tag."""
    lower = desc.lower()
    return any(phrase in lower for phrase in IRRELEVANT_PHRASES)


def generate_description(pad: dict) -> str:
    """Build a varied, detailed description from available pad fields."""
    slug = pad.get("slug", pad.get("name", ""))
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)

    parts = []
    name = pad["name"]
    city = pad.get("city", "")
    state = pad.get("state", "")
    pad_type = pad.get("type", "")
    admission = pad.get("admission", "")
    features = pad.get("features", [])
    if isinstance(features, str):
        features = [features] if features else []
    age_range = pad.get("age_range", [])
    if isinstance(age_range, str):
        age_range = [age_range] if age_range else []
    rating = pad.get("rating", 0)
    review_count = pad.get("review_count", 0)
    hours = pad.get("hours", "")

    # ── Type descriptions for richer content ──────────────────────────────
    TYPE_INFO = {
        "Splash Pad": (
            "a splash pad featuring ground-level water jets, spray nozzles, and "
            "interactive water features designed for safe, zero-depth water play"
        ),
        "Spray Park": (
            "a spray park with ground-level sprayers and interactive water features "
            "that let kids run, dodge, and cool off without any standing water"
        ),
        "Water Park": (
            "a water park offering slides, pools, and splash attractions "
            "for visitors of all ages"
        ),
        "Aquatic Center": (
            "an aquatic center with swimming pools and water play areas "
            "designed for both recreation and fitness"
        ),
        "Indoor Splash Pad": (
            "an indoor splash pad that operates year-round regardless of weather, "
            "featuring climate-controlled water play for families in every season"
        ),
        "Indoor Water Play": (
            "an indoor water play facility that offers year-round splash fun "
            "in a climate-controlled environment"
        ),
        "Resort Water Park": (
            "a resort-style water park with pools, slides, and splash areas "
            "available to resort guests and visitors"
        ),
        "Amusement Park": (
            "an amusement park that includes water attractions and splash zones "
            "alongside its rides and entertainment"
        ),
        "Campground Water Park": (
            "a campground with on-site water park facilities including splash pads "
            "and pools for guests to enjoy during their stay"
        ),
    }

    # ── Feature descriptions ──────────────────────────────────────────────
    FEATURE_INFO = {
        "Restrooms": "on-site restrooms",
        "Restroom": "on-site restrooms",
        "Shade": "shaded areas to escape the sun",
        "Picnic Area": "picnic areas for family lunches",
        "Picnic Areas": "picnic areas for family lunches",
        "Playground": "an adjacent playground",
        "Parking": "convenient parking",
        "Accessibility": "accessible design for visitors of all abilities",
        "Concessions": "a concession stand for snacks and drinks",
    }

    # ── Opening sentence (6 variations) ───────────────────────────────────
    variant = h % 6
    type_desc = TYPE_INFO.get(pad_type, "")

    if type_desc and city and state:
        if variant == 0:
            parts.append(
                f"{name} is {type_desc}, located in {city}, {state}."
            )
        elif variant == 1:
            parts.append(
                f"Located in {city}, {state}, {name} is {type_desc} "
                f"that families return to throughout the summer."
            )
        elif variant == 2:
            parts.append(
                f"Families in {city}, {state} will find {name} — "
                f"{type_desc} — a great destination for cooling off on hot days."
            )
        elif variant == 3:
            parts.append(
                f"{name} brings water play to the {city}, {state} community as "
                f"{type_desc}."
            )
        elif variant == 4:
            parts.append(
                f"For families in the {city}, {state} area looking to beat the heat, "
                f"{name} offers {type_desc}."
            )
        else:
            parts.append(
                f"{name} in {city}, {state} is {type_desc}, making it a "
                f"popular choice for families during the warmer months."
            )
    elif city and state:
        if variant % 3 == 0:
            parts.append(
                f"{name} is a water play destination in {city}, {state}, "
                f"offering splash features and interactive water fun for families."
            )
        elif variant % 3 == 1:
            parts.append(
                f"Located in {city}, {state}, {name} provides water play "
                f"activities that families enjoy throughout the summer season."
            )
        else:
            parts.append(
                f"Families in {city}, {state} looking for water fun will find "
                f"{name} a great spot to cool off and play."
            )

    # ── Admission info ────────────────────────────────────────────────────
    if admission:
        adm_variant = (h >> 4) % 3
        if admission == "Free":
            if adm_variant == 0:
                parts.append(
                    "Admission is free, making it an accessible option for "
                    "families looking for no-cost summer fun."
                )
            elif adm_variant == 1:
                parts.append(
                    "Best of all, there's no admission fee — families can visit "
                    "as often as they like without worrying about cost."
                )
            else:
                parts.append(
                    "The facility is free to the public, which makes it easy to "
                    "stop by for a quick cool-down or spend a full afternoon."
                )
        elif admission == "Paid":
            if adm_variant == 0:
                parts.append(
                    "Admission is paid, with pricing that reflects the full range "
                    "of water attractions and amenities available."
                )
            elif adm_variant == 1:
                parts.append(
                    "There is an admission fee, but the facilities and attractions "
                    "make it a worthwhile outing for a family day."
                )
            else:
                parts.append(
                    "The facility charges admission, and it's a good idea to check "
                    "the website for current pricing and any seasonal passes available."
                )

    # ── Features (up to 4, with descriptions) ─────────────────────────────
    if features:
        described = []
        for feat in features[:4]:
            info = FEATURE_INFO.get(feat)
            if info:
                described.append(info)

        if described:
            feat_variant = (h >> 8) % 4
            if feat_variant == 0:
                intro = "Visitors will find "
            elif feat_variant == 1:
                intro = "The facility includes "
            elif feat_variant == 2:
                intro = "Amenities include "
            else:
                intro = "Families can take advantage of "

            if len(described) == 1:
                parts.append(f"{intro}{described[0]}.")
            elif len(described) == 2:
                parts.append(f"{intro}{described[0]} and {described[1]}.")
            else:
                feat_str = ", ".join(described[:-1]) + f", and {described[-1]}"
                parts.append(f"{intro}{feat_str}.")

    # ── Age range ─────────────────────────────────────────────────────────
    if age_range:
        age_variant = (h >> 12) % 3
        age_str = ", ".join(str(a) for a in age_range)

        if "Toddlers" in age_range and len(age_range) > 1:
            if age_variant == 0:
                parts.append(
                    "The water features are designed to be enjoyed by visitors "
                    "of multiple age groups, including toddlers, making it a "
                    "great choice for families with young children."
                )
            elif age_variant == 1:
                parts.append(
                    f"Water play areas cater to {age_str}, with gentler features "
                    f"available for the youngest visitors."
                )
            else:
                parts.append(
                    "Parents of toddlers will appreciate the age-appropriate "
                    "water features alongside options for older kids."
                )
        elif "Toddlers" in age_range:
            parts.append(
                "The gentle water features make this an especially good fit "
                "for toddlers and very young children."
            )
        elif age_range:
            if age_variant == 0:
                parts.append(f"The facility welcomes {age_str}.")
            else:
                parts.append(
                    f"Water play areas are designed for {age_str}, with features "
                    f"scaled to provide fun for the whole group."
                )

    # ── Rating ────────────────────────────────────────────────────────────
    if rating and float(rating) >= 4.0:
        rating_val = float(rating)
        rating_variant = (h >> 16) % 3
        review_str = ""
        if review_count and int(review_count) > 0:
            review_str = f" based on {int(review_count)} reviews"

        if rating_variant == 0:
            parts.append(
                f"The facility has earned a {rating_val}-star rating on Google"
                f"{review_str}, reflecting the positive experiences of visiting families."
            )
        elif rating_variant == 1:
            parts.append(
                f"Visitors have rated {name} {rating_val} out of 5 stars on "
                f"Google{review_str}."
            )
        else:
            parts.append(
                f"With a {rating_val}-star Google rating{review_str}, {name} is "
                f"well regarded by the local community."
            )

    # ── Closing sentence (4 variations) ───────────────────────────────────
    close_variant = (h >> 20) % 4
    if close_variant == 0 and city:
        parts.append(
            f"Check the facility's website or contact them directly for current "
            f"hours, seasonal schedules, and any updates before visiting."
        )
    elif close_variant == 1:
        parts.append(
            "Whether you're planning a quick splash break or a full afternoon "
            "of water play, this facility is worth adding to your summer lineup."
        )
    elif close_variant == 2:
        parts.append(
            "It's a good idea to arrive early on hot days, as popular splash "
            "facilities can get busy by late morning."
        )
    else:
        parts.append(
            "Pack sunscreen, water shoes, and a towel — and plan for a fun day "
            "of water play the whole family can enjoy."
        )

    return " ".join(parts)


def generate_supplement(pad: dict) -> str:
    """Build supplementary content to append to an existing short description.
    Skips the opening sentence (the existing description already introduces the facility)
    and generates admission, features, age range, rating, and closing sections only."""
    slug = pad.get("slug", pad.get("name", ""))
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)

    parts = []
    name = pad["name"]
    city = pad.get("city", "")
    admission = pad.get("admission", "")
    features = pad.get("features", [])
    if isinstance(features, str):
        features = [features] if features else []
    age_range = pad.get("age_range", [])
    if isinstance(age_range, str):
        age_range = [age_range] if age_range else []
    rating = pad.get("rating", 0)
    review_count = pad.get("review_count", 0)

    FEATURE_INFO = {
        "Restrooms": "on-site restrooms",
        "Restroom": "on-site restrooms",
        "Shade": "shaded areas to escape the sun",
        "Picnic Area": "picnic areas for family lunches",
        "Picnic Areas": "picnic areas for family lunches",
        "Playground": "an adjacent playground",
        "Parking": "convenient parking",
        "Accessibility": "accessible design for visitors of all abilities",
        "Concessions": "a concession stand for snacks and drinks",
    }

    # ── Admission info ────────────────────────────────────────────────────
    if admission:
        adm_variant = (h >> 4) % 3
        if admission == "Free":
            if adm_variant == 0:
                parts.append(
                    "Admission is free, making it an accessible option for "
                    "families looking for no-cost summer fun."
                )
            elif adm_variant == 1:
                parts.append(
                    "Best of all, there's no admission fee — families can visit "
                    "as often as they like without worrying about cost."
                )
            else:
                parts.append(
                    "The facility is free to the public, which makes it easy to "
                    "stop by for a quick cool-down or spend a full afternoon."
                )
        elif admission == "Paid":
            if adm_variant == 0:
                parts.append(
                    "Admission is paid, with pricing that reflects the full range "
                    "of water attractions and amenities available."
                )
            elif adm_variant == 1:
                parts.append(
                    "There is an admission fee, but the facilities and attractions "
                    "make it a worthwhile outing for a family day."
                )
            else:
                parts.append(
                    "The facility charges admission, and it's a good idea to check "
                    "the website for current pricing and any seasonal passes available."
                )

    # ── Features ──────────────────────────────────────────────────────────
    if features:
        described = []
        for feat in features[:4]:
            info = FEATURE_INFO.get(feat)
            if info:
                described.append(info)

        if described:
            feat_variant = (h >> 8) % 4
            if feat_variant == 0:
                intro = "Visitors will also find "
            elif feat_variant == 1:
                intro = "Additional amenities include "
            elif feat_variant == 2:
                intro = "The facility also offers "
            else:
                intro = "Families can take advantage of "

            if len(described) == 1:
                parts.append(f"{intro}{described[0]}.")
            elif len(described) == 2:
                parts.append(f"{intro}{described[0]} and {described[1]}.")
            else:
                feat_str = ", ".join(described[:-1]) + f", and {described[-1]}"
                parts.append(f"{intro}{feat_str}.")

    # ── Age range ─────────────────────────────────────────────────────────
    if age_range:
        age_variant = (h >> 12) % 3
        if "Toddlers" in age_range and len(age_range) > 1:
            if age_variant == 0:
                parts.append(
                    "The water features are suitable for multiple age groups, "
                    "including toddlers, making it a great choice for families "
                    "with young children."
                )
            elif age_variant == 1:
                age_str = ", ".join(str(a) for a in age_range)
                parts.append(
                    f"Water play areas cater to {age_str}, with gentler features "
                    f"available for the youngest visitors."
                )
            else:
                parts.append(
                    "Parents of toddlers will appreciate the age-appropriate "
                    "water features alongside options for older kids."
                )
        elif "Toddlers" in age_range:
            parts.append(
                "The gentle water features make this an especially good fit "
                "for toddlers and very young children."
            )

    # ── Rating ────────────────────────────────────────────────────────────
    if rating and float(rating) >= 4.0:
        rating_val = float(rating)
        rating_variant = (h >> 16) % 3
        review_str = ""
        if review_count and int(review_count) > 0:
            review_str = f" based on {int(review_count)} reviews"

        if rating_variant == 0:
            parts.append(
                f"The facility has earned a {rating_val}-star rating on Google"
                f"{review_str}, reflecting the positive experiences of visiting families."
            )
        elif rating_variant == 1:
            parts.append(
                f"Visitors have rated {name} {rating_val} out of 5 stars on "
                f"Google{review_str}."
            )
        else:
            parts.append(
                f"With a {rating_val}-star Google rating{review_str}, {name} is "
                f"well regarded by the local community."
            )

    # ── Closing sentence ──────────────────────────────────────────────────
    close_variant = (h >> 20) % 4
    if close_variant == 0 and city:
        parts.append(
            "Check the facility's website or contact them directly for current "
            "hours, seasonal schedules, and any updates before visiting."
        )
    elif close_variant == 1:
        parts.append(
            "Whether you're planning a quick splash break or a full afternoon "
            "of water play, this facility is worth adding to your summer lineup."
        )
    elif close_variant == 2:
        parts.append(
            "It's a good idea to arrive early on hot days, as popular splash "
            "facilities can get busy by late morning."
        )
    else:
        parts.append(
            "Pack sunscreen, water shoes, and a towel — and plan for a fun day "
            "of water play the whole family can enjoy."
        )

    return " ".join(parts)


APPEND_THRESHOLD = 150  # append mode targets descriptions 100-149 chars


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write enriched descriptions to Airtable")
    parser.add_argument("--append", action="store_true", help="Append supplementary content to short (100-149 char) descriptions")
    args = parser.parse_args()

    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, TABLE_NAME)
    records = table.all()

    print(f"Fetched {len(records)} records from Airtable\n")

    updates = []
    replaced_irrelevant = 0
    enriched_thin = 0
    appended = 0

    for record in records:
        fields = record.get("fields", {})
        record_id = record["id"]
        desc = str(fields.get("Description", "")).strip()

        pad = {
            "name": fields.get("Name", ""),
            "slug": slugify(fields.get("Name", "") + "-" + fields.get("City", "")),
            "city": fields.get("City", ""),
            "state": fields.get("State", ""),
            "type": fields.get("Type", ""),
            "admission": fields.get("Admission", ""),
            "features": fields.get("Features", []),
            "age_range": fields.get("Age Range", []),
            "rating": fields.get("Rating", 0),
            "review_count": fields.get("Review Count", 0),
            "hours": fields.get("Hours", ""),
        }

        if args.append:
            # Append mode: target descriptions 100-149 chars
            if not desc or len(desc) < MIN_DESC_LENGTH or len(desc) >= APPEND_THRESHOLD:
                continue
            if is_irrelevant(desc):
                continue  # these should be caught by a normal --apply run first

            supplement = generate_supplement(pad)
            if not supplement:
                continue

            new_desc = f"{desc} {supplement}"
            appended += 1
            label = "APPEND"
        else:
            # Replace mode: target descriptions < 100 chars or irrelevant
            if desc and len(desc) >= MIN_DESC_LENGTH and not is_irrelevant(desc):
                continue

            new_desc = generate_description(pad)

            if is_irrelevant(desc):
                replaced_irrelevant += 1
                label = "REPLACE (irrelevant)"
            else:
                enriched_thin += 1
                label = "ENRICH (thin)"

        updates.append({
            "id": record_id,
            "fields": {"Description": new_desc},
        })

        print(f"[{label}] {pad['name']} | {pad['city']}, {pad['state']}")
        print(f"  OLD ({len(desc)} chars): {desc[:80]}{'...' if len(desc) > 80 else ''}")
        print(f"  NEW ({len(new_desc)} chars): {new_desc[:120]}...")
        print()

    print(f"{'='*55}")
    print(f"Total to update:       {len(updates)}")
    if args.append:
        print(f"  Appended:            {appended}")
    else:
        print(f"  Replaced irrelevant: {replaced_irrelevant}")
        print(f"  Enriched thin:       {enriched_thin}")

    if not args.apply:
        print(f"\nDry run — no changes written. Use --apply to update Airtable.")
        return

    # Batch update Airtable
    print(f"\nWriting {len(updates)} updates to Airtable...")
    batch_size = 10
    for i in range(0, len(updates), batch_size):
        batch = updates[i:i + batch_size]
        table.batch_update(batch, typecast=True)
        print(f"  Updated {min(i + batch_size, len(updates))}/{len(updates)}")

    print(f"\nDone. {len(updates)} descriptions enriched.")
    print("Run build.py to regenerate the site with updated descriptions.")


if __name__ == "__main__":
    main()
