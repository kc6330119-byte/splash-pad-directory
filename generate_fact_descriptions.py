#!/usr/bin/env python3
"""
generate_fact_descriptions.py — fact-grounded splash-pad listing descriptions.

Phase 1 of the AdSense "Low Value Content" remediation (see DGL Files/
ADSENSE_REMEDIATION_PLAYBOOK.md). Replaces the hash-seeded spintax approach
(enrich_descriptions.py) with prose assembled ONLY from facts that are true for
that specific listing, joined from two sources:

  - Airtable structured fields: Type, Admission/Price, Features, Age Range.
  - Outscraper `about` attribute JSON + `working_hours`, joined by normalized
    name+city+state (DGL Files/Outscraper-*.xlsx). This adds the distinguishing
    facts the Airtable fields lack: water attractions (lazy river, wave pool,
    water slides), real amenities (lockers, cabanas, picnic tables, arcade,
    barbecue grills), accessibility, parking, payments, pets, ownership identity,
    discounts, and operating days. ~84% of listings join.

There is NO synonym shuffling, NO climate/filler sentences, and NO rating/review
sentence (this site strips rating claims — build.clean_description). Variation
comes only from real differing facts, which removes the scaled-content spam
signal. There is no length padding: listings whose honest facts fall under the
gate (build.evaluate_pad) stay short and get noindexed on purpose, shrinking the
indexed surface to genuinely fact-rich pages.

Phase 2 (website_descriptions.py) crawls each listing's own site for original
per-page value and falls back to this description.

Safety:
  - dry-run by default; --apply required to write Airtable.
  - ONLY updates the existing "Description" field; never inserts records.
  - before the first --apply, backs up every current Description to a timestamped
    JSON keyed by record id (data/description_backup_<ts>.json).
  - reuses build.evaluate_pad so the dry-run projection == the real build gate.

Usage:
  python3 generate_fact_descriptions.py                 # dry run: stats + samples
  python3 generate_fact_descriptions.py --limit 50      # dry run on first 50
  python3 generate_fact_descriptions.py --apply         # write "Description"
"""
import os
import re
import sys
import glob
import json
import argparse
import threading
from collections import Counter
from datetime import datetime
from pathlib import Path

import openpyxl
from dotenv import load_dotenv
from pyairtable import Api
from slugify import slugify

import config
import build  # reused for the gate: clean_description, evaluate_pad, etc.

# Empty-key guard (the playbook gotcha): a shell may export an EMPTY var that
# shadows the real key in .env, so check for blank, not just missing.
load_dotenv(Path(__file__).parent / ".env", override=True)
_KEY = (os.environ.get("AIRTABLE_API_KEY") or "").strip()
_BASE = (os.environ.get("AIRTABLE_BASE_ID") or "").strip()
_TABLE = (os.environ.get("AIRTABLE_TABLE_NAME") or "SplashPads").strip()

DESC_FIELD = "Description"
BASE_DIR = Path(__file__).parent
BACKUP_DIR = BASE_DIR / "data"
SAMPLE_FILE = BACKUP_DIR / "FACT_DESCRIPTIONS_SAMPLE.md"
OUTSCRAPER_GLOB = str(BASE_DIR / "DGL Files" / "Outscraper-*.xlsx")

# Neutral phrase when the Type field is absent (~68% of records). build.py
# defaults missing Type to "Splash Pad" for the gate, but we won't over-claim a
# specific type in prose — "a water play area" is true for everything here.
TYPE_PHRASE = {
    "Splash Pad": "a splash pad",
    "Water Park": "a water park",
    "Aquatic Center": "an aquatic center",
    "Indoor Water Play": "an indoor water play facility",
    "Campground Water Park": "a campground with on-site water play",
    "Resort Water Park": "a resort water park",
    "Amusement Park": "an amusement park with water attractions",
}
DEFAULT_TYPE_PHRASE = "a water play area"
WATER_TYPES = {"Water Park", "Aquatic Center", "Resort Water Park",
               "Campground Water Park", "Indoor Water Play"}

# Outscraper "Activities" attribute -> attraction phrase (water + recreation).
ACTIVITY_MAP = [
    ("lazy river", "a lazy river"),
    ("wave pool", "a wave pool"),
    ("mini golf", "mini golf"),
    ("go karts", "go-karts"),
    ("touch tank", "a touch tank"),
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
NUMWORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}


# ── text helpers ───────────────────────────────────────────────────────────────

def norm(s):
    if s is None:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", str(s).strip().lower()))


