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
  LLM_MODEL_NAME: z.string().default('gemini-3.5-flash-lite'),
  EMBEDDING_MODEL_NAME: z.string().default('models/gemini-embedding-001'),
  GEMINI_API_KEY: z.string(),
});

export const env = EnvSchema.parse(process.env);
