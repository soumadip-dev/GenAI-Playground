import { env } from './env.config.ts';
import { ChatOpenAI } from '@langchain/openai';
import { ChatGoogle } from '@langchain/google';
import { ChatGroq } from '@langchain/groq';
import type { BaseChatModel } from '@langchain/core/language_models/chat_models';

type ChatModelOptions = {
  temperature?: number;
  maxTokens?: number;
};

export function createChatModel(options: ChatModelOptions = {}): BaseChatModel {
  const temperature = options.temperature ?? 0.2;

  switch (env.MODEL_PROVIDER) {
    case 'openai':
      return new ChatOpenAI({
        model: env.OPENAI_MODEL,
        apiKey: env.OPENAI_API_KEY,
        temperature,
      });

    case 'groq':
      return new ChatGroq({
        model: env.GROQ_MODEL,
        apiKey: env.GROQ_API_KEY,
        temperature,
      });

    case 'gemini':
    default:
      return new ChatGoogle({
        model: env.GEMINI_MODEL,
        apiKey: env.GEMINI_API_KEY,
        temperature,
      });
  }
}
