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
     "meta_description": "Find 50+ splash pads in Alabama — free spray parks in Birmingham, Huntsville, and Mobile. Family water play areas updated for 2026.",
     "description": "Alabama's long, humid summers create genuine demand for water play from April through September, and the state's communities have responded with a growing network of splash pads and spray parks. Birmingham leads the way with multiple community splash pads distributed across its park system, giving neighborhoods across Jefferson County access without a long drive. Huntsville has invested in modern aquatic facilities as the city's population has grown, adding spray features to several community parks. Mobile's Gulf Coast location means the heat arrives early and lingers late, and its parks offer water play options that take advantage of the extended season. Montgomery and Tuscaloosa round out the major urban centers with community splash pads and aquatic centers suited to family visits. Most municipal splash pads in Alabama are free of charge, though some aquatic centers attached to recreation facilities charge a small admission fee. The season's peak runs from June through August, when temperatures and humidity both climb into uncomfortable territory. Many Alabama splash pads are paired with playgrounds and covered pavilions, making them an easy full-morning outing for families with young children. Weekday mornings are noticeably less crowded than weekend afternoons, especially at the most popular facilities. Bringing sunscreen, water bottles, and a change of clothes will make the visit more comfortable. Always check with local parks departments before visiting, as hours and opening dates vary."},
    {"name": "Alaska", "slug": "alaska", "abbr": "AK",
     "meta_description": "Find splash pads in Alaska — free summer spray parks in Anchorage, Fairbanks, and the Mat-Su Valley. Short season, big fun. Updated 2026.",
     "description": "Alaska's splash pad season is short by any measure, but what the state lacks in season length it makes up for in enthusiasm. From late June through August, communities across southcentral and interior Alaska make the most of the long summer daylight hours, and the warmest stretches — when temperatures in Anchorage and Fairbanks can push into the 70s and occasionally the 80s — send families looking for water play options. Anchorage, the state's largest city, has the most developed splash pad infrastructure, with spray features in several community parks that fill quickly on warm days. Fairbanks, in the interior, experiences some of Alaska's hottest summer temperatures, and its community water play areas are popular when the mercury climbs. Palmer and Wasilla in the Matanuska-Susitna Valley have added facilities suited to the region's growing population. The novelty of a hot day in Alaska should not be underestimated — locals take full advantage of every warm afternoon. Most municipal splash pads are free and operate during park hours, but the season can be unpredictable; some years a cool, wet summer limits attendance significantly. Checking local parks department websites before visiting is especially important in Alaska, where facilities may close or adjust hours based on weather conditions. Bring layers, as temperatures can shift quickly even on sunny days."},
    {"name": "Arizona", "slug": "arizona", "abbr": "AZ",
     "meta_description": "Find 100+ splash pads in Arizona — free spray parks in Phoenix, Scottsdale, and Tucson. Beat the desert heat with family water play, 2026.",
     "description": "In a state where summer temperatures routinely exceed 110 degrees in the low desert, splash pads are genuinely essential infrastructure — not a luxury amenity. Arizona's cities have invested heavily in water play facilities, and the results are among the most impressive in the country. Phoenix operates an extensive network of free community splash pads through its parks and recreation department, with dozens of locations spread across the metro area. Scottsdale and Tempe have added modern spray parks to their community parks, many with shade structures specifically designed for desert conditions. Tucson, in the Sonoran Desert to the south, offers its own community water play options through Pima County and city parks. The season in Arizona is unusually long by national standards, with many facilities opening as early as March and running through October to capture the full extent of the warm season. The brutal heat of June, July, and August means morning visits — before 10 a.m. — are the most comfortable option. Many Arizona splash pads include generous shade sails and covered seating areas, reflecting an understanding that sun protection is as important as water access in the desert. Most municipal splash pads are free. Bringing water bottles and applying sunscreen before entering the splash area will make a significant difference on the hottest days."},
    {"name": "Arkansas", "slug": "arkansas", "abbr": "AR",
     "meta_description": "Find 40+ splash pads in Arkansas — free spray parks in Little Rock, Fayetteville, and Bentonville. Family water play near you, updated 2026.",
     "description": "Arkansas summers are hot and humid, with temperatures regularly reaching the high 90s from June through August across the lowlands and river valleys. The state has expanded its splash pad offerings steadily in recent years, giving families across the Natural State more water play options than ever before. Little Rock anchors the state's splash pad network with multiple community facilities managed by city and county parks departments, including modern spray features that attract families from across the metro area. Fayetteville and the wider Northwest Arkansas region — one of the fastest-growing corners of the country — has seen significant investment in community parks and water play, with Bentonville and Rogers both adding facilities in recent years. Hot Springs, with its long tradition of tourism and recreation, offers water play options that complement the area's resort character. Fort Smith, near the Oklahoma border, has its own community splash pads serving the Arkansas River Valley. Most municipal splash pads in Arkansas are free of charge and operate from Memorial Day through Labor Day. The Ozarks region in the north tends to be slightly cooler than the lowlands, but summer heat is still significant enough to make water play very popular. Weekday mornings are the least crowded times at most facilities. Bringing sunscreen and insect repellent is advisable, as Arkansas summers can be both sunny and buggy."},
    {"name": "California", "slug": "california", "abbr": "CA",
     "meta_description": "Find 200+ splash pads in California — free spray parks near Los Angeles, San Diego, Sacramento, and the Bay Area. Updated 2026.",
     "description": "California's sheer geographic variety means splash pad seasons vary dramatically from one region to another. In San Diego, where the climate is mild year-round, some facilities operate continuously, while communities in the inland Central Valley — where summer temperatures in Fresno and Bakersfield routinely top 105 degrees — see their splash pads become critical cooling resources from May through October. Los Angeles operates spray features in community parks across its sprawling park system, giving urban families access without venturing far from their neighborhoods. The Bay Area's milder coastal climate tempers demand compared to inland California, but communities in the East Bay and South Bay have invested in water play areas suited to their warm summers. Sacramento and the surrounding suburbs have expanded their splash pad offerings as the region's population has grown. Northern California communities, including Redding and Chico, face intense summer heat and have developed aquatic facilities accordingly. Most California municipal splash pads are free, though some aquatic centers charge admission. The wide variation in climate and local policy means checking specific facility websites before visiting is especially important. On the hottest days, arriving in the morning gives families the best experience. Sun protection — sunscreen, hats, and shade-seeking — is essential throughout the state's inland and desert regions."},
    {"name": "Colorado", "slug": "colorado", "abbr": "CO",
     "meta_description": "Find 75+ splash pads in Colorado — free spray parks in Denver, Colorado Springs, and Fort Collins. Rocky Mountain water play, 2026.",
     "description": "Colorado's high-altitude sunshine makes water play a more urgent need than the state's dry climate might suggest. Even on days when temperatures seem moderate, the intensity of UV radiation at elevation means time outdoors can feel much more draining than in lower-altitude states. Denver's parks and recreation department operates splash pads in numerous community parks across the city, serving families in neighborhoods from Stapleton to Wash Park. The suburban communities along the Front Range — Aurora, Lakewood, Arvada, Westminster, and Thornton — have invested in modern spray parks that complement their community recreation centers. Colorado Springs has developed aquatic facilities suitable for the region's large military and family population. Fort Collins, with its strong park culture, offers community splash pads that draw crowds through the summer. The season along the Front Range typically runs from late May through September, with July and August being the busiest months. Colorado's afternoon thunderstorm pattern means morning visits are generally smarter than afternoon trips. Most municipal splash pads are free of charge; some recreation centers charge admission for access to their broader aquatic facilities. Sunscreen is non-negotiable at Colorado's elevation, and bringing water is always a good idea even at a water play facility."},
    {"name": "Connecticut", "slug": "connecticut", "abbr": "CT",
     "meta_description": "Find 50+ splash pads in Connecticut — free spray parks in Hartford, New Haven, and Stamford. New England family water play, updated 2026.",
     "description": "Connecticut packs a genuinely impressive number of splash pads into its relatively small footprint, and the quality of the state's community water play facilities reflects the region's investment in parks and recreation. Hartford has developed free spray features in several city parks, giving families in the capital region affordable water play options through the summer. New Haven and Bridgeport have invested in community aquatic facilities that include splash pad zones alongside traditional pool amenities. Stamford and Greenwich, in the southwestern corner of the state nearest to New York City, offer well-maintained community splash pads that attract local families and visitors alike. Manchester, Meriden, and other mid-sized Connecticut cities have added modern spray parks to their parks systems in recent years. The season runs from Memorial Day through Labor Day, occasionally stretching into mid-September during warm autumns. Connecticut's coastal humidity makes summer days feel hotter than the thermometer indicates, making a splash pad a genuine relief on July and August afternoons. Most municipal splash pads in Connecticut are free, though some larger aquatic centers charge a modest admission fee. Weekday mornings are the best times to visit popular facilities, as weekend afternoons can get quite crowded during peak summer weeks. Checking the local parks department website for current hours is always recommended before making the trip."},
    {"name": "Delaware", "slug": "delaware", "abbr": "DE",
     "meta_description": "Find splash pads in Delaware — free water play areas in Wilmington, Newark, and Dover. Mid-Atlantic family spray parks near you, 2026.",
     "description": "Delaware may be the nation's second-smallest state, but its communities take summer recreation seriously, and splash pads have become a welcome fixture in parks across the First State. Wilmington, the state's largest city, operates spray features in community parks that serve families throughout New Castle County, with free access during operating hours. Newark, home to the University of Delaware, has invested in community park improvements that include water play areas suited to the city's family-friendly neighborhoods. Dover, the state capital, offers water play options through its parks and recreation department, serving families in Kent County. Rehoboth Beach and the Delaware shore communities attract summer visitors from across the mid-Atlantic region, and some beach-adjacent parks feature spray features alongside their other amenities. The season in Delaware runs from Memorial Day through Labor Day, with peak demand in July and August when mid-Atlantic humidity makes the state's warm temperatures feel particularly intense. Most municipal splash pads in Delaware are free of charge and open to all residents during park hours. Delaware's small size is actually an advantage for families — no community in the state is more than an hour from multiple water play options. Checking local parks department websites is the most reliable way to find current operating hours and seasonal schedules before heading out."},
    {"name": "Florida", "slug": "florida", "abbr": "FL",
     "meta_description": "Find 200+ splash pads in Florida — free spray parks in Orlando, Tampa, Jacksonville, and Miami. Year-round family water play, 2026.",
     "description": "Florida is genuinely one of the best states in the country for splash pads, and the sheer volume of options reflects a culture built around water and outdoor recreation. The combination of year-round warm weather and a large, family-oriented population has driven investment in water play facilities at every scale, from small neighborhood spray features to elaborate aquatic parks. Orlando and the surrounding communities offer dozens of splash pads, both free municipal options and paid attractions tied to the area's resort and theme park economy. Tampa Bay communities — including Tampa, St. Petersburg, and Clearwater — operate free community splash pads in neighborhood parks throughout the metro area. Jacksonville, the largest city by area in the contiguous United States, has distributed water play facilities across its sprawling park system. Miami-Dade County offers splash pads that operate well into the fall, taking advantage of the region's subtropical climate. Many Florida splash pads operate year-round or close only during the mildest winter months. The summer rainy season, which runs roughly June through September, brings daily afternoon thunderstorms that can interrupt outdoor plans — morning visits are the safest bet. Most municipal splash pads are free. Always check local parks department websites for hours, as facilities in Florida often have specific operating schedules."},
    {"name": "Georgia", "slug": "georgia", "abbr": "GA",
     "meta_description": "Find 100+ splash pads in Georgia — free spray parks in Atlanta, Savannah, and Augusta. Family-friendly water play near you, updated 2026.",
     "description": "Georgia's hot, humid summers create strong and sustained demand for water play across the state, and communities from the mountains to the coast have responded with a growing network of splash pads and aquatic facilities. Metro Atlanta leads the state in both quantity and variety — Fulton, DeKalb, Gwinnett, and Cobb counties have all invested in community splash pads that serve suburban and urban families throughout the region. The city of Atlanta itself operates spray features in several parks, offering free water play in neighborhoods across the city. Savannah, with its coastal humidity and historic park squares, has added splash pad options that suit the city's character. Augusta and Columbus, as major mid-sized cities, each offer community aquatic facilities with spray features. The season in Georgia runs from April through September at many facilities, with the peak from June through August. Summer heat in Georgia is genuine and unrelenting — temperatures in the high 90s paired with humidity that makes conditions feel well above 100 degrees are common through July and August. Shade and seating near the splash area are important amenities to look for when choosing a facility. Most municipal splash pads in Georgia are free of charge. Weekend afternoons are the busiest times at popular facilities; weekday mornings offer a more relaxed experience. Sunscreen, water bottles, and a change of clothes are standard gear for Georgia splash pad visits."},
    {"name": "Hawaii", "slug": "hawaii", "abbr": "HI",
     "meta_description": "Find splash pads in Hawaii — free spray parks on Oahu, Maui, and the Big Island. Year-round family water play for all ages, 2026.",
     "description": "Hawaii's tropical climate means water play is a year-round possibility, and while the islands are internationally recognized for their beaches, splash pads have found a meaningful place in community parks across the state. On Oahu, which is home to the majority of Hawaii's population, community parks in Honolulu and surrounding municipalities offer spray features that give families a sheltered alternative to the beach — particularly useful for parents of very young children who benefit from the shallower, controlled water play environment. The Windward and Leeward sides of Oahu offer different microclimates, but both experience the kind of warm, humid conditions that make water play appealing year-round. Maui's growing communities, particularly around Kahului and Kihei, have developed park facilities that include water play options. The Big Island's diverse climate zones mean some areas, particularly around Kailua-Kona on the dry western coast, are especially well-suited to splash pad visits. Most community splash pads in Hawaii are free and open to the public during park hours. Hawaii's near-constant UV intensity means sunscreen is absolutely essential, even on overcast days. Visiting early in the morning is recommended to avoid both the midday heat and peak crowd times. The state's tourist economy means some water play facilities near resort areas may have different access arrangements than purely municipal parks."},
    {"name": "Idaho", "slug": "idaho", "abbr": "ID",
     "meta_description": "Find 40+ splash pads in Idaho — free spray parks in Boise, Nampa, and Meridian. Treasure Valley family water play areas, 2026.",
     "description": "Idaho's summers are drier and often hotter than visitors expect, especially in the southern valleys and the Treasure Valley around Boise. The combination of desert heat and abundant sunshine makes splash pads a valued community amenity across the state. Boise leads the state with the most developed splash pad infrastructure, with the Boise Parks and Recreation department operating water play facilities in multiple community parks across the city and its suburbs, including Nampa and Meridian. Meridian in particular has seen rapid population growth and has invested in modern community parks that include spray features well-suited to family visits. Twin Falls, situated near the Snake River Canyon, offers community water play options that serve the families of south-central Idaho. Coeur d'Alene, in the northern Panhandle, has a slightly different climate — more Pacific Northwest than high desert — but still sees warm enough summers to make splash pads worthwhile. The season statewide typically runs from June through early September, with peak demand in July and August when temperatures in the Treasure Valley can exceed 100 degrees. Most municipal splash pads in Idaho are free of charge. Mornings before 11 a.m. are the most comfortable visiting times during peak summer heat. Sunscreen, water, and sandals or water shoes are the practical essentials for an Idaho splash pad visit."},
    {"name": "Illinois", "slug": "illinois", "abbr": "IL",
     "meta_description": "Find 150+ splash pads in Illinois — free spray parks in Chicago, Naperville, and Springfield. Midwest family water play guide, 2026.",
     "description": "Illinois has one of the deepest splash pad networks in the Midwest, driven by the Chicago Park District's extensive investment in neighborhood water play and the steady development of suburban aquatic facilities across the collar counties. Chicago itself operates spray features and water play zones in dozens of parks across all 77 community areas, giving urban families free access to water play within walking distance of most neighborhoods. The northern suburbs — communities like Evanston, Naperville, and Wheaton — have built modern community splash pads that draw families throughout the summer. DuPage, Lake, Kane, and Will counties all feature multiple facilities ranging from free neighborhood spray parks to full aquatic centers with admission fees. Downstate Illinois is well-represented too: Peoria, Springfield, Rockford, and Champaign-Urbana all operate community water play facilities that serve their regions. The season across most of Illinois runs from Memorial Day through Labor Day, with July and August being the busiest months. Illinois summers bring genuine heat and humidity, particularly in the Chicago metro and central Illinois, with temperatures frequently climbing into the 90s. Most municipal splash pads in Chicago and the suburbs are free. For the largest facilities, arriving before 10 a.m. on weekends is the best strategy for finding open space. Always check the Chicago Park District or local parks department website for current schedules and any seasonal closures."},
    {"name": "Indiana", "slug": "indiana", "abbr": "IN",
     "meta_description": "Find 75+ splash pads in Indiana — free spray parks in Indianapolis, Fort Wayne, and South Bend. Hoosier State water play areas, 2026.",
     "description": "Indiana's parks departments have made splash pads a summer priority across the Hoosier State, and the result is a solid network of community water play options serving families from Gary to Evansville. Indianapolis anchors the state with the most options — Indy Parks operates spray features in neighborhoods throughout the city, and Hamilton County communities like Carmel and Fishers have built some of the state's most modern and well-equipped splash pad facilities. Fort Wayne, the state's second-largest city, has invested in community aquatic amenities that include splash pad zones with features suited to a range of ages. South Bend, Bloomington, and Muncie each offer community water play options through their parks and recreation departments. The season in Indiana runs from Memorial Day through Labor Day, with July and August being the peak months for attendance. Indiana summers are genuinely hot and humid — the Ohio River Valley in the south tends to be particularly steamy — making a well-maintained splash pad a meaningful relief for families on summer afternoons. Most municipal splash pads in Indiana are free of charge, though some recreation center aquatic facilities charge admission. Weekend mornings are the best time to visit popular facilities before the afternoon crowds arrive. Sunscreen, a towel, and a change of clothes are the practical basics for any Indiana splash pad outing."},
    {"name": "Iowa", "slug": "iowa", "abbr": "IA",
     "meta_description": "Find 60+ splash pads in Iowa — free spray parks in Des Moines, Cedar Rapids, and the Quad Cities. Family water play near you, 2026.",
     "description": "Iowa's splash pads and community aquatic facilities are genuine gathering places during the summer months, and the quality of the state's parks investment shows across both its cities and smaller communities. Des Moines has the most developed splash pad network in the state, with the city's parks department operating free spray features in neighborhoods across the metro and suburban communities like West Des Moines and Ankeny adding their own facilities. Cedar Rapids has similarly invested in community water play, with parks that pair splash pads with playgrounds and picnic amenities for a complete family outing. Davenport and the Quad Cities area, along the Mississippi River, offer water play options that serve both Iowa and Illinois families. Waterloo, Iowa City, and Sioux City round out the state's major urban centers with their own community aquatic amenities. The season typically runs from late May through Labor Day, with July and August bringing the most intense heat and humidity. Iowa summers can be surprisingly hot, with temperatures reaching the mid-90s and humidity that pushes heat index values well above 100 degrees during peak weeks. Most municipal splash pads in Iowa are free and operated during park hours without admission. Arriving on weekday mornings gives families the most relaxed experience at the most popular locations. Sunscreen and water bottles are practical necessities for any summer outing in Iowa's open, sun-exposed parks."},
    {"name": "Kansas", "slug": "kansas", "abbr": "KS",
     "meta_description": "Find 50+ splash pads in Kansas — free spray parks in Wichita, Overland Park, and Topeka. Sunflower State family water play, 2026.",
     "description": "Kansas summers are hot, often dry, and frequently windy, and the state's communities have built quality splash pads and aquatic facilities to help families cool off during the long warm season. Wichita leads the state with the most diverse collection of water play options, including free community splash pads in city parks and larger paid aquatic centers with multiple features. The city's park system serves families across south-central Kansas and draws visitors from the surrounding region. Overland Park and Olathe, in the Kansas City metro's Kansas portion, have invested heavily in modern community parks and recreation facilities that include well-designed splash pads popular with suburban families. Lawrence, home to the University of Kansas, offers community water play that reflects the college town's focus on family-friendly recreation. Topeka, the state capital, has community splash pads that serve central Kansas families through the summer months. The season typically runs from Memorial Day through Labor Day, with July being the most intense month for both heat and demand. Kansas is known for strong summer storms that can develop quickly, so checking the weather before heading out is a good habit. Most municipal splash pads across Kansas are free. Many facilities include shaded pavilion seating, which is a welcome feature in a state where the sun is intense and shade trees are not always abundant. Weekday mornings offer the least crowded visiting experience."},
    {"name": "Kentucky", "slug": "kentucky", "abbr": "KY",
     "meta_description": "Find 50+ splash pads in Kentucky — free spray parks in Louisville, Lexington, and Bowling Green. Bluegrass State water play, 2026.",
     "description": "Kentucky's warm, humid summers create steady demand for water play across the Bluegrass State, and the state's communities have developed a growing collection of splash pads and aquatic facilities that serve families from Appalachia to the Purchase region. Louisville anchors Kentucky's splash pad offerings with the most diverse selection in the state — the city's Metro Parks department operates spray features in community parks serving Louisville's sprawling urban and suburban neighborhoods, with several facilities offering free access. Lexington, the second-largest city, has invested in community aquatic facilities that include modern splash pad zones suited to the Fayette County family population. Bowling Green, a growing mid-sized city in south-central Kentucky, has expanded its parks and recreation options to include splash pad facilities. Northern Kentucky communities across the river from Cincinnati — including Covington and Florence — have developed water play options that complement the broader Cincinnati metro's aquatic offerings. The season runs from May through September, with the peak from June through August when Kentucky's river valley humidity makes conditions feel especially intense. Most municipal splash pads in Kentucky are free of charge. Many are paired with playgrounds and pavilion seating, making them well-suited to half-day family outings. Arriving on weekday mornings is the most relaxed visiting strategy. Always check local parks department websites for current seasonal hours."},
    {"name": "Louisiana", "slug": "louisiana", "abbr": "LA",
     "meta_description": "Find 50+ splash pads in Louisiana — free spray parks in Baton Rouge, New Orleans, and Lafayette. Bayou State water play, 2026.",
     "description": "Louisiana's climate is among the most challenging in the country for outdoor summer activity — heat and humidity combine to create conditions where a splash pad isn't just pleasant, it's a genuine public health benefit. The state's communities have responded with water play options that take advantage of Louisiana's long warm season, which can stretch from March through October in the southern parishes. Baton Rouge has developed one of the state's strongest municipal splash pad networks, with free community spray parks in city parks across East Baton Rouge Parish that serve families throughout the summer. New Orleans, with its distinctive neighborhood culture, has invested in community parks that include splash pads, though flooding-related park challenges require checking current facility status. Lafayette, in Acadiana, offers community water play options that reflect the region's investment in outdoor recreation. Shreveport and Monroe serve north Louisiana families with aquatic facilities suited to the region's hot summers. Most municipal splash pads in Louisiana are free, though some aquatic centers charge admission. The summer rainy season means afternoon thunderstorms are a near-daily occurrence from June through September, making morning visits the most reliable choice. Insect repellent is worth adding to the bag alongside sunscreen, particularly in areas near water. Check local parks departments for current hours and seasonal schedules, which can vary significantly across the state."},
    {"name": "Maine", "slug": "maine", "abbr": "ME",
     "meta_description": "Find splash pads in Maine — free summer spray parks in Portland, Bangor, and the Lewiston-Auburn area. Granite Coast water play, 2026.",
     "description": "Maine's summer season is shorter than almost any other state's, but the communities that have invested in splash pads treat them as genuine seasonal treasures that families look forward to all year. The season typically runs from mid-June through mid-August, occasionally extending to Labor Day during warm years, giving families a compact but enthusiastic window of water play. Portland, Maine's largest city, anchors the state's splash pad options with facilities in community parks that serve the Greater Portland metro and draw visitors from surrounding towns. Bangor, in central Maine, offers community water play options through its parks and recreation department that serve families across Penobscot County. The Lewiston-Auburn metro area has invested in community aquatic facilities that reflect the region's family-focused parks programs. Coastal communities like Saco and Biddeford, which attract summer visitors, have added water play features to their parks. Maine summers can be genuinely warm and humid — when the heat arrives in late July, a splash pad becomes one of the most popular destinations in any community. Most municipal splash pads in Maine are free of charge. Because the season is short, popular facilities fill up quickly on the hottest days, and weekday mornings are the most relaxed visiting option. Checking local parks department websites for opening dates is essential, as Maine facilities often have the shortest predictable operating windows of any New England state."},
    {"name": "Maryland", "slug": "maryland", "abbr": "MD",
     "meta_description": "Find 75+ splash pads in Maryland — free spray parks in Baltimore, Rockville, and Annapolis. Chesapeake region family water play, 2026.",
     "description": "Maryland's humid mid-Atlantic summers drive consistent demand for water play, and the state's diverse communities have built an impressive range of splash pads and aquatic facilities to serve families from the mountains to the Chesapeake Bay. The Baltimore metro leads the state in volume — the city's recreation and parks department operates spray features in community parks across Baltimore's neighborhoods, and surrounding counties including Baltimore County, Howard County, and Anne Arundel County have all invested in modern community splash pad facilities. Montgomery County, in the Washington D.C. suburbs, has one of the strongest aquatic recreation programs in the region, with multiple community splash pads and aquatic centers serving the county's large, family-oriented population. Prince George's County similarly offers community water play options that serve families across the suburban Washington corridor. On the Eastern Shore, communities like Annapolis and Ocean City-area parks offer splash pad options suited to their summer visitor populations. The season runs from Memorial Day through Labor Day, with the peak from late June through August when Maryland's coastal humidity makes conditions feel especially warm. Most municipal splash pads are free, though some county aquatic centers charge admission. Weekday mornings are consistently the least crowded visiting times. Always verify hours with local parks departments before visiting, as Maryland facility schedules vary widely by county and municipality."},
    {"name": "Massachusetts", "slug": "massachusetts", "abbr": "MA",
     "meta_description": "Find 75+ splash pads in Massachusetts — free spray parks in Boston, Worcester, and Springfield. Bay State family water play, 2026.",
     "description": "Massachusetts communities take their splash pads seriously, and the investment shows across the Commonwealth. Boston's extensive parks system operates spray decks in neighborhood parks from Jamaica Plain to East Boston, giving urban families easy access without a long drive. Suburban towns across Greater Boston — from the South Shore to the MetroWest region — have added dedicated splash pad facilities to their community parks, many of them free and open to all residents. The season typically runs from late June through Labor Day, though some facilities open as early as Memorial Day during warm springs. New England's humidity can make summer days in Massachusetts feel hotter than the thermometer suggests, making a shaded splash pad with nearby seating a genuine relief for parents and kids alike. Beyond the Boston metro, communities in the Pioneer Valley, Cape Cod, and the North Shore offer their own water play options. Many splash pads are paired with traditional playgrounds, picnic areas, and walking paths, making them an ideal all-day outing. Weekday mornings are generally the least crowded times to visit. Most municipal splash pads are free of charge, though some aquatic centers charge a small admission fee. Always check local parks department websites for seasonal opening dates and hours, as they vary by municipality."},
    {"name": "Michigan", "slug": "michigan", "abbr": "MI",
     "meta_description": "Find 100+ splash pads in Michigan — free spray parks in Detroit, Grand Rapids, and Lansing. Great Lakes family water play guide, 2026.",
     "description": "Michigan's position between four of the five Great Lakes gives it a distinctive summer climate — warm, occasionally humid, and enthusiastically embraced by residents who understand what a long winter means for summer recreation. The state has developed a strong splash pad network that serves both peninsulas, with Detroit and the metro area leading in volume. Detroit's city parks and suburban communities throughout Wayne, Oakland, and Macomb counties offer free and paid water play options at various scales, from neighborhood spray pads to full aquatic centers. Grand Rapids, Michigan's second-largest city, has invested in community parks that include modern splash pad facilities serving families across Kent County and the surrounding region. Lansing and East Lansing, home to Michigan State University, offer community water play options with a college-town sensibility. Traverse City, a popular northern Michigan destination, and communities throughout the Petoskey area and the Upper Peninsula bring water play options to summer tourists and year-round residents alike. The season typically runs from Memorial Day through Labor Day in Lower Michigan, with the Upper Peninsula's shorter warm season compressing operations to June through August. Most municipal splash pads in Michigan are free of charge. Lake Michigan's western shore draws substantial summer tourism, and communities like Muskegon and Holland offer water play facilities that complement beach access. Weekday mornings at popular facilities are significantly less crowded than weekend afternoons."},
    {"name": "Minnesota", "slug": "minnesota", "abbr": "MN",
     "meta_description": "Find 75+ splash pads in Minnesota — free spray parks in Minneapolis, St. Paul, and Rochester. Twin Cities water play guide, 2026.",
     "description": "Minnesota's summer arrives decisively and Minnesotans embrace it with equal decisiveness — and splash pads are a central part of that summer enthusiasm. The Twin Cities metro leads the state with the most robust splash pad network, with Minneapolis and St. Paul operating spray features in community parks across both cities through the Minneapolis Park and Recreation Board and St. Paul Parks and Recreation departments. Suburban communities in Hennepin, Ramsey, Dakota, and Washington counties have invested in modern spray parks that draw consistent crowds through the season. Rochester, home to the Mayo Clinic, has developed community parks with water play suited to its family-oriented population. Duluth, on the western end of Lake Superior, has a cooler microclimate than the Twin Cities but still offers community water play options during its warm summer months. St. Cloud and Mankato anchor central and southern Minnesota with their own community aquatic facilities. The season runs from mid-June through mid-August at most Minnesota facilities, with some extending to Labor Day. Minnesota's summer humidity can make July and August feel significantly hotter than the actual temperature, making a splash pad a genuine relief on peak summer days. Most municipal splash pads are free of charge. Weekday mornings are the least crowded option at popular facilities. Always check local parks department websites for current seasonal hours, as Minnesota facilities often have specific opening and closing windows tied to lifeguard staffing."},
    {"name": "Mississippi", "slug": "mississippi", "abbr": "MS",
     "meta_description": "Find 30+ splash pads in Mississippi — free spray parks in Jackson, Gulfport, and Hattiesburg. Gulf Coast family water play, 2026.",
     "description": "Mississippi's summers are long, hot, and intensely humid — conditions that make water play not just appealing but genuinely necessary for outdoor family time from late spring through early fall. The state's communities are steadily adding splash pads and spray features to their parks, and the pace of investment has increased as residents recognize the public benefit of free or affordable water play. Jackson, the state capital, has community parks with splash pad facilities that serve metro area families throughout the extended summer season. Gulfport and Biloxi on the Gulf Coast offer a more tourist-oriented set of water play options, with coastal humidity and warm temperatures that make the season unusually long — April through October is a realistic operational window. Hattiesburg serves south-central Mississippi families with community aquatic options, while Tupelo anchors water play access in the northeastern corner of the state. Most municipal splash pads in Mississippi are free of charge, reflecting the community-focused investment in parks across the state. The summer heat peaks in July and August, when daytime temperatures in the mid-to-upper 90s combined with humidity push heat index values well above 100 degrees. Morning visits — before 10 a.m. — are the most comfortable choice during peak summer weeks. Sunscreen, insect repellent near wooded parks, and water bottles are the practical essentials for a Mississippi splash pad outing. Local parks departments are the best source for current hours and seasonal schedules."},
    {"name": "Missouri", "slug": "missouri", "abbr": "MO",
     "meta_description": "Find 75+ splash pads in Missouri — free spray parks in Kansas City, St. Louis, and Springfield. Show-Me State water play, 2026.",
     "description": "Missouri's position at the geographic heart of the country means it gets the full force of Midwestern summer — heat, humidity, and the kind of sticky August days that make a splash pad one of the most appealing destinations in any community. The state's two major metros anchor the splash pad network on both ends. Kansas City operates spray features and community aquatic facilities through its parks system, and suburban communities throughout Johnson and Clay counties have invested in modern splash pads that serve the Missouri suburbs of the metro area. St. Louis offers free community splash pads through its city parks department, and St. Louis County communities including Chesterfield, Ballwin, and Kirkwood have developed their own facilities with features suited to family visits. Columbia, home to the University of Missouri and one of the state's fastest-growing mid-sized cities, has community splash pads that reflect the city's parks investment. Springfield serves southwest Missouri families with aquatic facilities appropriate to the Ozarks region. The season runs from Memorial Day through Labor Day across most of Missouri, with the peak demand falling in July and August when temperatures in the Kansas City and St. Louis metros frequently reach the mid-90s alongside oppressive humidity. Most municipal splash pads in Missouri are free. Some larger recreation center aquatic facilities charge admission. Weekday mornings are the least crowded times to visit. Checking local parks department websites for current hours is recommended, as schedules can change throughout the season."},
    {"name": "Montana", "slug": "montana", "abbr": "MT",
     "meta_description": "Find splash pads in Montana — free summer spray parks in Billings, Missoula, and Great Falls. Big Sky family water play, 2026.",
     "description": "Montana's reputation for dramatic scenery and outdoor adventure sometimes overshadows the practical reality of its summers: the valleys and plains can get genuinely hot, and families are grateful for any water play option within reach. Billings, the state's largest city, leads Montana's splash pad network with community aquatic facilities that serve the Yellowstone Valley region and draw visitors from the surrounding area. Missoula, anchored by the University of Montana and a strong outdoor recreation culture, has community splash pad facilities that reflect the city's parks investment and suit its family-friendly character. Great Falls and Helena, the state capital, offer community water play options through their parks and recreation departments. Bozeman, one of Montana's fastest-growing communities, has added splash pad facilities to keep pace with its expanding family population. The season typically runs from mid-June through August, capturing the core of Montana's mountain summer. July and August in the valleys can bring temperatures well into the 90s with lower humidity than most of the country, making the heat feel intense without the heaviness of the South or Midwest. Many Montana splash pads are free and operated by city parks departments during park hours. Because facilities are fewer and more spread out than in more densely populated states, verifying that a specific location is open before making a long drive is particularly worthwhile. Sunscreen is essential in Montana's high-altitude, clear-sky summer sun."},
    {"name": "Nebraska", "slug": "nebraska", "abbr": "NE",
     "meta_description": "Find 40+ splash pads in Nebraska — free spray parks in Omaha, Lincoln, and Grand Island. Cornhusker State family water play, 2026.",
     "description": "Nebraska's communities have invested steadily in splash pads and aquatic centers to combat the state's hot, humid summers, and the results are felt statewide. Omaha leads with multiple community splash pads spread across its parks system, serving families in neighborhoods throughout the metro. Lincoln's parks and recreation department has similarly expanded water play options, with facilities that draw consistent crowds through the summer months. Beyond the two major cities, mid-sized communities including Kearney, Norfolk, Grand Island, and Hastings have developed their own splash pad facilities, reflecting the broad community commitment to outdoor recreation across Nebraska. The season typically runs from Memorial Day through Labor Day, though peak attendance comes in July and August when temperatures and humidity peak on the Great Plains. The state's continental climate means summers can bring extended stretches of 90-degree days, making community water play especially welcome. Most municipal splash pads in Nebraska are free of charge and open to all residents, operating during park hours. Many are positioned alongside playgrounds and picnic shelters, making them a complete family outing. Arriving early on weekday mornings is the best strategy for avoiding weekend crowds at the most popular locations. Some larger aquatic centers combine splash pads with pools and slides and may charge admission."},
    {"name": "Nevada", "slug": "nevada", "abbr": "NV",
     "meta_description": "Find 75+ splash pads in Nevada — free spray parks in Las Vegas, Henderson, and Reno. Beat the desert heat with water play, 2026.",
     "description": "Nevada's desert climate makes splash pads something close to essential public infrastructure in the summer months. Las Vegas leads the state and is one of the most splash pad-rich cities in the country relative to its climate needs — the city of Las Vegas, Henderson, and the Clark County park system collectively operate multiple free community splash pads that serve the metropolitan area's large family population. Henderson in particular has invested in community parks with shade structures and spray features designed specifically for the desert environment, where summer temperatures routinely exceed 110 degrees and outdoor activity without water access becomes genuinely dangerous. Summerlin, a large planned community in the western Las Vegas Valley, has several neighborhood splash pads that serve the area's suburban families. North Las Vegas adds to the metro's water play options with its own community facilities. Reno, in northern Nevada, has a different climate — drier and slightly cooler than Las Vegas — but summer temperatures still frequently reach the 90s and above, driving demand for the splash pads available through the city's parks and recreation department. The season in the Las Vegas metro runs from approximately March through October, making it one of the longest operational windows in the country. Most municipal splash pads in Nevada are free. Morning visits, before the full desert heat arrives, are strongly recommended — for comfort and safety alike. Bringing water and applying sunscreen before arriving at the splash area is essential."},
    {"name": "New Hampshire", "slug": "new-hampshire", "abbr": "NH",
     "meta_description": "Find splash pads in New Hampshire — free spray parks in Manchester, Nashua, and Concord. Granite State family water play areas, 2026.",
     "description": "New Hampshire packs its splash pad season into a relatively compact window, but what the Granite State lacks in season length it compensates for with enthusiastic community investment in outdoor recreation. The season runs from late June through mid-August at most facilities, with some extending to Labor Day during warm summers. Manchester, the state's largest city, has community parks with splash pad features that serve families throughout the southern New Hampshire region. Nashua, near the Massachusetts border, offers community water play options that draw from the broader Merrimack Valley area and reflects the region's strong parks programs. Concord, the state capital, has invested in community aquatic facilities appropriate to its size and population. The Lakes Region — including communities near Lake Winnipesaukee — attracts summer visitors and has developed water play options alongside its other recreation amenities. The White Mountains region, while known primarily for hiking and scenic tourism, has community facilities in its valley towns that serve local families during the summer. New Hampshire's summer humidity can make July and August days feel meaningfully warmer than the thermometer suggests, particularly in the Merrimack Valley and the seacoast region near Portsmouth. Most municipal splash pads in New Hampshire are free of charge, reflecting the state's tradition of community-funded recreation. Because the season is short and popular on warm days, weekday mornings are the best time to visit without competition for space. Checking local parks department websites for opening dates and hours is especially important in New Hampshire, where facilities often have precise seasonal windows."},
    {"name": "New Jersey", "slug": "new-jersey", "abbr": "NJ",
     "meta_description": "Find 100+ splash pads in New Jersey — free spray parks near Newark, Trenton, and the Jersey Shore. Garden State water play, 2026.",
     "description": "New Jersey packs a dense network of splash pads into the Garden State, and the variety is genuinely impressive. From the Shore communities — where beachfront spray features attract summer tourists and locals alike — to the North Jersey suburbs close to New York City, the state offers water play at nearly every level of scale and budget. Central Jersey communities have built modern aquatic centers that combine traditional pools with splash pad zones, while South Jersey's residential neighborhoods feature free community spray parks that serve as neighborhood gathering places on hot days. The state's compact geography means most New Jersey families are within a 20-minute drive of at least one splash pad option. The season runs from Memorial Day through September, with the busiest period from late June through mid-August. New Jersey's mid-Atlantic climate brings genuine summer heat and humidity, with temperatures frequently reaching the high 80s and 90s during peak weeks. Most municipal splash pads in the state are free of charge and operate during park hours without advance registration. However, some aquatic centers require small admission fees and may fill quickly on the hottest days, so arriving early or visiting on weekday mornings gives families the best experience. Local parks department websites are the most reliable source for current hours and opening dates."},
    {"name": "New Mexico", "slug": "new-mexico", "abbr": "NM",
     "meta_description": "Find 40+ splash pads in New Mexico — free spray parks in Albuquerque, Santa Fe, and Las Cruces. High Desert family water play, 2026.",
     "description": "New Mexico's desert climate brings dry heat and intense high-altitude sunshine that makes water play one of the most sought-after summer activities across the Land of Enchantment. Albuquerque, the state's largest city, anchors New Mexico's splash pad network with community aquatic facilities managed by the city's parks and recreation department, offering free and low-cost water play for families throughout the Bernalillo County area. Rio Rancho, a large and rapidly growing suburb north of Albuquerque, has added community splash pad facilities that serve its expanding family population. Santa Fe, at an elevation of 7,000 feet, has a noticeably cooler summer climate than lower-elevation communities, but the high-altitude sun is intense and splash pads remain popular during the warmest months. Las Cruces, in the southern Mesilla Valley near the Texas border, experiences some of the state's most intense summer heat, and community water play options there reflect the extended season possible in New Mexico's south. Farmington serves families in the Four Corners region with its own community aquatic facilities. The season in most of New Mexico runs from late May through September, with the southern communities enjoying a somewhat longer operational window. New Mexico's monsoon season arrives in July and brings afternoon thunderstorms that can close outdoor splash pads temporarily — morning visits are the safest bet during monsoon months. Most municipal splash pads are free of charge. Sunscreen is essential at New Mexico's elevations, and staying hydrated in the dry desert air is important even when playing in the water."},
    {"name": "New York", "slug": "new-york", "abbr": "NY",
     "meta_description": "Find 200+ splash pads in New York — free spray parks in NYC, Buffalo, and Rochester. Empire State family water play guide, 2026.",
     "description": "New York State offers one of the most diverse and extensive splash pad networks in the country, driven by the sheer scale of New York City's parks investment and the strong parks programs in suburban and upstate communities. The NYC Parks department operates spray showers and water play features in hundreds of parks across all five boroughs, giving urban families free water play access within walking distance in most neighborhoods. The Bronx, Brooklyn, Queens, Manhattan, and Staten Island each have multiple facilities, with Brooklyn's Prospect Park and Queens' Flushing Meadows Corona Park among the most visited. Long Island communities in Nassau and Suffolk counties have built modern community splash pads that serve the region's large suburban family population. Westchester County, immediately north of the city, has a strong parks program with spray features and aquatic facilities across multiple communities. Upstate, Albany and the Capital Region, Buffalo and the Niagara Frontier, Rochester, and Syracuse all offer community splash pads and aquatic centers with free or low-cost access. The Finger Lakes and Hudson Valley regions add more options for families visiting those popular summer tourism areas. The season runs from Memorial Day through Labor Day across most of the state, with New York City spray features sometimes operating longer. Most municipal splash pads in New York are free. Weekday mornings are the best visiting strategy at the most popular locations, which can become very crowded on hot summer weekends."},
    {"name": "North Carolina", "slug": "north-carolina", "abbr": "NC",
     "meta_description": "Find 100+ splash pads in North Carolina — free spray parks in Charlotte, Raleigh, and Greensboro. Tar Heel water play, 2026.",
     "description": "North Carolina's warm climate, growing population, and strong community parks programs have combined to produce one of the Southeast's better splash pad networks — and the investment is visible from the mountains to the coast. Charlotte leads the state with the most diverse collection of options, with Mecklenburg County Parks and Recreation operating community splash pads and aquatic centers that serve families across the Charlotte metro. The Raleigh-Durham area, driven by the Research Triangle's rapid growth, has seen significant investment in community parks and water play, with Wake County and Durham County facilities complementing city-operated spray features. Greensboro and Winston-Salem in the Piedmont Triad offer community aquatic options that serve the region's urban and suburban families. The mountain region in the west — including communities near Asheville and Boone — has a cooler summer climate and fewer splash pads, but community options do exist and the mountain setting makes water play especially pleasant. Coastal communities like Wilmington and the Crystal Coast attract summer visitors and have splash pad options that reflect their tourism character. The season runs from May through September at most facilities, with the Coastal Plain's hotter climate enabling a longer window. Most municipal splash pads in North Carolina are free of charge. The state's afternoon thunderstorm pattern in summer means mornings are reliably the best time to visit outdoor facilities. Always check with local parks departments for current hours and seasonal schedules."},
    {"name": "North Dakota", "slug": "north-dakota", "abbr": "ND",
     "meta_description": "Find splash pads in North Dakota — free spray parks in Fargo, Bismarck, and Grand Forks. Prairie family water play areas, 2026.",
     "description": "North Dakota's summers arrive late and depart early, but the warmth they bring — and the relief they offer after a long prairie winter — makes splash pads a genuinely appreciated community amenity across the Peace Garden State. Fargo, the state's largest city and a growing regional hub, leads North Dakota's water play options with community splash pads and aquatic facilities that serve families throughout the Cass County area and draw visitors from surrounding communities. The Fargo-Moorhead metro's size relative to the rest of the state means it has the most developed infrastructure. Bismarck, the state capital, offers community water play through its parks department that serves the south-central North Dakota population. Grand Forks has community aquatic facilities that serve its university town population and the surrounding region. Minot, in the northwest, rounds out the state's major urban centers with water play options suited to its family-oriented community. The season in North Dakota is typically June through August, though July is the heart of the warm season — North Dakota summers can be genuinely hot on the open prairie, with temperatures reaching into the 90s during peak weeks. Most municipal splash pads are free of charge. The shorter season means facilities are particularly well-attended on the hottest days of summer, and weekday visits offer a noticeably more relaxed experience than crowded weekends. Checking local parks department websites before visiting is strongly recommended, as North Dakota facilities have some of the most precise seasonal windows in the country."},
    {"name": "Ohio", "slug": "ohio", "abbr": "OH",
     "meta_description": "Find 150+ splash pads in Ohio — free spray parks in Columbus, Cleveland, and Cincinnati. Buckeye State family water play guide, 2026.",
     "description": "Ohio has one of the most impressive splash pad networks in the country, and the depth of the state's aquatic recreation options reflects decades of investment in community parks and recreation. Columbus, the state capital and largest city, offers community splash pads through Columbus Recreation and Parks across multiple neighborhoods, along with the state's most visited aquatic destinations near the Columbus Zoo area. Cincinnati's park system operates spray features in community parks throughout Hamilton County, and the Greater Cincinnati metro's Ohio suburbs in Warren and Butler counties have built modern aquatic facilities with splash pad components. Cleveland's lakefront location on Lake Erie gives the city a distinctive summer culture, and the Greater Cleveland park systems — including the beloved Metroparks — offer water play options distributed across the region. Dayton's Five Rivers MetroParks is particularly well-regarded for its community recreation facilities, including splash pad and aquatic amenities. The northeastern Ohio communities around Akron, Canton, and Youngstown add further depth to the state's network, and the Lake Erie resort corridor around Sandusky brings additional paid water attractions. The season runs from Memorial Day through Labor Day at most Ohio facilities. Ohio summers are genuinely hot and humid, particularly in July and August, when temperatures reach the 90s and heat index values climb higher. Most municipal splash pads are free. The state's sheer density of options means nearly every Ohio family lives within 15 minutes of a water play facility during summer."},
    {"name": "Oklahoma", "slug": "oklahoma", "abbr": "OK",
     "meta_description": "Find 60+ splash pads in Oklahoma — free spray parks in Oklahoma City, Tulsa, and Norman. Sooner State family water play, 2026.",
     "description": "Oklahoma's summers are long, hot, and frequently accompanied by the kind of relentless sun that makes water play essential for outdoor family time. The state has developed a solid collection of splash pads and community aquatic facilities that typically open as early as late April and run through September, capturing a longer season than most Midwestern states. Oklahoma City anchors the state's splash pad network with the most options — the city's parks department operates community spray features in multiple neighborhoods, and surrounding communities including Edmond, Mustang, and Moore have added modern splash pad facilities to their parks systems in recent years. Tulsa, Oklahoma's second-largest city, offers community water play through Tulsa Parks with facilities that serve the metro area and reflect the city's investment in parks and recreation. Norman, home to the University of Oklahoma, has community aquatic options that suit its college-town and family character. Broken Arrow and Owasso, growing Tulsa suburbs, have developed their own splash pad facilities that serve the region's expanding family populations. The season's peak falls in June, July, and August, when Oklahoma temperatures routinely reach into the high 90s and above — summer heat in the state can be intense even by Southern standards. Most municipal splash pads are free. Mornings are the most comfortable visiting window. Sunscreen and water bottles are essential, and checking local parks websites for current hours is recommended before heading out."},
    {"name": "Oregon", "slug": "oregon", "abbr": "OR",
     "meta_description": "Find 75+ splash pads in Oregon — free spray parks in Portland, Salem, and Bend. Pacific Northwest family water play guide, 2026.",
     "description": "Oregon's relationship with water play is shaped by its famously variable climate — the wet western valleys and coast contrast sharply with the dry, hot eastern high desert, and splash pad demand and season length differ dramatically between regions. Portland leads the state with the most splash pad options, and the city's Parks and Recreation bureau operates spray features in community parks throughout the metro, drawing families during the summer dry season that typically runs from July through September. Portland's summers are genuinely warm and sunny, and the arrival of heat drives strong demand for water play in a city that doesn't broadly have air conditioning. Eugene and the southern Willamette Valley share a similar climate pattern, with a pronounced dry season making summer splash pad visits popular and practical. Eastern Oregon communities including Bend and Medford experience hotter, drier summers than the western valleys and have invested in community aquatic facilities that serve their growing populations through a longer warm season. Salem, Oregon's capital, sits in the heart of the Willamette Valley and has community splash pad options through its parks and recreation department. Most municipal splash pads in Oregon are free. The coastal communities west of the Coast Range experience a milder, foggier summer that limits splash pad demand, though some facilities exist. Checking local parks department websites is especially important in Oregon, where the dry season's arrival can shift the practical splash pad season by weeks from one year to the next."},
    {"name": "Pennsylvania", "slug": "pennsylvania", "abbr": "PA",
     "meta_description": "Find 100+ splash pads in Pennsylvania — free spray parks in Philadelphia, Pittsburgh, and Allentown. Keystone State water play, 2026.",
     "description": "Pennsylvania's geographic breadth — from the Delaware Valley to the Laurel Highlands and Lake Erie shore — means splash pad options span a wide range of settings and seasons. Philadelphia and its surrounding counties lead the state in volume, with the Philadelphia Parks and Recreation department operating free spray features in neighborhood parks across the city and Montgomery, Bucks, Chester, and Delaware counties offering modern community aquatic facilities in their parks systems. Pittsburgh's parks network on the western end of the state includes splash pad features in community parks throughout Allegheny County, and the city's surrounding suburban communities have invested in aquatic recreation that serves the region's family population. Central Pennsylvania communities including Harrisburg, Lancaster, York, and State College offer community splash pads and aquatic centers that serve their respective regions. The Lehigh Valley around Allentown and Bethlehem has a strong community parks program with water play options. The season runs from Memorial Day through Labor Day across most of Pennsylvania, with the Philadelphia area's mid-Atlantic climate making those summer months warm and humid enough to drive consistent demand. Most municipal splash pads in Pennsylvania are free, though some recreation center aquatic facilities charge admission. The state's afternoon summer thunderstorm pattern means mornings are generally the more reliable choice for outdoor water play. Weekday mornings at popular facilities offer the most relaxed visiting experience during peak summer weeks."},
    {"name": "Rhode Island", "slug": "rhode-island", "abbr": "RI",
     "meta_description": "Find splash pads in Rhode Island — free spray parks in Providence, Cranston, and Warwick. Ocean State family water play areas, 2026.",
     "description": "Rhode Island may be the smallest state in the country, but its communities have made room for water play, and the state punches above its weight in community recreation investment relative to its size. Providence, the capital and largest city, anchors Rhode Island's splash pad offerings with spray features in city parks that serve urban families and give residents in the dense city neighborhoods a free water play option during the summer months. Cranston and Warwick, the state's second and third-largest cities, have community parks programs that include splash pads suited to their suburban family populations. North Providence, Woonsocket, and Pawtucket contribute additional options across the northern part of the state. The South County communities near the coast — including South Kingstown and Narragansett — offer water play options that complement the region's beach access, giving families a splash pad alternative on days when the ocean is less appealing. Newport, one of the state's most-visited tourist destinations, has community park amenities including water play features that serve both residents and summer visitors. The season runs from Memorial Day through Labor Day, with July and August being the peak months. Rhode Island's coastal humidity makes summer temperatures feel warmer than the thermometer reads, and a shaded splash pad with nearby seating is a genuine relief on the hottest afternoons. Most municipal splash pads are free of charge. Checking local parks department websites before visiting is the most reliable approach, as hours can vary significantly across Rhode Island's small but active parks network."},
    {"name": "South Carolina", "slug": "south-carolina", "abbr": "SC",
     "meta_description": "Find 75+ splash pads in South Carolina — free spray parks in Charleston, Columbia, and Greenville. Palmetto State water play, 2026.",
     "description": "South Carolina's long, hot summers and strong community investment in outdoor recreation have produced a splash pad network that spans the state's three distinct geographic regions — the Upstate, Midlands, and Lowcountry. Charleston and the surrounding Lowcountry lead in visibility, with the coastal heat and humidity creating conditions that make water play popular from April through October — one of the longest operational windows in the country. Charleston County's parks system and the city's recreation programs offer community splash pads that serve both residents and the region's substantial summer visitor population. Columbia, the state capital in the Midlands, operates community splash pads through Richland County and city parks departments, with facilities distributed across the metro area. Greenville anchors the Upstate with modern community aquatic facilities that reflect the region's rapid growth and investment in parks infrastructure. Spartanburg and the surrounding communities add to the Upstate's water play options. Myrtle Beach and the Grand Strand attract large numbers of summer visitors, and beach-adjacent parks in the area offer spray features alongside their other amenities. The season across most of South Carolina runs from late April through September, with Lowcountry facilities often opening earlier and staying open later. Most municipal splash pads are free of charge. South Carolina's afternoon thunderstorm season in summer means morning visits are the most reliable choice. Sunscreen, water, and a change of clothes are standard gear for any South Carolina splash pad outing."},
    {"name": "South Dakota", "slug": "south-dakota", "abbr": "SD",
     "meta_description": "Find splash pads in South Dakota — free spray parks in Sioux Falls, Rapid City, and Aberdeen. Prairie family water play, 2026.",
     "description": "South Dakota's communities make the most of their warm summer months with splash pads and aquatic facilities that give families practical relief from the open-plains heat. Sioux Falls, the state's largest city and one of the fastest-growing mid-sized cities in the Midwest, leads the state with the most developed splash pad network — the city's parks and recreation department operates community water play facilities in several parks across the metro, and the quality of Sioux Falls' community parks reflects consistent investment in recreation. Rapid City, the gateway to the Black Hills and Mount Rushmore, offers community aquatic options that serve both year-round residents and summer tourists who visit the western South Dakota region. Aberdeen in the northeast and Watertown serve their surrounding regions with community splash pads that reflect small-city investment in family recreation. Brookings, home to South Dakota State University, has community water play options with a college-town character. The season typically runs from June through August, with July being the warmest month across most of the state. South Dakota summers can bring genuine heat to the eastern plains, with temperatures in Sioux Falls and surrounding communities reaching into the 90s during peak weeks. Most municipal splash pads are free. The Black Hills region experiences somewhat cooler temperatures than the eastern plains, though community facilities there still operate through the summer season. Checking local parks department websites for current hours is recommended, particularly for smaller community facilities that may have limited staffing or specific operating windows."},
    {"name": "Tennessee", "slug": "tennessee", "abbr": "TN",
     "meta_description": "Find 100+ splash pads in Tennessee — free spray parks in Nashville, Memphis, and Knoxville. Volunteer State water play guide, 2026.",
     "description": "Tennessee's hot, humid summers create sustained demand for water play from one end of the Volunteer State to the other, and the state's communities have built a strong splash pad network that reflects that need. Nashville leads the state in both volume and variety — Metro Nashville Parks operates community splash pads in several city parks, and surrounding Davidson County communities and the rapidly growing suburbs of Williamson and Rutherford counties have invested in modern aquatic facilities that serve the metro area's large family population. Knoxville anchors east Tennessee with community water play through Knox County Parks, with facilities that serve the Knoxville metro and draw families from surrounding communities in the valley. Memphis, on the Mississippi River, offers community splash pads through its parks and recreation department that serve the city's neighborhoods and reflect the long West Tennessee warm season — Memphis's season can stretch from late April into October. Chattanooga, with its outdoor recreation culture and growing downtown, has community water play options that suit the city's character. The Great Smoky Mountains region around Gatlinburg and Pigeon Forge brings a mix of community and commercial water play options that cater to the area's enormous tourism population. The season across most of Tennessee runs from May through September. Most municipal splash pads are free of charge. Tennessee's afternoon thunderstorm pattern means mornings are the most reliable time for outdoor water play. Weekday visits offer noticeably less competition for space than summer weekends."},
    {"name": "Texas", "slug": "texas", "abbr": "TX",
     "meta_description": "Find 200+ splash pads in Texas — free spray parks in Houston, Dallas, Austin, and San Antonio. Lone Star family water play, 2026.",
     "description": "Texas has one of the largest and most diverse collections of splash pads in the country, and the state's intense heat — combined with its enormous and family-oriented population — has driven consistent investment in community water play at every scale. Houston leads the state in sheer volume, with the Houston Parks and Recreation Department operating free community splash pads in neighborhood parks throughout the city and Harris County communities adding their own facilities across the metro. Dallas and Fort Worth together anchor North Texas with dozens of splash pads spread across the DFW metroplex, ranging from free neighborhood spray features to elaborate community aquatic centers with multiple water attractions. Austin's parks network has invested in community splash pads that reflect the city's outdoor recreation culture, and surrounding communities in the Austin metro including Round Rock, Cedar Park, and Pflugerville have added modern facilities in recent years. San Antonio's parks system serves one of the country's largest cities with community water play options appropriate to the South Texas heat. El Paso in the far west and Corpus Christi on the Gulf Coast extend the state's splash pad reach into its distinct regional climates. The season in most of Texas runs from March through November, with the peak from May through September when temperatures across the state regularly reach triple digits. Most municipal splash pads are free. Morning visits before 10 a.m. are strongly recommended during the peak summer heat. Sunscreen, water, and shade-seeking are non-negotiable practical habits for Texas summer outings."},
    {"name": "Utah", "slug": "utah", "abbr": "UT",
     "meta_description": "Find 75+ splash pads in Utah — free spray parks in Salt Lake City, Provo, and Ogden. Wasatch Front family water play areas, 2026.",
     "description": "Utah's dry heat along the Wasatch Front makes splash pads one of the most popular warm-weather destinations for families during the summer months. Salt Lake City and its surrounding suburbs — including West Jordan, Sandy, and Murray — feature community splash pads in parks that range from neighborhood-scale spray areas to larger aquatic facilities with multiple water features. Moving south along the Wasatch Front, Provo and Orem offer well-maintained community water play areas that draw families from Utah, Salt Lake, and Summit counties. Farther north, Ogden and the communities of Weber County have invested in public splash pads and spray parks that make the most of Utah's dry, sunny summers. The season along the Wasatch Front typically runs from late May through September, though southern Utah's communities — particularly in St. George and the Washington County area — enjoy a longer warm season that can push splash pad operation from April through October. The combination of desert heat and high-altitude sunshine means sun protection is essential; most veteran Utah splash pad visitors bring sunscreen, hats, and water bottles as standard gear. Many Utah splash pads are free of charge and operated by city parks and recreation departments. Some aquatic centers charge admission for access to pools and slides. Hours and opening dates vary by facility, so checking local parks department websites before visiting is advisable."},
    {"name": "Vermont", "slug": "vermont", "abbr": "VT",
     "meta_description": "Find splash pads in Vermont — free summer spray parks in Burlington and Rutland. Green Mountain family water play, updated 2026.",
     "description": "Vermont's summer season is genuinely short — communities typically operate splash pads from late June through mid-August — but the enthusiasm families bring to those weeks more than compensates for the compressed calendar. Burlington, the state's largest city and cultural anchor, leads Vermont's water play options with community parks and recreation facilities that include spray features suited to the city's compact, walkable neighborhoods. The Burlington waterfront parks area, with its views of Lake Champlain, provides a particularly appealing setting for outdoor summer recreation. Rutland, in the center of the state, has community aquatic options through its parks and recreation department that serve south-central Vermont families. Montpelier, the small but vibrant state capital, and nearby Barre offer community recreation facilities including water play options appropriate to their size. Stowe and the ski resort communities, which pivot to outdoor summer recreation after the snow melts, attract visitors who find spray features and splash pads in their community parks. Vermont's Green Mountains moderate summer temperatures — the state is generally cooler than southern New England — but genuine summer heat does arrive in July and early August, and when it does, splash pads are among the most popular destinations in any Vermont community. Most municipal splash pads are free of charge, and many are paired with playground equipment and picnic areas that make them a full family outing. Because the season is short, popular facilities fill quickly on the hottest days. Checking local recreation department websites for current hours is essential before visiting."},
    {"name": "Virginia", "slug": "virginia", "abbr": "VA",
     "meta_description": "Find 100+ splash pads in Virginia — free spray parks in Northern Virginia, Richmond, and Virginia Beach. Updated water play 2026.",
     "description": "Virginia's geographic diversity — from the mountains in the west to the Chesapeake Bay in the east — is matched by an equally varied splash pad landscape that serves families across the state through a long and humid summer season. Northern Virginia, in the Washington D.C. suburbs, has the most developed splash pad network in the state. Fairfax County's park authority operates some of the region's best community aquatic facilities, and communities including Arlington, Alexandria, Reston, and Loudoun County have invested in modern splash pads that serve the area's large family population. Richmond, the state capital and a growing mid-sized city, offers community splash pads through Richmond and Henrico County parks programs that serve families across the metro area. Virginia Beach and the Hampton Roads region — including Chesapeake, Norfolk, and Newport News — benefit from the coastal climate and have invested in community aquatic facilities suited to the region's large military and civilian family population. Charlottesville and the Blue Ridge area offer community options appropriate to their size and character. Roanoke serves western Virginia families with community aquatic facilities through its parks department. The season across Virginia runs from May through September, with Northern Virginia's proximity to the D.C. metro's humidity making summer feel intense through August. Most municipal splash pads are free of charge, though some recreation center aquatic facilities charge admission. Mornings are the least crowded and most comfortable visiting time at popular facilities."},
    {"name": "Washington", "slug": "washington", "abbr": "WA",
     "meta_description": "Find 100+ splash pads in Washington — free spray parks in Seattle, Spokane, and Tacoma. Pacific Northwest water play guide, 2026.",
     "description": "Washington's splash pad season is defined by the state's dramatic west-east climate divide. West of the Cascades, the marine climate of the Puget Sound region keeps summers mild — but the dry season from July through September brings reliable sunshine that makes outdoor water play genuinely popular. Seattle's parks department operates spray features in community parks across the city, and the arrival of summer heat in July sends families to water play options that aren't always needed in the city's mild June. Tacoma, Bellevue, and the broader King and Pierce County communities have invested in community splash pads that serve their large family populations during the Pacific Northwest's distinctive sunny season. East of the Cascades, the climate changes dramatically — Spokane, the Tri-Cities area, and the Yakima Valley experience genuinely hot, dry summers with temperatures regularly exceeding 100 degrees, and the communities there have developed aquatic facilities with longer operational windows that reflect the extended warm season. Spokane in particular has a strong splash pad network for its size, with the Spokane Parks Department operating community water play facilities that serve the region from June through September. Most municipal splash pads in Washington are free of charge. Sunscreen is essential even in the Pacific Northwest, where UV intensity during the dry season can be underestimated. Checking local parks department websites before visiting is important, as Washington facilities have varying seasonal schedules that reflect the region's weather patterns."},
    {"name": "West Virginia", "slug": "west-virginia", "abbr": "WV",
     "meta_description": "Find splash pads in West Virginia — free spray parks in Charleston, Huntington, and Morgantown. Mountain State water play, 2026.",
     "description": "West Virginia's mountain communities have embraced splash pads as a summer staple, offering water play areas that provide genuine relief during the warm, humid months from June through August. Charleston, the state capital, anchors the state's water play options with community parks that serve the Kanawha Valley's families, and the city has expanded its outdoor recreation facilities to include updated spray features and aquatic amenities. The Mountain State's geography creates regional variation in summer temperatures: the lower valleys and southern coalfields experience hotter, more humid conditions that make splash pads especially appealing, while the higher elevations of the eastern highlands offer a somewhat cooler summer climate. Communities throughout the state — from Huntington and Parkersburg in the west to Morgantown in the north and Beckley in the south — have developed water play options suited to their local populations. The season typically runs from Memorial Day through Labor Day, with peak demand during the hottest stretches of July and August. Most municipal splash pads in West Virginia are free of charge and operate during park hours. Families visiting the state during summer should also take advantage of West Virginia's state park system, which includes swimming areas and water-adjacent recreation that pair well with a splash pad visit. Checking local parks department websites for current hours and seasonal schedules is recommended before heading out."},
    {"name": "Wisconsin", "slug": "wisconsin", "abbr": "WI",
     "meta_description": "Find 75+ splash pads in Wisconsin — free spray parks in Milwaukee, Madison, and Green Bay. Badger State family water play, 2026.",
     "description": "Wisconsin's splash pad landscape spans two very different ends of the water play spectrum — the tight-knit community facilities in city parks across the state, and the Wisconsin Dells, which bills itself as the Waterpark Capital of the World and delivers on that claim with an astonishing concentration of indoor and outdoor water attractions. Milwaukee, the state's largest city, has invested in community spray features distributed across its neighborhood parks, giving urban families free access to water play throughout the metro area. Madison, home to the University of Wisconsin and a city with a strong parks culture, operates community splash pads that serve the Dane County metro and reflect the city's consistent investment in outdoor recreation. Green Bay, Appleton, and Racine round out Wisconsin's major urban centers with their own community aquatic facilities. The Wisconsin Dells area in the central part of the state offers year-round indoor waterpark options through its resort hotels and dedicated parks — a genuine draw for families from across the Midwest. The broader Dells region operates extensive outdoor water attractions during the summer season from late May through September. Community splash pads across Wisconsin are typically free of charge and run from June through August, with July the peak month. Wisconsin summers bring warm, humid conditions that make water play particularly appealing in the inland communities away from Lake Michigan's cooling influence. Weekday visits at community splash pads are noticeably less crowded than weekend afternoons during peak summer."},
    {"name": "Wyoming", "slug": "wyoming", "abbr": "WY",
     "meta_description": "Find splash pads in Wyoming — free summer spray parks in Cheyenne, Casper, and Jackson. Big Sky family water play, updated 2026.",
     "description": "Wyoming's small population and vast open spaces mean splash pads are fewer and farther between than in most states, but the communities that have made the investment treat their facilities as valued public amenities that give families a meaningful cool-down option during the mountain summer. Cheyenne, the state capital and largest city, anchors Wyoming's splash pad network with community aquatic facilities that serve southeast Wyoming families through the summer season — the city's parks and recreation department has invested in water play options that reflect Cheyenne's steady population base. Casper, in the center of the state along the North Platte River, offers community water play through its parks department that serves the surrounding Natrona County population and draws families from central Wyoming. Gillette, the energy industry hub of Campbell County, has community recreation facilities including splash pad amenities suited to its family-oriented workforce population. Laramie, home to the University of Wyoming, offers community aquatic options that serve the college town's student and family population during the summer months. The season across Wyoming typically runs from late June through August, reflecting the state's high-altitude climate — even in summer, Wyoming's nights are cool and the daytime season window is compressed compared to lower-elevation states. Most municipal splash pads are free of charge. Sunscreen is essential at Wyoming's elevations, where clear mountain air provides less UV protection than families may expect. Because options are geographically spread out, verifying facility hours and opening dates before driving is a practical necessity across the state."},
]

