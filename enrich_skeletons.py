#!/usr/bin/env python3
"""
enrich_skeletons.py — rewrite Phase-1 "skeleton" fallback descriptions.

Target: live pads whose Description still opens with the templated skeleton
("<Name> is a water play area in <City>, <State>…") AND that have Google's own
venue summary (the `description` column in the Outscraper exports under
"DGL Files/") AND water evidence in that summary.

For each, Haiku writes ONE original, fact-bounded paragraph from (a) Google's
summary — paraphrased, never verbatim — and (b) verified attributes from the
Airtable record + Outscraper `about` join. Guards (2026-05-30 dry-run lessons):
  * never feed Age Range (it fabricated toddler claims on non-water venues)
  * never claim splash pad / water play without explicit source evidence
  * paraphrase check: no 8-word verbatim overlap with Google's text
Every output re-passes build.hard_exclusion_reason + build.evaluate_pad.

Usage:
  python3 enrich_skeletons.py              # dry run: cohort stats only (no API)
  python3 enrich_skeletons.py --sample 6   # generate 6 proposals, print, no writes
  python3 enrich_skeletons.py --apply      # backup all Descriptions, write Airtable
"""
import argparse
import datetime
import glob
import json
import pathlib
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import openpyxl
from dotenv import load_dotenv

import build
import config
import generate_fact_descriptions as gfd

MODEL = "claude-haiku-4-5-20251001"
SKELETON_RE = re.compile(r"\bis a water play area in\b", re.I)
WATER_RE = re.compile(
    r"\b(splash|spray|water\s*play|water\s*park|waterpark|aquatic|pool|wading|"
    r"lazy\s+river|water\s*slide|slides|swim|fountain|sprayground|water\s*feature)\b", re.I)
BANNED = ["nestled", "hidden gem", "look no further", "whether you"]

SYSTEM = ("You write factual venue descriptions for a U.S. family-outings "
          "directory. You never invent facts, and you never copy source phrasing.")


def google_desc_index():
    """join_key -> longest Google `description` across the Outscraper exports."""
    idx = {}
    for path in sorted(glob.glob(gfd.OUTSCRAPER_GLOB)):
        try:
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        except Exception:
            continue
        ws = wb.active
        rows = ws.iter_rows(values_only=True)
        try:
            header = [gfd.norm(x) for x in next(rows)]
        except StopIteration:
            wb.close()
            continue
        ci = {h: i for i, h in enumerate(header)}
        if "name" not in ci or "description" not in ci:
            wb.close()
            continue

        def cell(row, col):
            i = ci.get(col)
            return row[i] if i is not None and i < len(row) else None

        for row in rows:
            name = cell(row, "name")
            if not name:
                continue
            desc = cell(row, "description")
            if not isinstance(desc, str) or len(desc.strip()) < 40:
                continue
            k = gfd.join_key(name, cell(row, "city"), cell(row, "state"))
            if len(desc) > len(idx.get(k, "")):
                idx[k] = desc.strip()
        wb.close()
    return idx


def facts_for(pad):
    """Verified-attribute block.

    Deliberately excludes Age Range AND the Airtable `type` field (5/30 + 6/09
    lessons): both are first-party claims that stamped fabricated water-play
    text onto mistyped records. Only third-party-verifiable attributes
    (Google `about` join, features, hours, admission) reach the model.
    """
    fields = {"Name": pad.get("name"), "City": pad.get("city"), "State": pad.get("state")}
    about, _ = gfd.about_for(fields)
    lines = []
    if str(pad.get("admission") or "").strip():
        lines.append(f"Admission: {pad['admission']}")
    feats = [str(f) for f in (pad.get("features") or []) if str(f).strip()]
    if feats:
        lines.append("Verified amenities: " + ", ".join(feats[:10]))
    for cat, attrs in sorted(about.items()):
        if any(k in cat for k in ("water", "amenit", "access", "highlight", "kid", "child")):
            lines.append(f"{cat.title()}: " + ", ".join(sorted(attrs)[:8]))
    hours = str(pad.get("hours") or "").strip()
    if hours:
        lines.append("Hours: " + hours[:160])
    return "\n".join(lines) if lines else "(none beyond the Google summary)"