def join_key(n, c, s):
    return f"{norm(n)}|{norm(c)}|{norm(s)}"


def oxford(items):
    items = [i for i in items if i]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


def _as_list(v):
    if v is None:
        return []
    if isinstance(v, str):
        return [x.strip() for x in v.split(",")] if v.strip() else []
    return list(v)


# ── Outscraper `about` join (lazy-loaded once, thread-safe) ─────────────────────

_about_idx = None
_about_lock = threading.Lock()
# normalized header names we read (norm() drops underscores: working_hours->workinghours)
_COL = {"name": "name", "city": "city", "state": "state",
        "about": "about", "hours": "workinghours"}


def _read_outscraper():
    idx = {}
    for path in sorted(glob.glob(OUTSCRAPER_GLOB)):
        try:
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        except Exception:
            continue
        ws = wb.active
        rows = ws.iter_rows(values_only=True)
        try:
            header = [norm(x) for x in next(rows)]
        except StopIteration:
            wb.close()
            continue
        ci = {h: i for i, h in enumerate(header)}
        if "name" not in ci or "about" not in ci:
            wb.close()
            continue

        def cell(row, col):
            i = ci.get(_COL[col])
            return row[i] if i is not None and i < len(row) else None

        for row in rows:
            name = cell(row, "name")
            if not name:
                continue
            about = cell(row, "about")
            hours = cell(row, "hours")
            k = join_key(name, cell(row, "city"), cell(row, "state"))
            cur = idx.setdefault(k, {"about": "", "hours": ""})
            if isinstance(about, str) and about.strip() and len(about) > len(cur["about"]):
                cur["about"] = about
            if isinstance(hours, str) and hours.strip() and not cur["hours"]:
                cur["hours"] = hours
        wb.close()
    return idx


def about_index():
    global _about_idx
    if _about_idx is None:
        with _about_lock:
            if _about_idx is None:
                _about_idx = _read_outscraper()
    return _about_idx


def parse_about(raw):
    """Flatten about JSON -> {norm(category): set(norm(true-attr))}."""
    try:
        d = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        return {}
    if not isinstance(d, dict):
        return {}
    out = {}
    for cat, attrs in d.items():
        s = set()
        if isinstance(attrs, dict):
            s = {norm(a) for a, v in attrs.items() if v is True}
        elif isinstance(attrs, list):
            s = {norm(x) for x in attrs}
        if s:
            out[norm(cat)] = s
    return out


def about_for(fields):
    """Return (parsed_about_dict, working_hours_raw) for one Airtable record."""
    rec = about_index().get(join_key(fields.get("Name"), fields.get("City"), fields.get("State")))
    if not rec:
        return {}, ""
    return parse_about(rec["about"]), rec["hours"]


def _trues(about, cat):
    return about.get(norm(cat), set())


def _has(about, cat, token):
    return any(token in a for a in _trues(about, cat))


def hours_clause(airtable_hours, hours_json):
    h = (airtable_hours or "").strip()
    if h.lower().startswith("daily"):
        return "It is open daily."
    if hours_json:
        try:
            d = json.loads(hours_json)
        except Exception:
            d = {}
        if isinstance(d, dict):
            open_days = [day for day in DAYS
                         if isinstance(d.get(day), list) and d.get(day)
                         and not any("close" in str(x).lower() for x in d[day])]
            n = len(open_days)
            if n == 7:
                return "It is open seven days a week."
            if n >= 1:
                base = (f"It is open {NUMWORD.get(n, n)} days a week"
                        if n > 1 else "It is open one day a week")
                if "Saturday" in open_days and "Sunday" in open_days:
                    base += ", including weekends"
                elif "Saturday" in open_days:
                    base += ", including Saturdays"
                return base + "."
    return ""


# ── compose ─────────────────────────────────────────────────────────────────────