# Feature filter categories (used for filter pages and nav)
CATEGORIES = [
    {"name": "Free Admission", "slug": "free-admission", "icon": "🆓",
     "seo_title": "Free Splash Pads Near You",
     "description": "Splash pads with no admission cost",
     "intro": "Free splash pads are one of the best-kept secrets for family fun. Operated by city parks departments and community recreation centers, these facilities offer the same water play experience as paid attractions — ground-level jets, spray nozzles, and interactive features — without any cost. Many are located in public parks with playgrounds, restrooms, and picnic areas, making them a complete family outing at zero cost."},
    {"name": "Best for Toddlers", "slug": "toddlers", "icon": "👶",
     "seo_title": "Best Splash Pads for Toddlers Near You",
     "description": "Gentle water features ideal for toddlers and young children",
     "intro": "Toddler-friendly splash pads feature gentle, low-pressure water jets and shallow ground-level spray areas designed for the youngest visitors. These facilities avoid the high-intensity sprayers and deep water that can overwhelm small children, offering a safe introduction to water play. Many also include shaded seating areas where parents can watch comfortably. If your child is between 1 and 4, these are the splash pads to start with."},
    {"name": "Best for Families", "slug": "families", "icon": "👨‍👩‍👧‍👦",
     "seo_title": "Best Family Splash Pads Near You",
     "description": "Large splash pads with features for all ages",
     "intro": "Family splash pads offer something for every age — from gentle spray areas for toddlers to high-energy water cannons and dumping buckets for older kids. These larger facilities are designed so siblings of different ages can all play together without anyone being bored or overwhelmed. Many include adjacent playgrounds, picnic areas, and restrooms so families can spend a full morning or afternoon."},
    {"name": "With Shade", "slug": "with-shade", "icon": "⛱️",
     "seo_title": "Splash Pads with Shade Near You",
     "description": "Splash pads with shaded areas to keep the sun off",
     "intro": "Shade matters — especially at splash pads where kids can spend hours in direct sunlight. These facilities include covered pavilions, shade sails, trees, or other structures that protect visitors from UV exposure. Shaded splash pads are particularly important in southern and desert states where summer sun intensity peaks. Even with shade, sunscreen is still recommended, but having a shaded rest area makes a big difference for both kids and parents."},
    {"name": "With Restrooms", "slug": "with-restrooms", "icon": "🚻",
     "seo_title": "Splash Pads with Restrooms Near You",
     "description": "Browse splash pads with on-site restrooms and family changing areas",
     "intro": "On-site restrooms are one of those amenities you don't think about until you need them — and at a splash pad with young children, you'll need them. Every splash pad listed here has dedicated restroom facilities on-site, often including family changing rooms where you can get kids into and out of swimwear without hunting for a nearby building. Whether you're planning a quick stop or a full morning out, restroom access turns a splashing session into a proper outing. Use the state filter below to find locations near you."},
    {"name": "With Picnic Areas", "slug": "with-picnic-areas", "icon": "🧺",
     "seo_title": "Splash Pads with Picnic Areas Near You",
     "description": "Splash pads near picnic tables or pavilions",
     "intro": "Splash pads with picnic areas let families turn water play into a full outing. Pack a lunch, claim a table, and alternate between eating and splashing without having to leave and come back. Many facilities include shaded pavilions, grills, or nearby concession stands. It's the difference between a 30-minute splash and a three-hour family day."},
    {"name": "Indoor", "slug": "indoor", "icon": "🏠",
     "seo_title": "Indoor Splash Pads Near You — Year-Round Water Play",
     "description": "Year-round indoor water play areas",
     "intro": "Indoor splash pads and water play areas operate year-round regardless of weather or season. These climate-controlled facilities — often found inside recreation centers, resorts, and dedicated waterpark buildings — offer slides, spray features, and pools in a warm, enclosed environment. They're the answer for families in northern states who want water play in January, or for anyone looking to avoid sunburn and rain delays."},
    {"name": "Accessible", "slug": "accessible", "icon": "♿",
     "seo_title": "Accessible Splash Pads Near You — ADA-Friendly Water Play",
     "description": "ADA accessible splash pads and water play areas",
     "intro": "Accessible splash pads are designed so children and adults of all abilities can enjoy water play. These facilities feature ADA-compliant surfaces, wheelchair-accessible spray areas, ground-level jets that don't require climbing or standing, and accessible paths to and from the water play area. Many also include accessible restrooms and parking. Every child deserves to play in the water — these facilities make that possible."},
    {"name": "Amusement Parks", "slug": "amusement-parks", "icon": "🎢",
     "seo_title": "Splash Pads at Amusement Parks Near You",
     "description": "Theme and amusement parks with splash pad and water attractions",
     "intro": "Many of the country's most popular theme and amusement parks include splash pads, spray zones, and dedicated water areas alongside their rides and attractions. These facilities range from themed splash zones designed for younger visitors to full-scale water rides and play areas. They're a great way to cool off between coaster rides and add a water play dimension to a theme park visit."},
    {"name": "Water Parks", "slug": "water-parks", "icon": "🌊",
     "seo_title": "Water Parks with Splash Pads Near You",
     "description": "Dedicated water parks and resort water parks with slides and attractions",
     "intro": "Dedicated water parks go well beyond a basic splash pad — they offer water slides, wave pools, lazy rivers, and multi-level splash structures alongside traditional spray features. These are full-day destinations with amenities like locker rooms, concessions, cabana rentals, and lifeguard coverage. Whether it's a community-operated aquatic park or a resort-scale waterpark, these facilities deliver the most complete water play experience available."},
]

