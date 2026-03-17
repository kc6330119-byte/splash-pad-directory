#!/usr/bin/env python3
"""
scan_websites.py — Scan websites to verify each record qualifies for the splash pad directory.

For each record in data/SplashPads_NEW_ONLY.csv:
  1. Fetches the website URL (with timeout and error handling)
  2. Sends page text to Claude Haiku for classification
  3. Returns QUALIFY / REJECT / UNCERTAIN + a brief reason

Saves:
  data/SplashPads_SCAN_RESULTS.csv  — all records with verdict + reason
  data/SplashPads_QUALIFIED.csv     — QUALIFY only (ready for import review)
  data/SplashPads_UNCERTAIN.csv     — UNCERTAIN (needs manual review)
  data/scan_checkpoint.json         — progress checkpoint; rerun to resume

Usage:
  python scan_websites.py             # run all records (resumable)
  python scan_websites.py --limit 20  # test on first 20 records
"""

import argparse
import json
import os
import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import anthropic
from typing import Optional, Tuple

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────────────
INPUT_FILE      = Path("data/SplashPads_NEW_ONLY.csv")
RESULTS_FILE    = Path("data/SplashPads_SCAN_RESULTS.csv")
QUALIFIED_FILE  = Path("data/SplashPads_QUALIFIED.csv")
UNCERTAIN_FILE  = Path("data/SplashPads_UNCERTAIN.csv")
CHECKPOINT_FILE = Path("data/scan_checkpoint.json")

# ── Settings ─────────────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    )
}
FETCH_TIMEOUT   = 10      # seconds per HTTP request
MAX_TEXT_CHARS  = 3000    # characters of page text sent to AI
SLEEP_BETWEEN   = 0.5     # seconds between records
CHECKPOINT_EVERY = 25     # save checkpoint every N records

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# ── Web fetch ─────────────────────────────────────────────────────────────────
def fetch_page_text(url: str) -> Optional[str]:
    """Fetch URL and return stripped plain text, or None on failure."""
    url = str(url).strip()
    if not url or url.lower() == "nan":
        return None
    try:
        resp = requests.get(url, headers=HEADERS, timeout=FETCH_TIMEOUT, allow_redirects=True)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        text = " ".join(text.split())   # normalize whitespace
        return text[:MAX_TEXT_CHARS] if text else None
    except Exception:
        return None


# ── AI classification ─────────────────────────────────────────────────────────
def classify(name: str, city: str, state: str, page_text: Optional[str]) -> Tuple[str, str]:
    """
    Ask Claude Haiku whether this facility qualifies for the splash pad directory.
    Returns (verdict, reason) where verdict is QUALIFY / REJECT / UNCERTAIN.
    """
    if page_text:
        context = (
            f"Facility name: {name}\n"
            f"Location: {city}, {state}\n\n"
            f"Website content (excerpt):\n{page_text}"
        )
    else:
        context = (
            f"Facility name: {name}\n"
            f"Location: {city}, {state}\n\n"
            f"No website content available — classify based on name only."
        )

    prompt = f"""You are a data reviewer for SplashPadLocator.com, a national directory of splash pads, spray parks, aquatic centers, and water play areas for families.

{context}

Does this facility have a splash pad, spray park, spray ground, aquatic center, water park, splash zone, interactive water play area, or similar family water play feature?

Respond with exactly one verdict on the first line, then a brief reason (max 15 words) on the second line:

QUALIFY   — facility clearly has water play features
REJECT    — facility does not have water play features
UNCERTAIN — cannot determine from the information available

Example:
QUALIFY
Has a dedicated splash pad and spray ground open Memorial Day through Labor Day."""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=80,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        lines = text.split("\n", 1)
        verdict = lines[0].strip().upper()
        reason  = lines[1].strip() if len(lines) > 1 else ""

        if verdict not in ("QUALIFY", "REJECT", "UNCERTAIN"):
            verdict = "UNCERTAIN"
            reason  = "AI response unclear"

        return verdict, reason

    except Exception as e:
        return "UNCERTAIN", f"AI error: {str(e)[:60]}"


