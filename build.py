#!/usr/bin/env python3
"""
Splash Pad Finder - Static Site Generator

Fetches splash pad listings from Airtable and generates a static HTML site.
Falls back to sample data if Airtable is not configured.
"""
import hashlib
import csv
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

import requests
import markdown as md_lib
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup
from slugify import slugify

import config


# Sentence patterns that present third-party (Google) ratings as first-party signal,
# or that read as AI boilerplate. Stripped from descriptions at fetch time so the
# rating claim never reaches the rendered page or the JSON-LD body.
RATING_CLAIM_PATTERNS = [
    re.compile(r"\bvisitors?\s+have\s+rated[\s\S]{0,240}?\d+\.?\d*\s+out of 5 stars? on Google(?: based on \d[\d,]* reviews?)?\.", re.I),
    re.compile(r"\b(?:the\s+)?facility\s+has\s+earned[\s\S]{0,180}?\d+\.?\d*[\s\-]?star\s+rating[\s\S]{0,120}?\.", re.I),
    re.compile(r"\bwith\s+(?:a|an)?\s*\d+\.?\d*[\s\-]?star\s+Google\s+rating[\s\S]{0,160}?\.", re.I),
    re.compile(r"[^.]*?\bvisitors?\b[^.]*?\b\d+\.?\d*\s*stars?\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\bvisitors?\s+have\s+rated\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\brated\b[^.]*?\bout of 5 stars?\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\b\d+\.?\d*\b[^.]*?\bGoogle\s+(?:rating|reviews?)\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\bGoogle\s+(?:rating|reviews?)\b[^.]*?\b\d+\.?\d*\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\bearned\s+(?:a|an)?\s*\d+\.?\d*[\s\-]?star\s+rating[^.]*\.", re.I),
    re.compile(r"[^.]*?\bmaintain(?:ing|s|ed)?\s+(?:a|an)?\s*\d+\.?\d*[\s\-]?star\s+rating[^.]*\.", re.I),
    re.compile(r"[^.]*?(?:with|holds?|carries|achieved)\s+(?:a|an)?\s*\d+\.?\d*[\s\-]?star\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\b\d+\.?\d*[\s\-]?star ratings?\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\bstars?\s+based\s+on\s+\d[\d,]*\s+reviews?\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\bbased\s+on\s+\d[\d,]*\s+reviews?\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\bfrom\s+(?:over\s+)?\d[\d,]*\s+(?:visitors?|reviews?)\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\b(?:highest|top|best)-rated\b[^.]*?\b\d+\.?\d*\s*stars?\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\bat\s+\d+\.?\d*\s+stars?\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\b(?:reflecting|reflects)\s+the\s+positive\s+experiences[^.]*\.", re.I),
    re.compile(r"[^.]*?\bconsistently\s+rate(?:d|s)?\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\bwell\s+regarded\s+by\s+the\s+local\s+community\b[^.]*\.", re.I),
    re.compile(r"[^.]*?\bsuggest\s+families\s+consistently\s+enjoy[^.]*\.", re.I),
    re.compile(r"[^.]*?\bstrong\s+Google\s+reviews\b[^.]*\.", re.I),
]

RATING_FRAGMENT_PATTERNS = [
    # Decimal-point sentence stripping can leave fragments such as
    # "5 out of 5 stars on Google" behind. Remove those fragments directly.
    re.compile(r"\s*(?:[A-Z][\w'&()/\-]*\s+){0,8}\d+\.?\d*\s+out of 5 stars? on Google(?: based on \d[\d,]* reviews?)?\.", re.I),
    re.compile(r"\s*(?:[A-Z][\w'&()/\-]*\s+){0,8}\d+\.?\d*[\s\-]?star\s+Google\s+rating[^.]*\.", re.I),
    re.compile(r"\s*\d+\.?\d*\s+stars?\s+by\s+(?:hundreds|thousands|\d[\d,]*)[^.]*\.", re.I),
]

RATING_FIELD_PATTERNS = [
    re.compile(r"\s*\|\s*\*\*Rating:\*\*\s*\d+\.?\d*", re.I),
    re.compile(r"\*\*Rating:\*\*\s*\d+\.?\d*\s*\|\s*", re.I),
    re.compile(r"\*\*Rating:\*\*\s*\d+\.?\d*", re.I),
    re.compile(r"\s*\|\s*Rating:\s*\d+\.?\d*", re.I),
    re.compile(r"Rating:\s*\d+\.?\d*\s*\|\s*", re.I),
    re.compile(r"Rating:\s*\d+\.?\d*", re.I),
]

RATING_SENTENCE_PATTERNS = [
    re.compile(r"\b(?:The|A|An)\s+(?:perfect\s+)?\d+\.?\d*\s+rating\b[^.!?\n]{0,220}[.!?]", re.I),
    re.compile(r"\b(?:Free admission|Full amenities|Accessible design|The walkable location)\s+and\s+a\s+\d+\.?\d*\s+rating\b[^.!?\n]{0,220}[.!?]", re.I),
    re.compile(r"\b(?:Both|They|It|This facility)\s+earn(?:s)?\s+(?:identical\s+)?\d+\.?\d*\s+ratings?\b[^.!?\n]{0,180}[.!?]", re.I),
    re.compile(r"\b[A-Z][^.!?\n]{0,120}?\bearns?\s+a\s+\d+\.?\d*\s+rating\b[^.!?\n]{0,180}[.!?]", re.I),
    re.compile(r"\b(?:One of the|The)\s+(?:highest|top|best|well|highly)-rated\b[^.!?\n]{0,220}[.!?]", re.I),
    re.compile(r"\b(?:The\s+)?\d+\.?\d*\s+rating\s+(?:reflects|makes|serves)\b[^.!?\n]{0,220}[.!?]", re.I),
]