# Pad-page indexability gate (AdSense remediation 2026-05-06).
# A pad ships indexable only if its Type is in the whitelist AND its description
# is free of AI-artifact phrases. Pages that fail are noindexed and excluded from
# the sitemap. A protected-URL guardrail (loaded from protected_urls.json) routes
# any GSC-trafficked URL to dist/REVIEW_QUEUE.txt instead of auto-noindexing.
PAD_TYPE_WHITELIST = {
    "Splash Pad",
    "Water Park",
    "Aquatic Center",
    "Campground Water Park",
    "Resort Water Park",
    "Indoor Water Play",
    # Amusement parks in this directory are curated for their water attractions
    # (splash pads, water slides, bumper boats); their descriptions are water-grounded.
    "Amusement Park",
}

# Phrases that, when present in a description, signal AI-refusal or "I don't have
# the data" boilerplate that leaked through enrichment. Case-insensitive.
PAD_ARTIFACT_PATTERNS = [
    r"\bI can'?t write\b",
    r"\bI cannot (?:write|create|generate|provide|describe|offer)\b",
    r"\bI'?m unable\b",
    r"\bI don'?t have specific\b",
    r"\bI appreciate you providing\b",
    r"\bfacility data appears incomplete\b",
    r"\bcannot verify\b",
    r"\bunable to verify\b",
    r"\bdoes(?:n'?t| not) indicate\b",
    r"\bas an AI\b",
    r"\bI'?m sorry\b",
    r"\bthe (?:provided|given) (?:information|data)\b",
    r"\bbased on the limited\b",
    r"\bthe listing information (?:is|provided is)\b",
    r"\binformation provided is incomplete\b",
    r"\bcan(?:not| ?n'?t) (?:provide|offer|describe)\b",
    r"\bgoogle\.com/travel/clk\b",
    r"\bprice_total\b",
    r"\bBluehost\b",
    r"\bweb hosting provider\b",
    r"\bfree 1 click installs\b",
    r"\bBorn and raised\b",
]

