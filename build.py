#!/usr/bin/env python3
"""
Splash Pad Finder - Static Site Generator

Fetches splash pad listings from Airtable and generates a static HTML site.
Falls back to sample data if Airtable is not configured.
"""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

import markdown as md_lib
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup
from slugify import slugify

import config


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

            state_name = fields.get("State", "")
            pad = {
                "name": fields.get("Name", ""),
                "slug": slugify(fields.get("Name", "") + "-" + fields.get("City", "")),
                "description": fields.get("Description", ""),
                "address": fields.get("Address", ""),
                "city": fields.get("City", ""),
                "state": state_name,
                "state_slug": slugify(state_name),
                "zip": fields.get("Zip", ""),
                "phone": fields.get("Phone", ""),
                "website_url": fields.get("Website URL", ""),
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
            }
            pads.append(pad)

        print(f"Fetched {len(pads)} splash pads from Airtable.")
        return pads

    except Exception as e:
        print(f"Error fetching from Airtable: {e}")
        return None


def get_pads():
    """Get splash pads from Airtable or fall back to sample data."""
    pads = fetch_from_airtable()
    if pads is None:
        pads = get_sample_data()
        print(f"Using {len(pads)} sample splash pads.")
    return pads


def fetch_blog_posts():
    """Fetch published blog posts from Airtable."""
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
                "content": fields.get("Content", ""),
                "excerpt": fields.get("Excerpt", ""),
                "author": fields.get("Author", "Splash Pad Locator Staff"),
                "publish_date": fields.get("Publish Date", ""),
                "featured_image": fields.get("Featured Image", ""),
                "meta_description": fields.get("Meta Description", ""),
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

    featured = [p for p in pads if p.get("featured")][:config.FEATURED_COUNT]
    if not featured:
        featured = pads[:config.FEATURED_COUNT]

    recent = sorted(pads, key=lambda x: x.get("date_added", ""), reverse=True)[:config.RECENT_COUNT]

    # Group by state for state browse section
    by_state = group_pads_by_state(pads)
    state_counts = {s: len(v) for s, v in by_state.items()}

    # Separate featured post (hero card) from recent posts grid
    featured_post = next((p for p in posts if p.get("featured")), None)
    recent_posts = [p for p in posts if p is not featured_post][:3]

    html = template.render(
        featured_pads=featured,
        recent_pads=recent,
        all_pads=pads,
        state_counts=state_counts,
        total_count=len(pads),
        featured_post=featured_post,
        recent_posts=recent_posts,
        page_title=config.DEFAULT_META_TITLE,
        meta_description=config.DEFAULT_META_DESCRIPTION,
        request_path="/",
    )

    output_path = config.OUTPUT_DIR / "index.html"
    output_path.write_text(html)
    print(f"Built: index.html ({len(pads)} total pads)")


def build_state_pages(env, pads):
    """Build one page per US state."""
    template = env.get_template("state.html")
    grouped = group_pads_by_state(pads)

    MIN_PADS_FOR_INDEX = 5

    for state in config.US_STATES:
        state_pads = grouped.get(state["slug"], [])
        state_pads.sort(key=lambda x: x.get("city", ""))

        thin_state = len(state_pads) < MIN_PADS_FOR_INDEX

        html = template.render(
            state=state,
            pads=state_pads,
            page_title=f"Splash Pads in {state['name']} - {config.SITE_NAME}",
            meta_description=f"Find {len(state_pads)} splash pads, spray parks, and water play areas in {state['name']}. Free and paid options for families.",
            request_path=f"/state/{state['slug']}.html",
            noindex=thin_state,
        )

        output_path = config.OUTPUT_DIR / "state" / f"{state['slug']}.html"
        output_path.write_text(html)
        print(f"Built: state/{state['slug']}.html ({len(state_pads)} pads)")


def is_thin_pad(pad):
    """Check if a pad page has too little content to be indexed."""
    desc = str(pad.get("description", "")).strip()
    desc_ok = len(desc) >= 100 and desc.lower() != "nan"
    hours_ok = bool(str(pad.get("hours", "")).strip()) and str(pad.get("hours", "")).strip().lower() != "nan"
    features = pad.get("features", [])
    features_ok = isinstance(features, list) and len(features) > 0
    type_val = str(pad.get("type", "")).strip()
    type_ok = bool(type_val) and type_val.lower() not in ("nan", "splash pad")

    content_signals = sum([desc_ok, hours_ok, features_ok, type_ok])
    return content_signals <= 1


