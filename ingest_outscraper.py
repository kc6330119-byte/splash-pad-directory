#!/usr/bin/env python3
"""
ingest_outscraper.py — turn a QUERY-method Outscraper extract into vetted,
publishable splash-pad candidates.

HARD RULE (see memory/data_ingestion_pipeline.md): Outscraper rows are LEADS, not
listings. A query like "Splash Pad" (exactMatch off) returns many ordinary parks
and playgrounds with NO water-play feature. Bulk-importing raw is what caused the
AdSense "Low Value Content" rejection. So every venue is verified against its OWN
website before it can be published, and only then is it typed as a Splash Pad.

Stages
  A  load + dedup(place_id) + PII-strip + net-new(jkey vs build.get_pads)
     + crawlable count.  OFFLINE, no network beyond the one Airtable read for
     the existing-directory join.  Always runs.  -> data/INGEST_CANDIDATES_*.txt
  B  --verify : crawl each net-new venue's own site, hand the site text + Google
     about/description to Haiku, which (1) CONFIRMS a real water-play feature and
     (2) writes an ORIGINAL 2-4 sentence description.  Run the real
     build.evaluate_pad gate.  Classify PUBLISH / HOLD / REJECT.  DRY, cached,
     no Airtable writes.  -> data/INGEST_VERIFY_*.md
  C  --apply : create Airtable records for the PUBLISH set.  GUARDED — refuses
     unless --i-have-confirmed-field-mapping is also passed, because it creates
     new source-of-truth rows at scale (AdSense-sensitive).

Reuses the proven machinery: website_descriptions.crawl_site / is_crawlable /
caching, generate_fact_descriptions.pad_shape, and the real build gate.

Usage
  python3 ingest_outscraper.py data/Outscraper-XXXX.xlsx                 # Stage A
  python3 ingest_outscraper.py data/Outscraper-XXXX.xlsx --verify --limit 10
  python3 ingest_outscraper.py data/Outscraper-XXXX.xlsx --verify --all
"""
import os
import re
import sys
import json
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import openpyxl

import config
import build
import generate_fact_descriptions as gfd
import website_descriptions as wd   # crawl_site, is_crawlable, caches, pricing, _client
from auto_features import features_to_add

BASE_DIR = Path(__file__).parent
HAIKU_MODEL = wd.HAIKU_MODEL
MIN_DESC_LEN = config.MIN_DESCRIPTION_LENGTH
MIN_SITE_TEXT = wd.MIN_SITE_TEXT
PUBLISH_TYPE = "Splash Pad"            # canonical, whitelisted; justified by verification

# Outscraper columns we are willing to carry forward. Everything else — crucially
# email / phone / whitepages / contact person data — is dropped at the door and
# NEVER published. Allowlist (not denylist) so a new PII column can't leak in.
SAFE_COLS = {
    "name", "city", "state", "us_state", "postal_code", "full_address", "address",
    "type", "subtypes", "category", "description", "about",
    "website", "site", "place_id", "google_id", "latitude", "longitude",
    # non-PII enrichment columns: photo, maps link, Google rating, reviews, hours
    "photo", "location_link", "rating", "reviews", "working_hours",
}

WATER_HINT = re.compile(
    r"splash|spray|water[ _-]?(play|feature|park)|wading|aquatic|wet play|"
    r"interactive (water|fountain)|fountain|wave pool", re.I)


# ── load + dedup + PII-strip ───────────────────────────────────────────────────

