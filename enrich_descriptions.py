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

# ── State climate context sentences ──────────────────────────────────────────
# One sentence per state that adds unique geographic/climate flavor to descriptions.
# Used as a second sentence for many pad descriptions to break the template pattern.
STATE_CLIMATE = {
    "Alabama": "Alabama's long, humid summers make water play a go-to escape from the heat for families across the state.",
    "Alaska": "Even in Alaska's brief but sunny summers, communities make the most of warm days with outdoor water play.",
    "Arizona": "In Arizona's intense desert heat — where summers regularly top 110°F — splash pads are a genuine seasonal necessity.",
    "Arkansas": "Arkansas summers are long and steamy, and splash pads across the Natural State offer welcome relief from the heat.",
    "California": "California's diverse climate means splash pads stay busy from the scorching Inland Empire to the Bay Area's foggy summers.",
    "Colorado": "Colorado's high-altitude sunshine makes summer afternoons ideal for outdoor water play, even at elevation.",
    "Connecticut": "Connecticut's warm, humid summers give families a short but busy window to enjoy outdoor splash pads and water parks.",
    "Delaware": "Delaware's compact coastline and warm Mid-Atlantic summers keep local splash facilities busy from June through August.",
    "Florida": "In Florida's year-round subtropical heat, splash pads and water parks get steady use well beyond the traditional summer season.",
    "Georgia": "Georgia's long, sweltering summers give families plenty of motivation to seek out local splash pads for cooling off.",
    "Hawaii": "Hawaii's tropical climate means outdoor water play is appealing nearly year-round for local families and visitors alike.",
    "Idaho": "Idaho's warm, dry summers are a perfect backdrop for outdoor splash pads, especially in the Treasure Valley and Magic Valley regions.",
    "Illinois": "Illinois summers can be brutally humid, and splash pads from Chicago's lakefront neighborhoods to downstate communities offer real relief.",
    "Indiana": "Indiana's sticky Midwest summers make community splash pads a popular destination for families from Memorial Day through Labor Day.",
    "Iowa": "Iowa's hot, humid summers may surprise visitors, but local families know exactly where to find water play when temperatures climb.",
    "Kansas": "Kansas summers are known for their intense heat and humidity, and splash pads provide a low-cost way for families to stay cool.",
    "Kentucky": "Kentucky's warm summers and high humidity make splash pads and water parks a seasonal staple for families statewide.",
    "Louisiana": "Louisiana's subtropical heat and humidity make water play not just fun but essential throughout the long summer season.",
    "Maine": "Maine's summers are short but glorious, and local splash facilities make the most of the warm months from late June through August.",
    "Maryland": "Maryland's humid summers stretch well into September, giving families a solid window to enjoy splash pads across the state.",
    "Massachusetts": "Massachusetts summers can be surprisingly hot and humid, making local splash facilities a popular option when temperatures climb.",
    "Michigan": "Michigan summers are warm and welcoming, and water play facilities are spread across both the Upper and Lower peninsulas.",
    "Minnesota": "Minnesota summers are warm and sometimes surprisingly humid, and local communities invest in splash pads to make the most of the season.",
    "Mississippi": "Mississippi's intense summer heat and humidity make water play a near-daily priority for families looking to cool off.",
    "Missouri": "Missouri summers are hot and muggy, and splash pads and water parks across the state draw families from late May through early September.",
    "Montana": "Montana's dry, sunny summers are ideal for outdoor water play, with splash pads popular in Billings, Missoula, and smaller communities.",
    "Nebraska": "Nebraska summers are hot and often humid, and splash pads provide a budget-friendly way for families to beat the heat.",
    "Nevada": "Nevada's desert heat — with Las Vegas and Reno regularly exceeding 100°F — makes water play a high-demand summer activity.",
    "New Hampshire": "New Hampshire's brief but warm summers draw families to splash pads and water parks nestled among the state's scenic landscapes.",
    "New Jersey": "New Jersey's humid summers give families a solid four-month window to enjoy the state's many water parks and splash facilities.",
    "New Mexico": "New Mexico's dry, sunny summers and high-altitude terrain make water play a refreshing break from the heat.",
    "New York": "New York State's summers range from humid city heat in NYC to refreshing mountain temperatures upstate, and splash pads are popular across both.",
    "North Carolina": "North Carolina's warm, humid summers stretch from the coast to the Piedmont, giving families plenty of time to enjoy water play.",
    "North Dakota": "North Dakota summers are shorter but genuinely hot, and local splash pads and water parks see heavy use during the peak season.",
    "Ohio": "Ohio summers are warm and humid, and splash pads are found in community parks from Cleveland and Columbus to smaller rural towns.",
    "Oklahoma": "Oklahoma's sweltering summers — with heat indexes routinely above 105°F — make splash pads a top destination for local families.",
    "Oregon": "Oregon's warm, dry summers — especially east of the Cascades — make outdoor water play a much-anticipated seasonal activity.",
    "Pennsylvania": "Pennsylvania summers can be hot and sticky, and splash pads and water parks are spread across the state from the Philly suburbs to Pittsburgh.",
    "Rhode Island": "Rhode Island's compact coastline and warm summers give families access to both ocean beaches and inland splash pad facilities.",
    "South Carolina": "South Carolina's long, humid summers make water play one of the most popular warm-weather activities for families statewide.",
    "South Dakota": "South Dakota summers are warm and dry, and local splash pads offer a cool break in communities ranging from Sioux Falls to the Black Hills.",
    "Tennessee": "Tennessee's hot, muggy summers make splash pads a neighborhood staple, especially in Nashville, Memphis, and Knoxville.",
    "Texas": "Texas summers are relentlessly hot, and splash pads are found in nearly every city and suburb — from Houston's bayou neighborhoods to Dallas-Fort Worth's sprawling suburbs.",
    "Utah": "Utah's hot, dry summers — particularly in Salt Lake City and St. George — make splash pads a popular addition to local parks.",
    "Vermont": "Vermont summers are short but genuinely warm, and splash pads attract families looking for outdoor fun between July and August.",
    "Virginia": "Virginia's humid summers give families a solid season to enjoy splash pads from Northern Virginia's busy suburbs to the Hampton Roads area.",
    "Washington": "Washington's warm, dry summers east of the Cascades and milder summers on the coast both draw families to splash pads and water parks.",
    "West Virginia": "West Virginia's mountain summers are warm and green, and local splash facilities offer cooling relief during the peak July and August heat.",
    "Wisconsin": "Wisconsin summers are warm and often humid, and splash pads are popular in communities from Milwaukee and Madison to the Northwoods.",
    "Wyoming": "Wyoming's high-altitude summers are warm and sunny, and splash pads in Cheyenne, Casper, and smaller towns see steady summer use.",
    "District of Columbia": "Washington D.C.'s sweltering summers make water play a popular option for families in the city's parks and recreation areas.",
}