def build_pad_pages(env, pads):
    """Build individual splash pad detail pages."""
    template = env.get_template("pad.html")
    noindex_count = 0

    for pad in pads:
        # Related pads: same state, different pad
        related = [p for p in pads if p["slug"] != pad["slug"] and p.get("state_slug") == pad.get("state_slug")][:4]

        thin = is_thin_pad(pad)
        if thin:
            noindex_count += 1

        html = template.render(
            pad=pad,
            related_pads=related,
            page_title=f"{pad['name']} - {pad['city']}, {pad['state']} - {config.SITE_NAME}",
            meta_description=pad.get("description", "")[:160],
            request_path=f"/pad/{pad['slug']}.html",
            noindex=thin,
        )

        output_path = config.OUTPUT_DIR / "pad" / f"{pad['slug']}.html"
        output_path.write_text(html)

    print(f"Built: {len(pads)} pad pages ({noindex_count} noindexed as thin content)")


def build_category_pages(env, pads):
    """Build feature/filter category pages."""
    template = env.get_template("category.html")

    category_filters = {
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

    for category in config.CATEGORIES:
        filter_fn = category_filters.get(category["slug"], lambda p: True)
        category_pads = [p for p in pads if filter_fn(p)]

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
            page_title=f"{category['name']} Splash Pads - {config.SITE_NAME}",
            meta_description=category["description"],
            request_path=f"/category/{category['slug']}.html",
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
        request_path="/blog.html",
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
        html = template.render(
            post=post,
            all_posts=posts,
            page_title=f"{post['title']} - {config.SITE_NAME}",
            meta_description=post.get("meta_description") or post.get("excerpt", "")[:160],
            request_path=f"/blog/{post['slug']}.html",
        )
        output_path = config.OUTPUT_DIR / "blog" / f"{post['slug']}.html"
        output_path.write_text(html)
        print(f"Built: blog/{post['slug']}.html")


def build_search_index(pads):
    """Generate search-index.json for client-side search."""
    index = [
        {"name": p["name"], "city": p.get("city", ""), "state": p.get("state", ""), "slug": p["slug"]}
        for p in pads if p.get("name") and p.get("slug")
    ]
    output_path = config.OUTPUT_DIR / "search-index.json"
    with open(output_path, "w") as f:
        json.dump(index, f, ensure_ascii=False)
    print(f"Built: search-index.json ({len(index)} pads)")


def build_sitemap(pads, posts):
    """Generate sitemap.xml."""
    urls = [
        f"{config.SITE_URL}/",
        f"{config.SITE_URL}/blog.html",
        f"{config.SITE_URL}/about.html",
        f"{config.SITE_URL}/contact.html",
        f"{config.SITE_URL}/privacy.html",
        f"{config.SITE_URL}/terms.html",
    ]

    grouped = group_pads_by_state(pads)
    for state in config.US_STATES:
        state_pads = grouped.get(state["slug"], [])
        if len(state_pads) >= 5:
            urls.append(f"{config.SITE_URL}/state/{state['slug']}.html")

    for category in config.CATEGORIES:
        urls.append(f"{config.SITE_URL}/category/{category['slug']}.html")

    for pad in pads:
        if not is_thin_pad(pad):
            urls.append(f"{config.SITE_URL}/pad/{pad['slug']}.html")

    for post in posts:
        if post.get("slug"):
            urls.append(f"{config.SITE_URL}/blog/{post['slug']}.html")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap += f"  <url><loc>{url}</loc></url>\n"
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
            request_path=f"/{page['output']}",
            total_count=total_count,
        )
        output_path = config.OUTPUT_DIR / page["output"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html)
        print(f"Built: {page['output']}")


def main():
    """Main build process."""
    print(f"\n{'='*50}")
    print(f"Building {config.SITE_NAME}")
    print(f"{'='*50}\n")

    print("Setting up output directory...")
    setup_output_directory()

    print("\nFetching splash pads...")
    pads = get_pads()

    print("\nFetching blog posts...")
    posts = fetch_blog_posts()

    env = create_jinja_env()

    print("\nBuilding pages...")
    build_homepage(env, pads, posts)
    build_state_pages(env, pads)
    build_pad_pages(env, pads)
    build_category_pages(env, pads)
    build_static_pages(env, pads)
    build_blog_page(env, posts)
    build_post_pages(env, posts)

    print("\nBuilding SEO files...")
    build_sitemap(pads, posts)
    build_robots()
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
