import dotenv from 'dotenv';
import { z } from 'zod';

dotenv.config();

export type Provider = 'openai' | 'gemini' | 'groq';

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
  PROVIDER: z.enum(['openai', 'gemini', 'groq']).default('openai'),
});

export const env = EnvSchema.parse(process.env);
