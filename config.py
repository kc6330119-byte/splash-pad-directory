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
AIRTABLE_BLOG_TABLE_NAME = os.getenv("AIRTABLE_BLOG_TABLE_NAME", "Blog Posts")

# US States for state-based pages
US_STATES = [
    {"name": "Alabama", "slug": "alabama", "abbr": "AL",
     "description": "Alabama's long summers and warm Gulf Coast climate make splash pads a staple across the state. From Birmingham's community parks to Mobile's waterfront play areas, families will find free and paid water play options in cities large and small."},
    {"name": "Alaska", "slug": "alaska", "abbr": "AK",
     "description": "Alaska's short but intense summers bring surprising demand for water play. While options are limited compared to warmer states, the communities that have splash pads make the most of the long daylight hours from June through August."},
    {"name": "Arizona", "slug": "arizona", "abbr": "AZ",
     "description": "In a state where summer temperatures regularly exceed 110 degrees, splash pads aren't just fun — they're essential. Arizona's cities have invested heavily in water play, with many facilities operating from March through October. Phoenix, Scottsdale, and Tucson lead the way with dozens of free community splash pads."},
    {"name": "Arkansas", "slug": "arkansas", "abbr": "AR",
     "description": "Arkansas offers a growing collection of splash pads across the Natural State. From Little Rock's park system to smaller communities in the Ozarks and Delta regions, families are finding more water play options each summer."},
    {"name": "California", "slug": "california", "abbr": "CA",
     "description": "California has one of the largest collections of splash pads and water parks in the country. The state's year-round warm climate in the south and intense Central Valley heat mean splash pads operate longer seasons than almost anywhere else. From San Diego's iconic Waterfront Park to Sacramento's community splash pads and LA's theme park waterparks, there's water play for every family and budget."},
    {"name": "Colorado", "slug": "colorado", "abbr": "CO",
     "description": "Colorado's dry heat and 300 days of sunshine make splash pads a popular summer escape along the Front Range. Denver, Colorado Springs, Fort Collins, and their suburbs feature community splash pads that run from late May through September, offering relief from the altitude-intensified sun."},
    {"name": "Connecticut", "slug": "connecticut", "abbr": "CT",
     "description": "Connecticut packs a surprising number of splash pads into its small footprint. Community parks across the state offer free water play from Memorial Day through Labor Day, giving families an easy cool-down option on humid New England summer days."},
    {"name": "Delaware", "slug": "delaware", "abbr": "DE",
     "description": "The First State may be small, but its communities offer splash pad options for families looking to cool off during the humid mid-Atlantic summers. Check local parks departments for seasonal hours and availability."},
    {"name": "Florida", "slug": "florida", "abbr": "FL",
     "description": "Florida is splash pad paradise. With year-round warm weather and a culture built around water, the Sunshine State offers hundreds of splash pads, spray parks, and aquatic centers from Key West to Jacksonville. Many operate year-round, and the sheer number of free municipal options makes Florida one of the best states in the country for water play."},
    {"name": "Georgia", "slug": "georgia", "abbr": "GA",
     "description": "Georgia's hot, humid summers drive strong demand for splash pads across the state. Metro Atlanta leads with dozens of community spray parks and aquatic centers, while coastal cities like Savannah and smaller towns throughout the Peach State offer their own water play options from April through September."},
    {"name": "Hawaii", "slug": "hawaii", "abbr": "HI",
     "description": "Hawaii's tropical climate and beach culture mean water play happens year-round. While the islands are better known for their beaches, a growing number of community parks offer splash pad facilities for families looking for a break from the sand and surf."},
    {"name": "Idaho", "slug": "idaho", "abbr": "ID",
     "description": "Idaho's dry summers bring temperatures that surprise visitors, especially in the Boise area and southern valleys. Community splash pads and aquatic centers provide welcome relief, typically operating from June through early September."},
    {"name": "Illinois", "slug": "illinois", "abbr": "IL",
     "description": "Illinois has one of the strongest splash pad networks in the Midwest. Chicago's park district operates numerous spray features across the city, and suburban communities from the North Shore to the south suburbs have invested in modern splash pads and aquatic centers. Downstate cities add to the mix with community water parks that rival their metro counterparts."},
    {"name": "Indiana", "slug": "indiana", "abbr": "IN",
     "description": "Indiana's parks departments have embraced splash pads as a summer staple. Indianapolis, Fort Wayne, and communities across the state offer free and paid water play options, with most facilities running from Memorial Day through Labor Day."},
    {"name": "Iowa", "slug": "iowa", "abbr": "IA",
     "description": "Iowa's splash pads and aquatic centers are community gathering places throughout the summer. Des Moines, Cedar Rapids, and smaller towns across the state have invested in modern water play facilities that families return to week after week from late May through September."},
    {"name": "Kansas", "slug": "kansas", "abbr": "KS",
     "description": "Kansas communities have built quality splash pads to combat the state's hot, windy summers. From Wichita's park system to smaller towns across the plains, families will find free and paid water play options with solid amenities."},
    {"name": "Kentucky", "slug": "kentucky", "abbr": "KY",
     "description": "Kentucky offers a growing selection of splash pads and aquatic centers across the Bluegrass State. Louisville and Lexington anchor the state's water play options, with community parks and recreation departments providing free and affordable splash pad access from May through September."},
    {"name": "Louisiana", "slug": "louisiana", "abbr": "LA",
     "description": "Louisiana's long, hot summers make splash pads a necessity, not a luxury. Baton Rouge leads the state with multiple free community park splash pads, while New Orleans, Lafayette, and Lake Charles offer their own water play destinations. Many facilities operate from April through October thanks to the extended warm season."},
    {"name": "Maine", "slug": "maine", "abbr": "ME",
     "description": "Maine's shorter summer season makes every splash pad day count. Communities across the Pine Tree State open their water play facilities in mid-June and run through August, giving families a compact but enthusiastic window of water fun."},
    {"name": "Maryland", "slug": "maryland", "abbr": "MD",
     "description": "Maryland's humid summers drive families to splash pads across the state. From the Baltimore metro's community spray parks to Montgomery County's aquatic facilities and Eastern Shore water play areas, there are options from Memorial Day through Labor Day."},
    {"name": "Massachusetts", "slug": "massachusetts", "abbr": "MA",
     "description": "Massachusetts communities take their splash pads seriously. Boston's parks system and suburban towns across the Commonwealth operate spray decks and splash pads that draw families throughout the summer months, typically from late June through Labor Day."},
    {"name": "Michigan", "slug": "michigan", "abbr": "MI",
     "description": "Michigan's warm summers along the Great Lakes and inland create strong demand for splash pads. Detroit, Grand Rapids, and communities across both peninsulas offer water play options ranging from free park splash pads to full aquatic centers."},
    {"name": "Minnesota", "slug": "minnesota", "abbr": "MN",
     "description": "Minnesota makes the most of its warm season with splash pads across the Twin Cities metro and outstate communities. Minneapolis, St. Paul, and their suburbs feature modern spray parks that run from June through August, giving families a welcome break from the Land of 10,000 Lakes' summer humidity."},
    {"name": "Mississippi", "slug": "mississippi", "abbr": "MS",
     "description": "Mississippi's hot, humid climate creates a long splash pad season that often stretches from April into October. Communities across the Magnolia State are adding water play features to their parks, giving families affordable cooling options during the long Southern summer."},
    {"name": "Missouri", "slug": "missouri", "abbr": "MO",
     "description": "Missouri's blend of Midwestern heat and humidity makes splash pads a summer essential. Kansas City, St. Louis, and communities across the Show-Me State offer free and paid water play options, with most facilities operating from Memorial Day through Labor Day."},
    {"name": "Montana", "slug": "montana", "abbr": "MT",
     "description": "Montana's Big Sky summers can bring surprising heat to the valleys and plains. Community aquatic centers and splash pads in cities like Billings, Missoula, and Great Falls provide welcome relief during the warm months from June through August."},
    {"name": "Nebraska", "slug": "nebraska", "abbr": "NE",
     "description": "Nebraska's communities have invested in splash pads and aquatic centers to combat the state's hot, humid summers. Omaha and Lincoln lead the way, with smaller cities across the state offering their own water play options from Memorial Day through Labor Day."},
    {"name": "Nevada", "slug": "nevada", "abbr": "NV",
     "description": "In a desert state where summer temperatures routinely top 100 degrees, splash pads are critical infrastructure. Las Vegas, Henderson, and Reno all feature community splash pads, with many operating from April through October thanks to the extended heat."},
    {"name": "New Hampshire", "slug": "new-hampshire", "abbr": "NH",
     "description": "New Hampshire's compact summer season runs from late June through August, and communities across the Granite State make the most of it with splash pads and water play areas in town parks and recreation centers."},
    {"name": "New Jersey", "slug": "new-jersey", "abbr": "NJ",
     "description": "New Jersey packs a dense network of splash pads into the Garden State. From the Shore communities to North Jersey suburbs and the cities in between, families have access to spray parks, aquatic centers, and water play areas from Memorial Day through September."},
    {"name": "New Mexico", "slug": "new-mexico", "abbr": "NM",
     "description": "New Mexico's dry desert heat makes water play a welcome summer tradition. Albuquerque, Santa Fe, and Las Cruces offer community splash pads and aquatic centers that operate through the warm months, providing cooling relief at altitude."},
    {"name": "New York", "slug": "new-york", "abbr": "NY",
     "description": "New York State offers splash pads from the five boroughs to the Finger Lakes. New York City's parks department operates dozens of spray showers and splash features across all boroughs, while suburban communities on Long Island, in Westchester, and upstate cities provide their own water play options from Memorial Day through Labor Day."},
    {"name": "North Carolina", "slug": "north-carolina", "abbr": "NC",
     "description": "North Carolina's warm climate and growing population have fueled investment in splash pads statewide. Charlotte, Raleigh-Durham, and the Triad lead with modern spray parks and aquatic centers, while mountain and coastal communities offer seasonal water play from May through September."},
    {"name": "North Dakota", "slug": "north-dakota", "abbr": "ND",
     "description": "North Dakota's summers bring warm temperatures that make splash pads a welcome addition to community parks. Fargo, Bismarck, and other cities across the state offer water play facilities during the June through August season."},
    {"name": "Ohio", "slug": "ohio", "abbr": "OH",
     "description": "Ohio has one of the deepest collections of splash pads and water parks in the country. Cincinnati's riverfront parks, Columbus's zoo-adjacent waterparks, Dayton's outstanding metro parks system, and Sandusky's Lake Erie resort corridor give families over 100 water play destinations. The state is especially strong in free community splash pads operated by metro park systems."},
    {"name": "Oklahoma", "slug": "oklahoma", "abbr": "OK",
     "description": "Oklahoma's hot summers drive families to splash pads across the Sooner State. Oklahoma City, Tulsa, and communities throughout the state offer free and paid water play options, with most facilities opening in late April and running through September."},
    {"name": "Oregon", "slug": "oregon", "abbr": "OR",
     "description": "Oregon's summers may be shorter, but when the heat arrives in the Willamette Valley and eastern regions, splash pads become essential. Portland, Eugene, and communities across the state offer water play facilities typically running from June through September."},
    {"name": "Pennsylvania", "slug": "pennsylvania", "abbr": "PA",
     "description": "Pennsylvania communities have embraced splash pads from Philadelphia to Pittsburgh and everywhere in between. The state offers a strong mix of free municipal spray parks, community aquatic centers, and water play areas that run from Memorial Day through Labor Day."},
    {"name": "Rhode Island", "slug": "rhode-island", "abbr": "RI",
     "description": "The smallest state still makes room for water play. Rhode Island's communities offer splash pads and spray features in public parks, giving families a free way to cool off during the humid New England summer months."},
    {"name": "South Carolina", "slug": "south-carolina", "abbr": "SC",
     "description": "South Carolina's long, hot summers make splash pads a staple from the Upstate to the Lowcountry. Charleston, Columbia, Greenville, and Myrtle Beach all offer water play options, with many facilities running from April through October thanks to the state's warm climate."},
    {"name": "South Dakota", "slug": "south-dakota", "abbr": "SD",
     "description": "South Dakota communities make the most of their warm summers with splash pads and aquatic centers. Sioux Falls, Rapid City, and smaller towns offer water play facilities that draw families during the June through August season."},
    {"name": "Tennessee", "slug": "tennessee", "abbr": "TN",
     "description": "Tennessee's hot, humid summers drive strong demand for water play across the Volunteer State. Nashville and Middle Tennessee lead with community splash pads, the Smoky Mountains offer both indoor and outdoor waterparks, and Knoxville's metro parks provide free spray pad options. With over 50 facilities statewide, there's water play near every major city."},
    {"name": "Texas", "slug": "texas", "abbr": "TX",
     "description": "Everything is bigger in Texas — including the splash pad selection. The Lone Star State has one of the largest collections of water play facilities in the country, from Houston's massive park system to Dallas-Fort Worth's suburban spray parks, Austin's Barton Springs area, and San Antonio's community pools. Texas heat means many splash pads operate from March through November."},
    {"name": "Utah", "slug": "utah", "abbr": "UT",
     "description": "Utah's dry heat along the Wasatch Front drives families to splash pads and aquatic centers throughout the summer. Salt Lake City, Provo, and communities from Ogden to St. George offer water play options, with the southern part of the state enjoying an especially long warm season."},
    {"name": "Vermont", "slug": "vermont", "abbr": "VT",
     "description": "Vermont's short but sweet summer season brings families to community splash pads and water play areas across the Green Mountain State. The season runs from late June through August, making every splash pad day a treasured one."},
    {"name": "Virginia", "slug": "virginia", "abbr": "VA",
     "description": "Virginia offers splash pads from the Northern Virginia suburbs of Washington D.C. to the Hampton Roads coast and everywhere in between. The state's warm, humid summers run from May through September, and communities from Fairfax County to Virginia Beach have invested in modern spray parks and aquatic facilities."},
    {"name": "Washington", "slug": "washington", "abbr": "WA",
     "description": "Washington's splash pads shine during the dry summer months from July through September. Seattle, Tacoma, and communities across the Puget Sound and eastern Washington offer water play facilities that families look forward to as soon as the rain stops and the sun comes out."},
    {"name": "West Virginia", "slug": "west-virginia", "abbr": "WV",
     "description": "West Virginia's mountain communities offer splash pads and water play areas that provide relief during the warm summer months. From Charleston to smaller towns across the Mountain State, families will find community options from Memorial Day through Labor Day."},
    {"name": "Wisconsin", "slug": "wisconsin", "abbr": "WI",
     "description": "Wisconsin's splash pads and water parks span from Milwaukee's urban spray features to the Wisconsin Dells — the self-proclaimed Waterpark Capital of the World. Communities across the state operate seasonal splash pads from June through August, and the Dells offers year-round indoor waterpark options."},
    {"name": "Wyoming", "slug": "wyoming", "abbr": "WY",
     "description": "Wyoming's communities offer water play facilities to help families cool off during the warm mountain summers. While options are more limited than in more populated states, the cities and towns that have splash pads make them a valued part of the summer experience."},
]