def clean_description(text):
    """Strip rating-claim sentences and AI-boilerplate from a description.

    The rating values themselves come from Google Places and were embedded in
    descriptions during enrichment. Presenting them in body copy alongside
    structured-data is a Google rating-snippet policy violation when no on-site
    reviews exist. We strip whole sentences rather than substitute, so the
    surrounding prose stays grammatical.
    """
    if not text:
        return text
    cleaned = text
    for pattern in RATING_FIELD_PATTERNS:
        cleaned = pattern.sub("", cleaned)
    cleaned = re.sub(r"\s+\|\s+\|", " | ", cleaned)
    cleaned = re.sub(r"\|\s*(?=\n|$|---|###)", "", cleaned)
    for pattern in RATING_CLAIM_PATTERNS:
        cleaned = pattern.sub("", cleaned)
    for pattern in RATING_FRAGMENT_PATTERNS:
        cleaned = pattern.sub("", cleaned)
    for pattern in RATING_SENTENCE_PATTERNS:
        cleaned = pattern.sub("", cleaned)
    cleaned = re.sub(r"\b\d+\.?\d*[\s-]?rated\s+", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*,?\s*and\s+(?:well|highly|top|best|highest)-rated\b", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\b(?:well|highly|top|best|highest)-rated\b\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*,?\s*(?:and\s+)?rated\s+\d+\.?\d*\.?", ".", cleaned, flags=re.I)
    # Collapse the double-spaces and orphaned spaces that strip-by-sentence leaves behind.
    cleaned = re.sub(r"\s+([,.;:!?])", r"\1", cleaned)
    cleaned = re.sub(r"([.!?])(?=[A-Z])", r"\1 ", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned


def normalize_url(url):
    """De-mangle double-encoded website URLs coming from Airtable.

    Some 'Website URL' values (chiefly auto-generated Google Business Profile
    booking/UTM links) had their entire query string percent-encoded into the
    path: '?a=b&c=d' was stored as '%3Fa%3Db%26c%3Dd'. The server then sees a
    garbage literal path and returns 403/404, breaking the outbound link.

    We act only when an encoded '?' (%3F) is present — the unambiguous signature
    that a whole query string was encoded — then decode the query delimiters.
    Gating on %3F avoids touching legitimately-encoded path segments (e.g. a
    bare %2B in a store-locator path). Validated against 248 known-mangled URLs:
    reproduces the HTTP-verified clean URL in every case.
    """
    if not url or not isinstance(url, str):
        return url or ""
    u = url.strip()
    if "%3f" not in u.lower():
        return u
    # %26amp; (HTML-entity-then-encode double-mangle) must be undone before %26.
    u = u.replace("%26amp;", "&").replace("%26", "&")
    u = u.replace("%3F", "?").replace("%3f", "?")
    u = u.replace("%3D", "=").replace("%3d", "=")
    return u


def generate_pad_faq(pad):
    """Generate 2-3 FAQ Q&A pairs from a pad's existing data fields.

    Used as a fallback when no custom FAQ is stored in Airtable. Returns a list
    of {"q": "...", "a": "..."} dicts. Only generates questions for which a
    meaningful answer can be derived from the available data.
    """
    name = pad.get("name", "this splash pad")
    faqs = []

    # Admission / cost question
    admission = pad.get("admission", "")
    price = pad.get("price", "")
    if admission == "Free":
        faqs.append({
            "q": f"Is {name} free?",
            "a": f"Yes, {name} is free and open to the public. No admission fee is required.",
        })
    elif admission == "Paid" and price:
        faqs.append({
            "q": f"How much does {name} cost?",
            "a": f"Admission to {name} is {price}.",
        })
    elif admission:
        faqs.append({
            "q": f"Is there an admission fee at {name}?",
            "a": f"Admission is listed as {admission}. Check the official website or call ahead to confirm current pricing.",
        })

    # Hours question
    hours = pad.get("hours", "")
    if hours:
        faqs.append({
            "q": f"What are the hours at {name}?",
            "a": f"{name} is open {hours}. Hours may vary on holidays — call ahead or check the official website to confirm.",
        })

    # Season question
    season = pad.get("season", "")
    if season and season.lower() not in ("year-round", "year round"):
        faqs.append({
            "q": f"What season is {name} open?",
            "a": f"{name} is typically open {season}. Opening and closing dates may shift slightly by year depending on weather.",
        })

    # Age range question
    age_range = pad.get("age_range", [])
    if age_range:
        ages = ", ".join(age_range)
        faqs.append({
            "q": f"What age groups is {name} suitable for?",
            "a": f"{name} is suitable for {ages}.",
        })

    # Accessibility question
    features = pad.get("features", [])
    if "Accessibility" in features:
        faqs.append({
            "q": f"Is {name} accessible for guests with disabilities?",
            "a": f"Yes, {name} includes accessible water features designed for guests of all abilities.",
        })

    # Return up to 3 FAQs
    return faqs[:3]


def get_sample_data():
    """Return sample splash pads for testing without Airtable."""
    return [
        {
            "name": "Centennial Park Splash Pad",
            "slug": "centennial-park-splash-pad",
            "description": "A large, free splash pad featuring over 20 water jets, spray arches, and dumping buckets. "
                           "Perfect for kids of all ages. Open Memorial Day through Labor Day.",
            "address": "123 Main St",
            "city": "Nashville",
            "state": "Tennessee",
            "state_slug": "tennessee",
            "zip": "37201",
            "phone": "(615) 555-0100",
            "website_url": "",
            "google_maps_url": "",
            "photo_url": "",
            "hours": "Mon-Sun: 9am - 8pm (Memorial Day - Labor Day)",
            "admission": "Free",
            "price": "$0",
            "age_range": ["Toddlers", "Kids", "All Ages"],
            "features": ["Restrooms", "Shade", "Parking", "Picnic Area", "Playground"],
            "type": "Splash Pad",
            "season": "Memorial Day - Labor Day",
            "status": "Active",
            "date_added": "2025-01-01",
            "rating": 4.7,
            "review_count": 128,
            "faq": [],
            "last_verified": "",
            "latitude": 36.1627,
            "longitude": -86.7816,
        },
        {
            "name": "Riverside Water Park",
            "slug": "riverside-water-park",
            "description": "Indoor water play area open year-round. Features a zero-depth splash zone ideal for toddlers "
                           "and a larger spray area for older kids. Admission required.",
            "address": "456 River Rd",
            "city": "Austin",
            "state": "Texas",
            "state_slug": "texas",
            "zip": "78701",
            "phone": "(512) 555-0200",
            "website_url": "",
            "google_maps_url": "",
            "photo_url": "",
            "hours": "Mon-Fri: 10am - 6pm, Sat-Sun: 9am - 7pm",
            "admission": "Paid",
            "price": "$8 adults / $5 children",
            "age_range": ["Toddlers", "Kids", "Families"],
            "features": ["Restrooms", "Parking", "Snack Bar", "Accessibility"],
            "type": "Indoor Water Play",
            "season": "Year-Round",
            "status": "Active",
            "date_added": "2025-01-02",
            "rating": 4.5,
            "review_count": 89,
            "faq": [],
            "last_verified": "",
            "latitude": 30.2672,
            "longitude": -97.7431,
        },
        {
            "name": "Maple Grove Spray Park",
            "slug": "maple-grove-spray-park",
            "description": "Community spray park with ADA accessible water features. Low-intensity water jets make "
                           "this ideal for toddlers and children with sensory sensitivities.",
            "address": "789 Oak Ave",
            "city": "Chicago",
            "state": "Illinois",
            "state_slug": "illinois",
            "zip": "60601",
            "phone": "(312) 555-0300",
            "website_url": "",
            "google_maps_url": "",
            "photo_url": "",
            "hours": "Daily: 10am - 7pm (June - August)",
            "admission": "Free",
            "price": "$0",
            "age_range": ["Toddlers", "Kids"],
            "features": ["Restrooms", "Shade", "Accessibility", "Picnic Area"],
            "type": "Spray Park",
            "season": "June - August",
            "status": "Active",
            "date_added": "2025-01-03",
            "rating": 4.3,
            "review_count": 56,
            "faq": [],
            "last_verified": "",
            "latitude": 41.8781,
            "longitude": -87.6298,
        },
    ]


def fetch_from_airtable():
    """Fetch splash pads from Airtable API."""
    if not config.AIRTABLE_API_KEY or not config.AIRTABLE_BASE_ID:
        print("Airtable not configured. Using sample data.")
        return None

    try:
        from pyairtable import Api

        api = Api(config.AIRTABLE_API_KEY)
        table = api.table(config.AIRTABLE_BASE_ID, config.AIRTABLE_TABLE_NAME)
        records = table.all()

        pads = []
        for record in records:
            fields = record.get("fields", {})

            # Skip drafts
            if fields.get("Status") == "Draft":
                continue

            # Skip off-topic listings (theme parks, water parks, aquatic centers)
            OFF_TOPIC_PREFIXES = (
                "Six Flags", "Great Wolf Lodge", "Kings Island",
                "Kings Dominion", "Kroger Aquatic Center", "Rivertown",
            )
            if any(fields.get("Name", "").startswith(p) for p in OFF_TOPIC_PREFIXES):
                continue

            state_name = fields.get("State", "")
            # Parse FAQ: stored in Airtable as a JSON array [{"q":"...","a":"..."}]
            # or as newline-separated "Q: ...\nA: ..." blocks.
            raw_faq = fields.get("FAQ", "")
            custom_faq = []
            if raw_faq:
                try:
                    custom_faq = json.loads(raw_faq)
                except (json.JSONDecodeError, TypeError):
                    # Parse "Q: ...\nA: ..." plain-text format
                    lines = [l.strip() for l in raw_faq.strip().splitlines() if l.strip()]
                    current_q = None
                    for line in lines:
                        if line.startswith("Q:"):
                            current_q = line[2:].strip()
                        elif line.startswith("A:") and current_q:
                            custom_faq.append({"q": current_q, "a": line[2:].strip()})
                            current_q = None

            pad = {
                "_airtable_id": record.get("id", ""),
                "name": fields.get("Name", ""),
                "slug": slugify(fields.get("Name", "") + "-" + fields.get("City", "")),
                "description": clean_description(fields.get("Description", "")),
                "address": fields.get("Address", ""),
                "city": fields.get("City", ""),
                "state": state_name,
                "state_slug": slugify(state_name),
                "zip": fields.get("Zip", ""),
                "phone": fields.get("Phone", ""),
                "website_url": normalize_url(fields.get("Website URL", "")),
                "google_maps_url": fields.get("Google Maps URL", ""),
                "photo_url": fields.get("Photo URL", ""),
                "hours": fields.get("Hours", ""),
                "admission": fields.get("Admission", ""),
                "price": fields.get("Price", ""),
                "age_range": fields.get("Age Range", []),
                "features": fields.get("Features", []),
                "type": fields.get("Type", "Splash Pad"),
                "season": fields.get("Season", ""),
                "status": fields.get("Status", "Active"),
                "featured": fields.get("Featured", False),
                "date_added": fields.get("Date Added", ""),
                "rating": fields.get("Rating", 0),
                "review_count": fields.get("Review Count", 0),
                "latitude": fields.get("Latitude", ""),
                "longitude": fields.get("Longitude", ""),
                "faq": custom_faq,
                "last_verified": fields.get("Last Verified", ""),
            }
            pads.append(pad)

        print(f"Fetched {len(pads)} splash pads from Airtable.")
        return pads

    except Exception as e:
        print(f"Error fetching from Airtable: {e}")
        return None


def clear_airtable_photo_url(airtable_id):
    """Clear the Photo URL field in Airtable for a pad with an expired URL.

    This prevents future builds from repeatedly attempting expired Google Places URLs.
    Only runs when AIRTABLE_API_KEY and AIRTABLE_BASE_ID are configured.
    """
    if not config.AIRTABLE_API_KEY or not config.AIRTABLE_BASE_ID or not airtable_id:
        return
    try:
        from pyairtable import Api
        api = Api(config.AIRTABLE_API_KEY)
        table = api.table(config.AIRTABLE_BASE_ID, config.AIRTABLE_TABLE_NAME)
        table.update(airtable_id, {"Photo URL": ""})
    except Exception as e:
        print(f"  Warning: could not clear Airtable photo_url for {airtable_id}: {e}")


def load_pads_from_csv(path=None):
    """Load splash pads from the committed CSV export (data/pads.csv) — the
    post-Airtable data source. Mirrors fetch_from_airtable()'s record mapping
    exactly so both paths produce identical pad dicts; returns None when the
    file is absent so the Airtable fallback can take over."""
    path = Path(path) if path else config.PADS_CSV
    if not path or not path.exists():
        return None
    OFF_TOPIC_PREFIXES = (
        "Six Flags", "Great Wolf Lodge", "Kings Island",
        "Kings Dominion", "Kroger Aquatic Center", "Rivertown",
    )

    def _iso_date(v):
        # Airtable CSV exports dates US-style ("3/1/2026"); the API returns ISO
        # ("2026-03-01"). Normalize so both paths hash and render identically.
        try:
            from datetime import datetime as _dt
            return _dt.strptime(str(v).strip(), "%m/%d/%Y").strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return v

    def num(v):
        try:
            f = float(v)
            return int(f) if f.is_integer() else f
        except (TypeError, ValueError):
            return v

    pads = []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            fields = {k: v for k, v in row.items()
                      if k and v is not None and str(v).strip() != ""}
            if fields.get("Status") == "Draft":
                continue
            if any(fields.get("Name", "").startswith(p) for p in OFF_TOPIC_PREFIXES):
                continue
            state_name = fields.get("State", "")
            raw_faq = fields.get("FAQ", "")
            custom_faq = []
            if raw_faq:
                try:
                    custom_faq = json.loads(raw_faq)
                except (json.JSONDecodeError, TypeError):
                    lines = [l.strip() for l in raw_faq.strip().splitlines() if l.strip()]
                    current_q = None
                    for line in lines:
                        if line.startswith("Q:"):
                            current_q = line[2:].strip()
                        elif line.startswith("A:") and current_q:
                            custom_faq.append({"q": current_q, "a": line[2:].strip()})
                            current_q = None
            pads.append({
                "_airtable_id": "",
                "name": fields.get("Name", ""),
                "slug": slugify(fields.get("Name", "") + "-" + fields.get("City", "")),
                "description": clean_description(fields.get("Description", "")),
                "address": fields.get("Address", ""),
                "city": fields.get("City", ""),
                "state": state_name,
                "state_slug": slugify(state_name),
                "zip": fields.get("Zip", ""),
                "phone": fields.get("Phone", ""),
                "website_url": normalize_url(fields.get("Website URL", "")),
                "google_maps_url": fields.get("Google Maps URL", ""),
                "photo_url": fields.get("Photo URL", ""),
                "hours": fields.get("Hours", ""),
                "admission": fields.get("Admission", ""),
                "price": fields.get("Price", ""),
                "age_range": [s.strip() for s in str(fields.get("Age Range", "")).split(",") if s.strip()],
                "features": [s.strip() for s in str(fields.get("Features", "")).split(",") if s.strip()],
                "type": fields.get("Type", "Splash Pad"),
                "season": fields.get("Season", ""),
                "status": fields.get("Status", "Active"),
                "featured": str(fields.get("Featured", "")).strip().lower() in ("true", "1", "yes", "checked"),
                "date_added": _iso_date(fields.get("Date Added", "")),
                "rating": num(fields.get("Rating", 0)),
                "review_count": num(fields.get("Review Count", 0)),
                "latitude": num(fields.get("Latitude", "")),
                "longitude": num(fields.get("Longitude", "")),
                "last_verified": fields.get("Last Verified", ""),
                "faq": custom_faq,
            })
    print(f"Loaded {len(pads)} splash pads from {path.name}.")
    return pads


def get_pads():
    """Get splash pads. Prefers the committed CSV (data/pads.csv) so the site
    builds with no Airtable dependency; falls back to Airtable, then samples."""
    pads = load_pads_from_csv()
    if pads:
        return pads
    pads = fetch_from_airtable()
    if not pads:
        pads = get_sample_data()
        print(f"Using {len(pads)} sample splash pads.")
    return pads


def _fetch_blog_posts_airtable():
    """Fetch published blog posts from the Airtable Blog Posts table."""
    if not config.AIRTABLE_API_KEY or not config.AIRTABLE_BASE_ID:
        return []

    try:
        from pyairtable import Api

        api = Api(config.AIRTABLE_API_KEY)
        table = api.table(config.AIRTABLE_BASE_ID, config.AIRTABLE_BLOG_TABLE_NAME)
        records = table.all()

        posts = []
        for record in records:
            fields = record.get("fields", {})

            if fields.get("Status") != "Published":
                continue

            title = fields.get("Title", "")
            post = {
                "title": title,
                "slug": (fields.get("Slug", "") or slugify(title)).strip(),
                "content": clean_description(fields.get("Content", "")),
                "excerpt": clean_description(fields.get("Excerpt", "")),
                # E-E-A-T remediation (2026-06): bylines are normalized at build
                # time to the organization-level editorial team, regardless of
                # the Airtable "Author" value. Airtable data is left untouched;
                # no individual personas are rendered as authors.
                "author": "Splash Pad Locator Editorial Team",
                "publish_date": fields.get("Publish Date", ""),
                "featured_image": fields.get("Featured Image", ""),
                "meta_description": clean_description(fields.get("Meta Description", "")),
                "status": fields.get("Status", "Published"),
                "featured": fields.get("Featured", False),
            }
            posts.append(post)

        posts.sort(key=lambda x: x.get("publish_date", ""), reverse=True)
        print(f"Fetched {len(posts)} blog posts from Airtable.")
        return posts

    except Exception as e:
        print(f"Note: Could not fetch blog posts ({e})")
        return []


def load_blog_posts_from_csv(path=None):
    """Blog fallback: load posts from the committed CSV export of the Airtable
    Blog Posts table so the blog still builds when Airtable is unavailable."""
    path = Path(path) if path else config.BLOG_POSTS_CSV
    if not path or not path.exists():
        return []
    posts = []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if (row.get("Status") or "").strip() != "Published":
                continue
            title = (row.get("Title") or "").strip()
            posts.append({
                "title": title,
                "slug": ((row.get("Slug") or "") or slugify(title)).strip(),
                "content": clean_description(row.get("Content", "") or ""),
                "excerpt": clean_description(row.get("Excerpt", "") or ""),
                "author": "Splash Pad Locator Editorial Team",
                "publish_date": row.get("Publish Date", "") or "",
                "featured_image": row.get("Featured Image", "") or "",
                "meta_description": clean_description(row.get("Meta Description", "") or ""),
                "status": "Published",
                "featured": str(row.get("Featured", "")).strip().lower() in ("true", "1", "yes", "checked"),
            })
    posts.sort(key=lambda x: x.get("publish_date", ""), reverse=True)
    return posts


def fetch_blog_posts():
    """Fetch blog posts: Airtable when available, else the committed CSV export."""
    posts = _fetch_blog_posts_airtable()
    if posts:
        return posts
    posts = load_blog_posts_from_csv()
    if posts:
        print(f"Loaded {len(posts)} blog posts from {config.BLOG_POSTS_CSV.name}.")
    return posts


def setup_output_directory():
    """Create clean output directory."""
    if config.OUTPUT_DIR.exists():
        shutil.rmtree(config.OUTPUT_DIR)

    config.OUTPUT_DIR.mkdir(parents=True)
    (config.OUTPUT_DIR / "state").mkdir()
    (config.OUTPUT_DIR / "pad").mkdir()
    (config.OUTPUT_DIR / "category").mkdir()
    (config.OUTPUT_DIR / "blog").mkdir()

    # Copy static files
    if config.STATIC_DIR.exists():
        shutil.copytree(config.STATIC_DIR, config.OUTPUT_DIR / "static")

    # Serve /favicon.ico at the site root (browsers and crawlers request that
    # path independently of any <link rel="icon"> tag).
    favicon_src = config.STATIC_DIR / "favicon.ico"
    if favicon_src.exists():
        shutil.copy2(favicon_src, config.OUTPUT_DIR / "favicon.ico")


def create_jinja_env():
    """Create Jinja2 environment with custom filters."""
    env = Environment(
        loader=FileSystemLoader(config.TEMPLATES_DIR),
        autoescape=True
    )

    def format_date(date_str):
        if not date_str:
            return ""
        try:
            dt = datetime.strptime(str(date_str)[:10], "%Y-%m-%d")
            return dt.strftime("%B ") + str(dt.day) + dt.strftime(", %Y")
        except (ValueError, TypeError):
            return date_str

    env.filters["slugify"] = slugify
    env.filters["tojson"] = lambda v: json.dumps(v, ensure_ascii=False)
    env.filters["markdown"] = lambda text: Markup(md_lib.markdown(text or "", extensions=["extra", "nl2br"]))
    env.filters["format_date"] = format_date

    env.globals["site_name"] = config.SITE_NAME
    env.globals["site_url"] = config.SITE_URL
    env.globals["site_description"] = config.SITE_DESCRIPTION
    env.globals["categories"] = config.CATEGORIES
    env.globals["us_states"] = config.US_STATES
    env.globals["current_year"] = datetime.now().year
    env.globals["ga_measurement_id"] = config.GA_MEASUREMENT_ID

    return env


def group_pads_by_state(pads):
    """Group pads by state slug."""
    grouped = {}
    for pad in pads:
        state_slug = pad.get("state_slug", "")
        if state_slug:
            grouped.setdefault(state_slug, []).append(pad)
    return grouped


def build_homepage(env, pads, posts):
    """Build the homepage."""
    template = env.get_template("index.html")
    protected_slugs = _load_protected_pad_slugs()
    indexable_pads = filter_indexable_pads(pads, protected_slugs)

    featured = [p for p in indexable_pads if p.get("featured")][:config.FEATURED_COUNT]
    if not featured:
        featured = indexable_pads[:config.FEATURED_COUNT]

    recent = sorted(indexable_pads, key=lambda x: x.get("date_added", ""), reverse=True)[:config.RECENT_COUNT]

    # Group by state for state browse section
    by_state = group_pads_by_state(indexable_pads)
    state_counts = {s: len(v) for s, v in by_state.items()}

    # Separate featured post (hero card) from recent posts grid
    featured_post = next((p for p in posts if p.get("featured")), None)
    recent_posts = [p for p in posts if p is not featured_post][:3]

    # Popular Cities — homepage internal links down to /city/ landing pages.
    # Mirror build_city_pages' indexable filter; only link non-thin (>=3 pad) cities.
    abbr_by_slug = {s["slug"]: s["abbr"] for s in config.US_STATES}
    popular_cities = []
    for state_slug, cities in config.CITY_PAGES.items():
        for city in cities:
            cname = city["name"].strip().lower()
            n = sum(
                1 for p in indexable_pads
                if p.get("state_slug") == state_slug
                and p.get("city", "").strip().lower() == cname
            )
            if n >= 3:
                popular_cities.append({
                    "name": city["name"],
                    "slug": city["slug"],
                    "abbr": abbr_by_slug.get(state_slug, ""),
                    "count": n,
                })
    popular_cities.sort(key=lambda c: (-c["count"], c["name"]))

    html = template.render(
        featured_pads=featured,
        recent_pads=recent,
        all_pads=indexable_pads,
        popular_cities=popular_cities,
        state_counts=state_counts,
        total_count=len(indexable_pads),
        posts=posts,
        featured_post=featured_post,
        recent_posts=recent_posts,
        page_title=config.DEFAULT_META_TITLE,
        meta_description=config.DEFAULT_META_DESCRIPTION,
        request_path="/",
    )

    output_path = config.OUTPUT_DIR / "index.html"
    output_path.write_text(html)
    print(f"Built: index.html ({len(indexable_pads)} indexable pads shown)")


def build_state_pages(env, pads):
    """Build one page per US state."""
    template = env.get_template("state.html")
    protected_slugs = _load_protected_pad_slugs()
    indexable_pads = filter_indexable_pads(pads, protected_slugs)
    grouped = group_pads_by_state(indexable_pads)

    MIN_PADS_FOR_INDEX = 5

    for state in config.US_STATES:
        state_pads = grouped.get(state["slug"], [])
        state_pads.sort(key=lambda x: x.get("city", ""))

        thin_state = len(state_pads) < MIN_PADS_FOR_INDEX

        city_pages = config.CITY_PAGES.get(state["slug"], [])

        html = template.render(
            state=state,
            pads=state_pads,
            city_pages=city_pages,
            page_title=f"Splash Pads in {state['name']} - {config.SITE_NAME}",
            meta_description=state.get("meta_description") or state["description"][:155],
            request_path=f"/state/{state['slug']}",
            noindex=thin_state,
            ads_allowed=not thin_state,
        )

        output_path = config.OUTPUT_DIR / "state" / f"{state['slug']}.html"
        output_path.write_text(html)
        print(f"Built: state/{state['slug']}.html ({len(state_pads)} pads)")


def build_city_pages(env, pads):
    """Build city-level landing pages defined in config.CITY_PAGES."""
    template = env.get_template("city.html")
    output_dir = config.OUTPUT_DIR / "city"
    output_dir.mkdir(parents=True, exist_ok=True)
    protected_slugs = _load_protected_pad_slugs()
    indexable_pads = filter_indexable_pads(pads, protected_slugs)
    min_city_pads_for_index = 3

    for state_slug, cities in config.CITY_PAGES.items():
        for city in cities:
            city_name_lower = city["name"].lower()
            city_pads = [
                p for p in indexable_pads
                if p.get("state_slug") == state_slug
                and p.get("city", "").strip().lower() == city_name_lower
            ]
            city_pads.sort(key=lambda x: x.get("name", ""))
            thin_city = len(city_pads) < min_city_pads_for_index

            # Sibling cities in the same state (excluding current)
            other_cities = [c for c in cities if c["slug"] != city["slug"]]

            html = template.render(
                city=city,
                pads=city_pads,
                other_cities=other_cities,
                page_title=f"Splash Pads in {city['name']}, {city['state']} - {config.SITE_NAME}",
                meta_description=city["meta_description"],
                request_path=f"/city/{city['slug']}",
                noindex=thin_city,
                ads_allowed=not thin_city,
            )

            output_path = output_dir / f"{city['slug']}.html"
            output_path.write_text(html)
            print(f"Built: city/{city['slug']}.html ({len(city_pads)} pads)")


_ARTIFACT_RE = re.compile("|".join(config.PAD_ARTIFACT_PATTERNS), re.I)

# The Phase-1 fallback composer's signature opener. Pads still carrying it are
# fact-stub pages (~80-120 words); evaluate_pad rule 4 noindexes them unless
# GSC-protected. See the 2026-07-18 fewer-but-richer decision.
_SKELETON_RE = re.compile(r"\bis a water play area in\b", re.I)
_OFF_TOPIC_NAME_RE = re.compile("|".join(config.PAD_OFF_TOPIC_NAME_PATTERNS), re.I)
_WATER_NAME_RE = re.compile("|".join(config.PAD_WATER_NAME_PATTERNS), re.I)


def hard_exclusion_reason(pad):
    """Return a reason when a listing should be removed from the built site."""
    slug = pad.get("slug", "")
    if slug in config.PAD_EXCLUDE_SLUGS:
        return config.PAD_EXCLUDE_SLUGS[slug]

    name = str(pad.get("name", "")).strip()
    off_topic_match = _OFF_TOPIC_NAME_RE.search(name)
    if off_topic_match and not _WATER_NAME_RE.search(name):
        return f"Off-topic name pattern: {off_topic_match.group(0)}"

    return None


def split_pads_for_build(pads):
    """Remove hard false positives before page generation."""
    kept = []
    dropped = []
    for pad in pads:
        reason = hard_exclusion_reason(pad)
        if reason:
            pad["_drop_reason"] = reason
            dropped.append(pad)
        else:
            kept.append(pad)

    if dropped:
        dropped_path = config.OUTPUT_DIR / "DROPPED_PADS.txt"
        with dropped_path.open("w") as f:
            f.write("# Hard-dropped false-positive listings\n")
            f.write(f"# Generated: {datetime.now().isoformat(timespec='seconds')}\n")
            f.write("# These records were not generated as pad pages and should be Drafted or deleted in Airtable.\n\n")
            f.write(f"Total dropped: {len(dropped)}\n\n")
            for pad in sorted(dropped, key=lambda p: (p.get("state", ""), p.get("name", ""))):
                f.write(
                    f"  /pad/{pad.get('slug', '')}\n"
                    f"    name: {pad.get('name', '')}\n"
                    f"    state: {pad.get('state', '')}\n"
                    f"    reason: {pad.get('_drop_reason', '')}\n\n"
                )

    print(f"Hard-dropped {len(dropped)} false-positive pads before build")
    return kept, dropped


def _load_protected_pad_slugs():
    """Read pad slugs that earned GSC traffic in the prior 28-day window.

    These slugs are excluded from auto-noindex actions; instead, candidate
    matches are written to dist/REVIEW_QUEUE.txt for manual triage. Re-derive
    the JSON when the next AdSense decision lands (event-based trigger, not
    calendar). Returns an empty set if the manifest is missing — fail-safe so
    a missing file never silently expands the noindex set.
    """
    path = config.BASE_DIR / "protected_urls.json"
    if not path.exists():
        print("WARNING: protected_urls.json missing — proceeding with empty protected set")
        return set()
    try:
        data = json.loads(path.read_text())
        return set(data.get("pad_slugs", []))
    except (json.JSONDecodeError, OSError) as e:
        print(f"WARNING: could not load protected_urls.json ({e}) — empty protected set")
        return set()


def evaluate_pad(pad, protected_slugs):
    """Decide whether a pad should be indexed and surface the reason.

    Returns one of:
      ("ok", None)                    — ship indexable
      ("noindex_phrase", phrase)      — AI artifact in description; auto-noindex
      ("noindex_type", type_val)      — venue type not in whitelist; auto-noindex
      ("noindex_thin", reason)        — description too short / placeholder
      ("noindex_manual", reason)      — listed in PAD_NOINDEX_SLUGS
      ("queued_phrase", phrase)       — would noindex by phrase, but slug is on
                                        the protected list; route to review queue
      ("queued_type", type_val)       — same, for type-whitelist failure

    The protected guardrail intentionally only catches *new* noindex actions
    (phrase / type / thin). Manual entries in PAD_NOINDEX_SLUGS bypass the
    guardrail because they were chosen with traffic data already in mind.
    """
    slug = pad.get("slug", "")

    if slug in config.PAD_NOINDEX_SLUGS:
        return ("noindex_manual", config.PAD_NOINDEX_SLUGS[slug])

    desc = str(pad.get("description", "")).strip()
    desc_lc = desc.lower()
    is_protected = slug in protected_slugs
    artifact_source = " ".join(
        str(pad.get(field, ""))
        for field in (
            "name",
            "description",
            "admission",
            "price",
            "hours",
            "website_url",
            "google_maps_url",
        )
    )

    # 1. Artifact phrases — strongest signal, cannot ship even if "protected".
    #    But per Kevin's rule: branded-traffic pages with bad text get queued
    #    for content-fix in Airtable rather than blanket auto-noindexed here.
    artifact_match = _ARTIFACT_RE.search(artifact_source)
    if artifact_match:
        return ("queued_phrase" if is_protected else "noindex_phrase", artifact_match.group(0))

    # 2. Description too thin or placeholder.
    if not desc or desc_lc in ("nan", ""):
        if is_protected:
            return ("queued_type", "(empty/nan description)")
        return ("noindex_thin", "(empty/nan description)")
    if len(desc) < config.MIN_DESCRIPTION_LENGTH:
        if is_protected:
            return ("queued_type", f"description {len(desc)} chars (< {config.MIN_DESCRIPTION_LENGTH})")
        return ("noindex_thin", f"description {len(desc)} chars (< {config.MIN_DESCRIPTION_LENGTH})")

    # 3. Venue-type whitelist.
    type_val = str(pad.get("type", "")).strip()
    if type_val not in config.PAD_TYPE_WHITELIST:
        return ("queued_type" if is_protected else "noindex_type", type_val or "(empty type)")

    # 4. Skeleton fallback opener (fewer-but-richer, post-rejection #3 2026-07-18).
    #    Descriptions still opening with the Phase-1 fact-stub frame are
    #    true-but-thin 80-120 word stubs; at ~28% of the index they are the
    #    "thin content" the AdSense rejections keep pointing at. Concentrate the
    #    index on substantial pages: noindex the stubs but keep them live for
    #    users and hub navigation. GSC-protected (trafficked) slugs stay
    #    indexed — real search traffic outranks composition purity.
    if _SKELETON_RE.search(desc) and not is_protected:
        return ("noindex_skeleton", "skeleton fallback description")

    return ("ok", None)


def is_thin_pad(pad, protected_slugs=None):
    """Backwards-compatible wrapper kept for any external callers.

    Returns True if the pad should NOT be indexed. New code should call
    evaluate_pad() directly to access the reason.
    """
    if protected_slugs is None:
        protected_slugs = _load_protected_pad_slugs()
    status, _ = evaluate_pad(pad, protected_slugs)
    return status != "ok"


def is_indexable_pad(pad, protected_slugs=None):
    """True only for pads that pass the AdSense quality gate outright."""
    if protected_slugs is None:
        protected_slugs = _load_protected_pad_slugs()
    status, _ = evaluate_pad(pad, protected_slugs)
    return status == "ok"


def filter_indexable_pads(pads, protected_slugs=None):
    """Return pads that can appear in sitemap, search, and listing surfaces."""
    if protected_slugs is None:
        protected_slugs = _load_protected_pad_slugs()
    return [p for p in pads if is_indexable_pad(p, protected_slugs)]


def build_pad_pages(env, pads):
    """Build individual splash pad detail pages.

    Each pad is evaluated against the AdSense-remediation gate:
      - manual override (PAD_NOINDEX_SLUGS) — auto-noindex
      - AI-artifact phrase in description — auto-noindex (or queue if protected)
      - description too short / empty — auto-noindex (or queue if protected)
      - venue type not in PAD_TYPE_WHITELIST — auto-noindex (or queue if protected)

    Pages on the protected URL list (clicks > 0 OR impressions > 5 in the most
    recent 28-day GSC window) are written to dist/REVIEW_QUEUE.txt for manual
    Airtable review. They are noindexed and ad-free until they pass the gate.
    """
    template = env.get_template("pad.html")
    protected_slugs = _load_protected_pad_slugs()
    indexable_pads = filter_indexable_pads(pads, protected_slugs)

    counts = {
        "ok": 0,
        "noindex_manual": 0,
        "noindex_phrase": 0,
        "noindex_thin": 0,
        "noindex_type": 0,
        "queued_phrase": 0,
        "queued_type": 0,
    }
    review_queue = []  # rows for REVIEW_QUEUE.txt

    for pad in pads:
        related = [
            p for p in indexable_pads
            if p["slug"] != pad["slug"] and p.get("state_slug") == pad.get("state_slug")
        ][:4]

        status, reason = evaluate_pad(pad, protected_slugs)
        counts[status] = counts.get(status, 0) + 1
        is_noindex = status != "ok"
        if status.startswith("queued_"):
            review_queue.append({
                "slug": pad["slug"],
                "name": pad.get("name", ""),
                "type": pad.get("type", ""),
                "status": status,
                "reason": reason,
            })

        faq = pad.get("faq") or generate_pad_faq(pad)

        html = template.render(
            pad=pad,
            faq=faq,
            related_pads=related,
            page_title=f"{pad['name']} - {pad['city']}, {pad['state']}",
            meta_description=pad.get("description", "")[:160],
            request_path=f"/pad/{pad['slug']}",
            noindex=is_noindex,
            ads_allowed=not is_noindex,
        )

        output_path = config.OUTPUT_DIR / "pad" / f"{pad['slug']}.html"
        output_path.write_text(html)

    total_noindex = sum(v for k, v in counts.items() if k.startswith("noindex_"))
    print(
        f"Built: {len(pads)} pad pages — "
        f"{counts['ok']} indexable, "
        f"{total_noindex} noindexed "
        f"(manual={counts['noindex_manual']}, phrase={counts['noindex_phrase']}, "
        f"thin={counts['noindex_thin']}, type={counts['noindex_type']}), "
        f"{counts['queued_phrase'] + counts['queued_type']} noindexed and queued for review"
    )

    # Persist review queue so Kevin can read it after each build.
    queue_path = config.OUTPUT_DIR / "REVIEW_QUEUE.txt"
    with queue_path.open("w") as f:
        f.write("# Pages flagged by AdSense remediation Batch 2 gate\n")
        f.write(f"# Generated: {datetime.now().isoformat(timespec='seconds')}\n")
        f.write("# These pads matched the artifact-phrase, thin-description, or\n")
        f.write("# venue-type filter, but their slug is on the protected URL list\n")
        f.write("# (clicks > 0 OR impressions > 5 in the prior 28 days). They are\n")
        f.write("# noindexed and ad-free until you fix/draft/delete them in Airtable.\n\n")
        f.write(f"Total queued: {len(review_queue)}\n\n")
        for row in sorted(review_queue, key=lambda r: (r["status"], r["slug"])):
            f.write(
                f"  [{row['status']}] /pad/{row['slug']}\n"
                f"    name: {row['name']}\n"
                f"    type: {row['type']}\n"
                f"    reason: {row['reason']}\n\n"
            )
    print(f"Built: REVIEW_QUEUE.txt ({len(review_queue)} pads to triage)")


def category_filter_map():
    return {
        "free-admission": lambda p: p.get("admission") == "Free",
        "toddlers": lambda p: "Toddlers" in p.get("age_range", []),
        "families": lambda p: "Families" in p.get("age_range", []) or "All Ages" in p.get("age_range", []),
        "with-shade": lambda p: "Shade" in p.get("features", []),
        "with-restrooms": lambda p: "Restrooms" in p.get("features", []),
        "with-picnic-areas": lambda p: "Picnic Area" in p.get("features", []),
        "indoor": lambda p: p.get("type") in ["Indoor Water Play", "Indoor Splash Pad"],
        "amusement-parks": lambda p: p.get("type") == "Amusement Park",
        "water-parks": lambda p: p.get("type") in ["Water Park", "Resort Water Park"],
        "accessible": lambda p: "Accessibility" in p.get("features", []),
    }


def pads_for_category(category, pads):
    filter_fn = category_filter_map().get(category["slug"], lambda p: True)
    return [p for p in pads if filter_fn(p)]


def build_category_pages(env, pads):
    """Build feature/filter category pages."""
    template = env.get_template("category.html")
    protected_slugs = _load_protected_pad_slugs()
    indexable_pads = filter_indexable_pads(pads, protected_slugs)

    for category in config.CATEGORIES:
        category_pads = pads_for_category(category, indexable_pads)
        is_empty = not category_pads

        # Build state list sorted by count desc for sidebar filter
        state_counts = {}
        for p in category_pads:
            s = p.get("state", "")
            if s:
                state_counts[s] = state_counts.get(s, 0) + 1
        state_list = sorted(state_counts.items(), key=lambda x: (-x[1], x[0]))

        html = template.render(
            category=category,
            pads=category_pads,
            state_list=state_list,
            page_title=f"{category.get('seo_title') or category['name'] + ' Splash Pads'} - {config.SITE_NAME}",
            meta_description=category["intro"][:155],
            request_path=f"/category/{category['slug']}",
            noindex=is_empty,
            ads_allowed=not is_empty,
        )

        output_path = config.OUTPUT_DIR / "category" / f"{category['slug']}.html"
        output_path.write_text(html)
        print(f"Built: category/{category['slug']}.html ({len(category_pads)} pads)")


def build_blog_page(env, posts):
    """Build the blog listing page."""
    template = env.get_template("blog.html")
    html = template.render(
        posts=posts,
        page_title=f"Blog - {config.SITE_NAME}",
        meta_description="Tips, guides, and articles to help families find and enjoy splash pads across America.",
        request_path="/blog",
    )
    output_path = config.OUTPUT_DIR / "blog.html"
    output_path.write_text(html)
    print(f"Built: blog.html ({len(posts)} posts)")


def build_post_pages(env, posts):
    """Build individual blog post pages."""
    template = env.get_template("post.html")

    for post in posts:
        if not post.get("slug"):
            continue
        overrides = config.BLOG_META_OVERRIDES.get(post["slug"], {})
        html = template.render(
            post=post,
            all_posts=posts,
            page_title=overrides.get("page_title") or f"{post['title']} - {config.SITE_NAME}",
            meta_description=overrides.get("meta_description") or post.get("meta_description") or post.get("excerpt", "")[:160],
            request_path=f"/blog/{post['slug']}",
        )
        output_path = config.OUTPUT_DIR / "blog" / f"{post['slug']}.html"
        output_path.write_text(html)
        print(f"Built: blog/{post['slug']}.html")


def build_guide_page(env, pads):
    """Build the splash pad guide page."""
    template = env.get_template("guide.html")

    guide_title = "How to Choose a Splash Pad: What Families Should Look For"
    guide_subtitle = "A practical, parent-tested guide to picking the right splash pad for your family — from free vs. paid options to safety, accessibility, and what to pack."
    guide_date = "2026-04-04"

    guide_intro = (
        "Taking the kids to a splash pad should be simple — but with thousands of options across the country, "
        "picking the right one can be surprisingly tricky. Is it free or paid? Are there restrooms? Will your "
        "toddler actually enjoy it, or is it built for older kids?\n\n"
        "This guide walks you through everything families should consider before heading out, so you spend less "
        "time researching and more time playing."
    )

    guide_sections = [
        {
            "id": "free-vs-paid",
            "icon": "💲",
            "title": "Free vs. Paid Splash Pads",
            "content": (
                "Most city and county park splash pads are **completely free** — you just show up during operating "
                "hours and play. These are usually smaller, located inside public parks, and don't require "
                "reservations.\n\n"
                "Paid splash pads are typically part of larger water parks, aquatic centers, or amusement parks. "
                "They tend to offer more elaborate water features, slides, and amenities like locker rooms and "
                "snack bars.\n\n"
                "**When free makes sense:** Quick weekday outings, toddler play dates, budget-friendly summer fun.\n\n"
                "**When paid is worth it:** Full-day excursions, birthday parties, older kids who want bigger thrills.\n\n"
                "Use our [Free Admission](/category/free-admission) filter to browse all no-cost options near you."
            ),
        },
        {
            "id": "age-suitability",
            "icon": "👶",
            "title": "Age Suitability",
            "content": (
                "Not all splash pads are created equal when it comes to age ranges. Some have gentle ground-level "
                "bubblers perfect for babies and toddlers, while others feature high-pressure jets and tall dump "
                "buckets designed for school-age kids.\n\n"
                "**What to look for by age:**\n\n"
                "- **Babies & Toddlers (0–3):** Look for zero-depth areas with low-pressure spray features and "
                "soft, non-slip surfaces. Check our [Best for Toddlers](/category/toddlers) listings.\n"
                "- **Preschoolers (3–5):** Interactive features like spray tunnels, animal-shaped sprayers, and "
                "small dump buckets keep this age group engaged.\n"
                "- **School-Age Kids (6–12):** Water cannons, tipping buckets, and multi-level spray structures "
                "provide the excitement they need.\n"
                "- **All Ages:** The best family splash pads separate zones by intensity so every age has something "
                "to enjoy.\n\n"
                "Many listings on Splash Pad Locator include age range tags so you can filter before you visit."
            ),
        },
        {
            "id": "amenities",
            "icon": "🏖️",
            "title": "Amenities Checklist",
            "content": (
                "The splash pad itself might be great — but the experience depends just as much on what's around it. "
                "Before you go, check for these amenities:\n\n"
                "- **Shade structures** — Essential for hot summer days. Without shade, surfaces heat up and young "
                "skin burns fast. Browse our [Splash Pads with Shade](/category/with-shade) listings.\n"
                "- **Restrooms** — Especially important with young children. Check our "
                "[With Restrooms](/category/with-restrooms) filter.\n"
                "- **Parking** — Some urban splash pads rely on street parking; suburban ones usually have lots.\n"
                "- **Picnic areas** — Pack a lunch and make it a full outing. Filter by "
                "[Picnic Areas](/category/with-picnic-areas).\n"
                "- **Nearby food** — Snack bars, food trucks, or restaurants within walking distance.\n"
                "- **Adult seating** — Benches, chairs, or grassy areas where parents can sit while supervising.\n"
                "- **Playground nearby** — Some parks combine splash pads with traditional playgrounds for dry play options."
            ),
        },
        {
            "id": "safety",
            "icon": "🛡️",
            "title": "Safety & Supervision",
            "content": (
                "Splash pads are one of the safest water-play options because there's no standing water — but a few "
                "things are still worth checking:\n\n"
                "- **Staffed vs. unstaffed:** Some splash pads have attendants; most public ones do not. "
                "Plan to actively supervise your children regardless.\n"
                "- **Surface material:** Look for textured, non-slip surfaces. Rubber and rubberized concrete "
                "are best; smooth tile or concrete can get slippery and hot.\n"
                "- **Water pressure:** High-pressure jets can knock over toddlers. Scout the pad before letting "
                "young kids explore freely.\n"
                "- **Drainage:** Good splash pads drain quickly so there are no puddles for kids to slip in.\n"
                "- **Sun exposure:** Surfaces in full sun can reach temperatures hot enough to burn bare feet. "
                "Water shoes are a smart precaution.\n\n"
                "**Always:** Apply sunscreen before arrival, bring water to drink, and never leave children unattended."
            ),
        },
        {
            "id": "accessibility",
            "icon": "♿",
            "title": "Accessibility",
            "content": (
                "Many modern splash pads are designed with accessibility in mind, but features vary widely.\n\n"
                "**ADA considerations:**\n\n"
                "- Wheelchair-accessible paths to and through the splash area\n"
                "- Ground-level spray features reachable from a seated position\n"
                "- Transfer-friendly surfaces\n"
                "- Accessible restrooms and parking nearby\n\n"
                "**Sensory-friendly features:**\n\n"
                "Some children with sensory sensitivities may find loud, high-pressure splash pads overwhelming. "
                "Look for pads with:\n\n"
                "- Adjustable or gentle spray settings\n"
                "- Quieter water flow features (bubblers, gentle arches)\n"
                "- Off-peak hours with fewer crowds\n\n"
                "Filter by [Accessible Splash Pads](/category/accessible) on our directory to find "
                "options near you."
            ),
        },
        {
            "id": "seasonal-timing",
            "icon": "📅",
            "title": "Seasonal Timing",
            "content": (
                "Splash pad seasons vary dramatically by region:\n\n"
                "- **Southern states** ([Texas](/state/texas), [Florida](/state/florida), "
                "[Arizona](/state/arizona)): Many open as early as March and run through October — "
                "some operate year-round.\n"
                "- **Midwest & Mid-Atlantic** ([Illinois](/state/illinois), [Ohio](/state/ohio), "
                "[Pennsylvania](/state/pennsylvania)): Typically Memorial Day through Labor Day "
                "(late May – early September).\n"
                "- **Northern states** ([Minnesota](/state/minnesota), [Michigan](/state/michigan), "
                "[New York](/state/new-york)): Shorter seasons, often mid-June through August.\n\n"
                "**Best times to visit:**\n\n"
                "- **Weekday mornings** are typically the least crowded.\n"
                "- **Avoid 12–3pm** on the hottest days — surfaces are scorching and UV exposure peaks.\n"
                "- **Early season** (opening weekend) can be hit-or-miss as maintenance schedules ramp up.\n\n"
                "Always check the individual listing on Splash Pad Locator for current hours and seasonal dates."
            ),
        },
        {
            "id": "ratings-reviews",
            "icon": "⭐",
            "title": "Using Recent Reviews",
            "content": (
                "Recent reviews can help you spot practical details that are hard to capture in a directory "
                "listing. Treat them as a maintenance check, not as the only way to choose a splash pad.\n\n"
                "**Tips for reading reviews:**\n\n"
                "- Filter for recent reviews (last season or current year)\n"
                "- Look for reviews from parents with kids the same age as yours\n"
                "- Pay attention to mentions of cleanliness, maintenance, and shade\n"
                "- Photos in reviews are more useful than star counts"
            ),
        },
    ]

    guide_checklist = [
        "Is it free or paid? If paid, what's the admission cost for your family size?",
        "Is it age-appropriate for your children? Look for dedicated toddler zones if needed.",
        "Are there restrooms on-site or nearby?",
        "Is there shade — both for the kids and for parent seating areas?",
        "What's the parking situation? Is there a lot, or street parking only?",
        "Is the splash pad currently open for the season? Check the listing for hours.",
        "What's the surface material? Non-slip and cool surfaces are safest for bare feet.",
        "Are there accessibility features if needed (wheelchair paths, ground-level sprays)?",
        "Is there food nearby, or should you pack lunch and snacks?",
        "Did you check recent reviews for maintenance or cleanliness issues?",
        "Do you have sunscreen, water shoes, towels, and a change of clothes packed?",
        "Is there a playground or other dry-play option nearby for when the kids are done with water?",
    ]

    html = template.render(
        guide_title=guide_title,
        guide_subtitle=guide_subtitle,
        guide_date=guide_date,
        guide_intro=guide_intro,
        guide_sections=guide_sections,
        guide_checklist=guide_checklist,
        total_count=len(pads),
        page_title=f"{guide_title} - {config.SITE_NAME}",
        meta_description="A parent's guide to choosing the right splash pad. Covers free vs. paid, age suitability, amenities, safety, and what to pack.",
        request_path="/splash-pad-guide",
    )

    output_path = config.OUTPUT_DIR / "splash-pad-guide.html"
    output_path.write_text(html)
    print("Built: splash-pad-guide.html")


def build_search_index(pads):
    """Generate search-index.json for client-side search."""
    protected_slugs = _load_protected_pad_slugs()
    indexable_pads = filter_indexable_pads(pads, protected_slugs)
    index = [
        {"name": p["name"], "city": p.get("city", ""), "state": p.get("state", ""), "slug": p["slug"]}
        for p in indexable_pads if p.get("name") and p.get("slug")
    ]
    output_path = config.OUTPUT_DIR / "search-index.json"
    with open(output_path, "w") as f:
        json.dump(index, f, ensure_ascii=False)
    print(f"Built: search-index.json ({len(index)} indexable pads)")


LASTMOD_STORE = Path(__file__).resolve().parent / "sitemap_lastmod.json"


def _stable_lastmods(entries, data_by_url=None):
    """Per-URL lastmod from a committed content-hash datestore (sitemap_lastmod.json).

    A URL's date bumps to the build date only when its content actually changed
    since the stored hash — so lastmod stays consistently accurate and Google
    can trust it, instead of seeing every URL restamped on every build (a
    pattern crawlers learn to ignore). The store is committed to git so Netlify
    builds read the same dates.

    Pad/blog URLs hash their SOURCE DATA (canonical JSON of the Airtable
    record), not the rendered HTML — rendered output varies across
    environments (Python/library versions on Netlify vs local), which would
    flip every hash on deploy and restamp the whole sitemap. Data hashes are
    environment-independent. The few hub/static URLs still hash rendered files.
    """
    data_by_url = data_by_url or {}
    try:
        store = json.loads(LASTMOD_STORE.read_text())
    except (OSError, ValueError):
        store = {}
    today = datetime.now().strftime("%Y-%m-%d")
    dates = {}
    new_store = {}
    for url, _priority, _default in entries:
        rec = store.get(url) or {}
        data = data_by_url.get(url)
        if data is not None:
            # _airtable_id is build-internal metadata, not page content — exclude
            # it so the CSV-sourced and Airtable-sourced paths hash identically.
            basis = json.dumps({k: v for k, v in data.items() if k != "_airtable_id"},
                               sort_keys=True, ensure_ascii=True, default=str)
            digest = hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]
        else:
            rel = url.replace(config.SITE_URL, "").strip("/")
            page = config.OUTPUT_DIR / (f"{rel}.html" if rel else "index.html")
            try:
                digest = hashlib.sha256(page.read_bytes()).hexdigest()[:16]
            except OSError:
                digest = rec.get("hash", "")
        if digest and digest == rec.get("hash"):
            date = rec.get("date") or today  # unchanged content keeps its date
        elif not digest:
            date = rec.get("date") or today  # page file missing — keep prior date
        else:
            date = today  # new or changed content
        dates[url] = date
        new_store[url] = {"hash": digest, "date": date}
    LASTMOD_STORE.write_text(json.dumps(new_store, indent=0, sort_keys=True) + "\n")
    return dates


