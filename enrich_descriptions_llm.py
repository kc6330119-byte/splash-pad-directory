#!/usr/bin/env python3
"""
enrich_descriptions_llm.py — Phase 1.5 LLM-synthesis enrichment.

Breaks the templated "[Name] is a water play area in [City], [State]." skeleton
opener (Google's "scaled content" tell, the AdSense Low-Value-Content trigger) by
folding Google's previously-UNUSED `description` editorial blurb + the verified
facts from generate_fact_descriptions.compose() into ONE original, fact-bounded
paragraph written by Claude.

Target = TRUE live (post-sweep, hard-exclusion aware) pads that:
  (a) carry the skeleton opener,
  (b) have a Google `description` (DGL Files/Outscraper-*.xlsx), and
  (c) have explicit WATER evidence in that description.
This is the clean 296-pad water-evidenced batch from the dry-run; the ~220
no-water enrichable pads are deliberately NOT touched (they are a triage signal,
not an enrich target).

Pipeline (per pad):
  compose(fields)  ->  strip skeleton opener + noisy Age-Range toddler/all-ages
  claim (_DROP)  ->  feed {Google description + verified facts} to the model with
  a strict prompt (rule 5 forbids inventing water)  ->  ONE 2-4 sentence paragraph.

Safety (mirrors generate_fact_descriptions.py):
  - dry-run by default; --apply REQUIRED to write Airtable.
  - ONLY updates the existing "Description" field; never inserts records.
  - before any write, backs up EVERY current Description to a timestamped JSON
    keyed by record id (data/description_backup_<ts>.json) — full restore point.
  - gates each rewrite with build.evaluate_pad: never writes a rewrite that would
    regress a pad ok->noindex, never writes an empty/LLM-error string.
  - writes a post-run audit (data/ENRICH_APPLIED_<ts>.md / ENRICH_DRYRUN_<ts>.md)
    showing before/after + the Google source for every change.

Usage:
  python3 enrich_descriptions_llm.py                  # dry run: stats + audit md
  python3 enrich_descriptions_llm.py --limit 10       # dry run on first 10 targets
  python3 enrich_descriptions_llm.py --apply          # write "Description" (Haiku)
  python3 enrich_descriptions_llm.py --apply --model claude-sonnet-4-6
"""
import os
import re
import sys
import glob
import json
import time
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import openpyxl
from dotenv import load_dotenv
from pyairtable import Api

REPO = Path(__file__).parent
sys.path.insert(0, str(REPO))
os.chdir(REPO)

import build
import generate_fact_descriptions as G  # compose / about_index / join_key / norm / pad_shape

load_dotenv(REPO / ".env", override=True)
_AT_KEY = (os.environ.get("AIRTABLE_API_KEY") or "").strip()
_AT_BASE = (os.environ.get("AIRTABLE_BASE_ID") or "").strip()
_AT_TABLE = (os.environ.get("AIRTABLE_TABLE_NAME") or "SplashPads").strip()
_ANTHRO_KEY = (os.environ.get("ANTHROPIC_API_KEY") or "").strip()

DESC_FIELD = "Description"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"  # cheap + strong paraphrase; claude-3-5-haiku-latest is 404 here
DATA = REPO / "data"


def norm(s):
    return G.norm(s)


def jkey(n, c, s):
    return G.join_key(n, c, s)


# ── Google `description` + `type` keyed by jkey (the field compose() ignores) ──
def load_google_idx():
    gdesc, gtype = {}, {}
    for path in sorted(glob.glob(str(REPO / "DGL Files" / "Outscraper-*.xlsx"))):
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb.active
        rows = ws.iter_rows(values_only=True)
        hdr = [norm(x) for x in next(rows)]
        ci = {h: i for i, h in enumerate(hdr)}

        def cell(r, c):
            i = ci.get(c)
            return r[i] if i is not None and i < len(r) else None

        for r in rows:
            nm = cell(r, "name")
            if not nm:
                continue
            k = jkey(nm, cell(r, "city"), cell(r, "state"))
            if k not in gdesc:
                gdesc[k] = (cell(r, "description") or "")
                gtype[k] = (cell(r, "type") or "")
        wb.close()
    return gdesc, gtype


SKEL = re.compile(r"\bis a (?:water play area|splash pad|water park|aquatic center|"
                  r"indoor water play facility|resort water park|campground with on-site water play|"
                  r"amusement park with water attractions) in\b", re.I)
WATER_TERM = re.compile(r"(water ?park|water ?slide|wave pool|lazy river|splash|spray|aquatic|"
                        r"swim|pool|wading|beach|lagoon|wet play|fountain)", re.I)
# Age-Range-derived water claims are noisy (compose() sets them on non-water venues) — drop.
_DROP = re.compile(r"(gentler? water features|water play is designed for|water features suited to)", re.I)


def fact_lines(fields):
    """compose() facts with the skeleton opener (sentence 0) + noisy toddler claim removed."""
    full = G.compose(fields)
    sents = re.split(r"(?<=[.!?])\s+", full.strip())
    return [s for s in sents[1:] if s.strip() and not _DROP.search(s)]