# ── Metro city context additions ──────────────────────────────────────────────
# Brief city-character phrases to differentiate large-metro descriptions.
METRO_CONTEXT = {
    "New York": "one of the most park-rich cities in the country",
    "Los Angeles": "a city where outdoor recreation is a year-round culture",
    "Chicago": "a city known for its extensive park district and lakefront recreation",
    "Houston": "a sprawling city where neighborhood parks and splash pads serve communities across all 88 square miles of city land",
    "Phoenix": "a metro area that has made splash pad infrastructure a public health priority given extreme summer heat",
    "Philadelphia": "a city with a long history of neighborhood recreation centers and public parks",
    "Dallas": "a growing metro where public parks and splash facilities serve expanding suburban and urban communities",
    "San Antonio": "a city proud of its community parks and family-friendly outdoor spaces",
    "San Diego": "a city where year-round mild weather supports outdoor recreation well beyond traditional summer months",
    "San Jose": "a Silicon Valley city with a strong network of community parks and recreation facilities",
    "Austin": "a fast-growing city that has invested in parks and outdoor recreation to serve its expanding population",
    "Jacksonville": "Florida's largest city by land area, with parks and recreation spread across a wide geographic footprint",
    "Columbus": "a Midwest city with a well-developed parks system and active community recreation culture",
    "Charlotte": "a rapidly growing Southern city that continues to expand its parks and recreation infrastructure",
    "Indianapolis": "a city that has revitalized its parks and waterways as part of broader urban reinvestment",
    "Seattle": "a city where dry summers bring families out to parks and water play areas from July through September",
    "Denver": "a city where outdoor recreation culture runs deep and parks attract families across the metro area",
    "Nashville": "a city experiencing rapid growth and corresponding investment in parks and community recreation",
    "Louisville": "a city with an extensive parks system designed by Frederick Law Olmsted's firm",
    "Memphis": "a city where neighborhood parks and recreation centers serve as community anchors",
    "Baltimore": "a city with a growing network of neighborhood recreation spaces and waterfront attractions",
    "Boston": "a city where compact neighborhoods and green spaces make parks a central part of daily family life",
    "Portland": "a city with strong commitment to public parks and outdoor recreation throughout the warm season",
    "Las Vegas": "a metro where intense summer heat makes water play facilities a practical necessity alongside the entertainment corridor",
    "Oklahoma City": "a city that has invested heavily in parks and outdoor recreation as part of its MAPS civic improvement program",
    "Tucson": "a desert city where shaded splash pads provide critical outdoor recreation relief during triple-digit summer heat",
    "Atlanta": "a city spread across a large metro footprint, with splash pads serving neighborhoods from Buckhead to East Atlanta",
    "Miami": "a subtropical city where water-based recreation is a year-round part of the local culture",
    "Minneapolis": "a city known for its park system — consistently ranked among the best-maintained in the country",
    "Tampa": "a Gulf Coast city where warm weather and proximity to water make outdoor recreation a lifestyle",
}


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
    season = pad.get("season", "")

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
        "Snack Bar": "a snack bar on-site",
        "Changing Rooms": "changing rooms for visitors",
        "Locker Rooms": "locker room facilities",
        "Lifeguard on Duty": "lifeguard supervision during operating hours",
        "Season Passes": "season pass options for frequent visitors",
        "Party Rentals": "rental space available for private events",
    }

    # ── Opening sentence (12 variations) ──────────────────────────────────
    variant = h % 12
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
        elif variant == 5:
            parts.append(
                f"{name} in {city}, {state} is {type_desc}, making it a "
                f"popular choice for families during the warmer months."
            )
        elif variant == 6:
            parts.append(
                f"When temperatures rise in {city}, {state}, families head to {name} — "
                f"{type_desc}."
            )
        elif variant == 7:
            parts.append(
                f"{city}, {state} is home to {name}, {type_desc} that draws "
                f"local families looking for outdoor water fun."
            )
        elif variant == 8:
            parts.append(
                f"A neighborhood favorite in {city}, {state}, {name} is "
                f"{type_desc} open to the community."
            )
        elif variant == 9:
            parts.append(
                f"Summer in {city}, {state} often means a trip to {name}, "
                f"{type_desc} popular with local families."
            )
        elif variant == 10:
            parts.append(
                f"{name} serves the {city}, {state} area as {type_desc}, "
                f"welcoming families of all sizes throughout the season."
            )
        else:
            parts.append(
                f"Right in the heart of {city}, {state}, {name} is "
                f"{type_desc} that makes warm-weather days easier for families."
            )
    elif city and state:
        if variant % 4 == 0:
            parts.append(
                f"{name} is a water play destination in {city}, {state}, "
                f"offering splash features and interactive water fun for families."
            )
        elif variant % 4 == 1:
            parts.append(
                f"Located in {city}, {state}, {name} provides water play "
                f"activities that families enjoy throughout the summer season."
            )
        elif variant % 4 == 2:
            parts.append(
                f"Families in {city}, {state} looking for water fun will find "
                f"{name} a great spot to cool off and play."
            )
        else:
            parts.append(
                f"{city}, {state} families have made {name} a summer staple "
                f"for outdoor water play and cooling off."
            )

    # ── State climate context (adds geographic uniqueness) ────────────────
    climate_sentence = STATE_CLIMATE.get(state, "")
    if climate_sentence:
        # Only include if the opening didn't already lean heavily on climate
        climate_variant = (h >> 2) % 3
        if climate_variant == 0:
            parts.append(climate_sentence)
        elif climate_variant == 1 and season:
            # Weave season in with a state-flavored note
            parts.append(
                f"Typically open {season}, it takes full advantage of the region's "
                f"warm-weather season."
            )
        elif climate_variant == 2 and not season:
            parts.append(climate_sentence)
        # else: skip climate sentence to avoid over-repetition

    # ── Season info ───────────────────────────────────────────────────────
    if season and (h >> 2) % 3 != 1:  # avoid duplication with climate block
        season_variant = (h >> 6) % 3
        if season_variant == 0:
            parts.append(f"The facility is typically open {season}.")
        elif season_variant == 1:
            parts.append(
                f"Visitors can plan their trip around the {season} operating window."
            )
        else:
            parts.append(
                f"The season runs {season}, so check ahead if you're visiting "
                f"near the start or end of the schedule."
            )

    # ── Admission info ────────────────────────────────────────────────────
    if admission:
        adm_variant = (h >> 4) % 4
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
            elif adm_variant == 2:
                parts.append(
                    "The facility is free to the public, which makes it easy to "
                    "stop by for a quick cool-down or spend a full afternoon."
                )
            else:
                parts.append(
                    "Free admission means families can make this a go-to summer "
                    "destination without budget concerns."
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
            elif adm_variant == 2:
                parts.append(
                    "The facility charges admission, and it's a good idea to check "
                    "the website for current pricing and any seasonal passes available."
                )
            else:
                parts.append(
                    "Paid admission helps support the facility's upkeep and the "
                    "range of amenities visitors enjoy on-site."
                )

    # ── Features (up to 4, with descriptions) ─────────────────────────────
    if features:
        described = []
        for feat in features[:4]:
            info = FEATURE_INFO.get(feat)
            if info:
                described.append(info)

        if described:
            feat_variant = (h >> 8) % 5
            if feat_variant == 0:
                intro = "Visitors will find "
            elif feat_variant == 1:
                intro = "The facility includes "
            elif feat_variant == 2:
                intro = "Amenities include "
            elif feat_variant == 3:
                intro = "Families can take advantage of "
            else:
                intro = "On-site you'll find "

            if len(described) == 1:
                parts.append(f"{intro}{described[0]}.")
            elif len(described) == 2:
                parts.append(f"{intro}{described[0]} and {described[1]}.")
            else:
                feat_str = ", ".join(described[:-1]) + f", and {described[-1]}"
                parts.append(f"{intro}{feat_str}.")

    # ── Age range ─────────────────────────────────────────────────────────
    if age_range:
        age_variant = (h >> 12) % 4
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
            elif age_variant == 2:
                parts.append(
                    "Parents of toddlers will appreciate the age-appropriate "
                    "water features alongside options for older kids."
                )
            else:
                parts.append(
                    f"Whether you're bringing toddlers or older kids, the "
                    f"facility has water play suited to {age_str}."
                )
        elif "Toddlers" in age_range:
            if age_variant % 2 == 0:
                parts.append(
                    "The gentle water features make this an especially good fit "
                    "for toddlers and very young children."
                )
            else:
                parts.append(
                    "Low-intensity water features make this a natural choice "
                    "for families with toddlers."
                )
        elif age_range:
            if age_variant == 0:
                parts.append(f"The facility welcomes {age_str}.")
            elif age_variant == 1:
                parts.append(
                    f"Water play areas are designed for {age_str}, with features "
                    f"scaled to provide fun for the whole group."
                )
            else:
                parts.append(
                    f"The facility caters to {age_str}, with water elements "
                    f"appropriate for the expected age groups."
                )

    # ── Rating ────────────────────────────────────────────────────────────
    if rating and float(rating) >= 4.0:
        rating_val = float(rating)
        rating_variant = (h >> 16) % 4
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
        elif rating_variant == 2:
            parts.append(
                f"With a {rating_val}-star Google rating{review_str}, {name} is "
                f"well regarded by the local community."
            )
        else:
            parts.append(
                f"Strong Google reviews ({rating_val} stars{review_str}) suggest "
                f"families consistently enjoy their visits here."
            )

    # ── Hours hint ────────────────────────────────────────────────────────
    if hours and (h >> 18) % 3 == 0:
        parts.append(
            f"Operating hours are {hours} — confirm directly with the facility "
            f"before your visit as schedules can vary."
        )

    # ── Closing sentence (5 variations) ───────────────────────────────────
    close_variant = (h >> 20) % 5
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
    elif close_variant == 3:
        parts.append(
            "Pack sunscreen, water shoes, and a towel — and plan for a fun day "
            "of water play the whole family can enjoy."
        )
    else:
        parts.append(
            "Bring the kids ready to splash, and plan to stay longer than you "
            "think — these facilities have a way of making time disappear."
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
    state = pad.get("state", "")
    admission = pad.get("admission", "")
    features = pad.get("features", [])
    if isinstance(features, str):
        features = [features] if features else []
    age_range = pad.get("age_range", [])
    if isinstance(age_range, str):
        age_range = [age_range] if age_range else []
    rating = pad.get("rating", 0)
    review_count = pad.get("review_count", 0)
    season = pad.get("season", "")

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
        "Snack Bar": "a snack bar on-site",
        "Changing Rooms": "changing rooms for visitors",
        "Locker Rooms": "locker room facilities",
        "Lifeguard on Duty": "lifeguard supervision during operating hours",
        "Season Passes": "season pass options for frequent visitors",
        "Party Rentals": "rental space available for private events",
    }

    # ── State climate context ─────────────────────────────────────────────
    climate_sentence = STATE_CLIMATE.get(state, "")
    if climate_sentence and (h >> 2) % 2 == 0:
        parts.append(climate_sentence)

    # ── Season info ───────────────────────────────────────────────────────
    if season:
        season_variant = (h >> 6) % 3
        if season_variant == 0:
            parts.append(f"The facility is typically open {season}.")
        elif season_variant == 1:
            parts.append(
                f"Visitors can plan their trip around the {season} operating window."
            )
        else:
            parts.append(
                f"The season runs {season}, so check ahead if you're visiting "
                f"near the start or end of the schedule."
            )

    # ── Admission info ────────────────────────────────────────────────────
    if admission:
        adm_variant = (h >> 4) % 4
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
            elif adm_variant == 2:
                parts.append(
                    "The facility is free to the public, which makes it easy to "
                    "stop by for a quick cool-down or spend a full afternoon."
                )
            else:
                parts.append(
                    "Free admission means families can make this a go-to summer "
                    "destination without budget concerns."
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
            elif adm_variant == 2:
                parts.append(
                    "The facility charges admission, and it's a good idea to check "
                    "the website for current pricing and any seasonal passes available."
                )
            else:
                parts.append(
                    "Paid admission helps support the facility's upkeep and the "
                    "range of amenities visitors enjoy on-site."
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
    close_variant = (h >> 20) % 5
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
    elif close_variant == 3:
        parts.append(
            "Pack sunscreen, water shoes, and a towel — and plan for a fun day "
            "of water play the whole family can enjoy."
        )
    else:
        parts.append(
            "Bring the kids ready to splash, and plan to stay longer than you "
            "think — these facilities have a way of making time disappear."
        )

    return " ".join(parts)


APPEND_THRESHOLD = 150  # append mode targets descriptions 100-149 chars
REGEN_DEFAULT_THRESHOLD = 250  # --regen-thin default: regenerate descriptions under this length


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write enriched descriptions to Airtable")
    parser.add_argument("--append", action="store_true", help="Append supplementary content to short (100-149 char) descriptions")
    parser.add_argument(
        "--regen-thin", nargs="?", const=REGEN_DEFAULT_THRESHOLD, type=int, metavar="MAX_CHARS",
        help=(
            f"Regenerate descriptions under MAX_CHARS length using the improved template. "
            f"Targets existing template-pattern descriptions that are too short to pass Google quality checks. "
            f"Default threshold: {REGEN_DEFAULT_THRESHOLD} chars."
        )
    )
    args = parser.parse_args()

    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, TABLE_NAME)
    records = table.all()

    print(f"Fetched {len(records)} records from Airtable\n")

    updates = []
    replaced_irrelevant = 0
    enriched_thin = 0
    appended = 0
    regen_count = 0

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
            "season": fields.get("Season", ""),
        }

        if args.regen_thin is not None:
            # Regen mode: replace short descriptions under the threshold
            if not desc or len(desc) >= args.regen_thin:
                continue
            if is_irrelevant(desc):
                continue  # handled by normal --apply mode

            new_desc = generate_description(pad)
            regen_count += 1
            label = f"REGEN (< {args.regen_thin} chars)"

        elif args.append:
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
    if args.regen_thin is not None:
        print(f"  Regenerated thin:    {regen_count} (threshold: < {args.regen_thin} chars)")
    elif args.append:
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