def build_sitemap(pads, posts):
    """Generate sitemap.xml with lastmod and priority to accelerate Google indexing."""
    today = datetime.now().strftime("%Y-%m-%d")
    protected_slugs = _load_protected_pad_slugs()
    indexable_pads = filter_indexable_pads(pads, protected_slugs)

    # Use clean URLs (no .html) to match canonical tags set in base.html
    entries = [
        (f"{config.SITE_URL}/", "1.0", today),
        (f"{config.SITE_URL}/blog", "0.8", today),
        (f"{config.SITE_URL}/splash-pad-guide", "0.8", today),
        (f"{config.SITE_URL}/about", "0.5", today),
        (f"{config.SITE_URL}/contact", "0.4", today),
        (f"{config.SITE_URL}/privacy", "0.3", today),
        (f"{config.SITE_URL}/terms", "0.3", today),
    ]

    grouped = group_pads_by_state(indexable_pads)
    for state in config.US_STATES:
        state_pads = grouped.get(state["slug"], [])
        if len(state_pads) >= 5:
            entries.append((f"{config.SITE_URL}/state/{state['slug']}", "0.8", today))

    for category in config.CATEGORIES:
        if pads_for_category(category, indexable_pads):
            entries.append((f"{config.SITE_URL}/category/{category['slug']}", "0.7", today))

    for state_slug, cities in config.CITY_PAGES.items():
        for city in cities:
            city_name_lower = city["name"].lower()
            city_pads = [
                p for p in indexable_pads
                if p.get("state_slug") == state_slug
                and p.get("city", "").strip().lower() == city_name_lower
            ]
            if len(city_pads) >= 3:
                entries.append((f"{config.SITE_URL}/city/{city['slug']}", "0.8", today))

    # Pad pages: include only pads that pass the indexability gate outright.
    for pad in indexable_pads:
        entries.append((f"{config.SITE_URL}/pad/{pad['slug']}", "0.6", today))

    for post in posts:
        if post.get("slug"):
            entries.append((f"{config.SITE_URL}/blog/{post['slug']}", "0.8", today))

    data_by_url = {f"{config.SITE_URL}/pad/{p['slug']}": p for p in indexable_pads}
    for post in posts:
        if post.get("slug"):
            data_by_url[f"{config.SITE_URL}/blog/{post['slug']}"] = post
    lastmods = _stable_lastmods(entries, data_by_url)

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, priority, lastmod in entries:
        sitemap += f"  <url><loc>{url}</loc><lastmod>{lastmods.get(url, lastmod)}</lastmod><priority>{priority}</priority></url>\n"
    sitemap += "</urlset>"

    output_path = config.OUTPUT_DIR / "sitemap.xml"
    output_path.write_text(sitemap)
    print("Built: sitemap.xml")


