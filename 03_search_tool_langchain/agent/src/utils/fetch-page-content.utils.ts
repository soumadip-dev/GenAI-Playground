// Fetch and sanitize web page content for LLM consumption.
//
// The model itself cannot browse the web. This utility acts as a controlled
// browser layer that decides which content is safe and relevant to expose.
//
// It fetches the page, removes unnecessary elements, converts HTML to plain
// text, normalizes whitespace, and limits the final output size.

import { convert } from 'html-to-text';
import { FetchPageContentOutputSchema } from '../schemas';

export async function fetchPageContent(url: string) {
  // Step 1: Validate and normalize the URL.
  const normalizedUrl = validateAndNormalizeUrl(url);

  // Step 2: Fetch the page manually.
  // Some websites block generic Node.js requests, so we send
  // a custom User-Agent to avoid unnecessary 403 responses.
  const response = await fetch(normalizedUrl, {
    headers: {
      'User-Agent': 'agent-core/1.0 (+course-demo)',
    },
  });

  if (!response.ok) {
    const errorBody = await getResponseBodySafely(response);

    throw new Error(`Failed to fetch ${normalizedUrl}: ${errorBody.slice(0, 100)}`);
  }

  // Step 3: Determine the response content type.
  const contentType = response.headers.get('content-type') ?? '';

  // Read the raw response body.
  const rawContent = await response.text();

  // Step 4: Convert HTML to plain text and remove irrelevant sections.
  const plainText = contentType.includes('text/html')
    ? convert(rawContent, {
        wordwrap: false,
        selectors: [
          { selector: 'nav', format: 'skip' },
          { selector: 'header', format: 'skip' },
          { selector: 'footer', format: 'skip' },
          { selector: 'script', format: 'skip' },
          { selector: 'style', format: 'skip' },
          { selector: 'aside', format: 'skip' },
        ],
      })
    : rawContent;

  // Step 5: Normalize whitespace.
  const cleanedText = collapseWhitespace(plainText);

  // Step 6: Limit the output size to prevent excessive token usage.
  const truncatedText = cleanedText.slice(0, 8000);

  // Step 7: Return the normalized output 
  return FetchPageContentOutputSchema.parse({
    url: normalizedUrl,
    content: truncatedText,
  });
}

//* Validates the URL and ensures only HTTP(S) protocols are allowed.
function validateAndNormalizeUrl(url: string): string {
  try {
    const parsedUrl = new URL(url);

    if (!/^https?:$/.test(parsedUrl.protocol)) {
      throw new Error('Only HTTP(S) URLs are supported');
    }

    return parsedUrl.toString();
  } catch {
    throw new Error(`Invalid URL: ${url}`);
  }
}

//* Safely extracts the response body for error reporting.
async function getResponseBodySafely(response: Response) {
  try {
    return await response.text();
  } catch {
    return '<empty response body>';
  }
}

//* Replaces consecutive whitespace characters with a single space.
function collapseWhitespace(text: string): string {
  return text.replace(/\s+/g, ' ').trim();
}
