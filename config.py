"""
Configuration for Splash Pad Finder Directory
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base Paths
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "dist"

# Site Configuration — UPDATE SITE_NAME and SITE_URL once domain is registered
SITE_NAME = "Splash Pad Locator"
SITE_DESCRIPTION = "Find splash pads, spray parks, and water play areas near you. Free, family-friendly fun for kids of all ages."
SITE_URL = os.getenv("SITE_URL", "https://splashpadlocator.com")
SITE_AUTHOR = "Splash Pad Locator"

# Airtable Configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "SplashPads")

# US States for state-based pages
US_STATES = [
    {"name": "Alabama", "slug": "alabama", "abbr": "AL"},
    {"name": "Alaska", "slug": "alaska", "abbr": "AK"},
    {"name": "Arizona", "slug": "arizona", "abbr": "AZ"},
    {"name": "Arkansas", "slug": "arkansas", "abbr": "AR"},
    {"name": "California", "slug": "california", "abbr": "CA"},
    {"name": "Colorado", "slug": "colorado", "abbr": "CO"},
    {"name": "Connecticut", "slug": "connecticut", "abbr": "CT"},
    {"name": "Delaware", "slug": "delaware", "abbr": "DE"},
    {"name": "Florida", "slug": "florida", "abbr": "FL"},
    {"name": "Georgia", "slug": "georgia", "abbr": "GA"},
    {"name": "Hawaii", "slug": "hawaii", "abbr": "HI"},
    {"name": "Idaho", "slug": "idaho", "abbr": "ID"},
    {"name": "Illinois", "slug": "illinois", "abbr": "IL"},
    {"name": "Indiana", "slug": "indiana", "abbr": "IN"},
    {"name": "Iowa", "slug": "iowa", "abbr": "IA"},
    {"name": "Kansas", "slug": "kansas", "abbr": "KS"},
    {"name": "Kentucky", "slug": "kentucky", "abbr": "KY"},
    {"name": "Louisiana", "slug": "louisiana", "abbr": "LA"},
    {"name": "Maine", "slug": "maine", "abbr": "ME"},
    {"name": "Maryland", "slug": "maryland", "abbr": "MD"},
    {"name": "Massachusetts", "slug": "massachusetts", "abbr": "MA"},
    {"name": "Michigan", "slug": "michigan", "abbr": "MI"},
    {"name": "Minnesota", "slug": "minnesota", "abbr": "MN"},
    {"name": "Mississippi", "slug": "mississippi", "abbr": "MS"},
    {"name": "Missouri", "slug": "missouri", "abbr": "MO"},
    {"name": "Montana", "slug": "montana", "abbr": "MT"},
    {"name": "Nebraska", "slug": "nebraska", "abbr": "NE"},
    {"name": "Nevada", "slug": "nevada", "abbr": "NV"},
    {"name": "New Hampshire", "slug": "new-hampshire", "abbr": "NH"},
    {"name": "New Jersey", "slug": "new-jersey", "abbr": "NJ"},
    {"name": "New Mexico", "slug": "new-mexico", "abbr": "NM"},
    {"name": "New York", "slug": "new-york", "abbr": "NY"},
    {"name": "North Carolina", "slug": "north-carolina", "abbr": "NC"},
    {"name": "North Dakota", "slug": "north-dakota", "abbr": "ND"},
    {"name": "Ohio", "slug": "ohio", "abbr": "OH"},
    {"name": "Oklahoma", "slug": "oklahoma", "abbr": "OK"},
    {"name": "Oregon", "slug": "oregon", "abbr": "OR"},
    {"name": "Pennsylvania", "slug": "pennsylvania", "abbr": "PA"},
    {"name": "Rhode Island", "slug": "rhode-island", "abbr": "RI"},
    {"name": "South Carolina", "slug": "south-carolina", "abbr": "SC"},
    {"name": "South Dakota", "slug": "south-dakota", "abbr": "SD"},
    {"name": "Tennessee", "slug": "tennessee", "abbr": "TN"},
    {"name": "Texas", "slug": "texas", "abbr": "TX"},
    {"name": "Utah", "slug": "utah", "abbr": "UT"},
    {"name": "Vermont", "slug": "vermont", "abbr": "VT"},
    {"name": "Virginia", "slug": "virginia", "abbr": "VA"},
    {"name": "Washington", "slug": "washington", "abbr": "WA"},
    {"name": "West Virginia", "slug": "west-virginia", "abbr": "WV"},
    {"name": "Wisconsin", "slug": "wisconsin", "abbr": "WI"},
    {"name": "Wyoming", "slug": "wyoming", "abbr": "WY"},
]

# Feature filter categories (used for filter pages and nav)
CATEGORIES = [
    {"name": "Free Admission", "slug": "free-admission", "description": "Splash pads with no admission cost", "icon": "🆓"},
    {"name": "Best for Toddlers", "slug": "toddlers", "description": "Gentle water features ideal for toddlers and young children", "icon": "👶"},
    {"name": "Best for Families", "slug": "families", "description": "Large splash pads with features for all ages", "icon": "👨‍👩‍👧‍👦"},
    {"name": "With Shade", "slug": "with-shade", "description": "Splash pads with shaded areas to keep the sun off", "icon": "⛱️"},
    {"name": "With Restrooms", "slug": "with-restrooms", "description": "Splash pads that have on-site restrooms", "icon": "🚻"},
    {"name": "With Picnic Areas", "slug": "with-picnic-areas", "description": "Splash pads near picnic tables or pavilions", "icon": "🧺"},
    {"name": "Indoor", "slug": "indoor", "description": "Year-round indoor water play areas", "icon": "🏠"},
    {"name": "Accessible", "slug": "accessible", "description": "ADA accessible splash pads and water play areas", "icon": "♿"},
]

# Google Analytics
GA_MEASUREMENT_ID = os.getenv("GA_MEASUREMENT_ID", "")

# SEO Settings
DEFAULT_META_TITLE = f"{SITE_NAME} - Find Splash Pads Near You"
DEFAULT_META_DESCRIPTION = SITE_DESCRIPTION

# Build Settings
ITEMS_PER_PAGE = 24
FEATURED_COUNT = 6
RECENT_COUNT = 8
