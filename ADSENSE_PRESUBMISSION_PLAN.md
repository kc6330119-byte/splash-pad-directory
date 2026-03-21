# Google AdSense Pre-Submission Plan
<!-- Last updated: 2026-03-20 -->

## Context

SplashPadLocator.com has not yet submitted to AdSense. This plan is informed by two AdSense rejections on a sibling directory site (holisticvetdirectory.com) for "Low value content" citing thin content, doorway pages, and scraped/templated content. The goal is to address identical structural risks before the first submission to avoid rejection.

## Current Site Audit (2026-03-17)

| Metric | Count | Risk |
|--------|-------|------|
| Total indexable pages | ~3,263 | — |
| Pad detail pages (templated) | 3,186 | — |
| State pages (templated, zero editorial) | 50 | **Medium** — pure template, no per-state content |
| Category pages (templated, minimal editorial) | 10 | **Medium** — only config description is unique |
| Blog posts (original content) | 11 → 13 (in progress) | **High** — too few to offset 3,200+ templated pages |
| Static pages (about, contact, submit, privacy, terms, success) | 6 | OK |
| **Original-to-total content ratio** | **0.52%** → improving | **Critical** — identical to sibling site at rejection |
| Thin pad pages (≤1 content signal) | 444 → 400 (after enrichment) | **High** — noindexed |
| States with < 5 listings | 5 states | **Medium** — noindexed |
| No description | 0 | OK |
| Thin description (< 100 chars) | 183 → 0 (enriched) | ✅ Fixed |
| Short description (100-149 chars) | 222 → 0 (appended) | ✅ Fixed |
| No hours | 1,226 (38.5%) | — |
| No features | 1,339 (42%) | — |
| No type | 2,193 (68.8%) | — |

### Low-Listing States (Doorway Page Risk)

| State | Listings | Status |
|-------|----------|--------|
| Alaska | 2 | Noindexed |
| Rhode Island | 4 | Noindexed |
| Hawaii | 4 | Noindexed |
| District of Columbia | 5 | Noindexed |
| Vermont | 5 | Noindexed |
| Delaware | 8 | Indexed (above threshold) |

### Template Content Density (from audit)

| Page Template | Unique Content | Boilerplate | Density |
|---------------|----------------|-------------|---------|
| pad.html (minimal data) | 30-40 words | 200+ words | ~15% |
| state.html | 50-70 words | 350+ words | ~15-20% |
| category.html | 40-80 words | 400+ words | ~12-18% |
| index.html | 750-850 words | 600-700 words | ~50-55% |

---

## Remediation Actions

### Action 1: Noindex Thin Pad Pages
- **Status:** COMPLETED (2026-03-17)
- **Change:** Added `<meta name="robots" content="noindex, follow">` to pad pages with ≤1 content signal (description ≥100 chars, hours, features, or type)
- **Files modified:**
  - `build.py` — added `is_thin_pad()` function; computes `noindex` flag per pad
  - `templates/base.html` — conditional noindex meta tag
  - `build.py` — sitemap excludes noindexed pad pages
- **Impact:** 442 thin pages removed from Google's index → reduced to 400 after description enrichment
- **Note:** `follow` directive ensures linked pages are still crawled

### Action 2: Noindex Low-Listing State Pages
- **Status:** COMPLETED (2026-03-17)
- **Change:** Added `<meta name="robots" content="noindex, follow">` to state pages with < 5 listings
- **Files modified:**
  - `build.py` — `MIN_PADS_FOR_INDEX = 5` in `build_state_pages()`
  - `build.py` — sitemap excludes low-listing state pages
- **Impact:** 5 state pages noindexed (Alaska, Rhode Island, Hawaii, DC, Vermont)

### Action 3: Add Editorial Intros to State Pages
- **Status:** COMPLETED (2026-03-17)
- **Change:** Added unique 2-3 sentence editorial paragraph to every state page, tailored to each state's climate, geography, and splash pad characteristics
- **Files modified:**
  - `config.py` — added `description` field to all 50 states in `US_STATES` list
  - `templates/state.html` — added intro section below state header (gray background, max-width prose)
- **Impact:** 50 state pages now have unique editorial content; no longer pure template pages

### Action 4: Add Editorial Intros to Category Pages
- **Status:** COMPLETED (2026-03-17)
- **Change:** Expanded category descriptions from ~10-15 words to full editorial paragraphs (40-70 words each) explaining what the category means, who it's for, and what to expect
- **Files modified:**
  - `config.py` — added `intro` field to all 10 categories in `CATEGORIES` list (kept original short `description` for header display)
  - `templates/category.html` — added intro section below category header