def load_extract(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    hdr = [str(x).strip().lower() if x else "" for x in next(rows)]
    out = []
    for r in rows:
        rec = {h: v for h, v in zip(hdr, r) if h in SAFE_COLS}  # PII-strip here
        if rec.get("name"):
            out.append(rec)
    wb.close()
    return out


def g(rec, k):
    return (rec.get(k) or "") if rec else ""


def _num(x, cast):
    try:
        return cast(float(str(x).strip()))
    except (TypeError, ValueError):
        return None


def _fmt_hours(raw):
    """Compress Google working_hours JSON to a readable string (consecutive
    identical days grouped). Returns None when unparseable or fully closed."""
    if not raw:
        return None
    try:
        d = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        return None
    if not isinstance(d, dict):
        return None
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    abbr = {"Monday": "Mon", "Tuesday": "Tue", "Wednesday": "Wed", "Thursday": "Thu",
            "Friday": "Fri", "Saturday": "Sat", "Sunday": "Sun"}
    vals = {}
    for day in days:
        v = d.get(day)
        if isinstance(v, list):
            v = ", ".join(str(x) for x in v)
        vals[day] = v if v else "Closed"
    if len(set(vals.values())) == 1:
        h = vals["Monday"]
        return None if h == "Closed" else f"Daily: {h}"
    parts, i = [], 0
    while i < 7:
        j = i
        while j + 1 < 7 and vals[days[j + 1]] == vals[days[i]]:
            j += 1
        label = abbr[days[i]] if i == j else f"{abbr[days[i]]}-{abbr[days[j]]}"
        parts.append(f"{label}: {vals[days[i]]}")
        i = j + 1
    return "; ".join(parts)


def _about_to_features(raw):
    """Map Google 'about' amenity flags (true-valued keys) to directory Feature tags."""
    if not raw:
        return []
    try:
        d = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        return []
    true_keys = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if v is True:
                    true_keys.append(str(k).lower())
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(d)
    text = " | ".join(true_keys)
    feats = set()
    if "wheelchair" in text or "accessible" in text:
        feats.add("Accessibility")
    if "parking" in text:
        feats.add("Parking")
    if "restroom" in text or "toilet" in text:
        feats.add("Restrooms")
    if "picnic" in text:
        feats.add("Picnic Area")
    if "playground" in text:
        feats.add("Playground")
    return sorted(feats)


def dedup_place(records):
    """Outscraper returns the same venue once per matching query (~3x). Keep first
    by place_id; fall back to jkey when place_id is missing."""
    seen, out = set(), []
    for r in records:
        key = str(g(r, "place_id")).strip() or gfd.join_key(g(r, "name"), g(r, "city"), g(r, "state"))
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def about_summary(rec):
    """Flatten the Google `about` JSON into a compact 'section: key, key' string of
    TRUE amenities, plus the Google editorial description. Anchors the LLM."""
    bits = []
    desc = str(g(rec, "description")).strip()
    if desc:
        bits.append(f"Google description: {desc}")
    sub = str(g(rec, "subtypes")).strip()
    if sub:
        bits.append(f"Google subtypes: {sub}")
    ab = g(rec, "about")
    try:
        d = json.loads(ab) if ab else {}
    except Exception:
        d = {}
    for section, kv in (d.items() if isinstance(d, dict) else []):
        if isinstance(kv, dict):
            true_keys = [k for k, v in kv.items() if v is True]
            if true_keys:
                bits.append(f"{section}: " + ", ".join(true_keys))
    return "\n".join(bits)


# ── verify + compose (Haiku) ───────────────────────────────────────────────────

VERIFY_CACHE = wd.CACHE_DIR / "ingest_verify"
VERIFY_CACHE.mkdir(parents=True, exist_ok=True)

VERIFY_SYSTEM = (
    "You vet candidate listings for a splash-pad directory. A keyword search "
    "(\"splash pad\", \"spray park\", etc., NOT exact-match) returned this venue, so "
    "MANY candidates are ordinary parks or playgrounds with NO water-play feature, "
    "and some have only a single incidental sprinkler. Using the venue's OWN website "
    "text plus its Google profile, classify its water play into exactly one tier:\n"
    " - \"dedicated\": water play is a primary, designed feature — a splash pad, "
    "sprayground, water playground, spray park, or a water park / aquatic center. "
    "Signals: MULTIPLE jets/nozzles, dumping buckets, interactive water structures, "
    "zero-depth/beach entry, water slides, or an area explicitly named a 'splash pad' "
    "/ 'sprayground' / 'water playground'.\n"
    " - \"incidental\": an ordinary playground or park whose ONLY water is a single "
    "sprinkler or one lone spray shower bolted on for cooling off — water play is a "
    "minor add-on, not the attraction. This is BELOW the directory's bar.\n"
    " - \"none\": no public water-play feature at all (or only a decorative, "
    "look-don't-touch fountain).\n"
    "Classify ONLY from explicit evidence in the provided text — never from the search "
    "query or the venue's name alone. When the only evidence is a single 'sprinkler' "
    "or one 'spray shower' with no other water feature, that is \"incidental\", NOT "
    "\"dedicated\". When in doubt between dedicated and incidental, choose incidental.\n"
    "If and ONLY if the tier is \"dedicated\", write an ORIGINAL 2-4 sentence directory "
    "description grounded only in the provided facts. Never copy sentences or "
    "distinctive phrases verbatim — paraphrase. Never invent facts. NEVER mention star "
    "ratings, review counts, or testimonials. No filler ('nestled', 'boasting', "
    "'state-of-the-art', 'hidden gem', 'fun for the whole family', 'make a splash'). "
    "Respond with strict JSON only."
)

VERIFY_SCHEMA = (
    'Return ONLY this JSON: {"water_play_tier": "dedicated"|"incidental"|"none", '
    '"confidence": "high"|"medium"|"low", '
    '"evidence": "the specific feature or phrase that determined the tier (empty if none)", '
    '"description": "2-4 sentence original description (empty unless tier is dedicated)"}'
)


def llm_verify(name, city, state, source_text, use_cache=True):
    key = hashlib.md5(f"V3|{name}|{city}|{state}|{source_text[:4000]}".encode()).hexdigest()
    cache_path = VERIFY_CACHE / f"{key}.json"
    if use_cache and cache_path.exists():
        return json.loads(cache_path.read_text())
    user = (
        f"Venue: {name}\nLocation: {city}, {state}\n\n"
        f"Evidence (Google profile + the venue's own website text):\n"
        f'"""\n{source_text[:7000]}\n"""\n\n{VERIFY_SCHEMA}'
    )
    try:
        msg = wd._client().messages.create(
            model=HAIKU_MODEL, max_tokens=600, system=VERIFY_SYSTEM,
            messages=[{"role": "user", "content": user}],
        )
        raw = re.sub(r"^```(?:json)?|```$", "", msg.content[0].text.strip(), flags=re.M).strip()
        data = json.loads(raw)
        data["_in"] = msg.usage.input_tokens
        data["_out"] = msg.usage.output_tokens
    except Exception as e:
        data = {"has_water_play": False, "confidence": "low", "evidence": "",
                "description": "", "error": str(e), "_in": 0, "_out": 0}
    cache_path.write_text(json.dumps(data))
    return data


def verify_candidate(rec, protected, use_cache):
    name, city, state = g(rec, "name"), g(rec, "city"), g(rec, "state")
    raw_url = str(g(rec, "website") or g(rec, "site")).strip()
    url = build.normalize_url(raw_url) if raw_url else ""
    out = {"name": name, "city": city, "state": state, "url": url,
           "type_google": g(rec, "type"), "verdict": "HOLD", "reason": "",
           "tier": "", "evidence": "", "confidence": "", "description": "", "site_chars": 0,
           "in": 0, "out": 0}

    crawl = wd.crawl_site(url, use_cache=use_cache) if url and wd.is_crawlable(url) else {"text": "", "status": "no-site"}
    site_text = crawl.get("text", "")
    out["site_chars"] = len(site_text)

    source = about_summary(rec)
    if site_text:
        source += f"\n\nVenue website text:\n{site_text}"

    res = llm_verify(name, city, state, source, use_cache=use_cache)
    out["in"], out["out"] = res.get("_in", 0), res.get("_out", 0)
    out["tier"] = (res.get("water_play_tier") or "none").strip().lower()
    out["evidence"] = (res.get("evidence") or "").strip()
    out["confidence"] = (res.get("confidence") or "").strip()
    desc = (res.get("description") or "").strip()
    out["description"] = desc

    if out["tier"] == "none":
        out["verdict"], out["reason"] = "REJECT", "no water-play feature"
        return out
    if out["tier"] == "incidental":
        out["verdict"], out["reason"] = "BELOW_BAR", "incidental water play (lone sprinkler/spray shower)"
        return out

    # tier == "dedicated" -> type it as Splash Pad and run the REAL gate
    fields = {"Name": name, "City": city, "State": state, "Type": PUBLISH_TYPE,
              "Website URL": url, "Admission": "", "Hours": ""}
    pad = gfd.pad_shape(fields, desc)
    hard = build.hard_exclusion_reason(pad)
    if hard:
        out["verdict"], out["reason"] = "HOLD", f"hard-excluded: {hard}"
        return out
    status, detail = build.evaluate_pad(pad, protected)
    if status == "ok" and out["confidence"] in ("high", "medium"):
        out["verdict"], out["reason"] = "PUBLISH", f"dedicated water play ({out['confidence']})"
    elif status == "ok":
        out["verdict"], out["reason"] = "HOLD", "dedicated but low confidence — needs eyeball"
    else:
        out["verdict"], out["reason"] = "HOLD", f"gate={status} ({detail})"
    return out


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("extract", help="path to the Outscraper .xlsx")
    ap.add_argument("--verify", action="store_true",
                    help="Stage B: crawl + Haiku-verify net-new candidates (dry, cached)")
    ap.add_argument("--limit", type=int, default=None, help="verify only the first N net-new candidates")
    ap.add_argument("--all", action="store_true", help="verify ALL net-new candidates")
    ap.add_argument("--refresh", action="store_true", help="ignore crawl/LLM caches")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--apply", action="store_true", help="Stage C: create Airtable records (GUARDED)")
    ap.add_argument("--i-have-confirmed-field-mapping", action="store_true",
                    help="required co-flag to actually run --apply")
    ap.add_argument("--select-file", default=None,
                    help="Stage C: file of 'Name|City|State|Type' lines selecting which "
                         "PUBLISH venues to create (Type optional, defaults to Splash Pad). "
                         "Omit to target the whole PUBLISH set.")
    args = ap.parse_args()
    use_cache = not args.refresh
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not os.path.exists(args.extract):
        sys.exit(f"extract not found: {args.extract}")

    # ── Stage A ──
    raw = load_extract(args.extract)
    uniq = dedup_place(raw)
    pads = build.get_pads()
    existing = {gfd.join_key(p.get("name"), p.get("city"), p.get("state")) for p in pads}
    net_new = [r for r in uniq if gfd.join_key(g(r, "name"), g(r, "city"), g(r, "state")) not in existing]
    crawlable = [r for r in net_new
                 if wd.is_crawlable(build.normalize_url(str(g(r, "website") or g(r, "site")).strip()))]
    water_hint = sum(1 for r in net_new
                     if WATER_HINT.search(" ".join([str(g(r, "about")), str(g(r, "description")), str(g(r, "subtypes"))])))

    print(f"\n{'='*68}\n  Outscraper ingestion  [{args.extract}]\n{'='*68}")
    print(f"Stage A — load / dedup / PII-strip / net-new (PII columns dropped at load)")
    print(f"  raw rows:                 {len(raw)}")
    print(f"  unique venues (place_id): {len(uniq)}")
    print(f"  already in directory:     {len(uniq) - len(net_new)}  (overlap = skeleton-backfill source)")
    print(f"  NET-NEW candidates:       {len(net_new)}")
    print(f"    with crawlable own-site:{len(crawlable)}")
    print(f"    with water hint in text:{water_hint}  (informational only — the website verify is the gate)")
    print(f"  net-new Google type mix:  " +
          ", ".join(f"{t}={c}" for t, c in Counter(g(r, 'type') for r in net_new).most_common()))

    cand_path = BASE_DIR / "data" / f"INGEST_CANDIDATES_{ts}.txt"
    with open(cand_path, "w", encoding="utf-8") as fh:
        fh.write(f"# {len(net_new)} net-new candidates from {os.path.basename(args.extract)}\n")
        fh.write("# name | city, state | google_type | water_hint | website\n")
        for r in sorted(net_new, key=lambda x: (g(x, "state"), g(x, "name"))):
            wh = "WATER" if WATER_HINT.search(" ".join([str(g(r, "about")), str(g(r, "description")), str(g(r, "subtypes"))])) else "-----"
            fh.write(f"{g(r,'name')} | {g(r,'city')}, {g(r,'state')} | {g(r,'type')} | {wh} | "
                     f"{build.normalize_url(str(g(r,'website') or g(r,'site')).strip())}\n")
    print(f"  wrote {cand_path.relative_to(BASE_DIR)}")

    if not args.verify:
        print("\nStage A only. Re-run with --verify --all (or --limit N) for the crawl+verify dry-run.")
        return

    # ── Stage B ──
    batch = net_new if args.all else net_new[: (args.limit or 10)]
    print(f"\nStage B — crawl + Haiku-verify {len(batch)} candidate(s)  [DRY, cache={'on' if use_cache else 'off'}]")
    protected = build._load_protected_pad_slugs()
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(verify_candidate, r, protected, use_cache): r for r in batch}
        for i, fut in enumerate(as_completed(futs), 1):
            results.append(fut.result())
            if i % 20 == 0:
                print(f"  ...{i}/{len(batch)}")

    verdicts = Counter(r["verdict"] for r in results)
    in_tok = sum(r["in"] for r in results); out_tok = sum(r["out"] for r in results)
    cost = in_tok * wd.PRICE_IN + out_tok * wd.PRICE_OUT
    billed = sum(1 for r in results if r["in"])
    print(f"\n=== VERDICTS ({len(results)} verified) ===")
    for v in ("PUBLISH", "HOLD", "BELOW_BAR", "REJECT"):
        print(f"  {v:8s} {verdicts.get(v,0)}")
    print(f"  LLM: {billed} live calls (rest cached), tokens in={in_tok:,} out={out_tok:,}, est ${cost:.4f}")

    md = BASE_DIR / "data" / f"INGEST_VERIFY_{ts}.md"
    with open(md, "w", encoding="utf-8") as fh:
        fh.write(f"# Ingestion verify — {os.path.basename(args.extract)} — {ts}\n\n")
        fh.write(f"PUBLISH {verdicts.get('PUBLISH',0)} · HOLD {verdicts.get('HOLD',0)} · "
                 f"REJECT {verdicts.get('REJECT',0)}  (of {len(results)} net-new verified)\n")
        for v in ("PUBLISH", "HOLD", "BELOW_BAR", "REJECT"):
            grp = [r for r in results if r["verdict"] == v]
            fh.write(f"\n---\n# {v} ({len(grp)})\n")
            for r in sorted(grp, key=lambda x: (x["state"], x["name"])):
                fh.write(f"\n## {r['name']} — {r['city']}, {r['state']} "
                         f"_(google:{r['type_google']} · {r['reason']})_\n")
                fh.write(f"- **Site:** {r['url']}  ({r['site_chars']} chars crawled)\n")
                if r["evidence"]:
                    fh.write(f"- **Water evidence:** {r['evidence']}\n")
                if r["description"]:
                    fh.write(f"- **Proposed:** {r['description']}\n")
    print(f"  wrote {md.relative_to(BASE_DIR)}")

    print("\n=== SAMPLE PUBLISH (first 5) ===")
    for r in [r for r in results if r["verdict"] == "PUBLISH"][:5]:
        print(f"\n[{r['name']} — {r['city']},{r['state']}]  evidence: {r['evidence'][:80]}")
        print(f"   {r['description']}")
    print("\n=== SAMPLE BELOW_BAR (incidental water — lone sprinkler, deliberately skipped) ===")
    for r in [r for r in results if r["verdict"] == "BELOW_BAR"][:5]:
        print(f"  {r['name']} — {r['city']},{r['state']}  evidence: {r['evidence'][:70]}")
    print("\n=== SAMPLE REJECT (first 5 — confirm these really aren't splash pads) ===")
    for r in [r for r in results if r["verdict"] == "REJECT"][:5]:
        print(f"  {r['name']} — {r['city']},{r['state']}  (google:{r['type_google']})")

    if not args.apply:
        print("\nDRY RUN — nothing written to Airtable.")
        return

    # ── Stage C — create Airtable records for a SELECTED subset of PUBLISH ──
    # build.fetch_from_airtable() hard-skips these name prefixes at render time;
    # creating them would just clutter the table, so block them here too.
    OFF_TOPIC_PREFIXES = ("Six Flags", "Great Wolf Lodge", "Kings Island",
                          "Kings Dominion", "Kroger Aquatic Center", "Rivertown")
    publish = [r for r in results if r["verdict"] == "PUBLISH"]

    sel = {}  # jkey -> Type ; empty select-file means "whole PUBLISH set"
    if args.select_file:
        for line in Path(args.select_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 3:
                continue
            ty = parts[3] if len(parts) > 3 and parts[3] else PUBLISH_TYPE
            sel[gfd.join_key(parts[0], parts[1], parts[2])] = ty
        publish = [r for r in publish
                   if gfd.join_key(r["name"], r["city"], r["state"]) in sel]

    rec_by_key = {gfd.join_key(g(r, "name"), g(r, "city"), g(r, "state")): r for r in uniq}
    existing_slugs = {p.get("slug") for p in pads}

    payloads, blocked = [], []
    for r in publish:
        k = gfd.join_key(r["name"], r["city"], r["state"])
        ty = sel.get(k, PUBLISH_TYPE)
        rec = rec_by_key.get(k, {})
        raw_url = str(g(rec, "website") or g(rec, "site")).strip() or r["url"]
        url = build.normalize_url(raw_url) if raw_url else ""
        desc = r["description"]
        fields = {"Name": r["name"], "City": r["city"], "State": r["state"],
                  "Type": ty, "Website URL": url, "Description": desc}
        addr = str(g(rec, "address") or g(rec, "full_address")).strip()
        if addr:
            fields["Address"] = addr
        zc = str(g(rec, "postal_code")).strip()
        if zc:
            fields["Zip"] = zc
        for col, fld in (("latitude", "Latitude"), ("longitude", "Longitude")):
            try:
                fields[fld] = float(str(g(rec, col)).strip())
            except (TypeError, ValueError):
                pass
        # ── enrichment: non-PII extract data + sensible defaults ──
        photo = str(g(rec, "photo")).strip()
        if photo:
            fields["Photo URL"] = photo
        maps = str(g(rec, "location_link")).strip()
        if maps:
            fields["Google Maps URL"] = maps
        rt = _num(g(rec, "rating"), float)
        if rt is not None:
            fields["Rating"] = round(rt, 1)
        rv = _num(g(rec, "reviews"), int)
        if rv is not None:
            fields["Review Count"] = rv
        hrs = _fmt_hours(g(rec, "working_hours"))
        if hrs:
            fields["Hours"] = hrs
        feats = sorted(set(_about_to_features(g(rec, "about"))) |
                       set(features_to_add(r["name"], ty, [])))
        if feats:
            fields["Features"] = feats
        if ty == PUBLISH_TYPE:   # Free for splash pads; blank for paid types (Aquatic Center / Water Park)
            fields["Admission"] = "Free"
        fields["Age Range"] = ["Toddlers", "Kids", "Families"]
        slug = gfd.pad_shape(fields, desc)["slug"]
        reason = None
        if k in existing:
            reason = "already in directory (would duplicate)"
        elif any(r["name"].startswith(p) for p in OFF_TOPIC_PREFIXES):
            reason = "off-topic name prefix — build.py skips it at render"
        elif slug in existing_slugs:
            reason = "slug collision with an existing pad"
        elif not desc or len(desc) < MIN_DESC_LEN:
            reason = f"description {len(desc)} chars (< {MIN_DESC_LEN})"
        else:
            pad = gfd.pad_shape(fields, desc)
            hard = build.hard_exclusion_reason(pad)
            st, detail = build.evaluate_pad(pad, protected)
            if hard:
                reason = f"hard-excluded: {hard}"
            elif st != "ok":
                reason = f"gate={st} ({detail})"
        (blocked if reason else payloads).append((fields, slug, reason))

    print(f"\n{'='*68}\n  Stage C — CREATE preview  ({len(payloads)} ready · {len(blocked)} blocked)\n{'='*68}")
    for fields, slug, _ in payloads:
        print(f"\n  /pad/{slug}   [Type: {fields['Type']} · Status: Active (build default)]")
        print(f"    Name    : {fields['Name']}")
        print(f"    City/St : {fields['City']}, {fields['State']}")
        if fields.get("Address"):
            print(f"    Address : {fields['Address']}")
        loc = []
        if fields.get("Zip"):
            loc.append(f"Zip {fields['Zip']}")
        if fields.get("Latitude") is not None and fields.get("Longitude") is not None:
            loc.append(f"({fields['Latitude']}, {fields['Longitude']})")
        if loc:
            print(f"    Geo     : {'  '.join(loc)}")
        print(f"    Website : {fields['Website URL']}")
        if fields.get("Photo URL"):
            print(f"    Photo   : {str(fields['Photo URL'])[:58]}")
        if fields.get("Google Maps URL"):
            print(f"    Maps    : {str(fields['Google Maps URL'])[:58]}")
        meta = []
        if fields.get("Rating") is not None:
            meta.append(f"{fields['Rating']}★ ({fields.get('Review Count', 0)} reviews)")
        if fields.get("Admission"):
            meta.append(f"Admission: {fields['Admission']}")
        if meta:
            print(f"    Meta    : {' · '.join(meta)}")
        if fields.get("Hours"):
            print(f"    Hours   : {fields['Hours']}")
        if fields.get("Features"):
            print(f"    Features: {', '.join(fields['Features'])}")
        if fields.get("Age Range"):
            print(f"    Age     : {', '.join(fields['Age Range'])}")
        print(f"    Desc    : {fields['Description']}")
    for fields, slug, reason in blocked:
        print(f"\n  BLOCKED  {fields['Name']} — {fields['City']}, {fields['State']}: {reason}")

    if not args.__dict__["i_have_confirmed_field_mapping"]:
        print("\n--apply REFUSED (preview only): creating new Airtable source-of-truth rows is "
              "AdSense-sensitive. Review the field mapping above; re-run adding "
              "--i-have-confirmed-field-mapping to write.")
        return
    if not payloads:
        print("\nNothing to create.")
        return

    from pyairtable import Api
    table = Api(config.AIRTABLE_API_KEY).table(config.AIRTABLE_BASE_ID, config.AIRTABLE_TABLE_NAME)
    pre = [{"id": rr["id"], "Name": rr["fields"].get("Name", ""),
            "City": rr["fields"].get("City", ""), "State": rr["fields"].get("State", ""),
            "Status": rr["fields"].get("Status", "")} for rr in table.all()]
    backup_path = BASE_DIR / "data" / f"ingest_pre_apply_backup_{ts}.json"
    backup_path.write_text(json.dumps(pre, ensure_ascii=False, indent=2))
    print(f"\nBacked up {len(pre)} existing records -> {backup_path.relative_to(BASE_DIR)}")

    created = table.batch_create([fields for fields, _, _ in payloads], typecast=True)
    new_ids = [c["id"] for c in created]
    applied = BASE_DIR / "data" / f"INGEST_APPLIED_{ts}.md"
    with open(applied, "w", encoding="utf-8") as fh:
        fh.write(f"# Stage C applied — {len(created)} records created — {ts}\n\n")
        for c, (fields, slug, _) in zip(created, payloads):
            fh.write(f"## {fields['Name']} — {fields['City']}, {fields['State']}\n")
            fh.write(f"- airtable_id: {c['id']}\n- slug: /pad/{slug}\n")
            fh.write(f"- Type: {fields['Type']} · Status: Active (build default)\n")
            fh.write(f"- Website: {fields['Website URL']}\n")
            fh.write(f"- Description: {fields['Description']}\n\n")
    print(f"\nCreated {len(created)} records. New ids: {new_ids}")
    print(f"Audit -> {applied.relative_to(BASE_DIR)}")
    print("\nNext: `python3 build.py` locally to confirm the pages render & are indexable, then deploy.")
    print(f"Undo: delete these record ids in Airtable -> {new_ids}")


if __name__ == "__main__":
    main()