# Minimum description length, post-cleaning. Raised from 100 to 150 chars; pads
# whose descriptions were mostly rating boilerplate are correctly thinner now.
MIN_DESCRIPTION_LENGTH = 150


# Google Analytics
GA_MEASUREMENT_ID = os.getenv("GA_MEASUREMENT_ID", "")

# SEO Settings
DEFAULT_META_TITLE = "Best Splash Pads Near Me — Find Free & Family-Friendly Water Play"
DEFAULT_META_DESCRIPTION = "Find the best splash pads near you — free, family-friendly water play for all ages. Search by city or state to discover spray parks and water play areas."

# Blog post metadata overrides (keyed by slug).
# Use these to fix titles/descriptions for high-impression zero-click pages
# without requiring an Airtable edit.
BLOG_META_OVERRIDES = {
    "best-swim-diapers-for-splash-pads": {
        "page_title": "Best Swim Diapers for Splash Pads (2026) \u2014 Tested & Compared",
        "meta_description": "We tested the top swim diapers for splash pads in 2026. Reusable and disposable picks ranked by leak protection, fit, and value \u2014 so you can skip the trial and error.",
    },
    "best-splash-pads-in-texas": {
        "page_title": "Best Splash Pads in Texas: Top Water Play Spots for Families (2026) - Splash Pad Locator",
        "meta_description": "Discover the best splash pads in Texas for families in 2026. Free options in Dallas, Houston, Austin, and San Antonio plus top water parks.",
    },
    "best-splash-pads-in-illinois": {
        "page_title": "Best Splash Pads in Illinois: Top Picks for Families (2026) - Splash Pad Locator",
        "meta_description": "Discover the best splash pads in Illinois for 2026 \u2014 from Chicago suburb water parks to neighborhood spray pads. Updated with hours, admission, and family tips.",
    },
    "how-to-find-free-splash-pads-near-you": {
        "page_title": "How to Find Free Splash Pads Near You (2026 Guide) - Splash Pad Locator",
        "meta_description": "Find free splash pads near you with our step-by-step guide. Covers city park searches, apps, and what to look for so the whole family can splash for free.",
    },
}

# Pad pages to force noindex (misleading listings, off-topic venues, or pool-not-splash-pad).
# Keyed by slug — value is a note explaining the reason.
PAD_NOINDEX_SLUGS = {
    "lenora-park-pool-snellville": "Traditional swimming pool, not a splash pad — misleading to searchers.",
    "kings-island-mason": "Amusement park ticket booth listing, not a splash pad venue page — off-topic impressions.",
    # AdSense remediation 2026-05-06: AI-refusal text in description
    "parking-new-york": "AI-refusal text in description; venue is a parking lot.",
    "walmart-supercenter-punxsutawney": "AI-refusal text; venue is a Walmart store, not a splash pad.",
    "port-clinton-peanut-shop-port-clinton": "AI-refusal text; venue is a peanut shop.",
    "gettysburg-national-military-park-museum-visitor-center-gettysburg": "AI-refusal text; venue is a Civil War history museum.",
    # AdSense remediation 2026-05-06: off-topic venues described as splash pads
    "secret-caverns-howes-cave": "Off-topic — underground cavern attraction, not a splash pad.",
    "jane-s-carousel-brooklyn": "Off-topic — historic carousel, not a splash pad.",
    "manhattan-community-boathouse-pier-96-new-york": "Off-topic — kayak boathouse, not a splash pad.",
    "city-of-princeton-public-works-princeton": "Off-topic — municipal public works office.",
    "galaxy-theatres-riverbank-imax-riverbank": "Off-topic — IMAX movie theater.",
    "slick-city-action-park-columbus": "Off-topic — waterless indoor slide park.",
    "living-waters-watsu-coopersburg": "Off-topic — adult water-shiatsu therapy spa.",
    "salmoondion-tucson": "Off-topic — venue type unverifiable; AI-style fabricated copy.",
    "blackbeard-s-family-entertainment-fresno": "Off-topic — mini-golf / arcade family entertainment center.",
}

