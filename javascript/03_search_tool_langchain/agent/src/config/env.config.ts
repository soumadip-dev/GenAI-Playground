import dotenv from 'dotenv';
import { z } from 'zod';

dotenv.config();

const EnvSchema = z.object({
  NODE_ENV: z.string().default('development'),

  PORT: z.coerce.number().default(8080),

  CORS_ORIGINS: z
    .string()
    .default('')
    .transform(value =>
      value
        .split(',')
        .map(origin => origin.trim())
        .filter(Boolean)
    ),

  OPENAI_API_KEY: z.string().optional(),
  GROQ_API_KEY: z.string().optional(),
  GEMINI_API_KEY: z.string().optional(),

  MODEL_PROVIDER: z.enum(['openai', 'gemini', 'groq']).default('gemini'),

  OPENAI_MODEL: z.string().default('gpt-5-nano'),
  GEMINI_MODEL: z.string().default('gemini-2.5-flash-lite'),
  GROQ_MODEL: z.string().default('llama-3.1-8b-instant'),

  SEARCH_PROVIDER: z.string().default('tavily'),
  TAVILY_API_KEY: z.string().optional(),
});

export const env = EnvSchema.parse(process.env);