# ── Checkpoint helpers ────────────────────────────────────────────────────────
def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {}


def save_checkpoint(checkpoint: dict):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(checkpoint, f)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Process only first N records (0 = all)")
    args = parser.parse_args()

    df = pd.read_csv(INPUT_FILE)
    if args.limit:
        df = df.head(args.limit)
        print(f"-- TEST MODE: processing first {args.limit} records --\n")

    total = len(df)
    print(f"Loaded {total} records from {INPUT_FILE}")

    checkpoint = load_checkpoint()
    already_done = len(checkpoint)
    if already_done:
        print(f"Resuming — {already_done} records already in checkpoint\n")

    counts = {"QUALIFY": 0, "REJECT": 0, "UNCERTAIN": 0}
    no_website = 0
    results = []

    for i, row in df.iterrows():
        name  = str(row.get("name",  "")).strip()
        city  = str(row.get("city",  "")).strip()
        state = str(row.get("state", "")).strip()
        url   = str(row.get("website url", "")).strip()

        row_key = f"{name}|{city}|{state}"

        # Use cached result if available
        if row_key in checkpoint:
            cached  = checkpoint[row_key]
            verdict = cached["verdict"]
            reason  = cached["reason"]
            counts[verdict] += 1
            result = row.to_dict()
            result["verdict"] = verdict
            result["reason"]  = reason
            results.append(result)
            continue

        print(f"[{i+1}/{total}] {name} | {city}, {state}")

        # Fetch website
        page_text = fetch_page_text(url)
        if page_text:
            print(f"         fetched {len(page_text)} chars")
        else:
            no_website += 1
            print(f"         no page content — classifying by name only")

        verdict, reason = classify(name, city, state, page_text)
        print(f"         → {verdict}: {reason}")

        # Cache
        checkpoint[row_key] = {"verdict": verdict, "reason": reason}
        if (i + 1) % CHECKPOINT_EVERY == 0:
            save_checkpoint(checkpoint)

        counts[verdict] += 1
        result = row.to_dict()
        result["verdict"] = verdict
        result["reason"]  = reason
        results.append(result)

        time.sleep(SLEEP_BETWEEN)

    save_checkpoint(checkpoint)

    # ── Write output files ────────────────────────────────────────────────────
    results_df   = pd.DataFrame(results)
    qualified_df = results_df[results_df["verdict"] == "QUALIFY"]
    uncertain_df = results_df[results_df["verdict"] == "UNCERTAIN"]

    results_df.to_csv(RESULTS_FILE,   index=False)
    qualified_df.to_csv(QUALIFIED_FILE, index=False)
    uncertain_df.to_csv(UNCERTAIN_FILE, index=False)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print(f"Scan complete — {total} records processed")
    print(f"  QUALIFY:    {counts['QUALIFY']:>5}")
    print(f"  REJECT:     {counts['REJECT']:>5}")
    print(f"  UNCERTAIN:  {counts['UNCERTAIN']:>5}")
    print(f"  No website: {no_website:>5}")
    print(f"\nSaved:")
    print(f"  {RESULTS_FILE}  ({len(results_df)} rows — all results)")
    print(f"  {QUALIFIED_FILE} ({len(qualified_df)} rows — ready to review)")
    print(f"  {UNCERTAIN_FILE} ({len(uncertain_df)} rows — needs manual review)")

    qualify_pct = counts['QUALIFY'] / total * 100 if total else 0
    est_cost = (total * 400 / 1_000_000 * 0.80) + (total * 60 / 1_000_000 * 4.00)
    print(f"\nQualification rate: {qualify_pct:.1f}%")
    print(f"Estimated AI cost:  ${est_cost:.2f}")


if __name__ == "__main__":
    main()