# Listings to remove from the generated public site entirely. These are not
# merely thin pages; they are clear false positives for a splash-pad directory.
# They get redirected to their state page when the build has enough state data.
PAD_EXCLUDE_SLUGS = {
    **PAD_NOINDEX_SLUGS,
    "airgarage-public-parking-first-water-charlottesville-charlottesville": "Off-topic — parking garage.",
    "annapolis-maritime-museum-park-annapolis": "Off-topic — maritime museum / park.",
    "bathhouse-williamsburg-brooklyn": "Off-topic — bathhouse/spa.",
    "bricktown-water-taxi-oklahoma-city": "Off-topic — water taxi.",
    "culligan-of-syracuse-ny-east-syracuse": "Off-topic — water-treatment business.",
    "dandy-pizza-cafe-deli-towanda": "Off-topic — restaurant/convenience listing, not a splash pad.",
    "hoboken-cove-community-boathouse-hoboken": "Off-topic — boathouse.",
    "james-f-holland-memorial-park-palm-coast": "Off-topic false positive from memorial/park data.",
    "jamestown-newport-ferry-jamestown": "Off-topic — ferry service.",
    "new-york-water-taxi-brooklyn": "Off-topic — water taxi.",
    "pier-6-dog-run-brooklyn": "Off-topic — dog run.",
    "pirate-s-cove-adventure-golf-prudenville": "Off-topic — mini golf.",
    "point-fermin-lighthouse-san-pedro": "Off-topic — lighthouse.",
    "pool-lounge-at-grand-falls-casino-golf-resort-r-larchwood": "Off-topic — casino/hotel lounge.",
    "rockland-breakwater-lighthouse-rockland": "Off-topic — lighthouse.",
    "sea-the-city-jet-ski-jersey-city": "Off-topic — jet ski tour operator.",
    "smith-haven-mall-lake-grove": "Off-topic — shopping mall.",
    "spa-castle-new-york-college-point": "Off-topic — adult spa.",
    "st-james-theatre-new-york": "Off-topic — theater.",
    "the-pier-62-carousel-new-york": "Off-topic — carousel.",
    "the-riverstar-casino-terral": "Off-topic — casino.",
    "the-whaling-museum-education-center-of-cold-spring-harbor-cold-spring-harbor": "Off-topic — museum.",
    "viking-golf-go-karts-fenwick-island": "Off-topic — mini golf / go-karts.",
    # ── Non-water-venue sweep 20260530 (Google type ground-truth; reversible) ──
    "acac-fitness-wellness-adventure-central-charlottesville": "Off-topic — Gym (non-water); 20260530 sweep.",
    "adirondack-adventure-center-lake-luzerne": "Off-topic — Raft trip outfitter (non-water); 20260530 sweep.",
    "adirondack-experience-the-museum-on-blue-mountain-lake-blue-mountain-lake": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "adventure-park-at-talon-falls-melber": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "air-riderz-adventure-park-port-chester-new-york-port-chester": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "airborne-adventure-park-saginaw-mi-saginaw": "Indoor-fun/adventure venue — Google type 'Amusement center', no water signal; 20260530 sweep.",
    "akron-zoo-akron": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "alabama-aquarium-at-the-dauphin-island-sea-lab-dauphin-island": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "alka-pure-waters-union-city": "Off-topic — Bottled water supplier (non-water); 20260530 sweep.",
    "amc-port-chester-14-port-chester": "Off-topic — Movie theater (non-water); 20260530 sweep.",
    "andrew-stergiopoulos-ice-rink-great-neck": "Off-topic — Ice skating rink (non-water); 20260530 sweep.",
    "animal-adventure-park-harpursville": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "annapolis-maritime-museum-park-annapolis": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "anniston-aquatic-fitness-center-anniston": "Off-topic — Physical fitness program (non-water); 20260530 sweep.",
    "aquafun-pools-halifax": "Off-topic — Swimming pool contractor (non-water); 20260530 sweep.",
    "aquatic-development-group-adg-cohoes": "Off-topic — Contractor (non-water); 20260530 sweep.",
    "aquatix-r-by-landscape-structures-delano": "Off-topic — Manufacturer (non-water); 20260530 sweep.",
    "asheville-treetops-adventure-park-asheville": "Off-topic — Adventure sports center (non-water); 20260530 sweep.",
    "balmorhea-state-park-toyahvale": "Off-topic — State park (non-water); 20260530 sweep.",
    "banning-state-park-sandstone": "Off-topic — State park (non-water); 20260530 sweep.",
    "bathhouse-williamsburg-brooklyn": "Off-topic — Sauna (non-water); 20260530 sweep.",
    "bay-city-state-park-bay-city": "Off-topic — State park (non-water); 20260530 sweep.",
    "bayville-adventure-park-bayville": "Indoor-fun/adventure venue — Google type 'Theme park', no water signal; 20260530 sweep.",
    "bethesda-terrace-new-york": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "big-sky-resort-big-sky": "Off-topic — Ski resort (non-water); 20260530 sweep.",
    "blackwater-falls-state-park-davis": "Off-topic — State park (non-water); 20260530 sweep.",
    "blue-ridge-adventure-park-blue-ridge": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "boundary-waters-outfitters-ely": "Off-topic — Canoe & kayak rental service (non-water); 20260530 sweep.",
    "brannan-island-state-recreation-area-rio-vista": "Off-topic — State park (non-water); 20260530 sweep.",
    "breaks-interstate-park-breaks": "Off-topic — State park (non-water); 20260530 sweep.",
    "brick-city-adventure-park-ocala": "Indoor-fun/adventure venue — Google type 'Park', no water signal; 20260530 sweep.",
    "burgess-falls-state-park-sparta": "Off-topic — State park (non-water); 20260530 sweep.",
    "cabrillo-marine-aquarium-san-pedro": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "cameron-family-ymca-santee": "Off-topic — Fitness center (non-water); 20260530 sweep.",
    "canopy-adventure-park-midlothian": "Indoor-fun/adventure venue — Google type 'Recreation center', no water signal; 20260530 sweep.",
    "canyon-coaster-adventure-park-williams": "Indoor-fun/adventure venue — Google type 'Recreation center', no water signal; 20260530 sweep.",
    "canyon-park-subdivision-onalaska-texas-onalaska": "Off-topic — Association / Organization (non-water); 20260530 sweep.",
    "catapult-adventure-park-lakewood-lakewood": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "catapult-adventure-park-puyallup-puyallup": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "central-railroad-of-new-jersey-terminal-jersey-city": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "city-of-princeton-public-works-princeton": "Off-topic — Public works department (non-water); 20260530 sweep.",
    "cleland-ice-in-line-skating-rink-park-fort-bragg-fort-bragg": "Off-topic — Ice skating rink (non-water); 20260530 sweep.",
    "cloud-9-ranch-club-inc-caulfield": "Off-topic — Club (non-water); 20260530 sweep.",
    "cny-regional-market-syracuse": "Off-topic — Market (non-water); 20260530 sweep.",
    "cold-spring-harbor-fish-hatchery-aquarium-cold-spring-harbor": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "colorado-adventure-park-fraser": "Off-topic — Adventure sports center (non-water); 20260530 sweep.",
    "copper-sky-maricopa": "Off-topic — Gym (non-water); 20260530 sweep.",
    "costello-s-ace-hardware-of-island-park-island-park": "Off-topic — Hardware store (non-water); 20260530 sweep.",
    "crest-hollow-country-club-woodbury": "Off-topic — Event venue (non-water); 20260530 sweep.",
    "crocker-park-westlake": "Off-topic — Shopping mall (non-water); 20260530 sweep.",
    "cuivre-river-state-park-troy": "Off-topic — State park (non-water); 20260530 sweep.",
    "culligan-of-syracuse-ny-east-syracuse": "Off-topic — Water softening equipment supplier (non-water); 20260530 sweep.",
    "dandy-pizza-cafe-deli-towanda": "Off-topic — Convenience store (non-water); 20260530 sweep.",
    "demarest-lloyd-state-park-dartmouth": "Off-topic — State park (non-water); 20260530 sweep.",
    "discovery-space-of-central-pennsylvania-state-college": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "dunkin-south-ozone-park": "Off-topic — Coffee shop (non-water); 20260530 sweep.",
    "dunkin-towanda": "Off-topic — Coffee shop (non-water); 20260530 sweep.",
    "egp-land-sea-island-park": "Off-topic — Restaurant (non-water); 20260530 sweep.",
    "exxon-at-american-truck-plaza-milton": "Off-topic — Truck stop (non-water); 20260530 sweep.",
    "flip-side-watersports-birmingham": "Off-topic — Water skiing service (non-water); 20260530 sweep.",
    "flying-j-travel-center-mill-hall": "Off-topic — Truck stop (non-water); 20260530 sweep.",
    "fonthill-castle-doylestown": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "forebay-aquatic-center-oroville": "Off-topic — Boat rental service (non-water); 20260530 sweep.",
    "fort-eustis-mwr-outdoor-recreation-fort-eustis": "Off-topic — Military base (non-water); 20260530 sweep.",
    "fort-wayne-parks-and-recreation-fort-wayne": "Off-topic — Government office (non-water); 20260530 sweep.",
    "fraser-tubing-hill-fraser": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "funcity-adventure-park-fort-wayne": "Indoor-fun/adventure venue — Google type 'Indoor playground', no water signal; 20260530 sweep.",
    "funcity-entertainment-complex-burlington": "Off-topic — Video arcade (non-water); 20260530 sweep.",
    "galaxy-theatres-riverbank-imax-riverbank": "Off-topic — Movie theater (non-water); 20260530 sweep.",
    "garvies-point-glen-cove": "Off-topic — Real estate developer (non-water); 20260530 sweep.",
    "geneva-fun-plex-geneva": "Indoor-fun/adventure venue — Google type 'Indoor playground', no water signal; 20260530 sweep.",
    "gettysburg-national-military-park-museum-visitor-center-gettysburg": "Off-topic — Visitor center (non-water); 20260530 sweep.",
    "gifford-pinchot-state-park-lewisberry": "Off-topic — State park (non-water); 20260530 sweep.",
    "grand-canyon-national-park-us": "Off-topic — National park (non-water); 20260530 sweep.",
    "green-lakes-state-park-fayetteville": "Off-topic — State park (non-water); 20260530 sweep.",
    "greenbrier-state-park-boonsboro": "Off-topic — State park (non-water); 20260530 sweep.",
    "gretna-crossing-ymca-gretna": "Off-topic — Fitness center (non-water); 20260530 sweep.",
    "gt-kingston-karaoke-bar-south-ozone-park": "Off-topic — Jamaican restaurant (non-water); 20260530 sweep.",
    "h-mart-elkins-park-elkins-park": "Off-topic — Asian grocery store (non-water); 20260530 sweep.",
    "hampton-ponds-state-park-westfield": "Off-topic — State park (non-water); 20260530 sweep.",
    "hempstead-lake-state-park-west-hempstead": "Off-topic — State park (non-water); 20260530 sweep.",
    "hidden-river-cave-american-cave-museum-horse-cave": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "historic-london-town-gardens-edgewater": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "holy-land-usa-waterbury-waterbury": "Off-topic — Religious destination (non-water); 20260530 sweep.",
    "hudson-river-park-new-york": "Off-topic — State park (non-water); 20260530 sweep.",
    "hudson-river-recreation-croton-point-park-croton-on-hudson": "Off-topic — Canoe & kayak rental service (non-water); 20260530 sweep.",
    "huntsville-state-park-huntsville": "Off-topic — State park (non-water); 20260530 sweep.",
    "island-jet-skis-freeport": "Off-topic — Water sports equipment rental service (non-water); 20260530 sweep.",
    "island-lake-endeavors-new-auburn": "Off-topic — Boat rental service (non-water); 20260530 sweep.",
    "jack-hill-state-park-reidsville": "Off-topic — State park (non-water); 20260530 sweep.",
    "jackson-hole-mountain-resort-teton-village": "Off-topic — Ski resort (non-water); 20260530 sweep.",
    "japanese-garden-fort-worth": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "jersey-jet-ski-nyc-location-jersey-city": "Off-topic — Tour operator (non-water); 20260530 sweep.",
    "jordan-lobster-farms-island-park": "Off-topic — Seafood restaurant (non-water); 20260530 sweep.",
    "kanarra-falls-kanarraville": "Off-topic — Hiking area (non-water); 20260530 sweep.",
    "kaweah-whitewater-adventures-three-rivers": "Off-topic — Raft trip outfitter (non-water); 20260530 sweep.",
    "kinzua-bridge-state-park-mt-jewett": "Off-topic — State park (non-water); 20260530 sweep.",
    "kirkwood-mountain-resort-kirkwood": "Off-topic — Ski resort (non-water); 20260530 sweep.",
    "lake-colorado-city-state-park-colorado-city": "Off-topic — State park (non-water); 20260530 sweep.",
    "lake-norman-state-park-troutman": "Off-topic — State park (non-water); 20260530 sweep.",
    "lake-somerville-state-park-trailway-somerville": "Off-topic — State park (non-water); 20260530 sweep.",
    "lake-tobias-wildlife-park-halifax": "Off-topic — Zoo (non-water); 20260530 sweep.",
    "lake-waccamaw-state-park-lake-waccamaw": "Off-topic — State park (non-water); 20260530 sweep.",
    "lake-wister-state-park-wister": "Off-topic — State park (non-water); 20260530 sweep.",
    "lee-state-park-bishopville": "Off-topic — State park (non-water); 20260530 sweep.",
    "liberty-state-park-jersey-city": "Off-topic — State park (non-water); 20260530 sweep.",
    "life-time-florham-park": "Off-topic — Gym (non-water); 20260530 sweep.",
    "lily-dale-assembly-inc-lily-dale": "Off-topic — Religious organization (non-water); 20260530 sweep.",
    "liquor-wine-warehouse-island-park-island-park": "Off-topic — Liquor store (non-water); 20260530 sweep.",
    "living-treasures-animal-park-jones-mills": "Off-topic — Hotel (non-water); 20260530 sweep.",
    "long-point-state-park-on-lake-chautauqua-bemus-point": "Off-topic — State park (non-water); 20260530 sweep.",
    "lums-pond-state-park-bear": "Off-topic — State park (non-water); 20260530 sweep.",
    "macneil-park-boat-launch-college-point": "Off-topic — Boat ramp (non-water); 20260530 sweep.",
    "madison-base-big-sky-resort-gallatin-gateway": "Off-topic — Ski resort (non-water); 20260530 sweep.",
    "manatee-springs-state-park-tours-activities-chiefland": "Off-topic — Canoe & kayak rental service (non-water); 20260530 sweep.",
    "manhattan-community-boathouse-pier-96-new-york": "Off-topic — Non-profit organization (non-water); 20260530 sweep.",
    "massad-family-ymca-falmouth": "Off-topic — Non-profit organization (non-water); 20260530 sweep.",
    "massanutten-family-adventure-park-massanutten": "Indoor-fun/adventure venue — Google type 'Recreation center', no water signal; 20260530 sweep.",
    "mattel-adventure-park-glendale": "Indoor-fun/adventure venue — Google type 'Theme park', no water signal; 20260530 sweep.",
    "mcconnells-mill-state-park-portersville": "Off-topic — State park (non-water); 20260530 sweep.",
    "mesker-park-zoo-evansville": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "miller-park-zoo-bloomington": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "milton-state-park-milton": "Off-topic — State park (non-water); 20260530 sweep.",
    "mission-bay-aquatic-center-san-diego": "Off-topic — Water sports equipment rental service (non-water); 20260530 sweep.",
    "missouri-down-under-adventure-zoo-van-buren": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "mono-hot-springs-resort-lakeshore": "Off-topic — Hotel (non-water); 20260530 sweep.",
    "monroe-sky-valley-family-ymca-monroe": "Off-topic — Non-profit organization (non-water); 20260530 sweep.",
    "montana-whitewater-rafting-zipline-gallatin-gallatin-gateway": "Off-topic — Raft trip outfitter (non-water); 20260530 sweep.",
    "montana-whitewater-yellowstone-whitewater-rafting-ziplining-gardiner": "Off-topic — Raft trip outfitter (non-water); 20260530 sweep.",
    "moonlight-basin-big-sky": "Off-topic — Club (non-water); 20260530 sweep.",
    "moose-lake-state-park-moose-lake": "Off-topic — State park (non-water); 20260530 sweep.",
    "moraine-state-park-portersville": "Off-topic — State park (non-water); 20260530 sweep.",
    "mylan-park-morgantown": "Off-topic — Corporate office (non-water); 20260530 sweep.",
    "neverland-fun-berkeley-heights": "Off-topic — Children's party service (non-water); 20260530 sweep.",
    "new-york-media-boat-adventure-sightseeing-tours-new-york": "Off-topic — Boat tour agency (non-water); 20260530 sweep.",
    "ninja-kidz-action-park-east-rutherford": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "ninja-kidz-action-park-south-jordan": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "ninja-kingdom-adventure-park-charles-town": "Indoor-fun/adventure venue — Google type 'Indoor playground', no water signal; 20260530 sweep.",
    "north-haven-inn-market-north-haven": "Off-topic — Convenience store (non-water); 20260530 sweep.",
    "nsa-annapolis-mwr-annapolis": "Off-topic — Military base (non-water); 20260530 sweep.",
    "nyc-cycleboats-new-york": "Off-topic — Boat tour agency (non-water); 20260530 sweep.",
    "occoneechee-state-park-clarksville": "Off-topic — State park (non-water); 20260530 sweep.",
    "ozark-national-scenic-riverways-park-headquarters-no-visitor-center-van-buren": "Off-topic — Government office (non-water); 20260530 sweep.",
    "parking-new-york": "Off-topic — Parking lot (non-water); 20260530 sweep.",
    "patagonia-lake-state-park-nogales": "Off-topic — State park (non-water); 20260530 sweep.",
    "paterson-great-falls-national-historical-park-paterson": "Off-topic — National park (non-water); 20260530 sweep.",
    "peddler-s-village-lahaska": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "pedernales-falls-state-park-johnson-city": "Off-topic — State park (non-water); 20260530 sweep.",
    "pedernales-river-nature-park-johnson-city": "Off-topic — State park (non-water); 20260530 sweep.",
    "phelan-pinon-hills-community-services-district-phelan": "Off-topic — Water utility company (non-water); 20260530 sweep.",
    "pilot-travel-center-portersville": "Off-topic — Truck stop (non-water); 20260530 sweep.",
    "point-fermin-lighthouse-san-pedro": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "port-clinton-peanut-shop-port-clinton": "Off-topic — Candy store (non-water); 20260530 sweep.",
    "port-washington-skating-center-port-washington": "Off-topic — Ice skating rink (non-water); 20260530 sweep.",
    "project-puffin-visitor-center-rockland": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "pump-up-the-fun-huntington": "Indoor-fun/adventure venue — Google type 'Amusement center', no water signal; 20260530 sweep.",
    "punxsutawney-area-hospital-punxsutawney": "Off-topic — General hospital (non-water); 20260530 sweep.",
    "quail-meadows-riverbank": "Off-topic — Mobile home park (non-water); 20260530 sweep.",
    "queens-botanical-garden-flushing": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "renfro-valley-entertainment-center-mt-vernon": "Off-topic — Live music venue (non-water); 20260530 sweep.",
    "ringwood-state-park-ringwood": "Off-topic — State park (non-water); 20260530 sweep.",
    "rock-island-state-park-rock-island": "Off-topic — State park (non-water); 20260530 sweep.",
    "rockland-breakwater-lighthouse-rockland": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "royal-s-market-loa": "Off-topic — Grocery store (non-water); 20260530 sweep.",
    "rush-mountain-adventure-park-keystone": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "sacandaga-outdoor-center-hadley": "Off-topic — Raft trip outfitter (non-water); 20260530 sweep.",
    "saginaw-children-s-zoo-saginaw": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "science-central-fort-wayne": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "science-mill-johnson-city": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "sea-the-city-jet-ski-jersey-city": "Off-topic — Tour operator (non-water); 20260530 sweep.",
    "seven-tubs-recreation-area-pinchot-forest-district-wilkes-barre": "Off-topic — State park (non-water); 20260530 sweep.",
    "sipapu-ski-summer-resort-vadito": "Off-topic — Ski resort (non-water); 20260530 sweep.",
    "skudin-surf-american-dream-east-rutherford": "Off-topic — Surf school (non-water); 20260530 sweep.",
    "smash-park-westerville-westerville": "Off-topic — Restaurant (non-water); 20260530 sweep.",
    "smith-haven-mall-lake-grove": "Off-topic — Shopping mall (non-water); 20260530 sweep.",
    "soundview-park-amphitheater-bronx": "Off-topic — Amphitheater (non-water); 20260530 sweep.",
    "spa-castle-new-york-college-point": "Off-topic — Spa (non-water); 20260530 sweep.",
    "sportime-port-washington-jmta-long-island-port-washington": "Off-topic — Tennis club (non-water); 20260530 sweep.",
    "spring-lake-fitness-aquatic-center-spring-lake": "Off-topic — Physical fitness program (non-water); 20260530 sweep.",
    "st-francois-state-park-bonne-terre": "Off-topic — State park (non-water); 20260530 sweep.",
    "st-james-theatre-new-york": "Off-topic — Performing arts theater (non-water); 20260530 sweep.",
    "statue-city-cruises-battery-park-new-york": "Off-topic — Boat tour agency (non-water); 20260530 sweep.",
    "storybook-island-rapid-city": "Off-topic — Non-profit organization (non-water); 20260530 sweep.",
    "sunburst-ranch-caulfield": "Off-topic — Canoe & kayak rental service (non-water); 20260530 sweep.",
    "swartswood-state-park-swartswood": "Off-topic — State park (non-water); 20260530 sweep.",
    "swerve-watersports-center-hillsboro": "Off-topic — Water ski shop (non-water); 20260530 sweep.",
    "ta-travel-center-tallulah": "Off-topic — Truck stop (non-water); 20260530 sweep.",
    "the-adventure-park-at-virginia-aquarium-virginia-beach": "Off-topic — Adventure sports center (non-water); 20260530 sweep.",
    "the-adventure-park-on-maui-lahaina": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "the-aquatic-playground-seabrook": "Off-topic — Water sports equipment rental service (non-water); 20260530 sweep.",
    "the-aquatics-fitness-center-parlin": "Off-topic — Fitness center (non-water); 20260530 sweep.",
    "the-lake-midlothian": "Off-topic — Housing development (non-water); 20260530 sweep.",
    "the-landing-current-river-van-buren": "Off-topic — Raft trip outfitter (non-water); 20260530 sweep.",
    "the-mills-at-jersey-gardens-elizabeth": "Off-topic — Outlet mall (non-water); 20260530 sweep.",
    "the-plaza-at-harmon-meadow-secaucus": "Off-topic — Shopping mall (non-water); 20260530 sweep.",
    "the-preserve-harpursville": "Off-topic — Wildlife and safari park (non-water); 20260530 sweep.",
    "the-quarry-cable-park-grille-crystal-lake": "Off-topic — Water sports equipment rental service (non-water); 20260530 sweep.",
    "the-starling-princeton": "Off-topic — Apartment complex (non-water); 20260530 sweep.",
    "the-whaling-museum-education-center-of-cold-spring-harbor-cold-spring-harbor": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "tickfaw-state-park-springfield": "Off-topic — State park (non-water); 20260530 sweep.",
    "tracy-aviary-at-liberty-park-salt-lake-city": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    "treerunner-raleigh-adventure-park-putt-forest-raleigh": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "treetop-adventure-park-at-snow-king-mountain-jackson": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "valley-falls-state-park-fairmont": "Off-topic — State park (non-water); 20260530 sweep.",
    "valley-mills-vineyards-valley-mills": "Off-topic — Winery (non-water); 20260530 sweep.",
    "viking-lake-state-park-stanton": "Off-topic — State park (non-water); 20260530 sweep.",
    "village-of-croton-on-hudson-croton-on-hudson": "Off-topic — Government office (non-water); 20260530 sweep.",
    "visalia-adventure-park-visalia": "Indoor-fun/adventure venue — Google type 'Amusement park', no water signal; 20260530 sweep.",
    "wahconah-falls-state-park-dalton": "Off-topic — State park (non-water); 20260530 sweep.",
    "walgreens-south-ozone-park": "Off-topic — Convenience store (non-water); 20260530 sweep.",
    "walmart-supercenter-punxsutawney": "Off-topic — Department store (non-water); 20260530 sweep.",
    "waterhole-music-lounge-saranac-lake": "Off-topic — Event venue (non-water); 20260530 sweep.",
    "waters-car-wash-orlando": "Off-topic — Car wash (non-water); 20260530 sweep.",
    "watson-pond-state-park-taunton": "Off-topic — State park (non-water); 20260530 sweep.",
    "watters-pools-carmichaels": "Off-topic — Swimming pool supply store (non-water); 20260530 sweep.",
    "widewater-state-park-stafford": "Off-topic — State park (non-water); 20260530 sweep.",
    "winter-park-alpine-slide-winter-park": "Off-topic — Summer toboggan run (non-water); 20260530 sweep.",
    "winter-park-resort-winter-park": "Off-topic — Ski resort (non-water); 20260530 sweep.",
    "woods-valley-ski-area-westernville": "Off-topic — Cafeteria (non-water); 20260530 sweep.",
    "yohan-park-md-bayside": "Off-topic — Pediatrician (non-water); 20260530 sweep.",
    "zimmerman-center-for-heritage-susquehanna-nha-wrightsville": "Off-topic — Tourist attraction (non-water); 20260530 sweep.",
    # ── 20260530 NEEDS_TRIAGE removals: 138 false positives (hotels/casinos/
    # campgrounds/playgrounds with only a pool or no water evidence). Genuine
    # water-play venues (Kalahari, Wilderness, aquatic & rec centers, spray
    # playgrounds) were KEPT — see data/TRIAGE_KEEP_20260530.txt. ──
    "adventure-bound-camping-resorts-west-michigan-white-cloud": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "algona-recreation-department-algona": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "allegheny-national-forest-marienville": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "allegheny-river-campground-roulette": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "alpen-bluffs-outdoor-resort-gaylord": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "ancient-playground-new-york": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "black-chasm-cavern-national-natural-landmark-volcano": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "brantingham-lake-house-brantingham": "Triage — no Google water evidence (lodging); off-topic for a splash-pad directory.",
    "burger-s-lake-fort-worth": "Triage — pool-only amenity (other/attraction); a venue pool, not a splash pad.",
    "burns-park-funland-north-little-rock": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "cady-hollow-campground-port-allegany": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "camp-towanda-honesdale": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "camp-waldemar-hunt": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "cherokee-landing-bonne-terre": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "cherry-hill-new-york": "Triage — pool-only amenity (other/attraction); a venue pool, not a splash pad.",
    "city-park-campground-bridger": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "coconut-creek-family-fun-park-panama-city-beach": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "colona-scott-family-park-colona": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "cook-creek-park-lone-tree": "Triage — pool-only amenity (other/attraction); a venue pool, not a splash pad.",
    "coyote-springs-rv-la-sal": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "crispus-attucks-playground-brooklyn": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "days-inn-by-wyndham-watertown-fort-drum-ny-evans-mills": "Triage — no Google water evidence (lodging); off-topic for a splash-pad directory.",
    "days-inn-by-wyndham-woodbury-long-island-woodbury": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "driftwaters-resort-cameron": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "duck-puddle-campgrounds-nobleboro": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "duncans-mills-camping-club-duncans-mills": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "eagle-village-resort-tamiment": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "elwood-resort-campground-elwood": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "encore-paradise-sun-city": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
    "evelyn-s-playground-new-york": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "falling-waters-lodge-leland": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "fantasyworld-resort-kissimmee": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "giggleberry-fair-and-painted-pony-cafe-new-hope": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "gore-mountain-north-creek": "Triage — no Google water evidence (lodging); off-topic for a splash-pad directory.",
    "grand-falls-casino-golf-resort-r-larchwood": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "gravity-haus-winter-park-winter-park": "Triage — no Google water evidence (lodging); off-topic for a splash-pad directory.",
    "gray-s-riverside-campground-big-rapids": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "guntersville-city-harbor-guntersville": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "harlem-meer-new-york": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "highlands-outpost-scaly-mountain": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "holiday-inn-express-bradford-by-ihg-bradford": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "holiday-inn-express-corning-painted-post-by-ihg-painted-post": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "holiday-inn-express-suites-north-east": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "holiday-inn-express-suites-west-long-branch-eatontown-by-ihg-west-long-branch": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "holiday-inn-express-suites-winner-by-ihg-winner": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "hollywood-casino-hotel-lawrenceburg-lawrenceburg": "Triage — no Google water evidence (lodging); off-topic for a splash-pad directory.",
    "homeplace-recreational-park-ararat": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
    "hover-camp-swan-valley": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "howe-caverns-howes-cave": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "hunter-s-point-south-park-playground-long-island-city": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "imagination-playground-new-york": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "ives-run-campground-tioga": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "j-j-byrne-playground-brooklyn": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "jellystone-park-at-milton-milton": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "jellystone-park-pelahatchie-pelahatchie": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "jellystone-parktm-barton-lake-fremont": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
    "jellystone-parktm-chautauqua-county-jamestown": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "jellystone-parktm-pennsylvania-wilds-mansfield": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "jellystone-parktm-tabor-city-tabor-city": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
    "kah-nee-ta-resort-and-spa-warm-springs": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
    "kenton-county-parks-rec-covington": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "la-waterfront-san-pedro": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "lake-wisconsin-dells-wisconsin-dells": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "lakeland-recreation-houghton-lake": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "lakeside-resort-conference-center-houghton-lake": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "lanai-adventure-park-lanai-city": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "lefrak-center-at-lakeside-brooklyn": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "left-tailrace-campground-fort-thompson": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "legoland-r-discovery-center-new-jersey-east-rutherford": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "little-claremont-playground-bronx": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "log-cabin-lodge-suites-jones-mills": "Triage — no Google water evidence (lodging); off-topic for a splash-pad directory.",
    "marie-curie-playground-bayside": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "mccaffrey-playground-new-york": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "melt-away-bay-orlando": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "mill-creek-falls-of-kumbrabow-huttonsville": "Triage — pool-only amenity (other/attraction); a venue pool, not a splash pad.",
    "mirror-maze-east-rutherford": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "mohican-adventures-river-trips-fun-center-loudonville": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "montage-big-sky-big-sky": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "mt-sterling-montgomery-county-recreation-commission-mt-sterling": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "nappanee-park-department-nappanee": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "new-england-outdoor-center-millinocket": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "north-texas-jellystone-park-burleson": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
    "oak-point-park-and-nature-preserve-plano": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "ocean-trails-reserve-rancho-palos-verdes": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "orient-land-trust-valley-view-hot-springs-moffat": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "pa-grand-canyon-wellsboro": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "pepsi-cola-sign-long-island-city": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "pirate-adventures-on-the-chesapeake-annapolis": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "plainsboro-preserve-cranbury": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "pop-s-lake-campground-galway": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "quarry-park-adventures-rocklin": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "raleigh-county-recreation-auth-beckley": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "refreshing-mountain-retreat-and-adventure-center-stevens": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
    "renfro-valley-koa-holiday-mt-vernon": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
    "river-land-resort-earp": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "river-run-playground-new-york": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "riverbend-hot-springs-truth-or-consequences": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
    "riversport-adventures-oklahoma-city": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "rock-run-recreation-area-patton": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "rockwood-marina-rv-resort-rockwood": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "roseland-wake-park-canandaigua": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "sail-central-park-model-boat-sailing-new-york": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "sandy-river-outdoor-adventure-rice": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "schmidt-s-landing-big-stone-city": "Triage — no Google water evidence (lodging); off-topic for a splash-pad directory.",
    "seacoast-adventure-windham": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "serengeti-springs-at-the-hattiesburg-zoo-hattiesburg": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "silver-bay-ymca-conference-and-family-retreat-center-silver-bay": "Triage — no Google water evidence (lodging); off-topic for a splash-pad directory.",
    "sleepy-j-cabins-swan-valley": "Triage — no Google water evidence (lodging); off-topic for a splash-pad directory.",
    "small-town-campground-mallard": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "south-of-the-border-motor-inn-hamer": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "stone-park-bonne-terre": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "sun-outdoors-frontier-town-berlin": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "super-8-by-wyndham-big-rapids-big-rapids": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "super-8-by-wyndham-cooke-city-yellowstone-park-area-cooke-city": "Triage — no Google water evidence (lodging); off-topic for a splash-pad directory.",
    "surestay-plus-by-best-western-woodbury-inn-woodbury": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "sweetwater-river-resort-cotopaxi": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
    "tappan-lakeside-resort-waterfront-cabin-rentals-on-tappan-lake-oh-scio": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "tarr-coyne-wild-west-playground-new-york": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "teton-county-jackson-parks-recreation-jackson": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "the-adventure-park-at-sandy-spring-sandy-spring": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "the-arboretum-at-penn-state-state-college": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "the-granite-prospect-brooklyn": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "the-greenbrier-white-sulphur-springs": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "the-park-at-swan-valley-swan-valley": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "thunder-bay-falls-galena": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "tigerton-ohv-park-campground-tigerton": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "tioga-downs-casino-resort-nichols": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "trail-dust-town-tucson": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "trout-pond-park-muncy": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "twin-lakes-recreation-area-wilcox": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
    "vanderbilt-playground-brooklyn": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "wild-plumas-resort-and-campground-greenville": "Triage — no Google water evidence (campground/RV); off-topic for a splash-pad directory.",
    "william-sheridan-playground-brooklyn": "Triage — no Google water evidence (other/attraction); off-topic for a splash-pad directory.",
    "winter-park-chateau-winter-park": "Triage — no Google water evidence (lodging); off-topic for a splash-pad directory.",
    "winter-park-fraser-chamber-winter-park": "Triage — no Google water evidence (admin/org); off-topic for a splash-pad directory.",
    "winter-park-mountain-lodge-winter-park": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "worldmark-deer-harbor-deer-harbor": "Triage — pool-only amenity (lodging); a venue pool, not a splash pad.",
    "worlds-of-fun-village-kansas-city": "Triage — pool-only amenity (campground/RV); a venue pool, not a splash pad.",
}

