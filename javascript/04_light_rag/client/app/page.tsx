'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { Textarea } from '@/components/ui/textarea';
import { useState } from 'react';

type Source = {
  source: string;
  chunkId: number;
};

type QueryResponse = {
  answer: string;
  sources: Source[];
};

type IngestResponse = {
  docCount?: number;
  chunkCount?: number;
  source?: string;
  [key: string]: unknown;
};

type ApiErrorResponse = {
  success: false;
  error: string;
  details?: unknown;
};

export default function Home() {
  // Indexing state
  const [ingestText, setIngestText] = useState('');
  const [ingestSource, setIngestSource] = useState('');
  const [ingestLoading, setIngestLoading] = useState(false);
  const [ingestMsg, setIngestMsg] = useState<string | null>(null);
  const [ingestError, setIngestError] = useState<string | null>(null);

  // Query state
  const [question, setQuestion] = useState('');
  const [askLoading, setAskLoading] = useState(false);
  const [askError, setAskError] = useState<string | null>(null);
  const [answerData, setAnswerData] = useState<QueryResponse | null>(null);
  const [queryTime, setQueryTime] = useState<number | null>(null);
  const [showSources, setShowSources] = useState(true);

  // Reset state
  const [resetLoading, setResetLoading] = useState(false);
  const [resetMsg, setResetMsg] = useState<string | null>(null);

  /**
   * Ingest text into the knowledge base.
   *
   * POST /api/knowledge-base/ingest
   */
  async function handleIngest(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!ingestText.trim()) {
      setIngestError('Please enter some text to ingest.');
      setIngestMsg(null);
      return;
    }

    setIngestLoading(true);
    setIngestError(null);
    setIngestMsg(null);

    try {
      const response = await fetch('/api/ingest', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: ingestText,
          source: ingestSource.trim() || undefined,
        }),
      });

      const result = (await response.json()) as
        | {
            success: true;
            data: IngestResponse;
          }
        | ApiErrorResponse;

      if (!response.ok || !result.success) {
        throw new Error('Failed to ingest the text.');
      }

      setIngestMsg('Text successfully added to the knowledge base.');
      setIngestText('');
      setIngestSource('');
    } catch (error) {
      setIngestError(
        error instanceof Error ? error.message : 'Something went wrong while ingesting the text.'
      );
    } finally {
      setIngestLoading(false);
    }
  }

  /**
   * Query the knowledge base.
   *
   * POST /api/knowledge-base/query
   */
  async function handleAsk(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const normalizedQuestion = question.trim();

    if (normalizedQuestion.length < 3) {
      setAskError('Query must be at least 3 characters long.');
      return;
    }

    setAskLoading(true);
    setAskError(null);
    setAnswerData(null);
    setQueryTime(null);

    const startTime = performance.now();

    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: normalizedQuestion,
        }),
      });

      const result = (await response.json()) as
        | {
            success: true;
            data: QueryResponse;
          }
        | ApiErrorResponse;

      if (!response.ok || !result.success) {
        throw new Error('Failed to query the knowledge base.');
      }

      setAnswerData(result.data);
      setQueryTime(Math.round(performance.now() - startTime));
    } catch (error) {
      setAskError(
        error instanceof Error ? error.message : 'Something went wrong while querying the KB.'
      );
    } finally {
      setAskLoading(false);
    }
  }

  /**
   * Clear the knowledge base.
   *
   * POST /api/knowledge-base/reset
   */
  async function handleReset() {
    const confirmed = window.confirm('Are you sure you want to clear the entire knowledge base?');

    if (!confirmed) {
      return;
    }

    setResetLoading(true);
    setResetMsg(null);
    setIngestError(null);
    setAskError(null);

    try {
      const response = await fetch('/api/reset', {
        method: 'POST',
      });

      const result = (await response.json()) as
        | {
            success: true;
            message: string;
          }
        | ApiErrorResponse;

      if (!response.ok || !result.success) {
        throw new Error('Failed to reset the knowledge base.');
      }

      setResetMsg(result.message);
      setAnswerData(null);
      setQuestion('');
    } catch (error) {
      setResetMsg(
        error instanceof Error ? error.message : 'Something went wrong while resetting the KB.'
      );
    } finally {
      setResetLoading(false);
    }
  }

  function clearIngestForm() {
    setIngestText('');
    setIngestSource('');
    setIngestMsg(null);
    setIngestError(null);
  }

  return (
    <main className="min-h-screen px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-6xl space-y-8">
        {/* Header */}
        <header className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
          <div className="space-y-2">
            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">Knowledge Base</h1>

            <p className="max-w-2xl text-sm leading-6 text-muted-foreground sm:text-base">
              Light RAG Demo. Add your own documents, then ask questions. The model answers using
              only the content you have ingested.
            </p>
          </div>

          <Button type="button" variant="destructive" onClick={handleReset} disabled={resetLoading}>
            {resetLoading ? 'Resetting...' : 'Reset Knowledge Base'}
          </Button>
        </header>

        {resetMsg && (
          <div className="rounded-md border px-4 py-3 text-sm text-muted-foreground">
            {resetMsg}
          </div>
        )}

        {/* Main Content */}
        <section className="grid gap-6 lg:grid-cols-2">
          {/* Ingest */}
          <Card className="h-fit">
            <CardHeader className="border-b">
              <CardTitle>Add to Knowledge Base</CardTitle>
            </CardHeader>

            <CardContent className="pt-6">
              <form onSubmit={handleIngest} className="space-y-5">
                <div className="space-y-2">
                  <label htmlFor="source" className="text-sm font-medium leading-none">
                    Source Label
                  </label>

                  <Input
                    id="source"
                    value={ingestSource}
                    onChange={event => setIngestSource(event.target.value)}
                    placeholder="e.g. onboarding-guide.md"
                    disabled={ingestLoading}
                  />
                </div>

                <div className="space-y-2">
                  <label htmlFor="ingest-text" className="text-sm font-medium leading-none">
                    Text / Markdown
                  </label>

                  <Textarea
                    id="ingest-text"
                    value={ingestText}
                    onChange={event => setIngestText(event.target.value)}
                    placeholder="Paste docs, policy text or onboarding notes..."
                    className="min-h-56 resize-y"
                    disabled={ingestLoading}
                  />
                </div>

                {ingestError && (
                  <p className="rounded-md border border-destructive/30 bg-destructive/5 px-3 py-2 text-sm text-destructive">
                    {ingestError}
                  </p>
                )}

                {ingestMsg && (
                  <p className="rounded-md border px-3 py-2 text-sm text-muted-foreground">
                    {ingestMsg}
                  </p>
                )}

                <div className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={clearIngestForm}
                    disabled={ingestLoading}
                  >
                    Clear
                  </Button>

                  <Button type="submit" disabled={ingestLoading}>
                    {ingestLoading ? 'Ingesting...' : 'Ingest to KB'}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>

          {/* Ask */}
          <Card className="h-fit">
            <CardHeader className="border-b">
              <CardTitle>Ask Your Knowledge Base</CardTitle>
            </CardHeader>

            <CardContent className="space-y-6 pt-6">
              <form onSubmit={handleAsk} className="space-y-5">
                <div className="space-y-2">
                  <label htmlFor="question" className="text-sm font-medium leading-none">
                    Your Query
                  </label>

                  <Input
                    id="question"
                    value={question}
                    onChange={event => setQuestion(event.target.value)}
                    placeholder="Ask something about your documents..."
                    disabled={askLoading}
                  />
                </div>

                <p className="text-xs leading-5 text-muted-foreground">
                  The backend retrieves relevant chunks from the knowledge base, compresses them,
                  and generates an answer using Gemini.
                </p>

                {askError && (
                  <p className="rounded-md border border-destructive/30 bg-destructive/5 px-3 py-2 text-sm text-destructive">
                    {askError}
                  </p>
                )}

                <Button type="submit" className="w-full sm:w-auto" disabled={askLoading}>
                  {askLoading ? 'Searching...' : 'Ask KB'}
                </Button>
              </form>

              {/* Answer */}
              {answerData && (
                <div className="space-y-5">
                  <Separator />

                  <div className="space-y-3">
                    <div className="flex items-center justify-between gap-4">
                      <h2 className="text-sm font-semibold">Answer</h2>

                      {queryTime !== null && (
                        <span className="text-xs text-muted-foreground">{queryTime} ms</span>
                      )}
                    </div>

                    <div className="rounded-lg border p-4 text-sm leading-7 whitespace-pre-wrap">
                      {answerData.answer}
                    </div>
                  </div>

                  {/* Sources */}
                  {answerData.sources.length > 0 && (
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <h2 className="text-sm font-semibold">
                          Sources ({answerData.sources.length})
                        </h2>

                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => setShowSources(previous => !previous)}
                        >
                          {showSources ? 'Hide' : 'Show'}
                        </Button>
                      </div>

                      {showSources && (
                        <div className="space-y-2">
                          {answerData.sources.map((source, index) => (
                            <div
                              key={`${source.source}-${source.chunkId}-${index}`}
                              className="flex items-center justify-between gap-4 rounded-md border px-3 py-3"
                            >
                              <span className="min-w-0 truncate text-sm">{source.source}</span>

                              <span className="shrink-0 rounded-md border px-2 py-1 text-xs text-muted-foreground">
                                #{source.chunkId}
                              </span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {answerData.sources.length === 0 && (
                    <p className="text-xs text-muted-foreground">
                      No sources were returned for this query.
                    </p>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </section>
      </div>
    </main>
  );
}
