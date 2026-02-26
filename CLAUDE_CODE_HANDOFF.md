# Splash Pad Locator — Claude Code Handoff

## Project Summary
Building a **national splash pad directory** targeting families searching for "splash pads near me" (100K–1M monthly searches). Static site built with Python/Jinja2, data from Airtable, hosted on Netlify. This is a pivot from a previous financial tools directory on the same Netlify and Airtable accounts.

---

## Why This Niche
- 100K–1M monthly searches for "splash pads near me"
- Competitors (MySplashPad.com, SplashPadParks.com) are outdated WordPress blogs with no search/filter, no photos, no hours — very beatable
- Family/parenting audience = strong AdSense CPM, especially in summer
- Outscraper Google Maps provides all the listing data needed

---

## Tech Stack
| Layer | Tool |
|-------|------|
| Site generator | Python 3.9 + Jinja2 |
| Data/CMS | Airtable (existing account) |
| Hosting | Netlify (existing account, new site) |
| CSS | Tailwind CSS via CDN |
| Domain | TBD — register before connecting to Netlify |

---

## Existing Accounts to Reuse
| Service | Details |
|---------|---------|
| **Netlify** | Same account, create a NEW site for this project |
| **Airtable** | Same account, create a NEW Base called "Splash Pad Locator" |
| **Google AdSense** | Publisher ID: `ca-pub-9265762311868507` (already in ads.txt) |
| **Google Analytics** | Create a NEW property for the new domain |

---

## Directory Structure
```
splash-pad-directory/
├── build.py              # Main build script — FULLY WRITTEN, ready to use
├── config.py             # Site config, states, categories — FULLY WRITTEN
├── requirements.txt      # Python deps — COMPLETE
├── netlify.toml          # Netlify build config + redirects — COMPLETE
├── ads.txt               # AdSense publisher verification — COMPLETE
├── .gitignore            # COMPLETE
├── .env.example          # Template for .env — COMPLETE
├── .env                  # YOU CREATE THIS — add Airtable keys (never commit)
├── CLAUDE_CODE_HANDOFF.md # This file
├── templates/            # Jinja2 templates — NEED TO BE BUILT
│   ├── base.html         # Base layout (nav, footer, analytics, AdSense)
│   ├── index.html        # Homepage
│   ├── pad.html          # Individual splash pad detail page
│   ├── state.html        # State listing page (e.g. /state/texas.html)
│   ├── category.html     # Feature filter page (e.g. /category/free-admission.html)
│   ├── contact.html      # Contact form (Netlify Forms)
│   ├── success.html      # Form submission success page
│   ├── about.html        # About page
│   ├── privacy.html      # Privacy policy
│   └── terms.html        # Terms of service
├── static/
│   ├── css/custom.css    # NEED TO CREATE (minimal overrides)
│   ├── js/               # (optional JS files)
│   └── images/           # Logo, og-image.png (1200x630)
└── dist/                 # Generated output (gitignored, created by build.py)
```

---

## What's Already Done
- [x] `build.py` — complete, adapted for splash pads
- [x] `config.py` — all 50 US states, 8 filter categories, site name/description
- [x] `requirements.txt` — all Python dependencies
- [x] `netlify.toml` — build command + pretty URL redirects
- [x] `ads.txt` — AdSense publisher verification
- [x] `.gitignore`
- [x] `.env.example`

## What Needs to Be Done (in order)
1. [ ] Register domain name
2. [ ] Create GitHub repo and push this project
3. [ ] Create Airtable Base + Table (schema below)
4. [ ] Pull Outscraper data → import to Airtable
5. [ ] Build all Jinja2 templates (start with base.html, index.html, pad.html)
6. [ ] Set up local venv + test build
7. [ ] Connect GitHub repo to Netlify as new site
8. [ ] Point domain to Netlify
9. [ ] Set up new Google Analytics property
10. [ ] Apply for AdSense (same publisher account)

---

## Airtable Setup

### Create a new Base called: "Splash Pad Locator"
### Create a Table called: "SplashPads"

### Table Fields (exact names matter — build.py maps these)
| Field Name | Airtable Type | Notes |
|-----------|--------------|-------|
| Name | Single line text | Splash pad name |
| Description | Long text | 2-3 sentences about the location |
| Address | Single line text | Street address |
| City | Single line text | City name |
| State | Single line text | Full state name (e.g. "Texas") |
| Zip | Single line text | ZIP code |
| Phone | Single line text | Optional |
| Website URL | URL | Official site if available |
| Google Maps URL | URL | Direct Google Maps link |
| Photo URL | URL | Direct image URL |
| Hours | Single line text | e.g. "Mon-Sun: 9am-8pm" |
| Admission | Single select | Options: Free, Paid, Seasonal Pass |
| Price | Single line text | e.g. "$0" or "$5/person" |
| Age Range | Multiple select | Options: Toddlers, Kids, Tweens, All Ages, Families |
| Features | Multiple select | Options: Restrooms, Shade, Parking, Picnic Area, Playground, Snack Bar, Accessibility, Changing Rooms |
| Type | Single select | Options: Splash Pad, Spray Park, Indoor Water Play, Water Playground |
| Season | Single line text | e.g. "Memorial Day - Labor Day" |
| Status | Single select | Options: Active, Featured, Draft, Closed |
| Date Added | Date | Auto-set when adding records |
| Rating | Number | 0.0 - 5.0 |
| Review Count | Number | Number of reviews |