# Feature filter categories (used for filter pages and nav)
CATEGORIES = [
    {"name": "Free Admission", "slug": "free-admission", "icon": "🆓",
     "description": "Splash pads with no admission cost",
     "intro": "Free splash pads are one of the best-kept secrets for family fun. Operated by city parks departments and community recreation centers, these facilities offer the same water play experience as paid attractions — ground-level jets, spray nozzles, and interactive features — without any cost. Many are located in public parks with playgrounds, restrooms, and picnic areas, making them a complete family outing at zero cost."},
    {"name": "Best for Toddlers", "slug": "toddlers", "icon": "👶",
     "description": "Gentle water features ideal for toddlers and young children",
     "intro": "Toddler-friendly splash pads feature gentle, low-pressure water jets and shallow ground-level spray areas designed for the youngest visitors. These facilities avoid the high-intensity sprayers and deep water that can overwhelm small children, offering a safe introduction to water play. Many also include shaded seating areas where parents can watch comfortably. If your child is between 1 and 4, these are the splash pads to start with."},
    {"name": "Best for Families", "slug": "families", "icon": "👨‍👩‍👧‍👦",
     "description": "Large splash pads with features for all ages",
     "intro": "Family splash pads offer something for every age — from gentle spray areas for toddlers to high-energy water cannons and dumping buckets for older kids. These larger facilities are designed so siblings of different ages can all play together without anyone being bored or overwhelmed. Many include adjacent playgrounds, picnic areas, and restrooms so families can spend a full morning or afternoon."},
    {"name": "With Shade", "slug": "with-shade", "icon": "⛱️",
     "description": "Splash pads with shaded areas to keep the sun off",
     "intro": "Shade matters — especially at splash pads where kids can spend hours in direct sunlight. These facilities include covered pavilions, shade sails, trees, or other structures that protect visitors from UV exposure. Shaded splash pads are particularly important in southern and desert states where summer sun intensity peaks. Even with shade, sunscreen is still recommended, but having a shaded rest area makes a big difference for both kids and parents."},
    {"name": "With Restrooms", "slug": "with-restrooms", "icon": "🚻",
     "description": "Splash pads that have on-site restrooms",
     "intro": "On-site restrooms are one of those amenities you don't think about until you need them — and at a splash pad with young children, you'll need them. These facilities have dedicated restroom buildings, often including changing areas where families can get into and out of swimwear. It's a practical detail that separates a quick splash from a full outing."},
    {"name": "With Picnic Areas", "slug": "with-picnic-areas", "icon": "🧺",
     "description": "Splash pads near picnic tables or pavilions",
     "intro": "Splash pads with picnic areas let families turn water play into a full outing. Pack a lunch, claim a table, and alternate between eating and splashing without having to leave and come back. Many facilities include shaded pavilions, grills, or nearby concession stands. It's the difference between a 30-minute splash and a three-hour family day."},
    {"name": "Indoor", "slug": "indoor", "icon": "🏠",
     "description": "Year-round indoor water play areas",
     "intro": "Indoor splash pads and water play areas operate year-round regardless of weather or season. These climate-controlled facilities — often found inside recreation centers, resorts, and dedicated waterpark buildings — offer slides, spray features, and pools in a warm, enclosed environment. They're the answer for families in northern states who want water play in January, or for anyone looking to avoid sunburn and rain delays."},
    {"name": "Accessible", "slug": "accessible", "icon": "♿",
     "description": "ADA accessible splash pads and water play areas",
     "intro": "Accessible splash pads are designed so children and adults of all abilities can enjoy water play. These facilities feature ADA-compliant surfaces, wheelchair-accessible spray areas, ground-level jets that don't require climbing or standing, and accessible paths to and from the water play area. Many also include accessible restrooms and parking. Every child deserves to play in the water — these facilities make that possible."},
    {"name": "Amusement Parks", "slug": "amusement-parks", "icon": "🎢",
     "description": "Theme and amusement parks with splash pad and water attractions",
     "intro": "Many of the country's most popular theme and amusement parks include splash pads, spray zones, and dedicated water areas alongside their rides and attractions. These facilities range from themed splash zones designed for younger visitors to full-scale water rides and play areas. They're a great way to cool off between coaster rides and add a water play dimension to a theme park visit."},
    {"name": "Water Parks", "slug": "water-parks", "icon": "🌊",
     "description": "Dedicated water parks and resort water parks with slides and attractions",
     "intro": "Dedicated water parks go well beyond a basic splash pad — they offer water slides, wave pools, lazy rivers, and multi-level splash structures alongside traditional spray features. These are full-day destinations with amenities like locker rooms, concessions, cabana rentals, and lifeguard coverage. Whether it's a community-operated aquatic park or a resort-scale waterpark, these facilities deliver the most complete water play experience available."},
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
