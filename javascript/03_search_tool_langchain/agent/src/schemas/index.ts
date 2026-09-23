// Schema defines a contract between backend, AI model, and frontend

import { z } from 'zod';

export const SearchWebResultSchema = z.object({
  title: z.string().min(1),
  url: z.url(),
  snippet: z.string().optional().default(''),
});

// Limit the number of results to 10 for now
export const SearchWebResultsSchema = z.array(SearchWebResultSchema).max(10);

export type SearchWebResult = z.infer<typeof SearchWebResultsSchema>;

export const FetchPageContentInputSchema = z.object({
  url: z.url(),
});

export const FetchPageContentOutputSchema = z.object({
  url: z.url(),
  content: z.string().min(1),
});

export const SummarizeInputSchema = z.object({
  text: z.string().min(50, 'Input text must contain at least 50 characters.'),
});

export const SummarizeOutputSchema = z.object({
  summary: z.string().min(1, 'Summary content must not be empty.'),
});

export const searchInputSchema = z.object({
  query: z.string().min(5, 'Query must be at least 5 characters long.'),
});

export type SearchInput = z.infer<typeof searchInputSchema>;

export const searchOutputSchema = z.object({
  answer: z.string().min(1, 'Answer must not be empty.'),
  sources: z.array(z.url()).default([]),
});

export type SearchOutput = z.infer<typeof searchOutputSchema>;
