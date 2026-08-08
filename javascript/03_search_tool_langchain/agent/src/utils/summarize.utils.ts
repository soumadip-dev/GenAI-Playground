import { createChatModel } from '../config/models.config';
import { SummarizeInputSchema, SummarizeOutputSchema } from '../schemas';
import { HumanMessage, SystemMessage } from '@langchain/core/messages';

export async function summarize(text: string) {
  const { text: inputText } = SummarizeInputSchema.parse({ text });

  // Limit the input size to control token usage and model latency.
  const truncatedText = truncateText(inputText, 2000);

  const model = createChatModel({
    temperature: 0.2,
  });

  // Build a constrained conversation to generate a concise and factual summary.
  const messages = [
    new SystemMessage(
      [
        'You are a helpful assistant that writes short, accurate summaries.',
        'Guidelines:',
        '- Be factual and neutral. Avoid marketing or promotional language.',
        '- Write 5–8 sentences. Do not use bullet points or lists unless absolutely necessary.',
        '- Use only the information provided in the input.',
        '- Do not add assumptions, interpretations, or extra details.',
        '- Do not invent sources, facts, or context.',
        '- Keep the language clear and easy for beginners to understand.',
        '- If information is missing or unclear, omit it rather than guessing.',
      ].join('\n')
    ),
    new HumanMessage(
      [
        'Summarize the following content for a beginner-friendly audience.',
        'Focus only on the key facts and remove unnecessary details or fluff.',
        'Do not add, infer, or include any information that is not explicitly present in the provided text.',
        'Use clear and simple language.',
        'TEXT:',
        truncatedText,
      ].join('\n\n')
    ),
  ];

  const response = await model.invoke(messages);

  const rawSummary =
    typeof response.content === 'string' ? response.content : String(response.content);

  // Normalize whitespace and enforce the maximum output length.
  const normalizedSummary = normalizeSummary(rawSummary);

  return SummarizeOutputSchema.parse({
    summary: normalizedSummary,
  });
}

// Truncates text to the specified maximum length.
function truncateText(text: string, maxLength: number) {
  if (text.length > maxLength) {
    return text.slice(0, maxLength);
  } else {
    return text;
  }
}

// Cleans whitespace and constrains the final summary length.
function normalizeSummary(summary: string) {
  const normalizedText = summary
    .replace(/\s+\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  return normalizedText.slice(0, 2500);
}