def build_robots():
    """Generate robots.txt."""
    robots = f"""User-agent: *
Allow: /

Sitemap: {config.SITE_URL}/sitemap.xml
"""
    output_path = config.OUTPUT_DIR / "robots.txt"
    output_path.write_text(robots)
    print("Built: robots.txt")


def build_redirects(pads, posts, dropped_pads=None):
    """Generate _redirects file with explicit 301 rules for .html → extensionless URLs.

    Netlify's force=true does not reliably fire on wildcard/splat redirect patterns
    when the .html file physically exists in dist/. Explicit per-page rules in a
    _redirects file work consistently and resolve Google Search Console
    'Duplicate, Google chose different canonical than user' errors.
    """
    rules = []
    dropped_pads = dropped_pads or []

    # State pages
    grouped = group_pads_by_state(pads)
    for state in config.US_STATES:
        state_pads = grouped.get(state["slug"], [])
        if state_pads:
            rules.append(f"/state/{state['slug']}.html  /state/{state['slug']}  301!")

    # City pages
    for state_slug, cities in config.CITY_PAGES.items():
        for city in cities:
            rules.append(f"/city/{city['slug']}.html  /city/{city['slug']}  301!")

    # Pad pages
    for pad in pads:
        rules.append(f"/pad/{pad['slug']}.html  /pad/{pad['slug']}  301!")

    # Hard-dropped false positives: send old URLs to the relevant state page
    # so users and crawlers do not land on deleted off-topic detail pages.
    # Duplicate-cleanup drops 301 to their kept twin instead (PAD_REDIRECT_OVERRIDES)
    # so link equity and user intent land on the surviving listing.
    overrides = getattr(config, "PAD_REDIRECT_OVERRIDES", {})
    kept_slugs = {p["slug"] for p in pads}
    for pad in dropped_pads:
        target = overrides.get(pad["slug"])
        if target and target.startswith("/pad/") and target[len("/pad/"):] not in kept_slugs:
            target = None  # twin missing from this build — fall back to the state hub
        if not target:
            target = f"/state/{pad.get('state_slug')}" if pad.get("state_slug") else "/"
        rules.append(f"/pad/{pad['slug']}.html  {target}  301!")
        rules.append(f"/pad/{pad['slug']}  {target}  301!")

    # Category pages
    for category in config.CATEGORIES:
        rules.append(f"/category/{category['slug']}.html  /category/{category['slug']}  301!")

    # Blog post pages
    for post in posts:
        if post.get("slug"):
            rules.append(f"/blog/{post['slug']}.html  /blog/{post['slug']}  301!")

    # Blog listing page
    rules.append("/blog.html  /blog  301!")

    # Guide page
    rules.append("/splash-pad-guide.html  /splash-pad-guide  301!")

    # Static pages (about, contact, etc.) — already work via exact-match in
    # netlify.toml, but include here for completeness and as a safety net
    for page in STATIC_PAGES:
        if page["output"].endswith(".html") and page["output"] != "success/index.html":
            clean = page["output"].replace(".html", "")
            rules.append(f"/{clean}.html  /{clean}  301!")

    output_path = config.OUTPUT_DIR / "_redirects"
    output_path.write_text("\n".join(rules) + "\n")
    print(f"Built: _redirects ({len(rules)} explicit 301 rules)")


