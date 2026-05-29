#!/usr/bin/env python3
"""
website_descriptions.py — Phase 2 of the AdSense "Low Value Content" remediation.

Enriches listing descriptions with ORIGINAL, fact-grounded content mined from
each splash pad / water park's OWN website. This is what adds per-page value
*beyond* the business's Google profile — the thing the AdSense reviewer wants.

Pipeline (per listing):
  1. crawl    — fetch homepage + a couple of about/hours/admission pages, extract
                clean main text (trafilatura). Cached to disk so re-runs and the
                LLM pass never re-fetch.
  2. compose  — Claude Haiku extracts distinguishing facts from the site text and
                writes an ORIGINAL 2-4 sentence description, grounded only in those
                facts + the structured data. It must NOT copy site prose verbatim
                (that would re-introduce a scraped/copied-content problem) and must
                NOT include star ratings (this site strips rating claims by policy).
  3. fallback — listings with no usable own-site text keep the Phase-1 fact
                description from generate_fact_descriptions.compose().
  4. gate     — run the same build.evaluate_pad gate the real build uses.
  5. write    — (only with --apply) write the Airtable "Description" field.

SAFETY: dry-run by default; small --limit by default; crawls + LLM responses are
cached to disk so tuning never re-fetches or re-bills. Nothing is written to
Airtable without --apply, and the dry-run never touches Airtable at all.

JS-rendered sites (Wix/Canva/Google-Sites/app builders) return near-empty text
here and simply fall through to the Phase-1 fallback. A Playwright renderer is a
documented hook (see crawl_site) — intentionally not implemented unless asked.

Usage:
  python3 website_descriptions.py                  # dry run, 25 crawlable listings
  python3 website_descriptions.py --limit 200      # dry run, larger sample
  python3 website_descriptions.py --all            # dry run over EVERY listing
  python3 website_descriptions.py --all --apply     # PRODUCTION: write everything
  python3 website_descriptions.py --refresh         # ignore caches, re-fetch/re-bill
"""
import os
import re
import sys
import json
import time
import argparse
import hashlib
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse, urljoin
from urllib import robotparser
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import trafilatura
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pyairtable import Api

import config
import build                      # the real gate: evaluate_pad, clean_description, etc.
import generate_fact_descriptions as gfd  # Phase-1 composer reused as the fallback

# Empty-key guard (playbook gotcha): a shell may export an EMPTY var that shadows
# the real key in .env, so check for blank, not just missing.
load_dotenv(Path(__file__).parent / ".env", override=True)
_KEY = (os.environ.get("AIRTABLE_API_KEY") or "").strip()
_BASE = (os.environ.get("AIRTABLE_BASE_ID") or "").strip()
_TABLE = (os.environ.get("AIRTABLE_TABLE_NAME") or "SplashPads").strip()
_ANTHROPIC = (os.environ.get("ANTHROPIC_API_KEY") or "").strip()

BASE_DIR = Path(__file__).parent
CACHE_DIR = BASE_DIR / "data" / "site_cache"
CRAWL_CACHE = CACHE_DIR / "crawl"
LLM_CACHE = CACHE_DIR / "llm"
for d in (CRAWL_CACHE, LLM_CACHE):
    d.mkdir(parents=True, exist_ok=True)

DESC_FIELD = "Description"
HAIKU_MODEL = "claude-haiku-4-5-20251001"
UA = "Mozilla/5.0 (compatible; SplashPadLocatorBot/1.0; +https://splashpadlocator.com)"
TIMEOUT = 8
MIN_SITE_TEXT = 250                          # below this, treat site as no usable content
MIN_DESC_LEN = config.MIN_DESCRIPTION_LENGTH  # website desc must clear the same gate (150)
CRAWL_DELAY = 0.5                            # politeness pause between same-host requests

# Haiku 4.5 list price (USD per token), used only to report estimated cost.
PRICE_IN = 1.00 / 1_000_000
PRICE_OUT = 5.00 / 1_000_000

