// Schema defines a contract between backend, AI model, and frontend

import { z } from 'zod';

export const WebSearchResultSchema = z.object({
  title: z.string().min(1),
  url: z.url(),
  snippet: z.string().optional().default(''),
});

// Limit the number of results to 10 for now
export const WebSearchResultsSchema = z.array(WebSearchResultSchema).max(10);

export type WebSearchResult = z.infer<typeof WebSearchResultsSchema>;