def water_evidence(pad, gdesc):
    """True only when a third-party-verifiable source mentions water play:
    the venue's own name, Google's summary, or the Google about/features join.
    The Airtable `type` field deliberately does NOT count — it is the unreliable
    first-party claim that produced the skeleton fabrications."""
    fields = {"Name": pad.get("name"), "City": pad.get("city"), "State": pad.get("state")}
    about, _ = gfd.about_for(fields)
    bits = [str(pad.get("name") or ""), str(gdesc or "")]
    bits += [str(f) for f in (pad.get("features") or [])]
    for cat, attrs in about.items():
        bits.append(cat + " " + " ".join(attrs))
    return bool(WATER_RE.search(" ".join(bits)))


def prompt_for(pad, gdesc, facts, note=""):
    return f"""Venue: {pad['name']} — {pad.get('city')}, {pad.get('state')}

Write ONE original paragraph (3-4 sentences, 45-90 words) describing this venue for parents planning a visit.

SOURCE A — Google's venue summary (use its facts, but fully rephrase; never reuse its wording):
{gdesc}

SOURCE B — verified attributes:
{facts}

Hard rules:
- Every claim must be supported by Source A or B. No invented features, hours, fees, or atmosphere.
- Only mention a splash pad, spray features, or water play if a source explicitly supports it.
- Start with the venue name. Concrete, plain prose — no marketing language, no superlatives, no questions, no addressing the reader.
- Never mention Google, reviews, ratings, or stars.{note}

Return only the paragraph."""


def _shingles(text, n=8):
    w = re.findall(r"[a-z0-9']+", str(text).lower())
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def validate(pad, out, gdesc, prot, facts=""):
    t = build.clean_description(str(out).strip())
    t = re.sub(r"\s+", " ", t).strip()
    if not (150 <= len(t) <= 700):
        return None, f"length {len(t)}"
    # Every number in the output must appear in a source (catches world-knowledge
    # leaks like acreage/years the model "knows" but the sources never state).
    src = " ".join([str(gdesc), str(facts), str(pad.get("name") or ""), str(pad.get("zip") or "")])
    allowed = {n.replace(",", "") for n in re.findall(r"\d[\d,]*", src)}
    unsourced = {n.replace(",", "") for n in re.findall(r"\d[\d,]*", t)} - allowed
    if unsourced:
        return None, f"unsourced numbers: {sorted(unsourced)[:4]}"
    if SKELETON_RE.search(t):
        return None, "skeleton phrase reappeared"
    low = t.lower()
    for b in BANNED:
        if b in low:
            return None, f"banned phrase: {b}"
    if _shingles(t) & _shingles(gdesc):
        return None, "verbatim overlap with Google text"
    first = re.findall(r"[a-z0-9']+", str(pad["name"]).lower())[:1]
    if first and first[0] not in low:
        return None, "does not reference venue name"
    pad2 = dict(pad, description=t)
    if build.hard_exclusion_reason(pad2):
        return None, "hard exclusion"
    verdict, reason = build.evaluate_pad(pad2, prot)
    if verdict != "ok":
        return None, f"gate: {verdict} {reason}"
    return t, None


def call_model(client, prompt):
    import anthropic
    for attempt in range(4):
        try:
            r = client.messages.create(model=MODEL, max_tokens=400, temperature=0.8,
                                       system=SYSTEM,
                                       messages=[{"role": "user", "content": prompt}])
            return r.content[0].text.strip()
        except anthropic.RateLimitError:
            time.sleep(5 * (attempt + 1))
        except anthropic.APIStatusError as e:
            if getattr(e, "status_code", 0) in (429, 500, 502, 503, 529):
                time.sleep(5 * (attempt + 1))
            else:
                raise
    raise RuntimeError("model call failed after retries")