# Not the business's own site — these never carry original venue content worth
# crawling, and several are JS walls. (.gov / .org / city sites are NOT skipped:
# those municipal park pages are exactly the per-page value we want.)
SOCIAL = (
    "facebook.", "m.facebook", "fb.com", "fb.me", "instagram.", "linktr.ee",
    "twitter.", "x.com", "tiktok.", "youtube.", "youtu.be", "pinterest.",
    "yelp.", "tripadvisor.", "foursquare.", "mapquest.", "groupon.",
    "google.com", "goo.gl", "sites.google", "business.site",
    "booking.", "expedia.", "hotels.com", "wikipedia.org",
)

# Same-host secondary pages worth pulling for more venue context.
ABOUT_HINTS = (
    "about", "hours", "admission", "tickets", "rates", "prices", "pricing",
    "plan", "visit", "attractions", "amenities", "facilities", "things-to-do",
    "splash", "water", "aquatic", "pool", "park",
)


# ── crawl stage ───────────────────────────────────────────────────────────────

_robots_cache = {}


def robots_allows(url):
    """Best-effort robots.txt check, cached per host. Fails OPEN on any error."""
    try:
        parts = urlparse(url)
        base = f"{parts.scheme}://{parts.netloc}"
        if base not in _robots_cache:
            rp = robotparser.RobotFileParser()
            rp.set_url(urljoin(base, "/robots.txt"))
            try:
                rp.read()
            except Exception:
                rp = None
            _robots_cache[base] = rp
        rp = _robots_cache[base]
        return rp.can_fetch(UA, url) if rp else True
    except Exception:
        return True


def host_of(url):
    raw = url if url.startswith("http") else "http://" + url
    return urlparse(raw).netloc.lower().replace("www.", "")


def is_crawlable(url):
    """True if url is a real own-site URL worth crawling (not social/aggregator)."""
    url = (url or "").strip()
    if not url:
        return False
    host = host_of(url)
    if not host or "." not in host:
        return False
    return not any(s in host for s in SOCIAL)


def _fetch(url):
    if not url.startswith("http"):
        url = "https://" + url
    if not robots_allows(url):
        return None, "robots-disallow", None
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT, allow_redirects=True)
        return r.status_code, r.text, r.url
    except Exception as e:
        return None, type(e).__name__, None


def _extract(html):
    if not html:
        return ""
    txt = trafilatura.extract(html, include_comments=False, include_tables=False,
                              favor_precision=True)
    return (txt or "").strip()


def _find_secondary(html, base_url, host):
    """Return up to 2 same-host about/hours/admission URLs to deepen context."""
    found = []
    try:
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all("a", href=True):
            txt = (a.get_text() or "").strip().lower()
            href = a["href"].lower()
            if any(h in txt or h in href for h in ABOUT_HINTS):
                full = urljoin(base_url, a["href"])
                if host_of(full) == host and full not in found:
                    found.append(full)
            if len(found) >= 2:
                break
    except Exception:
        pass
    return found


def crawl_site(url, use_cache=True):
    """Fetch homepage + secondary pages, return {url, host, text, status}.

    NOTE: JS-rendered sites (Wix/Canva/Google-Sites/app builders) return near-empty
    text here. The planned Playwright fallback would render those; it is intentionally
    not wired up. Such sites fall through to the Phase-1 fallback description.
    """
    host = host_of(url)
    cache_path = CRAWL_CACHE / f"{hashlib.md5(url.encode()).hexdigest()}.json"
    if use_cache and cache_path.exists():
        return json.loads(cache_path.read_text())

    result = {"url": url, "host": host, "text": "", "status": None}
    if not is_crawlable(url):
        result["status"] = "social/skip"
        cache_path.write_text(json.dumps(result))
        return result

    code, html, final = _fetch(url)
    result["status"] = code
    if code and isinstance(code, int) and code < 400 and html:
        parts = [_extract(html)]
        for sec in _find_secondary(html, final or url, host):
            time.sleep(CRAWL_DELAY)
            sc, sh, _ = _fetch(sec)
            if sc and isinstance(sc, int) and sc < 400:
                parts.append(_extract(sh))
        result["text"] = "\n".join(p for p in parts if p).strip()
    cache_path.write_text(json.dumps(result))
    return result


