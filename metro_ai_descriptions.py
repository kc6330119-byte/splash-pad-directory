#!/usr/bin/env python3
"""
metro_ai_descriptions.py — AI-powered unique descriptions for top-50 metro pad pages.

Targets pad pages in large US metro cities where Google scrutiny is highest.
Generates 3-5 sentence descriptions that include genuine local context:
city character, regional climate, neighborhood identity, and community relevance.

This addresses the "Crawled, not indexed" problem by ensuring high-value metro
pages have truly unique content that cannot be pattern-matched as templated output.

Usage:
    python3 metro_ai_descriptions.py              # dry run — shows what would change
    python3 metro_ai_descriptions.py --apply      # write descriptions to Airtable
    python3 metro_ai_descriptions.py --limit 10   # limit AI calls for testing

Requirements:
    - ANTHROPIC_API_KEY in .env
    - AIRTABLE_API_KEY and AIRTABLE_BASE_ID in .env
"""

import argparse
import os
import time
from dotenv import load_dotenv
from pyairtable import Api

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "SplashPads")

CHUNK_SIZE = 10

# ── Top 50 metro target cities ────────────────────────────────────────────────
# Prioritized by population and Google indexing value.
# Each city has a context string used to enrich the AI prompt.
TOP_METRO_CITIES = {
    "New York": {
        "state": "New York",
        "context": "one of the most park-dense cities in the world, where borough identity and neighborhood character vary dramatically from block to block",
        "climate": "hot and humid summers with temperatures regularly reaching the mid-90s°F"
    },
    "Los Angeles": {
        "state": "California",
        "context": "a sprawling city where outdoor recreation is part of the culture year-round, with distinct neighborhood identities from the Valley to the Westside",
        "climate": "warm, sunny summers with low humidity and temperatures in the 80-90s°F inland"
    },
    "Chicago": {
        "state": "Illinois",
        "context": "a city famous for its extensive Chicago Park District, which operates hundreds of parks across 77 neighborhoods",
        "climate": "hot and humid summers after brutally cold winters, making outdoor water play especially anticipated"
    },
    "Houston": {
        "state": "Texas",
        "context": "a sprawling Gulf Coast city where neighborhood parks and splash pads serve communities across a massive geographic footprint",
        "climate": "sweltering subtropical summers with heat index values regularly exceeding 105°F from May through September"
    },
    "Phoenix": {
        "state": "Arizona",
        "context": "a desert metro where splash pad infrastructure is a genuine public health consideration given average July highs above 106°F",
        "climate": "extreme desert heat with summer temperatures among the highest of any major US city"
    },
    "Philadelphia": {
        "state": "Pennsylvania",
        "context": "a city with a long history of neighborhood recreation infrastructure including Fairmount Park, one of the largest urban park systems in the country",
        "climate": "hot, humid mid-Atlantic summers with July temperatures averaging in the high 80s°F"
    },
    "Dallas": {
        "state": "Texas",
        "context": "a fast-growing North Texas city where suburban expansion has driven investment in parks, splash pads, and outdoor recreation across the metro",
        "climate": "hot southern summers with temperatures frequently above 100°F from June through August"
    },
    "San Antonio": {
        "state": "Texas",
        "context": "a city proud of its community identity, with parks and outdoor spaces playing a central role in San Antonio's family-friendly culture",
        "climate": "long, hot Texas summers with high humidity and temperatures regularly above 95°F"
    },
    "San Diego": {
        "state": "California",
        "context": "a coastal city with year-round outdoor recreation culture, where even 'cool' summer days justify water play",
        "climate": "mild, consistent summers near the coast with warmer temperatures inland and low humidity"
    },
    "San Jose": {
        "state": "California",
        "context": "Silicon Valley's largest city, with a well-developed parks and recreation system serving a dense and diverse population",
        "climate": "warm, dry Bay Area summers with inland temperatures rising significantly during heat waves"
    },
    "Austin": {
        "state": "Texas",
        "context": "a rapidly growing city that has actively expanded its parks and outdoor recreation infrastructure to serve a booming population",
        "climate": "intense Central Texas heat with July averages above 97°F and frequent stretches above 105°F"
    },
    "Jacksonville": {
        "state": "Florida",
        "context": "Florida's largest city by land area, with diverse parks and recreation facilities spread across a wide geographic footprint along the St. Johns River",
        "climate": "subtropical Florida heat and humidity with a long summer season running from April through October"
    },
    "Columbus": {
        "state": "Ohio",
        "context": "a growing Midwest city with an active parks system and strong community investment in outdoor recreation facilities",
        "climate": "warm, humid Ohio summers with July temperatures in the upper 80s°F"
    },
    "Charlotte": {
        "state": "North Carolina",
        "context": "a rapidly expanding Southern city that continues to invest in parks infrastructure to serve its growing suburban and urban communities",
        "climate": "hot, humid Piedmont summers with high heat index values from June through August"
    },
    "Indianapolis": {
        "state": "Indiana",
        "context": "a Midwest city that has invested in its parks and waterways as part of broader urban revitalization efforts",
        "climate": "warm and humid Midwest summers with July temperatures in the mid-to-upper 80s°F"
    },
    "Seattle": {
        "state": "Washington",
        "context": "a city where dry, warm summers are eagerly anticipated after long gray winters, driving strong turnout at outdoor recreation facilities",
        "climate": "mild, dry summers with July temperatures in the 70s°F — a brief but beloved warm season"
    },
    "Denver": {
        "state": "Colorado",
        "context": "a city with deep outdoor recreation culture, where high-altitude sunshine makes parks and splash pads popular from late spring through early fall",
        "climate": "warm, sunny summers at 5,280 feet with low humidity and afternoon thunderstorms"
    },
    "Nashville": {
        "state": "Tennessee",
        "context": "a city experiencing rapid growth and corresponding expansion of parks and community recreation in both established neighborhoods and new developments",
        "climate": "hot and humid Tennessee summers with July averages in the upper 80s°F"
    },
    "Louisville": {
        "state": "Kentucky",
        "context": "a city with an extensive parks system designed by the Olmsted firm, with water play facilities woven into many of its historic green spaces",
        "climate": "warm, sticky Ohio Valley summers with temperatures regularly above 90°F from June through August"
    },
    "Memphis": {
        "state": "Tennessee",
        "context": "a city where neighborhood parks and recreation centers have long served as community anchors in diverse residential areas",
        "climate": "hot and muggy Mississippi Delta summers with heat indexes often above 100°F"
    },
    "Baltimore": {
        "state": "Maryland",
        "context": "a waterfront city with a growing network of neighborhood recreation spaces serving its many distinct urban communities",
        "climate": "hot, humid mid-Atlantic summers with temperatures in the upper 80s°F and high heat indexes"
    },
    "Boston": {
        "state": "Massachusetts",
        "context": "a compact city where neighborhood green spaces and parks play an outsized role in daily life given the dense urban fabric",
        "climate": "warm, humid New England summers with July temperatures in the mid-80s°F"
    },
    "Portland": {
        "state": "Oregon",
        "context": "a city with strong commitment to public parks and green space, where outdoor recreation culture thrives during the warm, dry summer months",
        "climate": "warm, dry Pacific Northwest summers from July through September after a long wet season"
    },
    "Las Vegas": {
        "state": "Nevada",
        "context": "a desert city where water play facilities serve the local residential population beyond the Strip, especially in suburban family neighborhoods",
        "climate": "extreme desert heat with summer temperatures regularly above 110°F — one of the hottest major cities in the US"
    },
    "Oklahoma City": {
        "state": "Oklahoma",
        "context": "a city that has invested heavily in parks and outdoor recreation through its MAPS civic improvement program",
        "climate": "hot, humid southern plains summers with frequent triple-digit temperatures from June through August"
    },
    "Tucson": {
        "state": "Arizona",
        "context": "a desert university city where shaded parks and splash pads provide critical outdoor relief during intense summer heat",
        "climate": "extreme desert heat with summer temperatures above 100°F and monsoon humidity arriving in July"
    },
    "Atlanta": {
        "state": "Georgia",
        "context": "a sprawling metro spread across a large geographic footprint, with splash pads serving diverse neighborhoods from Buckhead to East Atlanta Village",
        "climate": "hot, humid subtropical summers with July averages in the upper 80s°F and high humidity"
    },
    "Miami": {
        "state": "Florida",
        "context": "a subtropical city where water-based recreation is embedded in the local culture year-round, not just during summer",
        "climate": "year-round tropical heat and humidity with summer temperatures in the low 90s°F and frequent afternoon thunderstorms"
    },
    "Minneapolis": {
        "state": "Minnesota",
        "context": "a city consistently ranked as having one of the best-maintained urban park systems in the country, with strong community investment in outdoor recreation",
        "climate": "short but warm summers eagerly enjoyed after harsh winters, with July temperatures in the upper 80s°F"
    },
    "Tampa": {
        "state": "Florida",
        "context": "a Gulf Coast city where outdoor recreation culture is strong year-round, supported by warm weather and proximity to water",
        "climate": "hot, humid subtropical summers with daily temperatures in the low 90s°F and afternoon thunderstorms from June through September"
    },
    "New Orleans": {
        "state": "Louisiana",
        "context": "a city where neighborhood identity and community culture run deep, with parks and recreation serving as gathering spaces in every district",
        "climate": "intense subtropical heat and humidity with summers among the most challenging in the country — heat indexes routinely above 110°F"
    },
    "Cleveland": {
        "state": "Ohio",
        "context": "a Lake Erie city with an extensive parks system and community recreation infrastructure serving many distinct neighborhoods",
        "climate": "warm, humid Great Lakes summers with July temperatures in the mid-to-upper 80s°F"
    },
    "Kansas City": {
        "state": "Missouri",
        "context": "a city that straddles the Kansas-Missouri border with strong community park investment on both sides of the state line",
        "climate": "hot, humid Midwest summers with July temperatures averaging in the upper 80s°F and frequent heat waves"
    },
    "Virginia Beach": {
        "state": "Virginia",
        "context": "a coastal city where outdoor recreation culture is strong and water play facilities serve a large residential population beyond the tourist corridor",
        "climate": "hot, humid mid-Atlantic summers with ocean breezes tempering temperatures in the upper 80s°F"
    },
    "Raleigh": {
        "state": "North Carolina",
        "context": "a fast-growing Research Triangle city that has expanded its parks and recreation infrastructure alongside rapid population growth",
        "climate": "hot, humid Piedmont summers with July averages in the upper 80s°F and high heat index values"
    },
    "Colorado Springs": {
        "state": "Colorado",
        "context": "a city at the foot of Pikes Peak with an outdoor-oriented culture and access to both urban parks and nearby natural landscapes",
        "climate": "warm, dry mountain summers with lower humidity than the national average and frequent afternoon thunderstorms"
    },
    "Omaha": {
        "state": "Nebraska",
        "context": "a mid-sized Midwest city with a robust parks system and strong community investment in family recreation facilities",
        "climate": "hot, humid Great Plains summers with temperatures in the upper 80s to mid-90s°F from June through August"
    },
    "Long Beach": {
        "state": "California",
        "context": "a diverse Southern California coastal city where outdoor recreation infrastructure serves a dense and varied residential population",
        "climate": "mild, consistent Southern California summers with ocean influence keeping coastal temperatures in the 70-80s°F"
    },
    "Sacramento": {
        "state": "California",
        "context": "California's capital city, set in the Central Valley where summer heat rivals Phoenix and water play becomes essential for families",
        "climate": "intense valley heat with July temperatures regularly above 95°F and periods above 105°F"
    },
    "Fresno": {
        "state": "California",
        "context": "a Central Valley city where summer heat is among the most intense in California, making water play facilities a genuine public benefit",
        "climate": "extreme summer heat in the Central Valley with temperatures frequently above 100°F from June through August"
    },
    "Mesa": {
        "state": "Arizona",
        "context": "a large Phoenix suburb with extensive parks and recreation investment serving one of Arizona's largest cities",
        "climate": "extreme desert heat identical to Phoenix, with summer temperatures routinely above 105°F"
    },
    "Albuquerque": {
        "state": "New Mexico",
        "context": "a high-desert city where outdoor recreation thrives in the dry summer heat, with parks serving as important community spaces",
        "climate": "hot, dry summers at 5,300 feet with low humidity and July temperatures in the low 90s°F"
    },
    "Wichita": {
        "state": "Kansas",
        "context": "Kansas's largest city with a growing parks system and community recreation infrastructure that serves a broad regional population",
        "climate": "hot, humid southern plains summers with July averages in the upper 80s°F and frequent heat advisories"
    },
    "Arlington": {
        "state": "Texas",
        "context": "a DFW suburb and major entertainment hub with parks and recreation facilities serving a large residential community beyond its sports venues",
        "climate": "intense North Texas heat with summer temperatures regularly above 95-100°F from June through August"
    },
    "Bakersfield": {
        "state": "California",
        "context": "a Central Valley city known for intense summer heat where splash pads and water parks serve as important community relief facilities",
        "climate": "extreme valley heat with July averages above 97°F and frequent stretches above 105°F"
    },
    "Aurora": {
        "state": "Colorado",
        "context": "Denver's largest suburb with a well-developed parks system and recreation facilities serving a diverse and growing community",
        "climate": "warm, sunny Colorado summers with lower humidity and July temperatures in the mid-to-upper 80s°F"
    },
    "Anaheim": {
        "state": "California",
        "context": "an Orange County city where local families live year-round in an area better known for tourism, with community parks serving residential neighborhoods",
        "climate": "warm Southern California summers with inland temperatures rising into the 90s°F away from the coast"
    },
    "Henderson": {
        "state": "Nevada",
        "context": "Las Vegas's large neighboring suburb with strong parks and recreation investment serving a fast-growing residential population",
        "climate": "extreme desert heat matching Las Vegas, with summer temperatures above 105-110°F"
    },
    "Chandler": {
        "state": "Arizona",
        "context": "a Phoenix suburb that has invested heavily in parks and recreation as part of a broader livability strategy for its growing population",
        "climate": "extreme desert heat in the greater Phoenix area with July temperatures above 105°F"
    },
    "Scottsdale": {
        "state": "Arizona",
        "context": "an upscale Phoenix suburb known for high-quality parks and recreation facilities alongside its resort and arts culture",
        "climate": "intense Sonoran Desert heat with summer temperatures regularly above 105°F"
    },
}