def compose(fields):
    """Assemble an only-true-facts description from one record's fields + about join."""
    name = (fields.get("Name") or "").strip()
    if not name:
        return ""
    city = (fields.get("City") or "").strip()
    state = (fields.get("State") or "").strip()
    typ = (fields.get("Type") or "").strip()
    phrase = TYPE_PHRASE.get(typ, DEFAULT_TYPE_PHRASE)
    loc = ", ".join(x for x in (city, state) if x)
    about, hours_raw = about_for(fields)
    feats = {norm(x) for x in _as_list(fields.get("Features"))}

    S = [f"{name} is {phrase}" + (f" in {loc}." if loc else ".")]

    # ownership identity
    own = []
    for a in _trues(about, "from the business") | _trues(about, "other"):
        if "womenowned" in a:
            own.append("women-owned")
        elif "veteranowned" in a:
            own.append("veteran-owned")
        elif "lgbtq" in a and "owned" in a:
            own.append("LGBTQ+-owned")
        elif "asianowned" in a:
            own.append("Asian-owned")
        elif "latinoowned" in a:
            own.append("Latino-owned")
        elif "blackowned" in a:
            own.append("Black-owned")
        elif "indigenousowned" in a:
            own.append("Indigenous-owned")
        elif "disabledowned" in a:
            own.append("disabled-owned")
        elif "small business" in a:
            own.append("a small business")
    own = list(dict.fromkeys(own))
    if own:
        S.append(f"It identifies as {oxford(own)}.")

    # admission + planning
    adm = (fields.get("Admission") or "").strip()
    price = (fields.get("Price") or "").strip()
    price_ok = price and len(price) <= 40 and not any(c in price for c in ("{", "[", "http"))
    if adm == "Free":
        S.append("Admission is free.")
    elif adm == "Paid" and price_ok:
        S.append(f"Admission is {price}.")
    elif adm == "Paid":
        S.append("It is a paid facility.")
    elif adm == "Seasonal Pass":
        S.append("Access is available with a seasonal pass.")
    if _has(about, "planning", "membership required"):
        S.append("Membership is required.")
    elif _has(about, "planning", "appointment required"):
        S.append("Reservations are required.")
    elif _has(about, "planning", "tickets in advance"):
        S.append("Buying tickets in advance is recommended.")

    # water attractions / activities
    water_ctx = (_has(about, "activities", "lazy river") or _has(about, "activities", "wave pool")
                 or typ in WATER_TYPES
                 or any(t in feats for t in ("water park", "water slides", "splash")))
    acts = [label for token, label in ACTIVITY_MAP if _has(about, "activities", token)]
    if _has(about, "amenities", "slides") and water_ctx:
        acts.append("water slides")
    acts = list(dict.fromkeys(acts))
    if acts:
        S.append(f"On-site attractions include {oxford(acts)}.")

    # amenities (merge about + Airtable Features), deduped, fixed order
    amen = []

    def add(p):
        if p and p not in amen:
            amen.append(p)
    if "restrooms" in feats or _has(about, "amenities", "restroom"):
        add("restrooms")
    if _has(about, "amenities", "restaurant"):
        add("an on-site restaurant")
    elif _has(about, "offerings", "food") or "snack bar" in feats or "concessions" in feats:
        add("food service")
    if _has(about, "offerings", "arcade"):
        add("an arcade")
    if _has(about, "amenities", "picnic tables") or "picnic area" in feats:
        add("picnic areas")
    if "shade" in feats:
        add("shaded seating")
    if _has(about, "amenities", "lockers"):
        add("lockers")
    if "changing room" in feats:
        add("changing rooms")
    if _has(about, "amenities", "cabana"):
        add("cabana rentals")
    if _has(about, "amenities", "barbecue grill"):
        add("barbecue grills")
    if _has(about, "amenities", "bar onsite"):
        add("an on-site bar")
    if _has(about, "amenities", "basketball court"):
        add("a basketball court")
    if _has(about, "offerings", "gift shop"):
        add("a gift shop")
    if _has(about, "offerings", "sauna"):
        add("a sauna")
    if "playground" in feats or _has(about, "children", "playground"):
        add("an adjacent playground")
    if "lifeguard" in feats:
        add("lifeguards on duty")
    if _has(about, "offerings", "rv camping") or _has(about, "offerings", "rv water hookup"):
        add("RV camping with hookups")
    if _has(about, "amenities", "wifi"):
        add("Wi-Fi")
    if _has(about, "amenities", "party services"):
        add("party services")
    if amen:
        S.append(f"On-site amenities include {oxford(amen)}.")

    # accessibility
    acc = []
    if _has(about, "accessibility", "wheelchair accessible entrance") or "accessibility" in feats:
        acc.append("entrances")
    if _has(about, "accessibility", "wheelchair accessible parking"):
        acc.append("parking")
    if _has(about, "accessibility", "wheelchair accessible restroom"):
        acc.append("restrooms")
    if acc:
        S.append(f"It offers wheelchair-accessible {oxford(acc)}.")

    # parking + payments
    park = ""
    if _has(about, "parking", "free"):
        park = "free parking"
    elif _has(about, "parking", "paid"):
        park = "paid parking"
    pays = []
    if _has(about, "payments", "credit"):
        pays.append("credit cards")
    if _has(about, "payments", "debit"):
        pays.append("debit cards")
    if _has(about, "payments", "nfc") or _has(about, "payments", "mobile"):
        pays.append("mobile payments")
    if park and pays:
        S.append(f"The venue provides {park} and accepts {oxford(pays)}.")
    elif park:
        S.append(f"The venue provides {park}.")
    elif pays:
        S.append(f"It accepts {oxford(pays)}.")

    # pets
    if _has(about, "pets", "dog park"):
        S.append("There is a dog park on site.")
    elif _has(about, "pets", "dogs allowed"):
        S.append("Dogs are allowed.")

    # highlights
    hi = []
    if _has(about, "highlights", "military discount"):
        hi.append("active-military discounts")
    if _has(about, "highlights", "live performance") or _has(about, "highlights", "live music"):
        hi.append("live performances")
    if hi:
        S.append(f"It features {oxford(hi)}.")

    # crowd
    crowd = []
    if _has(about, "crowd", "lgbtq"):
        crowd.append("LGBTQ+ friendly")
    if _has(about, "crowd", "transgender"):
        crowd.append("a transgender safe space")
    if crowd:
        S.append(f"The venue is described as {oxford(crowd)}.")

    # hours
    hc = hours_clause(fields.get("Hours"), hours_raw)
    if hc:
        S.append(hc)

    # age — only the distinguishing values
    ages = {str(x).strip() for x in _as_list(fields.get("Age Range"))}
    if "Toddlers" in ages:
        S.append("It includes gentler water features suited to toddlers.")
    elif "All Ages" in ages:
        S.append("The water play is designed for visitors of all ages.")

    return " ".join(S)