---

## Data Pipeline: Outscraper → Airtable

### Step 1: Outscraper Google Maps
Search queries to use in Outscraper:
- "splash pad [city], [state]"
- "spray park [city], [state]"
- "water play area [city], [state]"

Fields to export: Name, Address, City, State, ZIP, Phone, Website, Google Maps URL, Photos, Hours, Rating, Reviews

### Step 2: Clean & Import to Airtable
- Map Outscraper columns → Airtable fields above
- Set all Status = "Active" initially
- Add Admission type and Features manually or batch-edit

### Step 3: Rebuild Site
```bash
source venv/bin/activate
python build.py
```

---

## Local Setup Commands

```bash
# Navigate to project
cd ~/Documents/Documents\ -\ Kevin\'s\ MacBook\ Pro/GitHub/splash-pad-directory

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your Airtable keys

# Test build (uses sample data if no .env configured)
python3 build.py

# Preview locally
cd dist
python3 -m http.server 8000
# Open http://localhost:8000
```

---

## Reference: Previous Project (Financial Tools Directory)

The previous project this was built from:
- **Path**: `~/Documents/Documents - Kevin's MacBook Pro/GitHub/financial-tools-directory/`
- **Live site**: smart-investor-financial-tools.com (being abandoned)
- **Key patterns to copy from that project**:
  - `templates/base.html` — nav, footer, AdSense slots, Analytics, Open Graph, JSON-LD
  - `templates/contact.html` — Netlify Forms with JavaScript fetch submission
  - `templates/success.html` — Thank you page (outputs to success/index.html)
  - Contact form JS pattern: POST to /contact.html, redirect to /success/index.html on success

---

## Key Lessons Learned from Previous Project

### Netlify Forms (contact form)
- The form must have `data-netlify="true"` and `name="contact"` attributes
- Use JavaScript fetch to POST (not native form submit) to avoid redirect issues
- POST to `/contact.html`, redirect manually to `/success/index.html` on success
- Always "Clear cache and deploy" in Netlify dashboard after first enabling form detection

### Netlify Build
- Never commit `.env` file — use Netlify Environment Variables in dashboard
- Use `netlify.toml` for pretty URL redirects
- `pip install -r requirements.txt && python build.py` as build command

### AdSense
- `ads.txt` must be at the root of `dist/` — copy it in `build.py` (already done)
- Same AdSense publisher account can cover multiple sites
- Need separate AdSense site approval per domain

### API Rate Limits
- If using any external APIs in Netlify Functions, use sequential calls with delays (1500ms)
- Never expose API keys in frontend code — always use Netlify Functions as proxy

---

## Site Architecture for SEO

The key SEO opportunity is **city + state long-tail search**:
- `/state/texas.html` → "Splash pads in Texas"
- `/pad/centennial-park-splash-pad.html` → "Centennial Park Splash Pad Nashville TN"
- `/category/free-admission.html` → "Free splash pads near me"

With 3000+ listings across 50 states, the site will auto-generate thousands of indexed pages.

---

## Template Design Notes

The previous site used:
- **Tailwind CSS via CDN** (no build step needed)
- Blue color scheme (`#2563eb` primary)
- Clean card-based layouts
- Mobile-responsive with hamburger menu

For this site, suggest:
- **Aqua/teal color scheme** (water theme): `#0891b2` or `#06b6d4`
- Large hero with search bar (search by city or state)
- Card grid for listings (photo, name, city, admission badge)
- State browse section on homepage
- Filter sidebar on listing pages

---

## Monetization Plan

1. **Google AdSense** — same publisher account (ca-pub-9265762311868507), apply for new domain
2. **Affiliate links** — summer gear (sunscreen, water shoes, swim diapers via Amazon Associates)
3. **Featured listings** — parks/recreation departments pay for top placement
4. **Display ads** — family-focused networks (Mediavine once traffic qualifies: 50K sessions/mo)

---

## Domain
**Registered: splashpadlocator.com** (registered via Netlify, Feb 2026)
- `SITE_URL` already set to `https://splashpadlocator.com` in config.py and .env.example
- Also set `SITE_URL=https://splashpadlocator.com` in Netlify site environment variables once the site is created