def enrich_one(client, pad, gdesc, prot):
    facts = facts_for(pad)
    out = call_model(client, prompt_for(pad, gdesc, facts))
    t, err = validate(pad, out, gdesc, prot, facts)
    if err:
        out = call_model(client, prompt_for(
            pad, gdesc, facts,
            note=f"\n- A previous attempt failed validation ({err}); avoid that."))
        t, err = validate(pad, out, gdesc, prot, facts)
    return t, err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0, help="generate N proposals, print, no writes")
    ap.add_argument("--apply", action="store_true", help="backup Descriptions then write Airtable")
    args = ap.parse_args()

    pads = build.get_pads()
    excl = set(config.PAD_EXCLUDE_SLUGS)
    live = [p for p in pads if p.get("slug") not in excl]
    prot = build._load_protected_pad_slugs()
    gidx = google_desc_index()

    cohort, skel, with_g = [], 0, 0
    for p in live:
        if not SKELETON_RE.search(str(p.get("description") or "")):
            continue
        skel += 1
        g = gidx.get(gfd.join_key(p.get("name"), p.get("city"), p.get("state")))
        if not g:
            continue
        with_g += 1
        if water_evidence(p, g):
            cohort.append((p, g))
    print(f"live {len(live)} | skeleton {skel} | +google-desc {with_g} | "
          f"water-evidenced cohort {len(cohort)}")

    if not args.sample and not args.apply:
        print("Dry run only. Use --sample N to preview or --apply to write.")
        return

    load_dotenv()
    import anthropic
    client = anthropic.Anthropic()
    todo = cohort[:args.sample] if args.sample else cohort

    results, failures = [], []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(enrich_one, client, p, g, prot): (p, g) for p, g in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            p, g = futs[fut]
            try:
                t, err = fut.result()
            except Exception as e:
                t, err = None, f"error: {e}"
            (results if t else failures).append((p, g, t if t else err))
            if i % 25 == 0 or i == len(futs):
                print(f"  {i}/{len(futs)} generated ({len(failures)} failed)")

    if args.sample:
        for p, g, t in results + failures:
            print("\n" + "=" * 72)
            print(f"{p['name']} ({p.get('city')}, {p.get('state')})  /pad/{p['slug']}")
            print(f"BEFORE: {str(p.get('description'))[:220]}")
            print(f"GOOGLE: {g[:220]}")
            print(f"AFTER : {t}")
        print(f"\nSample done: {len(results)} ok, {len(failures)} failed. No writes.")
        return

    # --apply
    from pyairtable import Api
    table = Api(config.AIRTABLE_API_KEY).table(config.AIRTABLE_BASE_ID, config.AIRTABLE_TABLE_NAME)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = {r["id"]: r["fields"].get("Description", "") for r in table.all(fields=["Description"])}
    bpath = pathlib.Path("data") / f"description_backup_{ts}.json"
    bpath.write_text(json.dumps(backup, ensure_ascii=False, indent=0))
    print(f"Backed up {len(backup)} Descriptions -> {bpath}")

    updates = [{"id": p["_airtable_id"], "fields": {"Description": t}} for p, _g, t in results]
    table.batch_update(updates)
    print(f"Updated {len(updates)} records in Airtable. {len(failures)} skipped (validation).")

    slugs = sorted(p["slug"] for p, _g, _t in results)
    pathlib.Path("data/enrich_applied_slugs.json").write_text(json.dumps(slugs))
    md = [f"# Enrichment applied {ts} — {len(results)} pads, {len(failures)} skipped\n"]
    for p, g, t in results[:10]:
        md += [f"\n## {p['name']} ({p.get('city')}, {p.get('state')})",
               f"**Before:** {p.get('description')}",
               f"**Google:** {g}",
               f"**After:** {t}"]
    md.append("\n## All updated slugs\n" + "\n".join(f"- {s}" for s in slugs))
    md += [f"- SKIPPED {p['slug']}: {err}" for p, _g, err in failures]
    apath = pathlib.Path("data") / f"enrich_applied_{ts}.md"
    apath.write_text("\n".join(md))
    print(f"Artifacts: {apath} + data/enrich_applied_slugs.json")


if __name__ == "__main__":
    main()
