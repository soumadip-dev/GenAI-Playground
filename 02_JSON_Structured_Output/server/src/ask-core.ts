import { createChatModel } from './lc-model';
import { AskResultSchema, type AskResult } from './schema';

export async function getStructuredAnswer(query: string): Promise<AskResult> {
  const { model } = createChatModel();

  // Keep the instruction brief so that schema stays visible to the model.
  const systemPrompt =
    'You are a concise assistant. Explain topics in simple English for beginners. Return only the requested JSON object without markdown or extra text.';

  const userPrompt =
    `Summarize the following topic in simple English for a beginner:\n\n"${query}"\n\n` +
    'Return these fields:\n' +
    '- summary: a short paragraph (2-4 sentences)\n' +
    '- confidence: a number between 0 and 1';

  const structuredModel = model.withStructuredOutput(AskResultSchema);

  const response = await structuredModel.invoke([
    {
      role: 'system',
      content: systemPrompt,
    },
    {
      role: 'user',
      content: userPrompt,
    },
  ]);

  return response;
}