# ── compose stage (Haiku) ───────────────────────────────────────────────────

_anthropic_client = None


def _client():
    global _anthropic_client
    if _anthropic_client is None:
        import anthropic
        _anthropic_client = anthropic.Anthropic(api_key=_ANTHROPIC, timeout=40.0)
    return _anthropic_client


LLM_SYSTEM = (
    "You write factual directory descriptions for splash pads, spraygrounds, water "
    "parks, and aquatic centers. You are given raw text scraped from the venue's own "
    "website. Extract concrete, venue-specific facts: water features (spray jets, "
    "dumping buckets, zero-depth/beach entry, slides, fountains, interactive play "
    "structures), the season and months/hours it operates, admission or pricing, "
    "whether it sits inside a larger park or aquatic center, accessibility, and "
    "amenities (restrooms, shade, picnic areas, parking, concessions, changing rooms). "
    "Then write an ORIGINAL 2-4 sentence description in your own words, grounded ONLY "
    "in those facts plus the structured data provided.\n"
    "Rules: never copy sentences or distinctive phrases from the source — paraphrase "
    "into your own words. Never invent facts. NEVER mention star ratings, review "
    "counts, or testimonials (this directory excludes ratings by policy). No filler "
    "('nestled', 'boasting', 'state-of-the-art', 'hidden gem', 'fun for the whole "
    "family', 'something for everyone', 'make a splash', 'dedicated team').\n"
    "Set sufficient=true whenever the text contains ANY concrete information about THIS "
    "specific splash pad / park / aquatic facility (water features, season/hours, "
    "admission, location specifics, or amenities). Set sufficient=false only when the "
    "text is purely navigation links, cookie/legal notices, an error page, an unrelated "
    "business, or says nothing specific about this venue or its water play. Respond "
    "with strict JSON only."
)

LLM_SCHEMA_HINT = (
    'Return ONLY this JSON, nothing else: '
    '{"sufficient": true|false, '
    '"description": "the 2-4 sentence original description (empty string if not sufficient)"}'
)


def llm_compose(name, city, state, summary, site_text, use_cache=True):
    key = hashlib.md5(f"{name}|{city}|{state}|{site_text[:4000]}".encode()).hexdigest()
    cache_path = LLM_CACHE / f"{key}.json"
    if use_cache and cache_path.exists():
        return json.loads(cache_path.read_text())

    user = (
        f"Venue: {name}\nLocation: {city}, {state}\n"
        f"Structured data (already known): {summary}\n\n"
        f"Website text (raw, may contain navigation/boilerplate):\n"
        f'"""\n{site_text[:6000]}\n"""\n\n'
        f"{LLM_SCHEMA_HINT}"
    )
    try:
        msg = _client().messages.create(
            model=HAIKU_MODEL,
            max_tokens=600,
            system=LLM_SYSTEM,
            messages=[{"role": "user", "content": user}],
        )
        raw = msg.content[0].text.strip()
        raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.M).strip()
        data = json.loads(raw)
        data["_in_tokens"] = msg.usage.input_tokens
        data["_out_tokens"] = msg.usage.output_tokens
    except Exception as e:
        data = {"sufficient": False, "description": "", "error": str(e),
                "_in_tokens": 0, "_out_tokens": 0}
    cache_path.write_text(json.dumps(data))
    return data


# ── structured-data summary for the LLM prompt ─────────────────────────────────

