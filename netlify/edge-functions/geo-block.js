const ALLOWED_COUNTRIES = new Set([
  // Core audience
  'US', 'CA', 'GB', 'AU', 'NZ',
  // Western Europe (English-speaking expats planning US trips)
  'IE', 'DE', 'FR', 'NL', 'BE', 'LU', 'AT', 'CH',
  'DK', 'NO', 'SE', 'FI', 'IS',
  'IT', 'ES', 'PT', 'GR', 'MT', 'CY',
  // Central Europe
  'PL', 'CZ', 'SK', 'HU', 'SI', 'HR',
  // Other (US military/expat presence)
  'JP', 'IL', 'MX',
]);

const BOT_PATTERNS = [
  /googlebot/i, /bingbot/i, /slurp/i, /duckduckbot/i,
  /applebot/i, /facebookexternalhit/i, /twitterbot/i,
  /linkedinbot/i, /semrushbot/i, /ahrefsbot/i,
  /yandexbot/i, /petalbot/i, /bytespider/i,
  /gptbot/i, /claudebot/i, /amazonbot/i,
  /dotbot/i, /mj12bot/i,
];

export default async (request, context) => {
  const country = context.geo?.country?.code;
  const ua = request.headers.get('user-agent') || '';

  // Always allow known search engine and social media crawlers
  if (BOT_PATTERNS.some(pattern => pattern.test(ua))) {
    return;
  }

  // Allow traffic from approved countries (or if country is unknown)
  if (!country || ALLOWED_COUNTRIES.has(country)) {
    return;
  }

  // Block everything else with a 403
  return new Response('Access restricted to supported regions.', {
    status: 403,
    headers: { 'Content-Type': 'text/plain' },
  });
};

export const config = {
  path: "/*",
  excludedPath: [
    "/static/*",
    "/robots.txt",
    "/sitemap.xml",
    "/ads.txt",
    "/favicon.ico",
    "/_redirects",
  ],
};
