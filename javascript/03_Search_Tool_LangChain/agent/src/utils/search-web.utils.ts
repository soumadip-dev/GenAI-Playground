/**
 * Internet search utility.
 *
 * Accepts a natural language query and returns a normalized array of:
 * { title, url, snippet }
 *
 * Uses Tavily as the underlying search provider.
 */

import { env } from '../config/env.config';
import { SearchWebResultSchema, SearchWebResultsSchema } from '../schemas/index';

//* Performs a web search and returns normalized search results.
export async function searchWeb(query: string) {
  const searchQuery = (query ?? '').trim();

  if (!searchQuery) {
    return [];
  }

  return searchWithTavily(searchQuery);
}

//* Executes a search request using Tavily.
async function searchWithTavily(query: string) {
  if (!env.TAVILY_API_KEY) {
    throw new Error('TAVILY_API_KEY is missing');
  }

  const response = await fetch('https://api.tavily.com/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${env.TAVILY_API_KEY}`,
    },
    body: JSON.stringify({
      query,
      search_depth: 'basic',
      max_results: 5,
      include_answer: false,
      include_images: false,
    }),
  });

  if (!response.ok) {
    const errorMessage = await getResponseBodySafely(response);

    throw new Error(`Tavily request failed (${response.status}): ${errorMessage}`);
  }

  const responseBody = await response.json();
  const searchResults = Array.isArray(responseBody?.results) ? responseBody.results : [];

  const normalizedResults = searchResults.slice(0, 5).map((result: any) =>
    SearchWebResultSchema.parse({
      title: String(result?.title ?? '').trim() || 'Untitled',
      url: String(result?.url ?? '').trim(),
      snippet: String(result?.content ?? '')
        .trim()
        .slice(0, 220),
    })
  );

  return SearchWebResultsSchema.parse(normalizedResults);
}

//* Safely extracts the response body for error reporting.
async function getResponseBodySafely(response: Response) {
  try {
    return await response.text();
  } catch {
    return '<empty response body>';
  }
}