def summary_for_llm(f):
    """Compact, true structured facts to anchor the LLM (no Price blob, no rating)."""
    bits = []
    typ = (f.get("Type") or "").strip()
    if typ:
        bits.append(f"type: {typ}")
    feats = gfd._as_list(f.get("Features"))
    if feats:
        bits.append("features: " + ", ".join(str(x) for x in feats))
    ages = gfd._as_list(f.get("Age Range"))
    if ages:
        bits.append("age suitability: " + ", ".join(str(x) for x in ages))
    adm = (f.get("Admission") or "").strip()
    if adm:
        bits.append(f"admission: {adm}")
    season = (f.get("Season") or "").strip()
    if season:
        bits.append(f"season: {season}")
    hrs = (f.get("Hours") or "").strip()
    if hrs and len(hrs) <= 200:
        bits.append(f"hours: {hrs}")
    return "; ".join(bits)


# ── orchestration ─────────────────────────────────────────────────────────────

def process_record(rec, use_cache):
    f = rec["fields"]
    url = (f.get("Website URL") or "").strip()
    out = {
        "id": rec["id"], "name": f.get("Name", ""), "fields": f,
        "source": "fallback", "description": "", "site_chars": 0,
        "crawl_status": None, "in_tokens": 0, "out_tokens": 0,
    }

    crawl = crawl_site(url, use_cache=use_cache) if url else {"text": "", "status": "no-url"}
    site_text = crawl.get("text", "")
    out["site_chars"] = len(site_text)
    out["crawl_status"] = crawl.get("status")

    if len(site_text) >= MIN_SITE_TEXT:
        result = llm_compose(f.get("Name", ""), f.get("City", ""), f.get("State", ""),
                             summary_for_llm(f), site_text, use_cache=use_cache)
        out["in_tokens"] = result.get("_in_tokens", 0)
        out["out_tokens"] = result.get("_out_tokens", 0)
        desc = (result.get("description") or "").strip()
        if result.get("sufficient") and len(desc) >= MIN_DESC_LEN:
            out["source"] = "website"
            out["description"] = desc
            return out

    out["description"] = gfd.compose(f)  # Phase-1 fact description
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=25,
                    help="number of CRAWLABLE listings to sample (ignored with --all)")
    ap.add_argument("--all", action="store_true",
                    help="process every non-Draft listing (crawl where possible, else fallback)")
    ap.add_argument("--apply", action="store_true", help="write the Description field to Airtable")
    ap.add_argument("--refresh", action="store_true", help="ignore crawl/LLM caches, re-fetch")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    use_cache = not args.refresh

    if not _KEY or not _BASE:
        sys.exit("Missing/empty AIRTABLE_API_KEY or AIRTABLE_BASE_ID in .env")
    if not _ANTHROPIC:
        sys.exit("Missing/empty ANTHROPIC_API_KEY in .env — required for the compose stage.")

    table = Api(_KEY).table(_BASE, _TABLE)
    recs = [r for r in table.all() if r["fields"].get("Status") != "Draft"]
    with_url = [r for r in recs if (r["fields"].get("Website URL") or "").strip()]
    crawlable = [r for r in with_url if is_crawlable(r["fields"]["Website URL"])]

    print(f"\n{'='*68}")
    print(f"  Phase 2: website-enriched descriptions  "
          f"[{'APPLY' if args.apply else 'DRY RUN'}, cache={'on' if use_cache else 'off'}]")
    print(f"{'='*68}")
    print(f"Addressable surface (full dataset):")
    print(f"  non-Draft listings:        {len(recs)}")
    print(f"  with any Website URL:      {len(with_url)} ({100*len(with_url)/len(recs):.0f}%)")
    print(f"  with crawlable own-site:   {len(crawlable)} ({100*len(crawlable)/len(recs):.0f}%)"
          f"  <- Phase 2 can enrich at most this many")

    batch = recs if args.all else crawlable[:args.limit]
    print(f"\nProcessing {len(batch)} listing(s) "
          f"({'ALL non-Draft' if args.all else 'sampled from crawlable'})...\n")

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(process_record, r, use_cache): r for r in batch}
        for i, fut in enumerate(as_completed(futs), 1):
            results.append(fut.result())
            if i % 25 == 0:
                print(f"  ...{i}/{len(batch)}")

    # ── outcome breakdown ──
    src = Counter(r["source"] for r in results)
    web = [r for r in results if r["source"] == "website"]
    n = len(results)
    print(f"\n=== OUTCOME ({n} processed) ===")
    print(f"  website-derived (original): {src['website']} ({100*src['website']/n:.0f}%)")
    print(f"  Phase-1 fallback:           {src['fallback']} ({100*src['fallback']/n:.0f}%)")

    # crawl-status breakdown (why fallbacks happened)
    cstat = Counter(str(r["crawl_status"]) for r in results if r["source"] == "fallback")
    if cstat:
        print("  fallback crawl-status: " + ", ".join(f"{k}={v}" for k, v in cstat.most_common()))
    empty_site = sum(1 for r in results if 0 < r["site_chars"] < MIN_SITE_TEXT)
    if empty_site:
        print(f"  (of those, {empty_site} fetched OK but yielded <{MIN_SITE_TEXT} chars — "
              f"likely JS-rendered)")

    # ── gate projection: current vs new, through the REAL build gate ──
    protected = build._load_protected_pad_slugs()
    cur_ok = new_ok = recovered = 0
    for r in results:
        f = r["fields"]
        cur_clean = build.clean_description(f.get("Description", "") or "")
        pad_cur = gfd.pad_shape(f, cur_clean)
        pad_new = gfd.pad_shape(f, r["description"])
        if build.hard_exclusion_reason(pad_new):
            continue
        s_cur = build.evaluate_pad(pad_cur, protected)[0]
        s_new = build.evaluate_pad(pad_new, protected)[0]
        cur_ok += (s_cur == "ok")
        new_ok += (s_new == "ok")
        if s_cur != "ok" and s_new == "ok":
            recovered += 1
    print(f"\n=== INDEXABLE (real build.evaluate_pad gate, {MIN_DESC_LEN} chars) ===")
    print(f"  current descriptions: {cur_ok}/{n} ({100*cur_ok/n:.0f}%)")
    print(f"  new descriptions:     {new_ok}/{n} ({100*new_ok/n:.0f}%)   "
          f"newly recovered: {recovered}")

    # ── cost ──
    in_tok = sum(r["in_tokens"] for r in results)
    out_tok = sum(r["out_tokens"] for r in results)
    cost = in_tok * PRICE_IN + out_tok * PRICE_OUT
    billed = sum(1 for r in results if r["in_tokens"])
    print(f"\n=== LLM COST (Haiku 4.5) ===")
    print(f"  live API calls this run: {billed}  (rest served from cache)")
    print(f"  tokens: in={in_tok:,} out={out_tok:,}   est. cost: ${cost:.4f}")
    if billed:
        per = cost / billed
        print(f"  ~${per:.5f}/call -> full crawlable surface ({len(crawlable)}) "
              f"≈ ${per*len(crawlable):.2f}")

    # ── samples ──
    print(f"\n=== SAMPLE WEBSITE-DERIVED DESCRIPTIONS (first 6) ===")
    for r in web[:6]:
        print(f"\n[{r['name']}] (site {r['site_chars']} chars)\n{r['description']}")

    if not args.apply:
        print("\nDRY RUN — nothing written to Airtable. Re-run with --all --apply to write.")
        return

    # ── APPLY ──
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BASE_DIR / "data" / f"description_backup_{ts}.json"
    backup = {r["id"]: (r["fields"].get("Description", "") or "") for r in batch}
    backup_path.write_text(json.dumps(backup, ensure_ascii=False, indent=2))
    print(f"\nBacked up {len(backup)} current descriptions -> {backup_path}")

    updates = [{"id": r["id"], "fields": {DESC_FIELD: r["description"]}}
               for r in results if r["description"]]
    print(f"--apply: writing {len(updates)} Description fields ...")
    for i in range(0, len(updates), 10):
        table.batch_update(updates[i:i + 10])
        print(f"  updated {min(i+10, len(updates))}/{len(updates)}")
    print("Done. Run python3 build.py locally to regenerate, then verify before deploy.")


if __name__ == "__main__":
    main()