# 20260602 HIGH public review-surface cleanup. These listings were flagged by
# scan_false_positive_pads.py as HIGH risk while still indexable and present in
# the sitemap. Exclude conservatively for AdSense resubmission readiness.
PAD_EXCLUDE_SLUGS.update({
    "aqua-bay-bar-and-grill-orlando": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "ace-adventure-resort-whitewater-rafting-west-virginia-oak-hill": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "velocity-island-park-woodland": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "wild-acadia-camping-resort-trenton": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "bananas-fun-park-grand-junction": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "elevated-wake-park-lexington": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "bear-paw-adventure-park-caledonia": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "blue-harbor-resort-sheboygan": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "buena-vista-whitewater-park-buena-vista": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "coco-key-resort-and-water-park-orlando-orlando": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "indian-springs-campground-splash-springs-aqua-park-garrett": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "tropicanoe-cove-lafayette": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "the-reef-indoor-water-park-billings": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "splash-lagoon-erie": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "lost-frontier-rv-park-and-bar-grill-hemphill": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "brush-creek-holl-r-mountain-coaster-princeton": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "glacier-highline-coram": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "wake-in-the-woods-aquapark-and-campground-lake-ariel": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "coral-empire-aquaculture-spokane": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "magnolia-physical-and-aquatic-therapy-of-huntington-beach-huntington-beach": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "east-lyme-aquatic-and-fitness-center-east-lyme": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "slick-city-action-park-fort-myers": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "inflatable-world-treasure-valley-meridian": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "rossville-water-pub-rossville": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "beech-bend-bowling-green": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "whoazone-at-heron-beach-holly": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "slick-city-action-park-chesterfield": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "morey-s-piers-beachfront-water-parks-wildwood": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "showboat-resort-atlantic-city-atlantic-city": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "whites-city-cavern-inn-whites-city": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "highlands-aerial-park-scaly-mountain": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "slick-city-action-park-plano": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "splashway-campground-sheridan": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "clearfield-aquatic-and-fitness-center-clearfield": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "the-crayfish-saloon-pamplin": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "water-s-edge-outfitters-campground-petersburg": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "rivers-edge-campground-birchwood-birchwood": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "slick-city-action-park-wauwatosa": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "sleeping-bear-rv-park-campground-lander": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "slick-city-action-park-peoria": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "raindance-river-resort-windsor": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "slick-city-action-park-lakewood": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "holmes-creek-canoe-livery-vernon": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "orlando-watersports-complex-orlando": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "lazy-l-lake-campground-west-terre-haute": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "rapid-river-lodge-baxter": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "slick-city-action-park-maple-grove": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "whitewater-inn-big-sky": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "the-boardwalk-at-the-spring-creek-marina-spring-creek": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "mountain-creek-resort-vernon-township": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "hope-lake-lodge-conference-center-cortland": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "jellystone-parktm-keystone-lake-mannford": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "chehalem-aquatic-and-fitness-center-newberg": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "split-rock-lodge-lake-harmony": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "jellystone-parktm-texas-wine-country-fredericksburg": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "paradise-springs-grapevine": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "pump-house-indoor-waterpark-jay": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "massanutten-resort-massanutten": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "kalahari-resorts-conventions-wisconsin-dells-baraboo": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "the-ingleside-hotel-pewaukee": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "owa-parks-resort-foley": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "terranea-resort-rancho-palos-verdes": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "splash-rv-resort-milton": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "westgate-vacation-villas-resort-kissimmee": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "egyptian-hills-resort-creal-springs": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "knight-s-action-park-springfield": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "indiana-beach-monticello": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "russell-sims-aquatic-center-bowling-green": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "boyne-mountain-resort-boyne-falls": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "arrowwood-resort-conference-center-alexandria": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "runaway-rapids-waterpark-keansburg": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "wave-resort-long-branch": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "big-big-on-the-battenkill-kayak-and-tubing-shushan": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "clason-point-park-bronx": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "rocking-horse-ranch-resort-highland": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "jungle-rapids-family-fun-park-wilmington": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "u-s-national-whitewater-center-charlotte": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "days-inn-hotel-governors-waterpark-rv-park-fitness-center-casselton": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "comfort-inn-splash-harbor-bellville": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "natural-springs-resort-rv-park-campground-and-recreation-destination-new-paris": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "knoebels-amusement-resort-elysburg": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "splash-magic-rv-resort-northumberland": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "the-lodge-at-water-s-edge-portersville": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "tioga-hammond-lakes-recreation-area-tioga": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "the-resort-at-governor-s-crossing-sevierville": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "palm-beach-at-moody-gardens-water-park-galveston": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "massanutten-indoor-waterpark-massanutten": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "twin-falls-resort-state-park-mullens": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "river-bend-rv-resort-watertown": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "encore-resort-at-reunion-kissimmee": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "river-country-water-park-river-ranch": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "treasure-island-waterslide-and-cabanas-treasure-island": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "marina-station-water-park-hiawassee": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "king-s-pointe-resort-storm-lake": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "jellystone-parktm-cranberry-acres-carver": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "double-jj-resort-rothbury": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "splash-universe-resort-dundee": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "grand-country-resort-branson": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "claremar-twin-lakes-camping-resort-new-london": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "jellystone-parktm-clay-s-resort-north-lawrence": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "brookings-inn-splash-zone-waterpark-brookings": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "hydrous-wake-park-little-elm": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "gene-fullmer-fitness-recreation-center-west-jordan": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "jay-peak-resort-jay": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "long-bridge-aquatics-fitness-center-arlington": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "midlothian-athletic-club-richmond": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "deer-valley-lodge-barneveld": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "meadowbrook-resort-wisconsin-dells": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "mt-olympus-water-theme-park-resort-wisconsin-dells": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "waylon-s-water-world-yuma": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "white-water-mountain-rehoboth-beach": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "wai-kai-ewa-beach": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "parrot-cove-indoor-water-park-garden-city": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "the-children-s-park-at-town-square-las-vegas-las-vegas": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "kalahari-indoor-waterpark-pocono-manor": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "sugar-hollow-marina-lafollette": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "wonderland-amusement-park-amarillo": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "kalahari-indoor-water-park-baraboo": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "kalahari-outdoor-water-park-baraboo": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "sheboygan-quarry-beach-adventure-park-and-water-sports-sheboygan": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "paqua-park-at-scorpion-bay-marina-morristown": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "aquatic-integration-atascadero": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "river-splash-anderson": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "discovery-aquatics-marine-fish-coral-saltwater-fish-store-palm-harbor": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "harold-hall-quarry-beach-batavia": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "mammoth-valley-park-cave-city": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "island-aqua-park-margate-city": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "bath-beach-park-brooklyn": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "community-splash-pad-ice-cream-cafe-somerville": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "calypso-cove-baytown": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "gator-bayou-adventure-park-new-caney": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "lighthouse-beach-splash-pad-port-lavaca": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "water-country-usa-williamsburg": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "surf-n-slide-water-park-moses-lake": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
    "dolphins-cove-sun-prairie": "20260602 HIGH public false-positive scan; excluded from AdSense review surface.",
})

# 20260602 user spot-checks that were below HIGH but still off-scope enough to
# remove from the public review surface.
PAD_EXCLUDE_SLUGS.update({
    "lake-stephens-rcpra-beckley": "20260602 user spot-check; off-scope venue removed from AdSense review surface.",
    "bobbi-s-world-morgantown": "20260602 user spot-check; off-scope venue removed from AdSense review surface.",
})

PAD_EXCLUDE_SLUGS.update({
    "ed-austin-regional-park-jacksonville": "20260606 owner swap - removed from public site, replaced with Murray Hill Playground.",
})

PAD_EXCLUDE_SLUGS.update({
    "busch-gardens-tampa-bay-tampa": "20260606 owner removal - amusement park, not a splash pad.",
    "fountains-at-gateway-murfreesboro": "20260606 duplicate of fountains-splash-pad-murfreesboro (same address/coords).",
})

# Name-level hard-drop guard for obvious false-positive venue classes. The
# water-name allowlist keeps legitimate "Splash Pad", "Waterpark", "Pool",
# etc. listings from being removed just because they are attached to a park.
PAD_OFF_TOPIC_NAME_PATTERNS = [
    r"\bparking\b",
    r"\bwalmart\b",
    r"\bpeanut shop\b",
    r"\bpublic works\b",
    r"\bcarousel\b",
    r"\bboathouse\b",
    r"\bwater taxi\b",
    r"\bjet ski\b",
    r"\bferry\b",
    r"\bdog run\b",
    r"\bpickleball\b",
    r"\bculligan\b",
    r"\bmuseum\b",
    r"\baquarium\b",
    r"\bhatchery\b",
    r"\blighthouse\b",
    r"\btheatre\b",
    r"\btheater\b",
    r"\bcasino\b",
    r"\bspa\b",
    r"\bwatsu\b",
    r"\bbathhouse\b",
    r"\bcave\b",
    r"\bgolf\b",
    r"\bgo-?karts?\b",
    r"\bmall\b",
]

PAD_WATER_NAME_PATTERNS = [
    r"\bsplash\b",
    r"\bsplashpad\b",
    r"\bspray\b",
    r"\bsprayground\b",
    r"\bwater\s*park\b",
    r"\bwaterpark\b",
    r"\baquatic\b",
    r"\bpool\b",
    r"\bswim(?:ming)?\b",
    r"\bbeach\b",
    r"\blagoon\b",
    r"\bsoak\b",
    r"\bwet\b",
    r"\bwater play\b",
]

