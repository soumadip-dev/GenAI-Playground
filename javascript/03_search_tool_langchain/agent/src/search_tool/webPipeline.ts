import { HumanMessage, SystemMessage } from '@langchain/core/messages';
import { RunnableLambda, RunnableSequence } from '@langchain/core/runnables';

import { createChatModel } from '../config/models.config';
import { fetchPageContent } from '../utils/fetch-page-content.utils';
import { searchWeb } from '../utils/search-web.utils';
import { summarize } from '../utils/summarize.utils';

import type { SearchWebResult } from '../schemas';
import type { Candidate } from './types';

//* Maximum number of web search results to retrieve and process.
const DEFAULT_TOP_RESULTS_COUNT = 5;

//* Runnable step to perform a web search query.
export const executeWebSearchStep = RunnableLambda.from(
  // Routing strategy that selects between web search and direct output.
  // Input shape: { q: string, mode: "web" | "direct" }
  async function (input: { q: string; mode: 'web' | 'direct' }) {
    // Call the searchWeb function to search the internet using Tavily.
    // The returned results array contains objects with the shape: { title, url, snippet }.
    const searchResults: SearchWebResult = await searchWeb(input.q);

    return {
      ...input,
      searchResults,
    };

    // Final return shape:
    // { q, mode, searchResults: Array<{ title, url, snippet }> }
  }
);

//* After getting the search results, open each URL, extract its content,
//* and then summarize the extracted content.
export const executeOpenAndSummarizeStep = RunnableLambda.from(async function (input: {
  q: string;
  mode: 'web' | 'direct';
  searchResults: SearchWebResult;
}) {
  // If there are no valid search results, return an empty summary list with a fallback status.
  if (!Array.isArray(input.searchResults) || input.searchResults.length === 0) {
    // { q, mode, searchResults, pageSummaries: [], fallback: 'no-results' }
    return {
      ...input,
      pageSummaries: [],
      fallback: 'no-results' as const,
    };
  }

  // Do not process all search results; select only the top 5 results.
  const topSearchResults = input.searchResults.slice(0, DEFAULT_TOP_RESULTS_COUNT);

  const settledResults = await Promise.allSettled(
    // Process each search result by opening its URL and summarizing the page content.
    topSearchResults.map(async searchResult => {
      // Open the URL and extract its content. Returns { url, content }.
      const openedPage = await fetchPageContent(searchResult.url);

      // Summarize the extracted page content.
      const pageSummary = await summarize(openedPage.content);

      return {
        url: openedPage.url,
        summary: pageSummary,
      };
    })
  );

  // Keep only successfully processed results.
  const successfulPageSummaries = settledResults
    .filter(result => result.status === 'fulfilled')
    .map(result => result.value);

  // Edge case: all page extraction and summarization attempts fail.
  if (successfulPageSummaries.length === 0) {
    const fallbackSnippetSummaries = topSearchResults
      .map(searchResult => ({
        url: searchResult.url,
        summary: String(searchResult.snippet || searchResult.title || '').trim(),
      }))
      .filter(result => result.summary.length > 0);

    return {
      ...input,
      pageSummaries: fallbackSnippetSummaries,
      fallback: 'snippets' as const,
    };
  }

  // Return { q, mode, searchResults, pageSummaries, fallback }.
  return {
    ...input,
    pageSummaries: successfulPageSummaries,
    fallback: 'none' as const,
  };
});

//* Compose the final answer using either the page summaries or a direct model response.
export const composeStep = RunnableLambda.from(async function (input: {
  q: string;
  pageSummaries: Array<{ url: string; summary: string }>;
  mode: 'web' | 'direct';
  fallback: 'none' | 'no-results' | 'snippets';
}): Promise<Candidate> {
  // Create the chat model used to generate the final answer.
  const model = createChatModel({ temperature: 0.2 });

  // If there are no page summaries, generate the answer directly from the user's question.
  if (!input.pageSummaries || input.pageSummaries.length === 0) {
    const response = await model.invoke([
      new SystemMessage(
        [
          'You are a helpful AI assistant that answers user questions clearly and concisely.',
          'Answer at a beginner-friendly level using simple and easy-to-understand language.',
          'If you are unsure about an answer, clearly state that you are unsure instead of making up information.',
          'Do not add unnecessary details or unrelated information.',
        ].join('\n')
      ),
      new HumanMessage(input.q),
    ]);

    // Convert the model response content into a string.
    const directAnswer =
      typeof response.content === 'string' ? response.content : String(response.content).trim();

    return {
      answer: directAnswer,
      sources: [],
      mode: 'direct',
    };
  }

  // Generate the final answer using the summarized web page content.
  const response = await model.invoke([
    new SystemMessage(
      [
        'You are a helpful AI assistant that answers questions using the provided web page summaries.',
        'Use only the information contained in the provided summaries.',
        'Do not invent, assume, or add facts that are not supported by the summaries.',
        'If the provided summaries do not contain enough information to answer the question, clearly say that the available information is insufficient.',
        'Give an accurate, neutral, and concise answer.',
        'Use simple language that is easy for beginners to understand.',
        'Keep the answer within 5-8 sentences unless additional detail is necessary for accuracy.',
      ].join('\n')
    ),
    new HumanMessage(
      [
        `Question: ${input.q}`,
        '',
        'Web Page Summaries:',
        JSON.stringify(input.pageSummaries, null, 2),
      ].join('\n')
    ),
  ]);

  // Convert the model response content into a string.
  const webAnswer =
    typeof response.content === 'string' ? response.content : String(response.content).trim();

  // Extract the source URLs from the page summaries.
  const sourceUrls = input.pageSummaries.map(pageSummary => pageSummary.url);

  return {
    answer: webAnswer,
    sources: sourceUrls,
    mode: 'web',
  };
});

export const webChain = RunnableSequence.from([
  executeWebSearchStep,
  executeOpenAndSummarizeStep,
  composeStep,
]);