def pad_shape(fields, new_desc):
    """Build the dict build.evaluate_pad expects, mirroring build.fetch_from_airtable."""
    name = fields.get("Name", "")
    city = fields.get("City", "")
    return {
        "slug": slugify(f"{name}-{city}"),
        "name": name,
        "city": city,
        "state": fields.get("State", ""),
        "description": new_desc,
        "type": fields.get("Type", "Splash Pad"),  # mirror build's default
        "admission": fields.get("Admission", ""),
        "price": fields.get("Price", ""),
        "hours": fields.get("Hours", ""),
        "website_url": fields.get("Website URL", ""),
        "google_maps_url": fields.get("Google Maps URL", ""),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the Description field in Airtable")
    ap.add_argument("--limit", type=int, default=None, help="process only the first N records (dry-run preview)")
    args = ap.parse_args()

    if not _KEY or not _BASE:
        sys.exit("Missing/empty AIRTABLE_API_KEY or AIRTABLE_BASE_ID in .env")

    idx = about_index()
    print(f"Loaded Outscraper about index: {len(idx)} keyed venues "
          f"from {OUTSCRAPER_GLOB}")

    table = Api(_KEY).table(_BASE, _TABLE)
    recs = [r for r in table.all() if r["fields"].get("Status") != "Draft"]
    if args.limit:
        recs = recs[: args.limit]
    protected = build._load_protected_pad_slugs()
    raised_bar = 250  # candidate raised gate, shown alongside the live gate

    rows = []          # (id, name, new_desc, new_len, status_new, status_cur, cur_len, has_about)
    excluded = 0
    for r in recs:
        f = r["fields"]
        name = f.get("Name", "")
        if not name:
            continue
        new_desc = compose(f)
        pad_new = pad_shape(f, new_desc)
        if build.hard_exclusion_reason(pad_new):  # off-topic / PAD_EXCLUDE_SLUGS — build drops these
            excluded += 1
            continue
        cur_clean = build.clean_description(f.get("Description", "") or "")
        status_new, _ = build.evaluate_pad(pad_new, protected)
        pad_cur = dict(pad_new, description=cur_clean)
        status_cur, _ = build.evaluate_pad(pad_cur, protected)
        has_about = bool(about_for(f)[0])
        rows.append((r["id"], name, new_desc, len(new_desc), status_new, status_cur,
                     len(cur_clean), has_about))

    n = len(rows)
    if n == 0:
        sys.exit("No records to process.")

    lengths = sorted(x[3] for x in rows)
    pct = lambda p: lengths[min(n - 1, int(p * n))]
    cur_ok = sum(1 for x in rows if x[5] == "ok")
    new_ok = sum(1 for x in rows if x[4] == "ok")
    new_ok_250 = sum(1 for x in rows if x[4] == "ok" and x[3] >= raised_bar)
    gained = sum(1 for x in rows if x[5] != "ok" and x[4] == "ok")
    lost = sum(1 for x in rows if x[5] == "ok" and x[4] != "ok")
    about_hits = sum(1 for x in rows if x[7])
    noindex_reasons = Counter(x[4] for x in rows if x[4] != "ok")

    print(f"\n{'='*64}")
    print(f"  Fact-grounded descriptions  [{'APPLY' if args.apply else 'DRY RUN'}]")
    print(f"{'='*64}")
    print(f"Records processed: {n}   (hard-excluded, not touched: {excluded})")
    print(f"about-join coverage: {about_hits}/{n} ({100*about_hits/n:.0f}%)")
    print(f"\nNEW description length:")
    print(f"  min={lengths[0]} p10={pct(.10)} p25={pct(.25)} median={pct(.5)} "
          f"p75={pct(.75)} p90={pct(.9)} max={lengths[-1]}")
    print(f"\nIndexable (build.evaluate_pad == 'ok'):")
    print(f"  CURRENT descriptions: {cur_ok}/{n} ({100*cur_ok/n:.0f}%)")
    print(f"  NEW @ live gate ({config.MIN_DESCRIPTION_LENGTH} chars): {new_ok}/{n} ({100*new_ok/n:.0f}%)")
    print(f"  NEW @ raised gate ({raised_bar} chars):  {new_ok_250}/{n} ({100*new_ok_250/n:.0f}%)")
    print(f"\nTransition under NEW descriptions (live gate):")
    print(f"  stay indexed: {cur_ok - lost}    newly indexed (gain): {gained}    "
          f"newly noindexed (regression): {lost}")
    if noindex_reasons:
        print("  new-noindex reasons: " + ", ".join(f"{k}={v}" for k, v in noindex_reasons.most_common()))

    # Samples across the information-density spectrum
    by_len = sorted(rows, key=lambda x: x[3])
    picks = [by_len[int(p * (n - 1))] for p in (0.05, 0.25, 0.45, 0.65, 0.85, 0.98)]
    BACKUP_DIR.mkdir(exist_ok=True)
    review = ["# Fact-grounded description samples (Phase 1, splash pads)\n",
              f"_Generated {datetime.now().isoformat(timespec='seconds')} — {n} records, "
              f"live gate {config.MIN_DESCRIPTION_LENGTH} chars._\n"]
    print(f"\n===== SAMPLES (low -> high information density) =====")
    for _id, name, text, L, snew, scur, _cl, _ha in picks:
        tag = "INDEX" if snew == "ok" else f"noindex:{snew}"
        print(f"\n[{L} chars | {tag}] {name}\n{text}")
        review.append(f"## {name}  _({L} chars, {tag})_\n\n{text}\n")
    SAMPLE_FILE.write_text("\n".join(review))
    print(f"\nWrote review file: {SAMPLE_FILE}")

    # Show a few regressions explicitly so the indexing impact is transparent
    regressions = [x for x in rows if x[5] == "ok" and x[4] != "ok"]
    if regressions:
        print(f"\n===== {len(regressions)} REGRESSIONS (were indexed, now noindexed) — first 5 =====")
        for _id, name, text, L, snew, scur, cl, _ha in regressions[:5]:
            print(f"\n[{cl}->{L} chars | {snew}] {name}\n{text}")

    if not args.apply:
        print("\nDRY RUN — nothing written. Re-run with --apply to write the Description field.")
        return

    # --- APPLY ---
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"description_backup_{ts}.json"
    backup = {r["id"]: (r["fields"].get("Description", "") or "")
              for r in recs if r["fields"].get("Name")}
    backup_path.write_text(json.dumps(backup, ensure_ascii=False, indent=2))
    print(f"\nBacked up {len(backup)} current descriptions -> {backup_path}")

    updates = [{"id": _id, "fields": {DESC_FIELD: text}}
               for _id, _name, text, _L, _sn, _sc, _cl, _ha in rows if text]
    print(f"--apply: writing {len(updates)} Description fields ...")
    for i in range(0, len(updates), 10):
        table.batch_update(updates[i:i + 10])
        print(f"  updated {min(i+10, len(updates))}/{len(updates)}")
    print("Done. Run python3 build.py locally to regenerate, then verify before deploy.")


if __name__ == "__main__":
    main()