PROMPT = """You write factual, neutral descriptions for a directory of splash pads, water parks, pools, and family water-recreation venues.
Rewrite the inputs below into ONE original paragraph of 2-4 sentences (about 45-95 words).

STRICT RULES:
1. Use ONLY facts present in the inputs. Never invent attractions, amenities, prices, hours, or claims.
2. Do NOT copy phrases verbatim from the "Google summary" — paraphrase in your own words and structure.
3. No marketing fluff, no superlatives, no ratings or review mentions.
4. Lead with what the place IS, then fold in its features and practical facts naturally.
5. CRITICAL: Do NOT state or imply the venue is a splash pad, water park, or has water-play / toddler water features UNLESS the Google summary or verified facts explicitly mention water, splash, spray, pool, slide, lazy river, wave, beach, fountain, or aquatic. If there is no water evidence, describe the venue accurately for what it is (e.g. a hotel, a ski resort, a park) — never invent water play.
Output ONLY the paragraph, no preamble.

Venue: {name} — {loc}
Approx type: {gtype}
Google summary: {gdesc}
Verified facts: {facts}"""


def llm_rewrite(client, model, fields, gdesc, gtype):
    loc = ", ".join(x for x in (fields.get("City", ""), fields.get("State", "")) if x)
    facts = " ".join(fact_lines(fields)) or "(no additional structured facts)"
    msg = PROMPT.format(name=fields.get("Name", ""), loc=loc, gtype=gtype or "n/a",
                        gdesc=gdesc or "(none)", facts=facts)
    r = client.messages.create(model=model, max_tokens=320, temperature=0.4,
                               messages=[{"role": "user", "content": msg}])
    return r.content[0].text.strip(), facts


