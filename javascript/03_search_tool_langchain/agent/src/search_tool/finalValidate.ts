import { HumanMessage, SystemMessage } from '@langchain/core/messages';
import { RunnableLambda } from '@langchain/core/runnables';

import { createChatModel } from '../config/models.config';
import { searchOutputSchema } from '../schemas';
import type { Candidate } from './types';

export const validateFinalOutputStep = RunnableLambda.from(async function validateFinalOutput(
  candidate: Candidate
) {
  const candidateOutput = {
    answer: candidate.answer,
    sources: candidate.sources ?? [],
  };

  const parsedResult = searchOutputSchema.safeParse(candidateOutput);

  if (parsedResult.success) {
    return parsedResult.data;
  }

  // Attempt to repair the output if it does not match the schema.
  const repairedResult = await repairSearchAnswer(candidateOutput);

  const repairedParsedResult = searchOutputSchema.safeParse(repairedResult);

  if (repairedParsedResult.success) {
    return repairedParsedResult.data;
  }

  throw new Error('Failed to validate or repair search output');
});

async function repairSearchAnswer(output: unknown): Promise<{ answer: string; sources: string[] }> {
  const model = createChatModel({ temperature: 0.2 });

  const response = await model.invoke([
    new SystemMessage(
      [
        'You are a JSON output repair assistant.',
        'Your task is to repair the provided object so that it exactly matches the required schema.',
        '',
        'Required schema:',
        '{',
        '  "answer": string,',
        '  "sources": string[]',
        '}',
        '',
        'Rules:',
        '- Return only a valid JSON object. Do not include Markdown, code fences, or explanations.',
        '- Keep the original answer content whenever possible. Only modify it when necessary to produce valid output.',
        '- The "answer" field must always be a string.',
        '- The "sources" field must always be an array of strings.',
        '- Each value in "sources" must be a valid URL string.',
        '- If there are no valid sources, return an empty array.',
        '- Do not add fields that are not part of the schema.',
      ].join('\n')
    ),
    new HumanMessage(
      [
        'Repair the following object so that it exactly matches the required schema.',
        '',
        'Input object:',
        JSON.stringify(output),
        '',
        'Return only the repaired JSON object.',
      ].join('\n')
    ),
  ]);

  const responseText =
    typeof response.content === 'string' ? response.content : String(response.content);

  const parsedJson = extractJsonObject(responseText);

  return {
    answer: String(parsedJson?.answer ?? '').trim(),
    sources: Array.isArray(parsedJson?.sources) ? parsedJson.sources.map(String) : [],
  };
}

function extractJsonObject(input: string): Record<string, unknown> {
  const startIndex = input.indexOf('{');
  const endIndex = input.lastIndexOf('}');

  if (startIndex === -1 || endIndex === -1 || endIndex <= startIndex) {
    return {};
  }

  try {
    const parsedJson: unknown = JSON.parse(input.slice(startIndex, endIndex + 1));

    if (typeof parsedJson === 'object' && parsedJson !== null && !Array.isArray(parsedJson)) {
      return parsedJson as Record<string, unknown>;
    }

    return {};
  } catch {
    return {};
  }
}
