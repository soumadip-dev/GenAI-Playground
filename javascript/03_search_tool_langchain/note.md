# Search Web Feature

These three utility files work together as a pipeline:

```text
User Query
      ↓
search-web.utils.ts
      ↓
Search Results (title, url, snippet)
      ↓
fetch-page-content.utils.ts
      ↓
Clean Plain Text
      ↓
summarize.utils.ts
      ↓
Final Summary
```

---

# search-web.utils.ts

This file is responsible for searching the internet. It **does not fetch the content of websites**. Instead, it sends the user's query to the **Tavily Search API** and returns the top search results.

### Steps

1. Validate the search query.
   - If the query is empty, return an empty array.
   - Check whether `TAVILY_API_KEY` exists.

2. Send a `POST` request to the Tavily Search API with a request body similar to:

```json
{
  "query": "What is React?",
  "search_depth": "basic",
  "max_results": 5,
  "include_answer": false,
  "include_images": false
}
```

3. Tavily returns search results containing fields such as:

```json
[
  {
    "title": "React",
    "url": "https://react.dev",
    "content": "React is a JavaScript library for building user interfaces..."
  },
  {
    "title": "React - Wikipedia",
    "url": "https://en.wikipedia.org/wiki/React_(software)",
    "content": "React is a free and open-source front-end JavaScript library..."
  }
]
```

4. The utility normalizes Tavily's response by mapping:

```text
content → snippet
```

Result:

```ts
[
  {
    title: 'React',
    url: 'https://react.dev',
    snippet: 'React is a JavaScript library for building user interfaces...',
  },
  {
    title: 'React - Wikipedia',
    url: 'https://en.wikipedia.org/wiki/React_(software)',
    snippet: 'React is a free and open-source front-end JavaScript library...',
  },
];
```

5. Each result is validated using **Zod** before being returned.

> **Note:** Although each result contains `title`, `url`, and `snippet`, in the current pipeline only the **URL** is used by the next utility (`fetch-page-content.utils.ts`). The `title` and `snippet` are useful for displaying search results or helping choose the most relevant page.

---

# fetch-page-content.utils.ts

Now that we have a URL from `search-web.utils.ts`, this utility fetches the **actual webpage content** and converts it into clean plain text.

### Steps

1. Validate and normalize the URL.
   - Only `http` and `https` URLs are allowed.

2. Fetch the webpage using `fetch()` with a custom `User-Agent`.

3. If the request succeeds:
   - Read the HTML.
   - Use **html-to-text** to convert HTML into plain text.
   - Skip unnecessary elements such as:
     - `nav`
     - `header`
     - `footer`
     - `script`
     - `style`
     - `aside`

4. Normalize whitespace by replacing multiple spaces and line breaks with a single space.

5. Limit the output to **8000 characters** to reduce token usage.

6. Validate the final output using **Zod** and return:

```ts
{
  url: "...",
  content: "..."
}
```

---

# summarize.utils.ts

Now we have a large block of plain text. Instead of returning the entire content to the user, this utility asks an LLM to generate a concise summary.

### Steps

1. Validate the input using **Zod**.

2. Truncate the input text to **2000 characters** before sending it to the model to reduce token usage and improve response time.

3. Create a chat model with a low temperature (`0.2`) to produce more factual and consistent summaries.

4. Send:
   - A **System Message** containing summarization rules.
   - A **Human Message** containing the webpage content.

5. The model generates a summary of approximately **5–8 sentences**.

6. Normalize whitespace and limit the summary to **2500 characters**.

7. Validate the final output using **Zod** and return:

```ts
{
  summary: '...';
}
```

# routeStratigy.ts

- this function check if the query is web(need to go to the web) or direct(need to go to the model)
- it check if the query is long or contains recent year or Heuristic patterns
- and return accordingly web or direct
