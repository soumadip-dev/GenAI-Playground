'use client';

import { SubmitEvent, useRef, useState } from 'react';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

type Answer = {
  summary: string;
  confidence: number;
};

export default function Home() {
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [query, setQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const formRef = useRef<HTMLFormElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleQuerySubmit(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault();

    const question = query.trim();

    if (!question || loading) return;

    setLoading(true);
    try {
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: question }),
      });

      if (!res.ok) {
        throw new Error('Request Failed');
      }

      const { data } = await res.json();

      const { summary, confidence } = data as Answer;

      setAnswers(prevAnswers => [{ summary, confidence }, ...prevAnswers]);
      setQuery('');

      inputRef.current?.focus();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-dvh w-full overflow-hidden bg-linear-to-br from-zinc-100 via-white to-zinc-200">
      <div className="mx-auto flex h-dvh w-full max-w-2xl flex-col overflow-hidden px-4 pb-32 pt-12">
        <header className="mb-8">
          <h1 className="text-3xl font-semibold tracking-tight text-zinc-900">Hello Agent</h1>
          <p className="mt-1 text-sm text-zinc-500">Ask anything and get instant responses</p>
        </header>

        <Card className="flex flex-1 flex-col overflow-hidden rounded-2xl border border-zinc-200/60 bg-white/70 shadow-lg backdrop-blur-xl">
          <CardHeader className="border-b border-zinc-100 bg-white/40">
            <CardTitle className="text-sm font-semibold tracking-wide text-zinc-700">
              Answers
            </CardTitle>
          </CardHeader>

          <CardContent className="flex-1 space-y-4 overflow-y-auto p-5">
            {answers.length === 0 ? (
              <div className="flex h-44 items-center justify-center rounded-xl border border-dashed border-zinc-300 bg-zinc-50">
                <p className="text-sm text-zinc-500">No answers yet. Ask a question below</p>
              </div>
            ) : (
              answers.map((answer, index) => (
                <div
                  key={index}
                  className="group rounded-2xl border border-zinc-200/70 bg-white/80 p-5 shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md"
                >
                  <div className="text-sm leading-6 text-zinc-900">{answer.summary}</div>

                  <div className="mt-3 flex items-center justify-between">
                    <div className="text-xs text-zinc-500">Confidence</div>

                    <div className="flex items-center gap-3">
                      <div className="h-1.5 w-28 overflow-hidden rounded-full bg-zinc-100">
                        <div
                          className="h-full rounded-full bg-linear-to-r from-zinc-700 to-zinc-900 transition-all"
                          style={{ width: `${answer.confidence * 100}%` }}
                        />
                      </div>
                      <span className="text-xs font-medium text-zinc-700 tabular-nums">
                        {answer.confidence.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              ))
            )}
          </CardContent>
        </Card>

        <form
          className="fixed inset-x-0 bottom-0 border-t border-zinc-200/60 bg-white/70 backdrop-blur-xl"
          ref={formRef}
          onSubmit={handleQuerySubmit}
        >
          <div className="mx-auto flex w-full max-w-2xl items-center gap-2 px-4 py-4">
            <Input
              placeholder="Type your question..."
              className="h-11 rounded-xl border-zinc-300 bg-white/80 shadow-sm focus-visible:ring-zinc-400"
              ref={inputRef}
              value={query}
              onChange={e => setQuery(e.target.value)}
              disabled={loading}
            />
            <Button type="submit" className="h-11 rounded-xl px-6 shadow-sm" disabled={loading}>
              {loading ? 'Thinking...' : 'Ask'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