# City pages — keyed by state slug, each city entry drives a /city/<slug> page.
# Add new states here as city-level content is created.
CITY_PAGES = {
    "arizona": [
        {
            "name": "Phoenix",
            "slug": "phoenix-arizona",
            "state": "Arizona",
            "state_slug": "arizona",
            "meta_description": "Find splash pads in Phoenix, AZ — free spray parks and water play areas across the Valley of the Sun. Family-friendly aquatic facilities updated for 2026.",
            "description": (
                "Phoenix operates one of the most extensive free splash pad networks in the country, "
                "a direct response to a climate where summer highs routinely reach 110°F and outdoor "
                "water play becomes a genuine necessity for families. The City of Phoenix Parks and "
                "Recreation department maintains splash pads and spray features at neighborhood parks "
                "across the metro, offering free, accessible water play without a reservation or "
                "admission fee. Many locations are equipped with shade sails and covered seating — "
                "a design standard in the Valley of the Sun that acknowledges sun exposure is as "
                "much a concern as heat. The season in Phoenix is unusually long: many facilities "
                "open as early as March and run through October, with the heaviest use concentrated "
                "in the brutal stretch from June through August. Morning visits before 10 a.m. are "
                "strongly recommended during peak summer — the heat index climbs quickly, and earlier "
                "visits are significantly more comfortable. Phoenix's size means splash pads are "
                "distributed across the city, from Central Phoenix neighborhoods to the far west and "
                "south sides. Bring water, apply sunscreen before arriving, and check Phoenix Parks "
                "and Recreation for current hours and any seasonal closures before your visit."
            ),
            "faq": [
                {
                    "q": "Are Phoenix splash pads free?",
                    "a": "Yes, Phoenix city-operated splash pads are free and open to the public during park hours. No admission fee is required at most neighborhood splash pad locations across the metro.",
                },
                {
                    "q": "When do Phoenix splash pads open for the season?",
                    "a": "Many Phoenix splash pads open as early as March and operate through October, taking advantage of the city's extended warm season. Peak usage runs from May through September. Check Phoenix Parks and Recreation for specific location schedules.",
                },
                {
                    "q": "What is the best time to visit a Phoenix splash pad in summer?",
                    "a": "Morning visits before 10 a.m. are strongly recommended during June, July, and August when temperatures can exceed 110°F by midday. Bring water, sunscreen, and shade gear — many Phoenix splash pads include shade sails but the sun is intense year-round.",
                },
            ],
        },
        {
            "name": "Scottsdale",
            "slug": "scottsdale-arizona",
            "state": "Arizona",
            "state_slug": "arizona",
            "meta_description": "Find splash pads in Scottsdale, AZ — free spray parks and water play in the East Valley. Family-friendly aquatic facilities updated for 2026.",
            "description": (
                "Scottsdale's parks system has invested in modern spray parks that reflect both the "
                "city's design sensibility and the practical demands of desert living. Located in the "
                "eastern Valley of the Sun, Scottsdale operates splash pad features at community "
                "parks throughout the city — from South Scottsdale neighborhoods to the newer "
                "developments in North Scottsdale near McDowell Mountain and Pinnacle Peak. Most "
                "city-operated splash pads are free to use during regular park hours. Scottsdale's "
                "facilities typically include shade structures, which are standard in the Arizona "
                "desert and make a real difference on days when temperatures push past 105°F. The "
                "extended desert season means Scottsdale splash pads can be active from spring "
                "through fall — a longer window than nearly any other city in the country. The city's "
                "proximity to tourist areas, Old Town, and the resort corridor makes it easy for "
                "visitors and locals alike to combine a splash pad stop with other activities. "
                "Morning hours are the most comfortable during peak summer. Check Scottsdale Parks "
                "and Recreation for current locations, hours, and seasonal availability."
            ),
            "faq": [
                {
                    "q": "Are Scottsdale splash pads free?",
                    "a": "Most Scottsdale city-operated splash pads are free and open to the public during regular park hours. No admission is required at neighborhood spray park locations.",
                },
                {
                    "q": "When are Scottsdale splash pads open?",
                    "a": "Scottsdale splash pads typically operate from spring through fall, with many locations active from March through October. Check Scottsdale Parks and Recreation for specific seasonal dates and hours by location.",
                },
                {
                    "q": "Do Scottsdale splash pads have shade?",
                    "a": "Yes, most Scottsdale splash pad facilities include shade sails or covered seating areas — a standard design feature in Arizona that helps manage the intense desert sun. Sunscreen and water are still strongly recommended regardless of available shade.",
                },
            ],
        },
        {
            "name": "Tempe",
            "slug": "tempe-arizona",
            "state": "Arizona",
            "state_slug": "arizona",
            "meta_description": "Find splash pads in Tempe, AZ — free spray parks and water play near ASU and Tempe Town Lake. Family aquatic facilities updated for 2026.",
            "description": (
                "Tempe sits at the center of the Phoenix metro, bordered by Phoenix to the west, "
                "Scottsdale to the north, and Chandler to the south — and its compact, walkable "
                "layout makes splash pad access straightforward for the city's mix of families, "
                "students, and residents. The City of Tempe Parks and Recreation operates splash "
                "features at neighborhood parks throughout the city, providing free water play "
                "during the long Arizona warm season. Tempe Town Lake, the city's landmark "
                "reservoir along the Salt River, anchors a recreation corridor that includes "
                "parks and green space where families spend time on the waterfront. The city's "
                "urban density means splash pads are accessible from most Tempe neighborhoods "
                "without a long drive. Tempe's summers match the broader Phoenix metro for "
                "intensity — June through August temperatures regularly exceed 105°F — making "
                "water play essential rather than optional. Most city-operated splash pads are "
                "free and open to the public during park hours. Shade structures are typically "
                "included at Arizona splash pad facilities. Morning visits are best during "
                "peak summer. Check Tempe Parks and Recreation for current schedules, locations, "
                "and any seasonal closures before visiting."
            ),
            "faq": [
                {
                    "q": "Are Tempe splash pads free?",
                    "a": "Yes, Tempe city-operated splash pads are free and open to the public during regular park hours. No admission fee is required at most spray park locations.",
                },
                {
                    "q": "When do Tempe splash pads open for the season?",
                    "a": "Tempe splash pads typically operate through the extended Arizona warm season, often from spring into fall. Check Tempe Parks and Recreation for specific dates and hours at each location.",
                },
                {
                    "q": "Are there splash pads near Tempe Town Lake?",
                    "a": "Tempe Town Lake and the surrounding Salt River recreation corridor include parks and green spaces that serve as recreational destinations. Check with Tempe Parks and Recreation for current water play locations near the lake and throughout the city.",
                },
            ],
        },
    ],
    "tennessee": [
        {
            "name": "Nashville",
            "slug": "nashville-tennessee",
            "state": "Tennessee",
            "state_slug": "tennessee",
            "meta_description": "Find splash pads in Nashville, TN — free spray parks, city water play areas, and family-friendly aquatic facilities in Davidson County. Updated 2026.",
            "description": (
                "Nashville's park system includes several free community splash pads spread across "
                "Davidson County, giving families access to water play without a long drive or admission fee. "
                "Metro Nashville Parks operates splash pads at Shelby Park, Centennial Park, and several "
                "neighborhood recreation centers — most open Memorial Day weekend and run through Labor Day. "
                "The city's rapid population growth over the past decade has pushed investment in new aquatic "
                "amenities, and surrounding communities in Williamson and Rutherford counties have added their "
                "own facilities to serve the metro's expanding suburbs. Murfreesboro, just 30 miles southeast, "
                "has built a strong parks network that includes free splash areas. Nashville summers are hot "
                "and humid, with July and August highs consistently in the 90s, making water play genuinely "
                "essential for families with young children. Morning visits — before 11 a.m. — are the most "
                "comfortable and least crowded. Most city-operated splash pads are free of charge. Bring "
                "sunscreen, a change of clothes, and water, and check Metro Parks hours before you go as "
                "schedules may vary by location."
            ),
            "faq": [
                {
                    "q": "Are Nashville splash pads free?",
                    "a": "Most Metro Nashville Parks splash pads are free and open to the public during regular park hours. Some aquatic centers within recreation facilities may charge a small admission fee — check the specific location before visiting.",
                },
                {
                    "q": "When do Nashville splash pads open for the season?",
                    "a": "Nashville splash pads typically open around Memorial Day weekend (late May) and operate through Labor Day (early September). Some locations may open earlier or close later depending on weather and staffing.",
                },
                {
                    "q": "What is the best time to visit a Nashville splash pad?",
                    "a": "Weekday mornings before 11 a.m. are the least crowded and most comfortable, especially in July and August when afternoon temperatures regularly reach the 90s. Bring sunscreen and arrive early for the best experience.",
                },
            ],
        },
        {
            "name": "Murfreesboro",
            "slug": "murfreesboro-tennessee",
            "state": "Tennessee",
            "state_slug": "tennessee",
            "meta_description": "Find splash pads in Murfreesboro, TN — free spray parks and water play in Rutherford County. Family-friendly aquatic facilities updated for 2026.",
            "description": (
                "Murfreesboro, located about 35 miles southeast of Nashville in Rutherford County, has "
                "developed a strong parks network to serve its rapidly growing population — and water play "
                "is a central part of that investment. The city's parks and recreation department operates "
                "community splash pads that provide free, accessible water play for families across the "
                "community. Murfreesboro is one of the fastest-growing cities in Tennessee, and its parks "
                "infrastructure has kept pace with that growth. The Murfreesboro area's summers are hot "
                "and humid, typical of Middle Tennessee, with peak season running from June through August. "
                "Most city splash pads are free of charge and open during regular park hours throughout the "
                "summer season. Greenway trails connect several parks, making it easy to combine a splash "
                "pad visit with a walk or bike ride. The Stones River Greenway and surrounding park network "
                "give Murfreesboro families a variety of outdoor options alongside the splash facilities. "
                "Check the Murfreesboro Parks and Recreation website for current hours and seasonal dates "
                "before visiting."
            ),
            "faq": [
                {
                    "q": "Are Murfreesboro splash pads free?",
                    "a": "Yes, Murfreesboro's city-operated splash pads are free and open to the public during regular park hours. No admission fee is required at most locations.",
                },
                {
                    "q": "When do Murfreesboro splash pads open?",
                    "a": "Murfreesboro splash pads typically open in late May or early June and operate through Labor Day weekend. Check the city's Parks and Recreation department for exact dates each season.",
                },
                {
                    "q": "What parks in Murfreesboro have splash pads?",
                    "a": "Murfreesboro Parks and Recreation operates splash pad facilities at several community parks. Visit the city's parks website or call ahead to confirm which locations are active this season.",
                },
            ],
        },
        {
            "name": "Hendersonville",
            "slug": "hendersonville-tennessee",
            "state": "Tennessee",
            "state_slug": "tennessee",
            "meta_description": "Find splash pads in Hendersonville, TN — free spray parks and water play in Sumner County. Family water play areas updated for 2026.",
            "description": (
                "Hendersonville sits on Old Hickory Lake in Sumner County, about 18 miles northeast of "
                "Nashville, and offers a suburban setting that blends lakeside recreation with community park "
                "amenities including water play facilities for families. The city's parks department serves "
                "a community that has grown substantially as part of the greater Nashville metro area, and "
                "splash pad access is part of that parks investment. Sumner County's warm summers — with "
                "peak temperatures in the 90s through July and August — drive strong demand for outdoor "
                "water play from Memorial Day through Labor Day. Most Hendersonville and Sumner County park "
                "splash pads are free to use during regular park hours. The area's proximity to Old Hickory "
                "Lake also gives families additional water recreation options, though the splash pads provide "
                "a safe, supervised alternative for younger children. Check with the Hendersonville Parks "
                "and Recreation department or Sumner County Parks for current seasonal schedules and "
                "locations before planning a visit."
            ),
            "faq": [
                {
                    "q": "Are Hendersonville splash pads free?",
                    "a": "Most Hendersonville and Sumner County splash pads are free and open to the public during regular park hours. No admission fee is required at city-operated spray parks.",
                },
                {
                    "q": "When is the splash pad season in Hendersonville?",
                    "a": "Hendersonville splash pads typically open around Memorial Day weekend and operate through Labor Day. Contact Hendersonville Parks and Recreation for exact seasonal dates and locations.",
                },
                {
                    "q": "What else is there to do near splash pads in Hendersonville?",
                    "a": "Hendersonville's location on Old Hickory Lake means many parks are near waterfront areas with walking trails, picnic facilities, and lake access — making it easy to combine a splash pad visit with other outdoor activities.",
                },
            ],
        },
        {
            "name": "Clarksville",
            "slug": "clarksville-tennessee",
            "state": "Tennessee",
            "state_slug": "tennessee",
            "meta_description": "Find splash pads in Clarksville, TN — free spray parks and water play in Montgomery County. Family aquatic facilities updated for 2026.",
            "description": (
                "Clarksville, Tennessee's fifth-largest city, sits at the confluence of the Cumberland and "
                "Red rivers in Montgomery County about 45 miles northwest of Nashville. The city's parks "
                "and recreation system serves a large and growing population — anchored significantly by "
                "Fort Campbell, which straddles the Tennessee-Kentucky border nearby — with community parks "
                "that include water play facilities for families. Clarksville summers are among the hottest "
                "in Tennessee, with July averages well into the 90s, making splash pads a key community "
                "amenity from late spring through early fall. The city has invested in its parks network, "
                "and splash areas are part of that infrastructure. Clarksville's Liberty Park, one of the "
                "largest urban parks in the state, offers multiple recreational amenities along the "
                "Cumberland River. Most city-operated splash pads are free of charge. Seasonal hours "
                "typically align with Memorial Day through Labor Day. Check with Clarksville Parks and "
                "Recreation for current locations, hours, and any temporary closures."
            ),
            "faq": [
                {
                    "q": "Are Clarksville splash pads free?",
                    "a": "Yes, most Clarksville Parks and Recreation splash pads are free and open to the public. Some aquatic center features may have admission fees — check the specific location before visiting.",
                },
                {
                    "q": "When do Clarksville splash pads open for summer?",
                    "a": "Clarksville splash pads typically open around Memorial Day and run through Labor Day. Check Clarksville Parks and Recreation for the current season's exact dates.",
                },
                {
                    "q": "Is Liberty Park a good place for families with splash pads?",
                    "a": "Liberty Park is one of Clarksville's signature recreational destinations along the Cumberland River. Check with the parks department to confirm current water play facilities and amenities at the park.",
                },
            ],
        },
        {
            "name": "Chattanooga",
            "slug": "chattanooga-tennessee",
            "state": "Tennessee",
            "state_slug": "tennessee",
            "meta_description": "Find splash pads in Chattanooga, TN — free spray parks and water play in Hamilton County. Family-friendly aquatic facilities updated for 2026.",
            "description": (
                "Chattanooga has built an identity as one of Tennessee's premier outdoor recreation cities, "
                "and its parks system reflects that reputation with well-maintained facilities that include "
                "community water play areas for families. Situated along the Tennessee River at the base of "
                "Lookout Mountain, Chattanooga's park network blends greenway trails, river access, and "
                "neighborhood amenities that include splash pads and spray features. The city's outdoor "
                "culture — shaped by its mountain biking trails, rock climbing access, and revitalized "
                "riverfront — extends to family-friendly water play. Hamilton County Parks and the City of "
                "Chattanooga operate facilities across the metro area. Chattanooga's summers are hot and "
                "humid, with peak temperatures in the upper 80s and 90s through July and August, creating "
                "genuine demand for water play from Memorial Day through Labor Day. Most city-operated "
                "splash pads are free of charge. The revitalized North Shore and South Side neighborhoods "
                "have seen increased recreational investment, and splash facilities are part of that growth. "
                "Check with Chattanooga Parks and Recreation or Hamilton County Parks for current "
                "seasonal schedules before visiting."
            ),
            "faq": [
                {
                    "q": "Are Chattanooga splash pads free?",
                    "a": "Most Chattanooga city-operated splash pads are free and open to the public during regular park hours. Some aquatic facilities within recreation centers may charge admission.",
                },
                {
                    "q": "When do Chattanooga splash pads open?",
                    "a": "Chattanooga splash pads typically open around Memorial Day weekend and run through Labor Day. Check Chattanooga Parks and Recreation or Hamilton County Parks for seasonal dates.",
                },
                {
                    "q": "What neighborhoods in Chattanooga have splash pads?",
                    "a": "Chattanooga has water play facilities distributed across several neighborhoods. The North Shore, South Side, and various community parks throughout Hamilton County have seen recreational investment. Check with the parks department for current active locations.",
                },
            ],
        },
    ],
    "texas": [
        {
            "name": "Dallas",
            "slug": "dallas-texas",
            "state": "Texas",
            "state_slug": "texas",
            "meta_description": "Find splash pads in Dallas, TX — free spray grounds and water play across Dallas County and the DFW metroplex. Family water play updated for 2026.",
            "description": "Dallas sits at the heart of North Texas and the sprawling Dallas–Fort Worth metroplex, where long, punishing summers make free water play a core part of family life from late spring through early fall. The Dallas Park and Recreation Department operates spray grounds and splash features at neighborhood parks across the city, offering free, no-reservation water play that runs through one of the longest warm seasons in the country. Dallas summers are hot and humid, with highs routinely in the upper 90s and frequent stretches above 100°F from June through September, so most spray grounds run on an extended schedule rather than the short Memorial-Day-to-Labor-Day window common farther north. Downtown, Klyde Warren Park's children's area draws families with an interactive fountain, while the broader park system spreads water play across neighborhoods from Oak Cliff to North Dallas. Because the metroplex is so large, families in surrounding cities — Plano, Arlington, Irving, and Garland among them — often have their own municipal spray grounds a short drive away. Most City of Dallas spray grounds are free and open during regular park hours, though hours and seasonal start dates vary by location. Morning visits before the midday heat peaks are the most comfortable during July and August. Bring water, apply sunscreen before you arrive, and check Dallas Park and Recreation for current locations, hours, and any seasonal closures before planning your visit.",
            "faq": [
                {
                    "q": "Are Dallas splash pads free?",
                    "a": "Most City of Dallas spray grounds and splash features are free and open to the public during regular park hours. Some aquatic centers with larger water-play areas may charge admission — check the specific location before visiting."
                },
                {
                    "q": "When does the Dallas splash pad season run?",
                    "a": "Thanks to North Texas's long, hot summers, many Dallas spray grounds operate on an extended season — often from spring into early fall — rather than the shorter Memorial Day to Labor Day window. Check Dallas Park and Recreation for current dates by location."
                },
                {
                    "q": "What's the best time to visit a Dallas splash pad in summer?",
                    "a": "Mornings before midday are the most comfortable during July and August, when temperatures regularly top 100°F. Bring water and sunscreen, and arrive early on weekends when popular locations fill up fast."
                }
            ]
        },
        {
            "name": "Houston",
            "slug": "houston-texas",
            "state": "Texas",
            "state_slug": "texas",
            "meta_description": "Find splash pads in Houston, TX — free spray pads and water play across Harris County and the Gulf Coast. Family aquatic facilities updated for 2026.",
            "description": "Houston, the largest city in Texas, sits on the humid Gulf Coast plain of Harris County, where a long subtropical summer makes water play less a seasonal treat than a near-necessity. The Houston Parks and Recreation Department operates splash pads and spray features at parks across the city, providing free water play that runs deep into the fall thanks to the region's warm, extended season. Houston's summers are defined as much by humidity as by heat — daytime highs in the 90s combine with Gulf moisture to push the heat index up quickly, so shaded splash areas and early-morning visits are especially valuable here. Downtown, Discovery Green's Gateway Fountain is one of the city's best-known interactive water features, drawing families into its programmed jets, while Hermann Park and neighborhood parks across the metro round out the options. Houston's enormous footprint means water play is spread widely, and surrounding communities in Harris and Fort Bend counties — Katy, Sugar Land, and Pearland among them — operate their own municipal splash pads. Afternoon thunderstorms are common during the summer wet season, so it's worth checking the forecast before heading out. Most city-operated splash pads are free and open during regular park hours, though schedules vary by location. Bring water, apply sunscreen, and check Houston Parks and Recreation for current locations, hours, and seasonal availability before your visit.",
            "faq": [
                {
                    "q": "Are Houston splash pads free?",
                    "a": "Most Houston Parks and Recreation splash pads and spray features are free and open to the public during regular park hours. Larger aquatic facilities may charge admission, so check the specific location before you go."
                },
                {
                    "q": "When do Houston splash pads open for the season?",
                    "a": "Houston's subtropical climate supports a long water-play season that often stretches from spring into the fall, with many splash pads operating well beyond the traditional summer window. Check Houston Parks and Recreation for current seasonal dates by location."
                },
                {
                    "q": "Where can I find interactive water features in downtown Houston?",
                    "a": "Discovery Green's Gateway Fountain is a popular downtown interactive water feature where children play among programmed jets. Hermann Park and parks throughout the city also offer water play. Confirm current operating status with the venue or Houston Parks and Recreation."
                }
            ]
        },
    ],
    "indiana": [
        {
            "name": "Indianapolis",
            "slug": "indianapolis-indiana",
            "state": "Indiana",
            "state_slug": "indiana",
            "meta_description": "Find splash pads in Indianapolis, IN — free spray grounds and water play across Marion County. Family-friendly aquatic facilities updated for 2026.",
            "description": "Indianapolis anchors central Indiana and Marion County, and its parks system gives families a strong network of free spray grounds to cool off during the Midwest's hot, humid summers. Indy Parks and Recreation operates spray grounds at neighborhood and regional parks across the city — free, walk-up water play that needs no reservation and typically runs from late spring through the end of summer. Indianapolis summers are warm and humid, with July and August highs commonly in the upper 80s and lower 90s, driving steady demand for water play from Memorial Day through Labor Day. The city's spray grounds are distributed across its neighborhoods, from the near-downtown parks to the suburban edges of Marion County, and many sit alongside playgrounds, trails, and sports fields that make for an easy half-day outing. Surrounding Hamilton County suburbs — Carmel, Fishers, and Noblesville among them — have invested heavily in their own parks and water-play amenities as the metro has grown. Most Indy Parks spray grounds are free and operate during regular park hours through the summer season, though start and end dates shift with the weather and staffing each year. Weekday mornings are the least crowded and most comfortable. Bring a change of clothes, apply sunscreen before arriving, and check Indy Parks and Recreation for current spray ground locations, hours, and seasonal dates before you head out.",
            "faq": [
                {
                    "q": "Are Indianapolis splash pads free?",
                    "a": "Yes, Indy Parks and Recreation spray grounds are free and open to the public during regular park hours. No admission or reservation is required at most neighborhood locations."
                },
                {
                    "q": "When do Indianapolis spray grounds open?",
                    "a": "Indianapolis spray grounds typically operate from late May (around Memorial Day) through Labor Day, following the Midwest's summer season. Exact opening dates vary year to year with the weather. Check Indy Parks and Recreation for the current schedule."
                },
                {
                    "q": "What are spray grounds in Indianapolis?",
                    "a": "Spray grounds are the city's term for splash pads — flat, zero-depth water-play areas with sprayers and jets and no standing water. Indy Parks operates them free of charge at parks across Marion County, and many sit next to playgrounds and trails."
                }
            ]
        },
    ],
    "new-york": [
        {
            "name": "New York",
            "slug": "new-york-new-york",
            "state": "New York",
            "state_slug": "new-york",
            "meta_description": "Find splash pads in New York, NY — free spray showers and water play in playgrounds across all five boroughs. NYC Parks features updated for 2026.",
            "description": "New York City operates one of the largest free water-play networks in the country, woven into the playgrounds of all five boroughs. Rather than a handful of destination splash pads, NYC Parks maintains hundreds of spray showers and water features in neighborhood playgrounds from Manhattan to the Bronx, Queens, Brooklyn, and Staten Island — free, walk-up cooling that's a defining part of a city summer. The spray showers are typically switched on for the season in late spring and run through the warm months, giving families in even the most densely built neighborhoods a place to cool off within walking distance. Because the system is built into playgrounds rather than standalone parks, water play in New York is unusually accessible by subway, bus, or on foot — no car required. Large parks add bigger draws: the city's flagship green spaces host popular water-play areas alongside their playgrounds, and waterfront parks have expanded family amenities in recent years. New York summers are hot and humid, with July and August highs in the upper 80s that feel warmer amid the concrete, so the spray showers see heavy use on peak afternoons. Most NYC Parks spray showers and water features are free and open during park hours through the season. Bring a towel and sunscreen, and check NYC Parks for current locations, seasonal on-dates, and any playground closures before your visit.",
            "faq": [
                {
                    "q": "Are New York City splash pads free?",
                    "a": "Yes. NYC Parks operates hundreds of free spray showers and water features in playgrounds across all five boroughs, open to the public during park hours. No admission or reservation is required."
                },
                {
                    "q": "When does NYC turn on the spray showers?",
                    "a": "New York City's playground spray showers are typically activated for the season in late spring and run through the warm summer months, with timing dependent on the weather each year. Check NYC Parks for current seasonal on-dates."
                },
                {
                    "q": "Where are splash pads in New York City?",
                    "a": "Water play in NYC is built into playgrounds throughout Manhattan, Brooklyn, Queens, the Bronx, and Staten Island, making it easy to reach on foot or by transit. Use NYC Parks' facility listings or this directory to find spray showers and water features near a specific neighborhood."
                }
            ]
        },
        {
            "name": "Brooklyn",
            "slug": "brooklyn-new-york",
            "state": "New York",
            "state_slug": "new-york",
            "meta_description": "Find splash pads in Brooklyn, NY — free spray showers and water play across Kings County, from Prospect Park to the Coney Island waterfront. Updated 2026.",
            "description": "Brooklyn, the most populous of New York City's five boroughs, has free water play threaded through its dense patchwork of neighborhoods — from brownstone Brooklyn and Bedford-Stuyvesant to Bay Ridge, Flatbush, and the Coney Island waterfront. NYC Parks operates spray showers and water features in playgrounds across the borough, switched on for the warm season and free to use during park hours, giving families a place to cool off without leaving their block. Prospect Park, Brooklyn's signature 500-plus-acre green space, anchors the borough's recreation alongside dozens of smaller neighborhood playgrounds that include sprayers and water features. The Coney Island and Brighton Beach waterfront adds beach and boardwalk play to the mix, making southern Brooklyn a summer destination in its own right. Because Brooklyn is so well served by the subway, most of its spray showers are reachable without a car — a real advantage on a hot afternoon. Brooklyn summers are warm and humid, with July and August highs in the upper 80s that feel hotter amid the borough's density, so playground spray showers see heavy use through the peak months. Most NYC Parks water features in Brooklyn are free and open during park hours for the season. Bring a towel and sunscreen, and check NYC Parks for current spray-shower locations, seasonal on-dates, and any playground closures before heading out.",
            "faq": [
                {
                    "q": "Are Brooklyn splash pads free?",
                    "a": "Yes. NYC Parks operates free spray showers and water features in playgrounds throughout Brooklyn, open during regular park hours. No admission or reservation is required."
                },
                {
                    "q": "When do Brooklyn spray showers open for the summer?",
                    "a": "Brooklyn's playground spray showers are typically turned on in late spring and run through the warm summer months, with exact timing set by NYC Parks based on the weather. Check NYC Parks for current seasonal dates."
                },
                {
                    "q": "Are there splash pads near Prospect Park or Coney Island?",
                    "a": "Prospect Park and the surrounding neighborhoods include playgrounds with water features, and the Coney Island–Brighton Beach waterfront adds beach and boardwalk play. Use this directory or NYC Parks listings to find specific spray-shower locations across the borough."
                }
            ]
        },
    ],
    "florida": [
        {
            "name": "Miami",
            "slug": "miami-florida",
            "state": "Florida",
            "state_slug": "florida",
            "meta_description": "Find splash pads in Miami, FL — free water playgrounds across Miami-Dade County, usable nearly year-round in the subtropical climate. Updated for 2026.",
            "description": "Miami's subtropical climate sets its splash pads apart from almost anywhere else in the country: with warm temperatures nearly year-round, water play in Miami-Dade County isn't confined to a summer season — it's a near-constant. The City of Miami and Miami-Dade County parks systems operate splash pads and water playgrounds across the metro, from the urban core to the suburban reaches of the county, offering free and low-cost cooling that families use far beyond the traditional summer window. Where most American cities open spray features around Memorial Day and close them by Labor Day, Miami's warm winters mean many water-play areas stay active through much of the year. The trade-off is the summer wet season, roughly May through October, when intense midday sun gives way to fast-moving afternoon thunderstorms — so morning visits are doubly wise, beating both the strongest UV and the typical afternoon downpour. Waterfront and downtown parks have added family water-play amenities as Miami-Dade has invested in its public spaces, and the county's sprawl means options are distributed widely from Miami Beach across to the western suburbs. Most city splash pads are free during park hours, while some county water playgrounds within larger parks may charge a small fee. Sun protection matters year-round at this latitude. Check the City of Miami and Miami-Dade County parks departments for current locations, hours, and seasonal details before your visit.",
            "faq": [
                {
                    "q": "Are Miami splash pads free?",
                    "a": "Most City of Miami splash pads are free and open during regular park hours. Some Miami-Dade County water playgrounds within larger parks may charge a small admission fee — check the specific location before visiting."
                },
                {
                    "q": "Can you use Miami splash pads year-round?",
                    "a": "Largely, yes. Miami's subtropical climate keeps temperatures warm through much of the year, so many water-play areas stay active well beyond the typical summer season. Check the City of Miami or Miami-Dade County parks for current hours, which vary by location and season."
                },
                {
                    "q": "What's the best time to visit a Miami splash pad in summer?",
                    "a": "Mornings are best during the May-to-October wet season, when intense midday sun is often followed by afternoon thunderstorms. Apply sunscreen before you arrive — UV is strong year-round at Miami's latitude — and check the forecast before heading out."
                }
            ]
        },
        {
            "name": "Jacksonville",
            "slug": "jacksonville-florida",
            "state": "Florida",
            "state_slug": "florida",
            "meta_description": "Find splash pads in Jacksonville, FL — free JaxParks spray features and water playgrounds across the city. Family water play updated for 2026.",
            "description": "Jacksonville is the largest city by land area in the country, sprawling across northeast Florida along the St. Johns River and the Atlantic coast — and its hot, humid subtropical summers make free water play a staple of family life. The City of Jacksonville's parks system (JaxParks) operates splash pads and spray features at neighborhood parks across the city, from the Westside to the beaches, giving families no-cost places to cool off. Most of these water features run on a seasonal schedule, opening around Memorial Day weekend and operating into the fall, with the heaviest use through the brutal July and August heat. Sites range from compact community parks like Wiley Road Playground and Abess Park — which pair their splash pads with playgrounds, ball fields, and picnic shelters — to larger draws like the splash pad inside oceanfront Kathryn Abbey Hanna Park. Because Jacksonville is so spread out, splash pads are distributed widely, and the surrounding beach towns of Jacksonville Beach and Atlantic Beach add their own. Most JaxParks splash pads are free and open during park hours through the season, though a few sites within larger parks may charge a gate fee. Morning visits are the most comfortable in peak summer. Check JaxParks for current splash pad locations, seasonal opening dates, and hours before your visit.",
            "faq": [
                {
                    "q": "Are Jacksonville splash pads free?",
                    "a": "Most City of Jacksonville (JaxParks) splash pads are free and open to the public during park hours. A few water features within larger parks — such as the splash pad at oceanfront Hanna Park — sit inside a park that charges a gate fee. Check the specific location before visiting."
                },
                {
                    "q": "When do Jacksonville splash pads open for the season?",
                    "a": "Jacksonville's splash pads typically open around Memorial Day weekend and run into the fall, often staying on into October depending on the weather. Peak season is the hot, humid stretch from June through September. Check JaxParks for current dates by location."
                },
                {
                    "q": "Which Jacksonville parks have splash pads?",
                    "a": "JaxParks operates splash pad sites at neighborhood parks across the city, including Wiley Road Playground, Abess Park, and Losco Regional Park, plus the splash pad inside Kathryn Abbey Hanna Park. The surrounding beach communities of Jacksonville Beach and Atlantic Beach have their own as well."
                }
            ]
        },
    ],
    "washington": [
        {
            "name": "Seattle",
            "slug": "seattle-washington",
            "state": "Washington",
            "state_slug": "washington",
            "meta_description": "Find splash pads in Seattle, WA — free spray parks and wading pools across King County, open during the Pacific Northwest's mild summer. Updated 2026.",
            "description": "Seattle's approach to summer water play is distinct from the rest of the country, shaped by the Pacific Northwest's short but reliable warm season. Rather than the months-long spray-pad schedules of the Sun Belt, Seattle Parks and Recreation runs a beloved network of free spray parks and seasonal wading pools that open for a concentrated summer window — generally from around late June through Labor Day. The payoff is a mild, comfortable climate: Seattle summers are dry and pleasant, with highs often in the 70s and low 80s rather than the punishing heat of southern cities, so a spray park here is about play and sunshine more than survival. Spray parks across King County offer free, walk-up water play with no standing water, while the city's classic wading pools — a Seattle institution — fill on warm days at parks throughout the neighborhoods. Because the warm season is short, locals make the most of it, and spray parks see enthusiastic crowds on the city's hottest July and August afternoons. The system is spread across Seattle's neighborhoods, from north-end parks to West Seattle, often paired with playgrounds and green space along Puget Sound. Most spray parks are free and open daily in season, while wading-pool schedules rotate by location and depend on weather and temperature thresholds. Check Seattle Parks and Recreation for current spray-park locations, wading-pool schedules, and seasonal opening dates before you go.",
            "faq": [
                {
                    "q": "Are Seattle spray parks free?",
                    "a": "Yes. Seattle Parks and Recreation operates free spray parks across the city, open to the public daily during the summer season. The city's seasonal wading pools are also free, though they run on rotating schedules."
                },
                {
                    "q": "When do Seattle spray parks and wading pools open?",
                    "a": "Seattle's spray parks and wading pools open for a short summer window, generally from around late June through Labor Day. Wading pools in particular open on warmer days based on temperature, so schedules vary. Check Seattle Parks and Recreation for current dates."
                },
                {
                    "q": "What's the difference between a spray park and a wading pool in Seattle?",
                    "a": "Spray parks are zero-depth water-play areas with sprayers and jets and no standing water, open daily in season. Wading pools are shallow pools that fill on warm days on a rotating, weather-dependent schedule. Seattle Parks runs both, free of charge, across the city."
                }
            ]
        },
    ],
    "illinois": [
        {
            "name": "Chicago",
            "slug": "chicago-illinois",
            "state": "Illinois",
            "state_slug": "illinois",
            "meta_description": "Find splash pads in Chicago, IL — free Chicago Park District spray features and water playgrounds across the city. Family water play updated for 2026.",
            "description": "Chicago's park system is one of the oldest and largest in the country, and the Chicago Park District threads free water play through neighborhoods from the North Side to the South Side. The district operates spray features and water playgrounds at parks across the city — zero-depth splash areas with sprayers and interactive jets that give families a free place to cool off during the city's hot, humid summers. Set along Lake Michigan in Cook County, Chicago pairs these neighborhood spray features with a long lakefront of public beaches, but the splash pads offer a closer, supervised option for younger children. The season is concentrated: water features typically run from late June through late August, the heart of a summer when temperatures climb into the upper 80s and lake humidity makes the heat feel heavier. Because the Park District is so large, spray features are spread widely — parks like McKinley Park and Fosco Park combine splash pads with pools and playgrounds, while harbor and lakefront sites add water-feature play near the water. Most Chicago Park District spray features and water playgrounds are free and open during park hours through the season, though start dates and hours vary by location and weather. Weekday mornings are the least crowded. Bring sunscreen, water, and a change of clothes, and check the Chicago Park District for current spray-feature locations, hours, and seasonal dates before you visit.",
            "faq": [
                {
                    "q": "Are Chicago splash pads free?",
                    "a": "Yes. Chicago Park District spray features and water playgrounds are free and open to the public during regular park hours. No admission or reservation is required at neighborhood spray locations, though some facilities with pools may charge separately."
                },
                {
                    "q": "When do Chicago splash pads open for the season?",
                    "a": "Chicago's water features typically run for a concentrated summer season, often from late June through late August. Exact start and end dates vary by location and weather each year. Check the Chicago Park District for the current schedule."
                },
                {
                    "q": "What does the Chicago Park District call splash pads?",
                    "a": "Chicago Park District facilities are usually listed as 'spray features' or 'water playgrounds' — zero-depth areas with sprayers and interactive jets and no standing water. They're spread across parks citywide, from the North Side to the South Side, and many sit alongside playgrounds and pools."
                }
            ]
        },
    ],
}