def rewrite_with_retry(client, model, fields, gdesc, gtype, tries=3):
    last = ""
    for t in range(tries):
        try:
            return llm_rewrite(client, model, fields, gdesc, gtype)
        except Exception as e:  # transient 429/5xx etc.
            last = f"{type(e).__name__}: {e}"
            if t < tries - 1:
                time.sleep(1.5 * (t + 1))
    return None, last  # None text -> caller skips this pad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the Description field in Airtable")
    ap.add_argument("--limit", type=int, default=None, help="process only the first N targets")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="Anthropic model id")
    ap.add_argument("--workers", type=int, default=6, help="concurrent LLM calls")
    args = ap.parse_args()

    if not _AT_KEY or not _AT_BASE:
        sys.exit("Missing/empty AIRTABLE_API_KEY or AIRTABLE_BASE_ID in .env")
    if not _ANTHRO_KEY:
        sys.exit("Missing/empty ANTHROPIC_API_KEY in .env")
    import anthropic
    client = anthropic.Anthropic(api_key=_ANTHRO_KEY)

    # ── build the target jkey set exactly as the dry-run did (the clean 296) ──
    gdesc_idx, gtype_idx = load_google_idx()

    def gdesc_of_pad(p):
        return (gdesc_idx.get(jkey(p.get("name"), p.get("city"), p.get("state"))) or "").strip()

    pads = build.get_pads()
    prot = build._load_protected_pad_slugs()

    def truly_live(p):
        if build.hard_exclusion_reason(p):
            return False
        st, _ = build.evaluate_pad(p, prot)
        return st == "ok"

    live = [p for p in pads if truly_live(p)]
    skel = [p for p in live if SKEL.search(str(p.get("description", "")))]
    enrichable = [p for p in skel if gdesc_of_pad(p)]
    enrich_water = [p for p in enrichable if WATER_TERM.search(gdesc_of_pad(p))]
    target_jkeys = {jkey(p.get("name"), p.get("city"), p.get("state")) for p in enrich_water}

    print(f"TRUE live indexable pads:                 {len(live)}")
    print(f"  skeleton opener:                        {len(skel)}")
    print(f"  enrichable (skeleton + Google desc):    {len(enrichable)}")
    print(f"  WATER-EVIDENCED enrich target:          {len(enrich_water)}  (jkeys: {len(target_jkeys)})")

    # ── pull the write payload from Airtable (the source of truth) ──
    table = Api(_AT_KEY).table(_AT_BASE, _AT_TABLE)
    recs = [r for r in table.all() if r["fields"].get("Status") != "Draft"]

    candidates = []  # (rec_id, fields, gdesc, gtype)
    seen = set()
    for r in recs:
        f = r["fields"]
        nm = f.get("Name", "")
        if not nm:
            continue
        k = jkey(nm, f.get("City", ""), f.get("State", ""))
        if k in target_jkeys and k not in seen:
            seen.add(k)
            candidates.append((r["id"], f, (gdesc_idx.get(k) or "").strip(), (gtype_idx.get(k) or "").strip()))
    if args.limit:
        candidates = candidates[: args.limit]
    print(f"Airtable records matched to target:       {len(candidates)}"
          f"  ({len(target_jkeys) - len(seen)} target jkeys had no Airtable match)")
    if not candidates:
        sys.exit("No candidate records — nothing to do.")

    # ── generate rewrites concurrently ──
    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"\n[{mode}] generating {len(candidates)} rewrites via {args.model} "
          f"({args.workers} workers) ...")
    results = {}  # rec_id -> dict(name, slug, cur, new, gdesc, gtype, status_new, err)
    lock = threading.Lock()
    done = [0]

    def work(item):
        rec_id, f, gd, gt = item
        new, facts_or_err = rewrite_with_retry(client, args.model, f, gd, gt)
        cur = build.clean_description(f.get("Description", "") or "")
        rec = {"name": f.get("Name", ""), "city": f.get("City", ""), "state": f.get("State", ""),
               "cur": cur, "gdesc": gd, "gtype": gt, "new": None, "status_new": None, "err": None}
        if not new:
            rec["err"] = facts_or_err or "empty"
        else:
            pad_new = G.pad_shape(f, new)
            rec["slug"] = pad_new["slug"]
            st, _ = build.evaluate_pad(pad_new, prot)
            rec["status_new"] = st
            rec["new"] = new
        with lock:
            done[0] += 1
            if done[0] % 25 == 0 or done[0] == len(candidates):
                print(f"  {done[0]}/{len(candidates)} rewritten")
        return rec_id, rec

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for rec_id, rec in ex.map(work, candidates):
            results[rec_id] = rec

    # ── decide writes: only rewrites that stay indexable, are non-empty, error-free ──
    writes = []  # (rec_id, new)
    errored, regressed = [], []
    for rec_id, rec in results.items():
        if rec["err"] or not rec["new"]:
            errored.append(rec)
            continue
        if rec["status_new"] != "ok":
            regressed.append(rec)  # would noindex — keep current skeleton instead
            continue
        writes.append((rec_id, rec["new"]))

    print(f"\nrewrites: {len(results)}   write-eligible: {len(writes)}   "
          f"skipped(error): {len(errored)}   skipped(would-noindex): {len(regressed)}")
    newlens = sorted(len(rec["new"]) for rid, rec in results.items() if rec["new"])
    if newlens:
        q = lambda p: newlens[min(len(newlens) - 1, int(p * len(newlens)))]
        print(f"new length chars: min={newlens[0]} median={q(.5)} p90={q(.9)} max={newlens[-1]}")

    # ── audit md (every change, before/after + Google source) ──
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    DATA.mkdir(exist_ok=True)
    audit = [f"# Enrichment {mode} — LLM synthesis ({args.model})\n",
             f"_Generated {datetime.now().isoformat(timespec='seconds')} · "
             f"{len(writes)} write-eligible / {len(candidates)} targets · "
             f"{len(errored)} errored · {len(regressed)} would-noindex_\n"]
    for rec_id, rec in results.items():
        if not rec["new"]:
            continue
        tag = "INDEX" if rec["status_new"] == "ok" else f"noindex:{rec['status_new']} (SKIPPED-keeps-current)"
        audit.append(f"## {rec['name']} — {rec['city']}, {rec['state']}  _({rec['gtype']}; "
                     f"{len(rec['new'])} chars; {tag})_\n")
        audit.append(f"- **Current (skeleton):** {rec['cur']}")
        audit.append(f"- **Google summary:** {rec['gdesc']}")
        audit.append(f"- **Proposed:** {rec['new']}\n")
    audit_path = DATA / (f"ENRICH_APPLIED_{ts}.md" if args.apply else f"ENRICH_DRYRUN_{ts}.md")
    audit_path.write_text("\n".join(audit))
    print(f"wrote audit -> {audit_path}")

    if errored:
        print("\nERRORED (kept current), first 5:")
        for rec in errored[:5]:
            print(f"  {rec['name']} — {rec['err']}")

    if not args.apply:
        print("\nDRY RUN — nothing written. Re-run with --apply to write the Description field.")
        return

    # ── APPLY ──
    backup_path = DATA / f"description_backup_{ts}.json"
    backup = {r["id"]: (r["fields"].get("Description", "") or "")
              for r in recs if r["fields"].get("Name")}
    backup_path.write_text(json.dumps(backup, ensure_ascii=False, indent=2))
    print(f"\nBacked up {len(backup)} current descriptions -> {backup_path}")

    updates = [{"id": rid, "fields": {DESC_FIELD: new}} for rid, new in writes]
    print(f"--apply: writing {len(updates)} Description fields ...")
    for i in range(0, len(updates), 10):
        table.batch_update(updates[i:i + 10])
        print(f"  updated {min(i + 10, len(updates))}/{len(updates)}")
    print("\nDone. Run `python3 build.py` locally to regenerate dist/, verify, then deploy.")
    print(f"Restore if needed: write the backup JSON values back to each id's '{DESC_FIELD}'.")


if __name__ == "__main__":
    main()