- **Impact:** 10 category pages now have unique editorial content

### Action 5: Write More Blog Posts
- **Status:** IN PROGRESS
- **Current count:** 29 published -- TARGET EXCEEDED
- **Target:** 25-30 published blog posts before AdSense submission
- **Blog post candidates:**
  - [x] Best Splash Pads in Tennessee (published 2026-03-17)
  - [x] Best Splash Pads in Ohio (published 2026-03-17)
  - [x] Best Splash Pads in Louisiana (published 2026-03-18)
  - [x] Best Splash Pads in California (published 2026-03-18)
  - [x] Best Portable Shade Tents for Splash Pads (published 2026-03-18)
  - [x] Your Toddler's First Splash Pad: What to Expect (published 2026-03-18)
  - [x] Best Splash Pad Toys for Kids (published 2026-03-18)
  - [x] Sensory-Friendly Splash Pads: What to Look For (published 2026-03-18)
  - [x] Best Splash Pads for Road Trips on I-95 (published 2026-03-18)
  - [x] Best Splash Pads in New York (published 2026-03-18)
  - [x] Best Splash Pads in Georgia (published 2026-03-18)
  - [x] Best Splash Pads in Arizona (published 2026-03-18)
  - [x] Best Splash Pads in North Carolina (published 2026-03-18)
  - [x] Splash Pad Etiquette: Do's and Don'ts (published 2026-03-18)
  - [x] The History of Splash Pads in America (published 2026-03-18)
  - [x] Splash Pads vs. Pools: Which is Better for Young Kids? (published 2026-03-18)
  - [x] Best Splash Pads in Iowa (published 2026-03-19)
  - [x] How to Find Free Splash Pads Near You (published 2026-03-19)
- **Impact:** Each post adds 1,000-2,500 words of genuinely unique, editorial content; shifts original-to-total ratio significantly
- **Estimated effort:** 15-20 hours over multiple sessions

