import { type Provider, env } from './env';
import { ChatOpenAI } from '@langchain/openai';
import { ChatGoogle } from '@langchain/google';
import { ChatGroq } from '@langchain/groq';

//* Creates and returns the configured chat model based on the selected provider.
export function createChatModel(): { provider: Provider; model: any } {
  const selectedProvider = (env.PROVIDER || '').toLowerCase();

  const isOpenAIConfigured = !!env.OPENAI_API_KEY;
  const isGeminiConfigured = !!env.GEMINI_API_KEY;
  const isGroqConfigured = !!env.GROQ_API_KEY;

  // Shared configuration for deterministic responses.
  const modelConfig = { temperature: 0 as const };

  // Use OpenAI when:
  // 1. The provider is explicitly set to 'openai', or
  // 2. No provider is specified and an OpenAI API key is available.
  if (selectedProvider === 'openai' || (!selectedProvider && isOpenAIConfigured)) {
    return {
      provider: 'openai',
      model: new ChatOpenAI({
        ...modelConfig,
        model: 'gpt-5-nano',
      }),
    };
  }

  // Use Gemini when:
  // 1. The provider is explicitly set to 'gemini', or
  // 2. No provider is specified and a Gemini API key is available.
  if (selectedProvider === 'gemini' || (!selectedProvider && isGeminiConfigured)) {
    return {
      provider: 'gemini',
      model: new ChatGoogle({
        ...modelConfig,
        model: 'gemini-2.5-flash-lite',
      }),
    };
  }

  // Use Groq when:
  // 1. The provider is explicitly set to 'groq', or
  // 2. No provider is specified and a Groq API key is available.
  if (selectedProvider === 'groq' || (!selectedProvider && isGroqConfigured)) {
    return {
      provider: 'groq',
      model: new ChatGroq({
        ...modelConfig,
        model: 'llama-3.1-8b-instant',
      }),
    };
  }

  // Default case : gemini
  return {
    provider: 'gemini',
    model: new ChatGoogle({
      ...modelConfig,
      model: 'gemini-2.5-flash-lite',
    }),
  };
}