def copy_ads_txt():
    """Copy ads.txt to output directory."""
    ads_txt_path = Path("ads.txt")
    if ads_txt_path.exists():
        shutil.copy(ads_txt_path, config.OUTPUT_DIR / "ads.txt")
        print("Built: ads.txt")


# Static pages
STATIC_PAGES = [
    {
        "template": "about.html",
        "output": "about.html",
        "title": "About Us",
        "description": "Learn about Splash Pad Finder and our mission to help families find the best splash pads near them.",
    },
    {
        "template": "privacy.html",
        "output": "privacy.html",
        "title": "Privacy Policy",
        "description": "Our privacy policy explains how we collect, use, and protect your information.",
    },
    {
        "template": "contact.html",
        "output": "contact.html",
        "title": "Contact Us",
        "description": "Get in touch with Splash Pad Finder for questions, suggestions, or to submit a new listing.",
    },
    {
        "template": "terms.html",
        "output": "terms.html",
        "title": "Terms of Service",
        "description": "Terms and conditions for using Splash Pad Finder.",
    },
    {
        "template": "success.html",
        "output": "success/index.html",
        "title": "Message Sent",
        "description": "Thank you for contacting us.",
        # Form-confirmation screen — a "behavioral purpose" page per AdSense
        # inventory-value policy; never index it (2026-07-18 reviewer audit).
        "noindex": True,
    },
    {
        "template": "submit.html",
        "output": "submit.html",
        "title": "Submit a Splash Pad",
        "description": "Submit a splash pad, spray park, or water play area to be added to our directory.",
    },
]