### Action 6: Fix Data Quality Issues
- **Status:** IN PROGRESS
- **Changes:**
  - [x] Removed non-water listings flagged in Search Console (Kings Island Ticket Booths, Flamingo Restaurant, Terry's Plumbing, Alamo Drafthouse, Lake Shawnee Abandoned, Bounce House Rentals)
  - [x] Removed 3 additional non-water listings (Caninballz Dog Waterpark, PetMassage Hydrotherapy, Sky Zone Westlake)
  - [x] Fixed "The Splash Pad at Plaza DeLuna" state from "FL" to "Florida"
  - [x] Thin descriptions (< 100 chars) enriched — see Action 7
  - [x] Short descriptions (100-149 chars) appended — see Action 8
- **Estimated effort:** 1-2 hours remaining

### Action 7: Enrich Thin Descriptions (Deterministic Template — Replace)
- **Status:** COMPLETED (2026-03-17)
- **Script:** `enrich_descriptions.py`
- **Approach:** Deterministic template generator using MD5 hash of slug for varied sentence selection (adapted from holisticvetdirectory Action 4)
- **Results:**
  - 192 descriptions updated (23 irrelevant replaced, 169 thin expanded)
  - Descriptions enriched from <100 chars to 400-700+ chars using facility data (type, features, admission, rating, age range)
  - 6 opening sentence variations, 4 feature intro variations, 3 admission variations, 3 age range variations, 3 rating variations, 4 closing variations
  - Noindex count reduced from 442 → 400 (42 pads regained indexable status)
  - Sitemap grew from 2,807 → 2,849 URLs
- **Cost:** $0 (no API calls — fully deterministic)

### Action 8: Enrich Short Descriptions (Deterministic Template — Append)
- **Status:** COMPLETED (2026-03-17)
- **Script:** `enrich_descriptions.py --append`
- **Approach:** Appended supplementary content (admission, features, age range, rating, closing) to existing short-but-relevant descriptions (100-149 chars), preserving original Google Maps content
- **Results:**
  - 222 descriptions appended
  - Descriptions expanded from 100-149 chars to 400-600+ chars
  - Original factual content preserved; deterministic supplement added
- **Cost:** $0

### Action 9: Validate All Listings (Water Facility Verification)
- **Status:** IN PROGRESS (2026-03-17)
- **Script:** `validate_listings.py`
- **Approach:** Adapted from holisticvetdirectory `validate_animal_practices.py`. Two-pass validation:
  - Pass 1: Pre-score from CSV fields (name, type, features, description) — high-confidence water facilities skip web fetch
  - Pass 2: Fetch website for uncertain records; score against water vs. non-water keyword lists
- **Input:** `data/SplashPads-Grid 2026-03-17.csv` (3,172 records)
- **Outputs:**
  - `data/validation_results.csv` — all records with scores and classification
  - `data/validation_flagged.csv` — REVIEW NEEDED and LIKELY NOT WATER records
- **Classifications:** LIKELY WATER / REVIEW NEEDED / LIKELY NOT WATER / NO WEBSITE
- **Results:**
  - LIKELY WATER: 2,700
  - REVIEW NEEDED: 311
  - LIKELY NOT WATER: 161
  - Web fetches performed: 2,071
  - All 161 LIKELY NOT WATER records reviewed; non-water listings removed
  - Directory reduced from 3,186 → 3,025 active listings
  - Action Taken column added to validation_flagged.csv for audit trail
- **Cost:** $0 (keyword scoring, no AI calls)

### Action 10: Add Local Weather Link to Pad Detail Pages
- **Status:** COMPLETED (2026-03-18)
- **Change:** Added "Local Weather" card in pad detail sidebar linking to National Weather Service forecast using lat/long coordinates
- **File modified:** `templates/pad.html`
- **Impact:** Every pad page with coordinates now shows a weather link — adds relevant, dynamic content with zero JavaScript, zero API calls, zero maintenance
- **Source:** weather.gov (US government, free, no API key)

### Action 11: Add Newsletter Signup
- **Status:** COMPLETED (2026-03-19)
- **Change:** Added email newsletter signup banner above the footer on every page
- **File modified:** `templates/base.html`
- **Implementation:** Netlify Forms (form-name: `newsletter`), inline success message, honeypot spam protection
- **Impact:** Email capture on every page; signals engaged, active site to AdSense reviewers; builds direct audience for future email marketing
- **Cost:** $0 (Netlify Forms free tier)

### Action 12: Add Social Sharing Buttons
- **Status:** COMPLETED (2026-03-19)
- **Change:** Added share buttons (Facebook, X/Twitter, Pinterest, Email) to blog posts and pad detail pages
- **Files modified:**
  - `templates/post.html` — share row after article content (Facebook, X/Twitter, Pinterest, Email)
  - `templates/pad.html` — compact share card in sidebar (Facebook, X/Twitter, Email)
- **Implementation:** URL-based share links — zero JavaScript, zero third-party scripts, zero page load impact
- **Impact:** Encourages content distribution; adds engagement signals; no Core Web Vitals impact

---

## Pre-Submission Timeline

| Date | Action | Status |
|------|--------|--------|
| 2026-03-17 | Created pre-submission plan based on sibling site rejection learnings | DONE |
| 2026-03-17 | Noindex thin pad pages (442 → 400 pages) — Action 1 | DONE |
| 2026-03-17 | Noindex low-listing state pages (< 5 listings) — Action 2 | DONE |
| 2026-03-17 | Sitemap reduced from ~3,263 to 2,849 URLs | DONE |
| 2026-03-17 | Removed non-water listings from Airtable (Kings Island, etc. — 9 records) | DONE |
| 2026-03-17 | Enriched 192 thin descriptions (<100 chars) — Action 7 | DONE |
| 2026-03-17 | Appended to 222 short descriptions (100-149 chars) — Action 8 | DONE |
| 2026-03-17 | Published Tennessee blog post — Action 5 | DONE |
| 2026-03-17 | Published Ohio blog post — Action 5 | DONE |
| 2026-03-17 | Listing validation script completed — 3,172 records scanned — Action 9 | DONE |
| 2026-03-18 | Reviewed all 161 LIKELY NOT WATER records, removed non-water listings | DONE |
| 2026-03-18 | Directory count: 3,186 → 3,025 after validation cleanup | DONE |
| 2026-03-18 | Site redeployed with cleaned data | DONE |
| 2026-03-17 | Added editorial intros to all 50 state pages — Action 3 | DONE |
| 2026-03-17 | Added editorial intros to all 10 category pages — Action 4 | DONE |
| 2026-03-17 | Drafted Louisiana blog post — Action 5 | DONE |
| 2026-03-17 | Drafted California blog post — Action 5 | DONE |
| 2026-03-18 | Published 5 more blog posts (I-95, History, Sensory, Pools vs, Etiquette) — 27 total | DONE |
| 2026-03-18 | Blog post target reached (27/25) — Action 5 | DONE |
| 2026-03-18 | Added dynamic blog count + listing count to homepage SEO text block | DONE |
| 2026-03-18 | All changes deployed to Netlify | DONE |
| 2026-03-18 | Added Local Weather link to pad detail pages — Action 10 | DONE |
| 2026-03-19 | Published Iowa + How to Find Free Splash Pads blog posts — 29 total | DONE |
| 2026-03-19 | Added newsletter signup to every page (Netlify Forms) — Action 11 | DONE |
| 2026-03-19 | Added social sharing buttons to blog posts + pad pages — Action 12 | DONE |
| ~2-3 weeks after deploy | Verify noindexed pages dropping from Google index | TODO |
| ~4-6 weeks after deploy | **Submit to AdSense** | TODO |

---

## Pre-Submission Checklist

Before submitting to AdSense, verify:

- [x] Thin pad pages noindexed (≤1 content signal) — 400 pages
- [x] Low-listing state pages noindexed (< 5 listings) — 5 states
- [x] Thin descriptions enriched (< 100 chars) — 192 records
- [x] Short descriptions appended (100-149 chars) — 222 records
- [x] Non-water listings removed (9 records from Search Console + manual review)
- [x] Listing validation complete and flagged records removed (Action 9) — 161 reviewed, directory at 3,025
- [x] Editorial intros added to all 50 state pages
- [x] Editorial intros expanded on all 10 category pages
- [x] 25+ published blog posts with original, substantive content (27 published)
- [x] Data quality issues fixed (state "FL" → "Florida")
- [ ] Site deployed with all changes live
- [ ] Google Search Console shows noindexed pages being excluded (2-3 week lag)
- [ ] Google Search Console shows 500+ indexed pages
- [ ] Site loads fast (Lighthouse score > 90)
- [ ] No broken links or 404 errors
- [ ] Mobile-friendly test passes
- [ ] All indexed pages have unique meta descriptions
- [ ] Schema markup validates (Google Rich Results Test)
- [ ] Privacy Policy and Terms pages are present and linked
- [ ] ads.txt is present with correct publisher ID (ca-pub-9265762311868507)

---

## Lessons from Sibling Site (holisticvetdirectory.com)

1. **Do NOT submit early.** A rejection creates a 30-day waiting period and a rejection record on the account.
2. **The original-to-templated content ratio matters.** At 0.5%, the vet site was rejected. Aim for 1%+ minimum.
3. **Thin/doorway pages are the primary trigger.** Google flagged 1,742 city pages with 1-2 vets as doorway pages. Our thin pad pages (444) are the same risk.
4. **Blog posts are the most effective remedy.** The vet site added 25 posts (27,750 words) to shift the ratio.
5. **Noindexing thin pages is safe.** Using `noindex, follow` removes pages from the index while preserving crawl paths. The vet site noindexed 1,742 pages with no negative impact.
6. **Quality over quantity for blog posts.** Each post should be 1,000+ words of genuinely useful, original content. Google can detect filler.
7. **AdSense reviewers look at the site holistically.** The combination of fewer indexed pages + more original content + cleaner listings presents a much stronger case.
8. **Wait for Google to recrawl after changes.** Noindexed pages take 2-3 weeks to drop from the index. Submitting before the index cleans up risks another rejection.
9. **Validate listing data quality.** The vet site removed 71 non-veterinary practices; our site has already removed 9+ non-water listings. Systematic validation (validate_listings.py) catches what manual review misses.

---

## Progress Summary (2026-03-17)

**Completed in one session:**
- 6 major site improvements implemented
- 9 non-water listings removed from directory
- 192 thin descriptions replaced with rich, varied content (deterministic template)
- 222 short descriptions appended with supplementary content
- 400 thin pad pages noindexed (down from 442 after enrichment)
- 5 low-listing state pages noindexed
- Sitemap reduced from ~3,263 to 2,849 URLs
- 2 state-specific blog posts drafted (Tennessee, Ohio) — informed by Search Console query data
- Listing validation script built and running (3,172 records)
- Search Console baseline established (Feb 28 – Mar 14 data)
- AdSense pre-submission plan created and maintained

**Total description enrichment:**
- Pass 1 (replace): 192 records — thin/irrelevant → 400-700+ chars
- Pass 2 (append): 222 records — short (100-149 chars) → 400-600+ chars
- **414 total descriptions improved** at $0 cost

---

## Notes

- AdSense Publisher ID: ca-pub-9265762311868507
- ads.txt already configured and deployed
- Google Search Console verified and sitemap submitted (2026-03-09)
- Indexing started 2026-03-02; 114 pages indexed as of 2026-03-09
- Current Performance (28-day as of 2026-03-09): 6 clicks, 1.4K impressions, 0.4% CTR, position 18.9
- Singapore bot traffic detected on direct visits — does not affect Search Console organic data
- scan_websites.py previously validated 3,027 park records for import qualification
- validate_listings.py now running systematic validation against all 3,172 current Airtable records

---

## Search Console Baseline (Feb 28 – Mar 14, 2026)

### Performance Summary (28-day)
- Total clicks: 6
- Total impressions: 1,400+
- Average CTR: 0.4%
- Average position: 18.9

### Key Query Rankings
| Query | Impressions | Position | Notes |
|-------|-------------|----------|-------|
| splash pad near me | 107 | 7.83 | Page 1 — #1 opportunity |
| splash pads near me | 44 | 7.98 | Page 1 |
| splash pad | 163 | 11.75 | Just off page 1 |
| best splash pads near me | 8 | 6.0 | Page 1 |
| splash pad park near me | 4 | 4.75 | Top 5 |
| splash pads open now | 2 | 3.5 | Top 4 |
| when does the splash pad open | 2 | 6.0 | Page 1 |

### Top Pages by Impressions
| Page | Clicks | Impressions | Position |
|------|--------|-------------|----------|
| Homepage | 4 | 217 | 23.21 |
| /state/ohio | 3 | 314 | 24.99 |
| /state/tennessee | 0 | 243 | 29.47 |
| /state/illinois | 0 | 181 | 33.31 |
| /blog/best-splash-pads-in-florida | 0 | 168 | 8.96 |
| /state/iowa | 2 | 146 | 19.12 |
| /category/with-restrooms | 1 | 133 | 7.75 |

### Blog Post Rankings (all on or near page 1)
| Blog Post | Impressions | Position |
|-----------|-------------|----------|
| Beyond the Splash (motor skills) | 22 | 6.73 |
| What to Pack | 11 | 6.82 |
| Best Swim Diapers | 80 | 7.70 |
| Best Splash Pads in Florida | 168 | 8.96 |
| Summers in Jacksonville | 42 | 12.86 |

### Hot Markets (by query volume)
1. **Tennessee** — 243 state page impressions + multiple city queries (Nashville, Murfreesboro, Hendersonville)
2. **Ohio** — 314 impressions, 3 clicks (strongest state page)
3. **Iowa** — 146 impressions, 2 clicks
4. **Illinois** — 181 impressions

### Data Quality Issues Found
Non-water listings appearing in search results (all removed 2026-03-17):
- ~~Kings Island Ticket Booths (82 impressions — not a water attraction)~~
- ~~Flamingo Restaurant, South Ozone Park (restaurant)~~
- ~~Terry's Plumbing Supply (plumbing store)~~
- ~~Alamo Drafthouse Cinema (movie theater)~~
- ~~Lake Shawnee Abandoned Amusement Park (abandoned)~~
- ~~Bounce House Water Slide Rentals (rental company, not a facility)~~
- ~~Caninballz Indoor Dog Waterpark (for dogs, not families)~~
- ~~Aquatic Massage Hydrotherapy at PetMassage (pet massage)~~
- ~~Sky Zone Westlake (trampoline park)~~

### Blog Post Priority (Data-Informed)
1. ~~Best Splash Pads in Tennessee/Nashville~~ — DRAFTED
2. ~~Best Splash Pads in Ohio~~ — DRAFTED
3. Best Splash Pads in Baton Rouge (multiple queries)
4. Best Splash Pads in El Paso (multiple queries, position 36-53)
5. Best Splash Pads in California (large market)

### Indexing Baseline (2026-03-18)
- Indexed: 203 pages
- Not indexed: 2,950
  - Discovered — currently not indexed: 2,947 (Google found but hasn't crawled yet)
  - Alternate page with proper canonical tag: 2 (normal, not an issue)
- Note: Sitemap now has 2,849 URLs (down from ~3,263 after noindex cleanup). As Google processes the updated sitemap, the "Discovered" count should decrease while indexed count grows.
- After noindex changes take effect (~2-3 weeks), expect "Excluded by noindex tag" to appear as a new category for ~400 pad pages + 5 state pages.

### Compare Against This Baseline (~April 14)
- Export fresh Pages and Queries reports from Search Console
- Key metrics to compare:
  - Total impressions and clicks (should increase)
  - Average position for "splash pad near me" (should improve from 7.83)
  - Number of pages with impressions (should decrease as noindexed pages drop)
  - Blog post visibility (new articles should begin appearing)
  - Non-water listings should stop appearing after removal/noindex
