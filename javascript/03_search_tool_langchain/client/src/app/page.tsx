'use client';

import { useEffect, useRef, useState } from 'react';
import Link from 'next/link';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { API_URL } from '@/lib/config';

type SearchResponse = {
  answer: string;
  sources: string[];
};

type CurrentChatTurn =
  | { role: 'user'; content: string }
  | {
      role: 'assistant';
      content: string;
      sources: string[];
      time: number;
      error?: string;
    };

export default function Home() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [chat, setChat] = useState<CurrentChatTurn[]>([]);

  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: 'smooth',
    });
  }, [chat, loading]);

  async function runSearch(prompt: string) {
    setLoading(true);
    setChat(old => [...old, { role: 'user', content: prompt }]);

    const startTime = performance.now();

    try {
      const res = await fetch(`/api/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: prompt }),
      });

      const json = await res.json();
      const timeDiff = Math.round(performance.now() - startTime);

      if (!res.ok) {
        setChat(old => [
          ...old,
          {
            role: 'assistant',
            content: 'I tried to answer, but something went wrong. Please try again.',
            sources: [],
            time: timeDiff,
            error: 'Request failed',
          },
        ]);
        return;
      }

      const data = json as SearchResponse;

      setChat(old => [
        ...old,
        {
          role: 'assistant',
          content: data.answer,
          sources: data.sources,
          time: timeDiff,
        },
      ]);
    } catch {
      const timeDiff = Math.round(performance.now() - startTime);
      setChat(old => [
        ...old,
        {
          role: 'assistant',
          content: 'I tried to answer, but something went wrong. Please try again.',
          sources: [],
          time: timeDiff,
          error: 'Request failed',
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function handleChatSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const prompt = query.trim();
    if (!prompt || loading) return;
    setQuery('');
    await runSearch(prompt);
  }

  return (
    <div className="flex h-dvh flex-col bg-neutral-50 text-neutral-900">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-neutral-200 bg-white/95 backdrop-blur-sm">
        <div className="mx-auto flex max-w-3xl items-center justify-between px-5 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-md bg-neutral-900 text-sm font-semibold text-white shadow-sm">
              S
            </div>
            <div className="flex flex-col leading-tight">
              <span className="text-lg font-semibold tracking-tight">Search V1</span>
              <span className="text-xs text-neutral-500">LCEL Web Agent</span>
            </div>
          </div>

          <span className="hidden rounded-md border border-neutral-200 bg-neutral-50 px-3 py-1 text-xs font-medium text-neutral-500 sm:inline-block">
            answers with sources
          </span>
        </div>
      </header>

      {/* Main chat area */}
      <main ref={scrollRef} className="flex-1 overflow-y-auto px-5 py-8">
        <div className="mx-auto max-w-3xl space-y-6">
          {/* Empty state */}
          {chat.length === 0 && (
            <div className="flex flex-col items-center justify-center pt-12 text-center sm:pt-20">
              <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-lg border border-neutral-200 bg-white shadow-sm">
                <svg
                  className="h-6 w-6 text-neutral-700"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456Z"
                  />
                </svg>
              </div>

              <h1 className="mb-2 text-3xl font-semibold tracking-tight sm:text-4xl">
                Ask anything
              </h1>
              <p className="mb-8 max-w-md text-sm text-neutral-500">
                Get answers with sources. Some queries will browse the web, others won&apos;t.
              </p>

              <div className="grid w-full max-w-lg gap-3 sm:grid-cols-2">
                <button
                  type="button"
                  onClick={() => setQuery('Top 10 engineering colleges in India 2025')}
                  className="rounded-lg border border-neutral-200 bg-white p-4 text-left shadow-sm transition-all hover:border-neutral-300 hover:bg-neutral-50 hover:shadow"
                >
                  <span className="mb-1 block text-sm font-medium text-neutral-900">Research</span>
                  <span className="text-sm leading-snug text-neutral-500">
                    Top 10 engineering colleges in India 2025
                  </span>
                </button>

                <button
                  type="button"
                  onClick={() => setQuery('Explain what Docker is for beginners')}
                  className="rounded-lg border border-neutral-200 bg-white p-4 text-left shadow-sm transition-all hover:border-neutral-300 hover:bg-neutral-50 hover:shadow"
                >
                  <span className="mb-1 block text-sm font-medium text-neutral-900">Learn</span>
                  <span className="text-sm leading-snug text-neutral-500">
                    Explain what Docker is for beginners
                  </span>
                </button>
              </div>
            </div>
          )}

          {/* Chat messages */}
          {chat.map((turn, idx) => {
            if (turn.role === 'user') {
              return (
                <div key={idx} className="flex justify-end">
                  <div className="max-w-[85%] rounded-lg bg-neutral-900 px-4 py-3 text-sm leading-relaxed text-white shadow-sm">
                    <div className="whitespace-pre-wrap break-words">{turn.content}</div>
                  </div>
                </div>
              );
            }

            return (
              <div key={idx} className="flex items-start gap-3">
                <div className="flex h-8 w-8 flex-none items-center justify-center rounded-md border border-neutral-200 bg-white text-xs font-semibold text-neutral-700 shadow-sm">
                  AI
                </div>

                <div className="flex-1 space-y-3">
                  <div className="inline-block max-w-full whitespace-pre-wrap break-words rounded-lg border border-neutral-200 bg-white px-4 py-3 text-sm leading-relaxed shadow-sm">
                    {turn.content}
                  </div>

                  <div className="flex flex-wrap items-center gap-x-4 text-xs text-neutral-400">
                    <span className="flex items-center gap-1.5">
                      <svg
                        className="h-3.5 w-3.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={2}
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                        />
                      </svg>
                      {turn.time} ms
                    </span>

                    {turn.error && (
                      <span className="flex items-center gap-1.5 text-red-500">
                        <svg
                          className="h-3.5 w-3.5"
                          fill="none"
                          viewBox="0 0 24 24"
                          strokeWidth={2}
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"
                          />
                        </svg>
                        {turn.error}
                      </span>
                    )}
                  </div>

                  {turn.sources.length > 0 && (
                    <div className="overflow-hidden rounded-lg border border-neutral-200 bg-white shadow-sm">
                      <div className="flex items-center gap-2 border-b border-neutral-200 bg-neutral-50 px-3.5 py-2.5">
                        <svg
                          className="h-3.5 w-3.5 text-neutral-400"
                          fill="none"
                          viewBox="0 0 24 24"
                          strokeWidth={2}
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244"
                          />
                        </svg>
                        <span className="text-xs font-medium text-neutral-500">Sources</span>
                      </div>

                      <ul className="divide-y divide-neutral-100">
                        {turn.sources.map((source, sourceIdx) => (
                          <li key={sourceIdx}>
                            <Link
                              href={source}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex items-center gap-2.5 px-3.5 py-2.5 text-xs text-neutral-500 transition-colors hover:bg-neutral-50 hover:text-neutral-900"
                            >
                              <span className="flex h-5 w-5 flex-none items-center justify-center rounded border border-neutral-200 bg-neutral-50 text-[11px] text-neutral-600">
                                {sourceIdx + 1}
                              </span>
                              <span className="truncate break-all">{source}</span>
                            </Link>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            );
          })}

          {/* Loading indicator */}
          {loading && (
            <div className="flex items-start gap-3">
              <div className="flex h-8 w-8 flex-none items-center justify-center rounded-md border border-neutral-200 bg-white text-xs font-semibold text-neutral-700 shadow-sm">
                AI
              </div>

              <div className="inline-flex items-center gap-2.5 rounded-lg border border-neutral-200 bg-white px-4 py-3 shadow-sm">
                <span className="flex gap-1.5">
                  <span className="h-2 w-2 animate-bounce rounded-full bg-neutral-300 [animation-delay:-0.3s]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-neutral-300 [animation-delay:-0.15s]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-neutral-300" />
                </span>
                <span className="text-sm text-neutral-400">Thinking…</span>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="sticky bottom-0 z-10 border-t border-neutral-200 bg-white/95 backdrop-blur-sm">
        <div className="mx-auto max-w-3xl px-5 py-4">
          <form onSubmit={handleChatSubmit} className="flex items-center gap-2.5">
            <div className="relative flex-1">
              <Input
                className="h-11 w-full rounded-lg border-neutral-200 bg-white pl-4 pr-10 text-sm placeholder:text-neutral-400 shadow-sm focus:border-neutral-400 focus:ring-2 focus:ring-neutral-100"
                placeholder="Write your query here…"
                value={query}
                onChange={event => setQuery(event.target.value)}
                disabled={loading}
              />
              <svg
                className="pointer-events-none absolute right-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-400"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
                />
              </svg>
            </div>

            <Button
              className="h-11 shrink-0 rounded-lg bg-neutral-900 px-5 text-sm font-medium text-white shadow-sm transition-colors hover:bg-neutral-800 disabled:opacity-40 disabled:cursor-not-allowed"
              disabled={loading || query.trim().length < 5}
              type="submit"
            >
              {loading ? (
                <span className="flex items-center gap-1.5 text-sm">
                  <svg className="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  <span className="hidden sm:inline">Sending…</span>
                </span>
              ) : (
                <span className="flex items-center gap-1.5 text-sm">
                  <span className="hidden sm:inline">Send</span>
                  <svg
                    className="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth={2}
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5"
                    />
                  </svg>
                </span>
              )}
            </Button>
          </form>

          <p className="mt-2.5 text-center text-xs text-neutral-400">
            AI can make mistakes — verify important information.
          </p>
        </div>
      </footer>
    </div>
  );
}