def build_static_pages(env, pads=None):
    """Build static informational pages."""
    total_count = len(pads) if pads else 0
    for page in STATIC_PAGES:
        template = env.get_template(page["template"])
        html = template.render(
            page_title=f"{page['title']} - {config.SITE_NAME}",
            meta_description=page["description"],
            request_path=f"/{page['output'].replace('/index.html', '').replace('.html', '')}",
            total_count=total_count,
            noindex=page.get("noindex", False),
        )
        output_path = config.OUTPUT_DIR / page["output"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)
        print(f"Built: {page['output']}")


def download_pad_images(pads):
    """Download external photo URLs locally to avoid Google Places URL expiry (403 errors).

    Google Places photo URLs (lh3.googleusercontent.com) have signed tokens that expire.
    Downloading at build time and serving from /static/images/ makes them permanent.
    Pads whose URLs have already expired will have photo_url cleared so the template
    gradient fallback activates.

    Images are saved to both dist/static/images/ (for the current build) and
    static/images/ (source tree, committed to git) so they survive across Netlify builds.
    On subsequent builds, setup_output_directory() copies static/images/ → dist/static/images/
    before this function runs, so the cache hit avoids re-downloading.
    """
    images_dir = config.OUTPUT_DIR / "static" / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Source-level backup: committed to git so images persist across Netlify builds.
    # setup_output_directory() copies static/ → dist/static/ before this runs, so
    # anything saved here is available in images_dir on the next build.
    source_images_dir = config.STATIC_DIR / "images"
    source_images_dir.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    skipped = 0
    failed = 0

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.google.com/",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }

    for pad in pads:
        url = pad.get("photo_url", "").strip()
        slug = pad.get("slug", "").strip()

        if not url or not slug:
            skipped += 1
            continue

        # If already a local path, nothing to do
        if url.startswith("/static/"):
            skipped += 1
            continue

        local_path = images_dir / f"{slug}.jpg"

        # Reuse existing downloaded file if present (avoids re-downloading on incremental builds)
        if local_path.exists():
            pad["photo_url"] = f"/static/images/{slug}.jpg"
            skipped += 1
            continue

        try:
            response = requests.get(url, headers=headers, timeout=15, stream=True)
            if response.status_code == 200:
                with open(local_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                # Also save to source static dir so git commit persists it across builds
                source_path = source_images_dir / f"{slug}.jpg"
                if not source_path.exists():
                    shutil.copy2(local_path, source_path)
                pad["photo_url"] = f"/static/images/{slug}.jpg"
                downloaded += 1
            else:
                print(f"  Image {response.status_code}: {pad.get('name', slug)} — clearing photo_url in Airtable")
                pad["photo_url"] = ""
                clear_airtable_photo_url(pad.get("_airtable_id", ""))
                failed += 1
        except Exception as e:
            print(f"  Image error for {pad.get('name', slug)}: {e} — clearing photo_url")
            pad["photo_url"] = ""
            failed += 1

    print(f"Images: {downloaded} downloaded, {skipped} skipped/cached, {failed} failed (will use gradient fallback)")


def main():
    """Main build process."""
    print(f"\n{'='*50}")
    print(f"Building {config.SITE_NAME}")
    print(f"{'='*50}\n")

    print("Setting up output directory...")
    setup_output_directory()

    print("\nFetching splash pads...")
    pads = get_pads()
    pads, dropped_pads = split_pads_for_build(pads)

    print("\nDownloading pad images (caches Google URLs locally)...")
    download_pad_images(pads)

    print("\nFetching blog posts...")
    posts = fetch_blog_posts()

    env = create_jinja_env()

    print("\nBuilding pages...")
    build_homepage(env, pads, posts)
    build_state_pages(env, pads)
    build_city_pages(env, pads)
    build_pad_pages(env, pads)
    build_category_pages(env, pads)
    build_static_pages(env, pads)
    build_blog_page(env, posts)
    build_post_pages(env, posts)
    build_guide_page(env, pads)

    print("\nBuilding SEO files...")
    build_sitemap(pads, posts)
    build_robots()
    build_redirects(pads, posts, dropped_pads)
    copy_ads_txt()
    build_search_index(pads)

    print(f"\n{'='*50}")
    print(f"Build complete! Output in: {config.OUTPUT_DIR}")
    print(f"{'='*50}")
    print(f"\nTo preview locally:")
    print(f"  cd {config.OUTPUT_DIR}")
    print(f"  python3 -m http.server 8000")
    print(f"  Open http://localhost:8000")


if __name__ == "__main__":
    main()