# ── Prompt builder ────────────────────────────────────────────────────────────

def build_prompt(pad: dict, city_context: dict) -> str:
    features = ", ".join(pad.get("features", [])) or "not specified"
    age_range = ", ".join(pad.get("age_range", [])) or "all ages"
    admission = pad.get("admission", "") or "not specified"
    pad_type = pad.get("type", "Splash Pad")
    season = pad.get("season", "") or "seasonal"
    hours = pad.get("hours", "") or "not specified"
    rating = pad.get("rating", "")
    review_count = pad.get("review_count", "")

    rating_info = ""
    if rating and float(rating) >= 4.0:
        rating_info = f"\nGoogle Rating: {rating} stars"
        if review_count:
            rating_info += f" ({review_count} reviews)"

    return (
        f"Write a 3-5 sentence description for a water play facility listing on a directory website.\n\n"
        f"REQUIREMENTS:\n"
        f"- Be specific to this exact facility and city — do not use generic filler\n"
        f"- Reference the city's character, climate, or community context naturally\n"
        f"- Vary sentence structure; do not start with '[Name] is a...'\n"
        f"- Do NOT invent specific facts (hours, prices, addresses) not provided below\n"
        f"- Do NOT use filler phrases like 'nestled', 'boasting', 'conveniently located'\n"
        f"- Include practical visitor information where available\n"
        f"- Write in third person, present tense\n"
        f"- Output only the description text — no headers, no quotes\n\n"
        f"FACILITY DATA:\n"
        f"Name: {pad['name']}\n"
        f"City: {pad['city']}, {pad['state']}\n"
        f"Type: {pad_type}\n"
        f"Admission: {admission}\n"
        f"Season: {season}\n"
        f"Hours: {hours}\n"
        f"Features/Amenities: {features}\n"
        f"Age Range: {age_range}"
        f"{rating_info}\n\n"
        f"CITY CONTEXT (use naturally, not verbatim):\n"
        f"City character: {city_context['context']}\n"
        f"Summer climate: {city_context['climate']}"
    )


