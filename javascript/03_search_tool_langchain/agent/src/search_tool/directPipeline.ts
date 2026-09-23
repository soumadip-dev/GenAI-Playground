import { HumanMessage, SystemMessage } from '@langchain/core/messages';
import { RunnableLambda } from '@langchain/core/runnables';

import { createChatModel } from '../config/models.config';

//* Runnable step to generate a direct answer from the user's question.
export const directPipeline = RunnableLambda.from(async function (input: {
  q: string;
  mode: 'web' | 'direct';
}) {
  //* Create the chat model used to generate the direct answer.
  const model = createChatModel({ temperature: 0.2 });

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
});
