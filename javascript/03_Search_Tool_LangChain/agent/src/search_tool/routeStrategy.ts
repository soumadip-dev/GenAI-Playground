//* Determines the route for the search query.
export function routeStrategy(query: string): 'web' | 'direct' {
  const normalizedQuery = query.toLowerCase().trim();

  // Use the web route for lengthy queries, which often require external context.
  const isLongQuery = normalizedQuery.length > 70;

  // Detect explicit references to recent years that may require up-to-date information.
  const recentYearPattern = /\b20(2[4-9]|3[0-9])\b/;

  const containsRecentYear = recentYearPattern.test(normalizedQuery);

  // Heuristic patterns used to identify queries that are likely to benefit from web search.
  const webSearchPatterns: RegExp[] = [
    // Rankings and comparisons
    /\btop[-\s]*\d+\b/u,
    /\bbest\b/u,
    /\brank(?:ing|ings)?\b/u,
    /\bwhich\s+is\s+better\b/u,
    /\b(?:vs\.?|versus)\b/u,
    /\b(compare|comparison)\b/u,

    // Pricing and affordability
    /\b(price|prices|pricing|cost|costs|cheapest|cheaper|affordable)\b/u,
    /\bunder\s*\d+(?:\s*[kK])?\b/u,
    /\p{Sc}\s*\d+/u,

    // Recent and time-sensitive information
    /\b(latest|today|now|current)\b/u,
    /\b(news|breaking|trending)\b/u,
    /\b(released?|launch|launched|announce|announced|update|updated)\b/u,
    /\b(changelog|release\s*notes?)\b/u,

    // Product lifecycle
    /\b(deprecated|eol|end\s*of\s*life|sunset)\b/u,
    /\broadmap\b/u,

    // Compatibility and installation
    /\bworks\s+with\b/u,
    /\bcompatible\s+with\b/u,
    /\bsupport(?:ed)?\s+on\b/u,
    /\binstall(ation)?\b/u,

    // Local search
    /\bnear\s+me\b/u,
    /\bnearby\b/u,

    // Reviews and recommendations
    /\breview(?:s)?\b/u,
    /\brating(?:s)?\b/u,
    /\brecommend(?:ed|ation)?s?\b/u,

    // Availability and release dates
    /\bavailability\b/u,
    /\bavailable\b/u,
    /\bwhen\s+(?:is|was)\b/u,

    // Versions
    /\bv\d+(?:\.\d+)*\b/u,
    /\bversion\b/u,

    // Documentation and APIs
    /\bdocs?\b/u,
    /\bdocumentation\b/u,
    /\bapi\b/u,

    // Downloads and setup
    /\bdownload\b/u,
    /\bsetup\b/u,
    /\bgetting\s+started\b/u,

    // Tutorials and examples
    /\bhow\s+to\b/u,
    /\bguide\b/u,
    /\bexample(?:s)?\b/u,
    /\btutorial\b/u,

    // Company information
    /\bceo\b/u,
    /\bfounder\b/u,
    /\bheadquarters\b/u,
    /\bcompany\b/u,

    // Status and incidents
    /\boutage\b/u,
    /\bstatus\b/u,
    /\bissue(?:s)?\b/u,
    /\bknown\s+issues?\b/u,

    // Financial and market data
    /\bstock\b/u,
    /\bmarket\s+cap\b/u,
    /\bshare\s+price\b/u,

    // Events and conferences
    /\bconference\b/u,
    /\bwwdc\b/u,
    /\bgoogle\s+i\/o\b/u,
    /\bevent\b/u,

    // Developer ecosystem
    /\bgithub\b/u,
    /\bstackoverflow\b/u,
    /\breddit\b/u,
    /\bnpm\b/u,
    /\bpackage\b/u,
    /\bdependency\b/u,
    /\bplugin\b/u,
    /\bextension\b/u,
    /\bframework\b/u,
    /\blibrary\b/u,
  ];

  const matchesWebSearchPattern = webSearchPatterns.some(pattern => pattern.test(normalizedQuery));

  if (isLongQuery || containsRecentYear || matchesWebSearchPattern) {
    return 'web';
  } else {
    return 'direct';
  }
}