# ── AI call ───────────────────────────────────────────────────────────────────

def generate_ai_description(pad: dict, city_context: dict, client) -> str:
    prompt = build_prompt(pad, city_context)
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate AI descriptions for top-metro pads")
    parser.add_argument("--apply", action="store_true", help="Write descriptions to Airtable")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of AI calls (0 = no limit)")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing descriptions (default: only fill missing/thin)")
    args = parser.parse_args()

    dry_run = not args.apply

    if not dry_run:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: ANTHROPIC_API_KEY not set in .env")
            return
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            print("Error: anthropic package not installed. Run: pip install anthropic")
            return
    else:
        client = None

    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, TABLE_NAME)

    print("Fetching records from Airtable...")
    records = table.all()
    print(f"Fetched {len(records)} total records.\n")

    # ── Find metro pads ───────────────────────────────────────────────────
    target_records = []
    for rec in records:
        fields = rec.get("fields", {})
        city = fields.get("City", "").strip()
        state = fields.get("State", "").strip()

        if city not in TOP_METRO_CITIES:
            continue
        city_def = TOP_METRO_CITIES[city]
        if city_def["state"] != state:
            continue  # guard against same city name in different states

        desc = str(fields.get("Description", "")).strip()
        if not args.overwrite and desc and len(desc) >= 200:
            continue  # skip pads that already have a good-length description

        target_records.append({
            "id": rec["id"],
            "city": city,
            "city_context": city_def,
            "pad": {
                "name": fields.get("Name", ""),
                "city": city,
                "state": state,
                "type": fields.get("Type", "Splash Pad"),
                "admission": fields.get("Admission", ""),
                "features": fields.get("Features", []),
                "age_range": fields.get("Age Range", []),
                "rating": fields.get("Rating", 0),
                "review_count": fields.get("Review Count", 0),
                "season": fields.get("Season", ""),
                "hours": fields.get("Hours", ""),
            },
            "current_desc": desc,
        })

    print(f"Metro pads needing descriptions: {len(target_records)}")

    # City breakdown
    city_counts = {}
    for r in target_records:
        city_counts[r["city"]] = city_counts.get(r["city"], 0) + 1
    for city, count in sorted(city_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {city}: {count}")

    if args.limit and len(target_records) > args.limit:
        print(f"\nLimiting to {args.limit} records (--limit flag).")
        target_records = target_records[:args.limit]

    if dry_run:
        print(f"\nDRY RUN — showing sample prompts for first 3 records:\n")
        for r in target_records[:3]:
            print(f"{'─'*60}")
            print(f"Pad: {r['pad']['name']} | {r['city']}, {r['pad']['state']}")
            print(f"Current desc ({len(r['current_desc'])} chars): {r['current_desc'][:100]}")
            print(f"\nPrompt preview:\n{build_prompt(r['pad'], r['city_context'])[:400]}...")
            print()
        est_cost = len(target_records) * 0.004
        print(f"{'='*60}")
        print(f"Would process {len(target_records)} pads.")
        print(f"Estimated cost: ~${est_cost:.2f}")
        print(f"\nRe-run with --apply to generate and write descriptions.")
        return

    # ── Generate and write ────────────────────────────────────────────────
    updates = []
    errors = 0

    print(f"\nGenerating descriptions for {len(target_records)} metro pads...\n")

    for i, r in enumerate(target_records):
        try:
            desc = generate_ai_description(r["pad"], r["city_context"], client)
            updates.append({
                "id": r["id"],
                "fields": {"Description": desc},
                "name": r["pad"]["name"],
                "city": r["city"],
            })
            print(f"  [{i+1}/{len(target_records)}] {r['pad']['name'][:45]} ({r['city']})")
            print(f"    {desc[:110]}...")
            time.sleep(0.3)  # gentle rate limiting
        except Exception as e:
            print(f"  [{i+1}/{len(target_records)}] ERROR — {r['pad']['name']}: {e}")
            errors += 1

    print(f"\nWriting {len(updates)} descriptions to Airtable...")
    batch = [{"id": u["id"], "fields": u["fields"]} for u in updates]
    for i in range(0, len(batch), CHUNK_SIZE):
        table.batch_update(batch[i:i + CHUNK_SIZE])
        print(f"  Updated {min(i + CHUNK_SIZE, len(batch))}/{len(batch)}...")

    print(f"\nDone! {len(updates)} metro descriptions written.")
    if errors:
        print(f"  ({errors} errors — re-run to retry)")
    print("Run python3 build.py to rebuild the site.")


if __name__ == "__main__":
    main()
