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
  // Input shape: { query: string, mode: "web" | "direct" }
  async function (input: { query: string; mode: 'web' | 'direct' }) {
    // Call the searchWeb function to search the internet using Tavily.
    // The returned results array contains objects with the shape: { title, url, snippet }.
    const searchResults: SearchWebResult = await searchWeb(input.query);

    return {
      ...input,
      searchResults,
    };

    // Final return shape:
    // { query, mode, searchResults: Array<{ title, url, snippet }> }
  }
);

//* After getting the search results, open each URL, extract its content,
//* and then summarize the extracted content.
export const executeOpenAndSummarizeStep = RunnableLambda.from(async function (input: {
  query: string;
  mode: 'web' | 'direct';
  searchResults: SearchWebResult;
}) {
  // If there are no valid search results, return an empty summary list with a fallback status.
  if (!Array.isArray(input.searchResults) || input.searchResults.length === 0) {
    // { query, mode, searchResults, pageSummaries: [], fallback: 'no-results' }
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

  // Return { query, mode, searchResults, pageSummaries, fallback }.
  return {
    ...input,
    pageSummaries: successfulPageSummaries,
    fallback: 'none' as const,
  };
});

//* Compose the final answer using either the page summaries or a direct model response.
export const composeStep = RunnableLambda.from(async function (input: {
  query: string;
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
      new HumanMessage(input.query),
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
        '',
        'SOURCE USAGE:',
        'Use only information supported by the provided summaries.',
        'Do not invent, assume, or add unsupported facts.',
        'You may combine relevant information from multiple summaries into one coherent answer.',
        'If the summaries do not contain enough information to answer the question, clearly state that the available information is insufficient.',
        '',
        'FINAL ANSWER STYLE:',
        'Answer the user directly instead of describing what the sources say.',
        'Transform information from the summaries into a natural, self-contained answer.',
        'Never copy source-introduction or source-attribution wording into the final answer.',
        'Do not mention web pages, websites, articles, guides, rankings, sources, summaries, or publications unless the user explicitly asks for them.',
        'Do not use phrases such as "according to", "the guide says", "the article says", "the website states", "the source states", "as reported by", "the ranking says", or similar source-referencing phrases.',
        'Do not mention the name of a ranking or publication merely because it appears in the summaries.',
        'Do not say that an institution, product, or option is "best" unless the provided information explicitly supports that conclusion.',
        'Present the relevant facts directly and naturally.',
        '',
        'STRUCTURE:',
        'Start with a direct answer to the question.',
        'For questions asking for multiple items, use a numbered list or bullet list.',
        'Include important supporting details only when they are relevant to the question.',
        'Do not repeat the same information in different forms.',
        'Use simple language that is easy for beginners to understand.',
        'Keep the answer concise while providing enough detail to answer the question properly.',
        '',
        'ACCURACY:',
        'Do not turn a ranking from one source into a universal or objective "best" list.',
        'If the summaries provide a specific ranking, you may present the ranked institutions as a ranking, but do not mention the ranking source unless explicitly requested.',
        'If the summaries contain different rankings or conflicting information, present the difference clearly and neutrally.',
      ].join('\\n')
    ),
    new HumanMessage(
      [
        `Question: ${input.query}`,
        '',
        'Web Page Summaries:',
        JSON.stringify(input.pageSummaries, null, 2),
      ].join('\\n')
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

export const webPipeline = RunnableSequence.from([
  executeWebSearchStep,
  executeOpenAndSummarizeStep,
  composeStep,
]);