# Build Settings
ITEMS_PER_PAGE = 24
FEATURED_COUNT = 6
RECENT_COUNT = 8

# ── Duplicate cleanup (2026-06-09 audit) ────────────────────────────────────────
# 74 same-address groups → keep one listing per venue, drop the 82 duplicates.
# Keep-rule: protected (GSC-trafficked) slug > venue-level name > longest description.
# Review artifact: data/dup_cleanup_proposal_20260609.txt (local).
PAD_EXCLUDE_SLUGS.update({
    "all-seasons-center-vernon-arena-and-siouxnami-waterpark-sioux-center": "duplicate of siouxnami-waterpark-sioux-center (same address)",
    "american-dream-east-rutherford": "duplicate of nickelodeon-universe-theme-park-east-rutherford (same address)",
    "aquatica-san-antonio-san-antonio": "duplicate of seaworld-san-antonio-san-antonio (same address)",
    "big-splash-interactive-fountain-suwanee": "duplicate of town-center-park-suwanee (same address)",
    "billy-beez-crossgates-mall-albany": "duplicate of 5-wits-albany-albany (same address)",
    "billy-beez-destiny-syracuse": "duplicate of wonderworks-destiny-syracuse (same address)",
    "blanchette-park-st-charles": "duplicate of blanchette-aquatic-facility-st-charles (same address)",
    "bridges-bay-resort-arnolds-park": "duplicate of boji-splash-indoor-waterpark-arnolds-park (same address)",
    "c-b-smith-park-pembroke-pines": "duplicate of paradise-cove-water-park-pembroke-pines (same address)",
    "calypso-cove-morgans-wonderland-san-antonio": "duplicate of rainbow-reef-morgan-s-inspiration-island-san-antonio (same address)",
    "cameron-run-regional-park-alexandria": "duplicate of great-waves-waterpark-alexandria (same address)",
    "cape-cod-inflatable-park-west-yarmouth": "duplicate of wicked-waves-cape-cod-west-yarmouth (same address)",
    "casitas-water-adventure-ventura": "duplicate of lake-casitas-recreation-area-ventura (same address)",
    "castaway-island-salem": "duplicate of canobie-lake-park-salem (same address)",
    "centennial-park-naperville": "duplicate of centennial-beach-naperville (same address)",
    "centennial-park-orland-park-orland-park": "duplicate of centennial-park-aquatic-center-orland-park-pool-orland-park (same address)",
    "central-park-carmel": "duplicate of carmel-clay-parks-recreation-carmel (same address)",
    "cheetah-chase-santa-claus": "duplicate of holiday-world-splashin-safari-santa-claus (same address)",
    "cove-point-pool-lusby": "duplicate of cove-point-park-lusby (same address)",
    "dansbury-park-swimming-pool-east-stroudsburg": "duplicate of dansbury-park-east-stroudsburg (same address)",
    "dixon-park-fredericksburg": "duplicate of doris-buffett-swimming-pool-fredericksburg (same address)",
    "dollywood-pigeon-forge": "duplicate of dollywood-s-splash-country-pigeon-forge (same address)",
    "doral-central-park-doral": "duplicate of doral-central-park-aquatic-center-doral (same address)",
    "dreamworks-water-park-east-rutherford": "duplicate of nickelodeon-universe-theme-park-east-rutherford (same address)",
    "edith-pettus-park-splash-pad-clarksville": "duplicate of edith-pettus-park-clarksville (same address)",
    "fins-up-water-park-seasonal-buford": "duplicate of margaritaville-at-lanier-islands-buford (same address)",
    "franklin-recreation-complex-franklin": "duplicate of franklin-splash-park-franklin (same address)",
    "freedom-pool-tucson": "duplicate of freedom-park-tucson (same address)",
    "frisco-athletic-center-frisco": "duplicate of frisco-water-park-frisco (same address)",
    "gwynn-family-aquatic-center-peoria": "duplicate of john-h-gwynn-jr-park-peoria (same address)",
    "heritage-park-splash-pad-clarksville": "duplicate of heritage-park-sports-complex-clarksville (same address)",
    "john-sevier-pool-maryville": "duplicate of john-sevier-park-maryville (same address)",
    "jurassic-park-river-adventuretm-orlando": "duplicate of universal-islands-of-adventure-orlando (same address)",
    "kasey-meadow-s-play-ground-hickory-hills": "duplicate of kasey-meadow-park-cynthia-neal-center-hickory-hills (same address)",
    "killens-pond-state-park-felton": "duplicate of killens-pond-water-park-felton (same address)",
    "kiwanis-wave-pool-tempe": "duplicate of kiwanis-recreation-center-tempe (same address)",
    "krakatau-aqua-coaster-orlando": "duplicate of universal-islands-of-adventure-orlando (same address)",
    "lake-george-expedition-park-lake-george": "duplicate of dino-roar-valley-lake-george (same address)",
    "lake-highlands-north-community-aquatic-center-dallas": "duplicate of lake-highlands-aquatic-center-dallas (same address)",
    "memorial-park-pool-blue-island": "duplicate of blue-island-memorial-park-blue-island (same address)",
    "morgan-s-wonderland-san-antonio": "duplicate of rainbow-reef-morgan-s-inspiration-island-san-antonio (same address)",
    "north-charleston-wannamaker-county-park-north-charleston": "duplicate of whirlin-waters-adventure-waterpark-north-charleston (same address)",
    "oasis-swim-center-surprise": "duplicate of rescue-oasis-surprise (same address)",
    "ohno-drop-slide-orlando": "duplicate of universal-islands-of-adventure-orlando (same address)",
    "otter-cove-aquatic-park-st-charles": "duplicate of otter-cove-splash-park-st-charles (same address)",
    "paradise-falls-kansas-city": "duplicate of typhoon-kansas-city (same address)",
    "parkwood-sports-complex-great-neck": "duplicate of great-neck-park-district-great-neck (same address)",
    "planet-snoopy-kansas-city": "duplicate of oceans-of-fun-kansas-city (same address)",
    "quiet-waters-park-deerfield-beach": "duplicate of ski-rixen-usa-deerfield-beach (same address)",
    "rec-aquatic-center-sulphur-parks-and-recreation-sulphur": "duplicate of spar-waterpark-sulphur-parks-and-recreation-sulphur (same address)",
    "rhodes-jordan-aquatic-center-lawrenceville": "duplicate of rhodes-jordan-park-lawrenceville (same address)",
    "rigby-s-entertainment-complex-warner-robins": "duplicate of rigby-s-water-world-warner-robins (same address)",
    "rio-vista-community-park-peoria": "duplicate of rio-vista-recreation-center-peoria (same address)",
    "riptide-raceway-kansas-city": "duplicate of typhoon-kansas-city (same address)",
    "saxon-woods-pool-white-plains": "duplicate of saxon-woods-park-white-plains (same address)",
    "sears-splash-abilene": "duplicate of arthur-sears-park-abilene (same address)",
    "soakya-water-park-rossville": "duplicate of lake-winnepesaukah-amusement-park-rossville (same address)",
    "sobelsohn-playground-richmond-hill": "duplicate of jackson-pond-playground-richmond-hill (same address)",
    "south-bay-shores-santa-clara": "duplicate of california-s-great-america-santa-clara (same address)",
    "spivey-splash-water-park-jonesboro": "duplicate of clayton-county-international-park-jonesboro (same address)",
    "splash-summit-waterpark-provo": "duplicate of seven-peaks-water-park-provo-provo (same address)",
    "spooky-world-presents-nightmare-new-england-litchfield": "duplicate of mel-s-funway-park-litchfield (same address)",
    "sprayground-at-dorbrook-recreation-area-colts-neck": "duplicate of dorbrook-recreation-area-colts-neck (same address)",
    "springbrook-pool-alcoa": "duplicate of alcoa-duck-pond-alcoa (same address)",
    "stewart-heights-park-tacoma": "duplicate of stewart-heights-pool-tacoma (same address)",
    "t-y-topeekeegee-yugnee-park-hollywood": "duplicate of castaway-island-ty-park-closed-for-season-hollywood (same address)",
    "the-boardwalk-at-hersheypark-hershey": "duplicate of hersheypark-hershey (same address)",
    "the-grove-resort-water-park-orlando-winter-garden": "duplicate of surfari-water-park-at-the-grove-resort-winter-garden (same address)",
    "tike-s-peak-orlando": "duplicate of teamboat-springs-orlando (same address)",
    "tomahawk-lake-sparta": "duplicate of tomahawk-lake-waterpark-sparta (same address)",
    "tropical-splash-currently-closed-lauderhill": "duplicate of central-broward-park-broward-county-stadium-lauderhill (same address)",
    "universal-orlando-resort-orlando": "duplicate of universal-islands-of-adventure-orlando (same address)",
    "universal-volcano-bay-orlando": "duplicate of universal-islands-of-adventure-orlando (same address)",
    "wake-zone-cable-park-oklahoma-city": "duplicate of lost-lakes-adventure-park-oklahoma-city (same address)",
    "warner-park-pool-splash-pad-chattanooga": "duplicate of warner-park-pool-chattanooga (same address)",
    "water-works-park-cuyahoga-falls": "duplicate of water-works-family-aquatic-center-cuyahoga-falls (same address)",
    "wave-pool-fairmont": "duplicate of east-marion-park-fairmont (same address)",
    "wedge-slides-waco": "duplicate of waco-surf-waco (same address)",
    "whatz-up-fun-park-seven-points": "duplicate of whatz-up-water-park-seven-points (same address)",
    "wildwater-adventure-muskegon": "duplicate of michigan-s-adventure-muskegon (same address)",
    "william-m-allen-park-wentzville": "duplicate of splash-station-aquatic-center-wentzville (same address)",
    "worlds-of-fun-kansas-city": "duplicate of oceans-of-fun-kansas-city (same address)",
})

# Dropped duplicates 301 to their kept twin instead of the generic state hub, so
# link equity and user intent land on the surviving page. Derived from the
# "duplicate of <slug>" reason strings above; build_redirects validates each
# target against the current build and falls back to the state hub if missing.
PAD_REDIRECT_OVERRIDES = {
    slug: "/pad/" + reason.split("duplicate of ", 1)[1].split(" ")[0]
    for slug, reason in PAD_EXCLUDE_SLUGS.items()
    if reason.startswith("duplicate of ")
}


# ── No-water-evidence removals (2026-06-09, Kevin's call) ──────────────────────
# Skeleton pads whose Google description shows a non-water venue and no source
# (name / Google desc / about-join / features) evidences water play — the
# "is a water play area" claim came only from the unreliable Airtable type field.
# Review artifact: data/no_water_removals_20260609_160732.txt (local)
PAD_EXCLUDE_SLUGS.update({
    "adventure-city-anaheim": "no water evidence in any source (skeleton fabrication risk)",
    "adventure-landing-gastonia-gastonia": "no water evidence in any source (skeleton fabrication risk)",
    "adventure-river-resort-eminence": "no water evidence in any source (skeleton fabrication risk)",
    "alley-pond-park-oakland-gardens": "no water evidence in any source (skeleton fabrication risk)",
    "andretti-thrill-park-melbourne": "no water evidence in any source (skeleton fabrication risk)",
    "armstrong-park-duncanville": "no water evidence in any source (skeleton fabrication risk)",
    "betti-stradling-park-coral-springs": "no water evidence in any source (skeleton fabrication risk)",
    "boomers-livermore-livermore": "no water evidence in any source (skeleton fabrication risk)",
    "boomers-modesto-modesto": "no water evidence in any source (skeleton fabrication risk)",
    "brooklyn-bridge-park-pier-5-brooklyn-heights": "no water evidence in any source (skeleton fabrication risk)",
    "brooklyn-heights-promenade-brooklyn": "no water evidence in any source (skeleton fabrication risk)",
    "bushkill-park-easton": "no water evidence in any source (skeleton fabrication risk)",
    "camden-park-huntington": "no water evidence in any source (skeleton fabrication risk)",
    "carolyn-crayton-park-macon": "no water evidence in any source (skeleton fabrication risk)",
    "carpenter-park-recreation-center-plano": "no water evidence in any source (skeleton fabrication risk)",
    "cascade-valley-metro-park-chuckery-area-akron": "no water evidence in any source (skeleton fabrication risk)",
    "cascade-valley-metro-park-schumacher-valley-area-akron": "no water evidence in any source (skeleton fabrication risk)",
    "centennial-park-davenport": "no water evidence in any source (skeleton fabrication risk)",
    "clemyjontri-park-mclean": "no water evidence in any source (skeleton fabrication risk)",
    "clove-lakes-park-staten-island": "no water evidence in any source (skeleton fabrication risk)",
    "columbus-park-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "conservatory-water-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "croton-gorge-park-croton-on-hudson": "no water evidence in any source (skeleton fabrication risk)",
    "cypress-park-coral-springs": "no water evidence in any source (skeleton fabrication risk)",
    "des-moines-water-works-park-des-moines": "no water evidence in any source (skeleton fabrication risk)",
    "discovery-green-houston": "no water evidence in any source (skeleton fabrication risk)",
    "doylestown-ymca-doylestown": "no water evidence in any source (skeleton fabrication risk)",
    "dumbo-archway-plaza-brooklyn": "no water evidence in any source (skeleton fabrication risk)",
    "durant-park-lansing": "no water evidence in any source (skeleton fabrication risk)",
    "edora-park-fort-collins": "no water evidence in any source (skeleton fabrication risk)",
    "elevated-acre-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "emerald-falls-family-recreation-center-panama-city": "no water evidence in any source (skeleton fabrication risk)",
    "empire-fulton-ferry-brooklyn": "no water evidence in any source (skeleton fabrication risk)",
    "falls-park-sioux-falls": "no water evidence in any source (skeleton fabrication risk)",
    "firefighter-s-memorial-park-union-city": "no water evidence in any source (skeleton fabrication risk)",
    "flat-fork-creek-park-fishers": "no water evidence in any source (skeleton fabrication risk)",
    "forest-park-woodhaven": "no water evidence in any source (skeleton fabrication risk)",
    "fossil-creek-park-fort-collins": "no water evidence in any source (skeleton fabrication risk)",
    "frankie-s-of-raleigh-raleigh": "no water evidence in any source (skeleton fabrication risk)",
    "franklin-d-roosevelt-four-freedoms-state-park-roosevelt-island": "no water evidence in any source (skeleton fabrication risk)",
    "frontier-park-st-charles": "no water evidence in any source (skeleton fabrication risk)",
    "fun-land-of-fredericksburg-fredericksburg": "no water evidence in any source (skeleton fabrication risk)",
    "fun-world-nashua": "no water evidence in any source (skeleton fabrication risk)",
    "funland-idaho-falls": "no water evidence in any source (skeleton fabrication risk)",
    "garlic-creek-park-buda": "no water evidence in any source (skeleton fabrication risk)",
    "grand-ferry-park-brooklyn": "no water evidence in any source (skeleton fabrication risk)",
    "great-river-park-east-hartford": "no water evidence in any source (skeleton fabrication risk)",
    "greenacre-park-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "haggard-park-plano": "no water evidence in any source (skeleton fabrication risk)",
    "huck-finn-s-playland-albany": "no water evidence in any source (skeleton fabrication risk)",
    "john-golden-park-bayside": "no water evidence in any source (skeleton fabrication risk)",
    "john-street-park-brooklyn": "no water evidence in any source (skeleton fabrication risk)",
    "kids-castle-central-park-doylestown": "no water evidence in any source (skeleton fabrication risk)",
    "kidstar-park-port-charlotte": "no water evidence in any source (skeleton fabrication risk)",
    "kreager-park-fort-wayne": "no water evidence in any source (skeleton fabrication risk)",
    "lake-benton-resort-lake-benton": "no water evidence in any source (skeleton fabrication risk)",
    "lakeside-park-fort-wayne": "no water evidence in any source (skeleton fabrication risk)",
    "legoland-r-discovery-center-arizona-tempe": "no water evidence in any source (skeleton fabrication risk)",
    "little-island-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "louis-valentino-jr-park-and-pier-brooklyn": "no water evidence in any source (skeleton fabrication risk)",
    "malibu-jack-s-lexington-lexington": "no water evidence in any source (skeleton fabrication risk)",
    "mel-s-funway-park-litchfield": "no water evidence in any source (skeleton fabrication risk)",
    "mill-river-park-stamford": "no water evidence in any source (skeleton fabrication risk)",
    "miramar-pineland-park-miramar": "no water evidence in any source (skeleton fabrication risk)",
    "monroeville-community-park-west-monroeville": "no water evidence in any source (skeleton fabrication risk)",
    "pacific-park-on-the-santa-monica-pier-santa-monica": "no water evidence in any source (skeleton fabrication risk)",
    "paradise-gardens-park-anaheim": "no water evidence in any source (skeleton fabrication risk)",
    "peace-valley-park-doylestown": "no water evidence in any source (skeleton fabrication risk)",
    "pictured-rocks-national-lakeshore-munising": "no water evidence in any source (skeleton fabrication risk)",
    "pier-1-playground-brooklyn": "no water evidence in any source (skeleton fabrication risk)",
    "pier-46-at-hudson-river-park-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "pier-84-at-hudson-river-park-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "pier-96-at-hudson-river-park-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "promenade-park-toledo": "no water evidence in any source (skeleton fabrication risk)",
    "prospect-playground-bronx": "no water evidence in any source (skeleton fabrication risk)",
    "quail-hollow-park-hartville": "no water evidence in any source (skeleton fabrication risk)",
    "rancho-san-rafael-regional-park-reno": "no water evidence in any source (skeleton fabrication risk)",
    "redbud-park-abilene": "no water evidence in any source (skeleton fabrication risk)",
    "revolution-cable-park-north-fort-myers": "no water evidence in any source (skeleton fabrication risk)",
    "richard-w-dekorte-park-lyndhurst": "no water evidence in any source (skeleton fabrication risk)",
    "richman-echo-park-bronx": "no water evidence in any source (skeleton fabrication risk)",
    "seaglass-carousel-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "solar-one-environmental-education-center-at-stuyvesant-cove-park-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "spring-canyon-park-fort-collins": "no water evidence in any source (skeleton fabrication risk)",
    "staten-island-funpark-staten-island": "no water evidence in any source (skeleton fabrication risk)",
    "storybook-land-egg-harbor-township": "no water evidence in any source (skeleton fabrication risk)",
    "sugarcreek-metropark-bellbrook": "no water evidence in any source (skeleton fabrication risk)",
    "super-silly-fun-land-studio-city": "no water evidence in any source (skeleton fabrication risk)",
    "sweetwater-wetlands-park-tucson": "no water evidence in any source (skeleton fabrication risk)",
    "the-battery-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "the-glen-resort-hoodsport": "no water evidence in any source (skeleton fabrication risk)",
    "the-water-works-in-buffalo-bayou-park-houston": "no water evidence in any source (skeleton fabrication risk)",
    "the-yards-park-washington": "no water evidence in any source (skeleton fabrication risk)",
    "theodore-roosevelt-park-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "thunder-road-of-sioux-falls-sioux-falls": "no water evidence in any source (skeleton fabrication risk)",
    "tonsler-recreation-center-charlottesville": "no water evidence in any source (skeleton fabrication risk)",
    "tropical-park-miami": "no water evidence in any source (skeleton fabrication risk)",
    "tweetsie-railroad-blowing-rock": "no water evidence in any source (skeleton fabrication risk)",
    "universal-islands-of-adventure-orlando": "no water evidence in any source (skeleton fabrication risk)",
    "virginia-highlands-park-arlington": "no water evidence in any source (skeleton fabrication risk)",
    "walden-ponds-wildlife-habitat-boulder": "no water evidence in any source (skeleton fabrication risk)",
    "walt-whitman-park-brooklyn": "no water evidence in any source (skeleton fabrication risk)",
    "wards-island-park-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "washington-market-park-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "waterfront-park-alexandria": "no water evidence in any source (skeleton fabrication risk)",
    "west-boynton-park-and-recreation-center-lake-worth-beach": "no water evidence in any source (skeleton fabrication risk)",
    "west-harlem-piers-new-york": "no water evidence in any source (skeleton fabrication risk)",
    "westwind-lakes-park-miami": "no water evidence in any source (skeleton fabrication risk)",
    "wildwood-park-harrisburg": "no water evidence in any source (skeleton fabrication risk)",
    "wnyc-transmitter-park-brooklyn": "no water evidence in any source (skeleton fabrication risk)",
    "wonderworks-destiny-syracuse": "no water evidence in any source (skeleton fabrication risk)",
})
