import dotenv from 'dotenv';

let loaded = false;

function loadEnv(): void {
  if (loaded) return;

  dotenv.config();
  loaded = true;
}

loadEnv();

export type Provider = 'openai' | 'gemini' | 'groq';

interface Env {
  OPENAI_API_KEY: string;
  GEMINI_API_KEY: string;
  GROQ_API_KEY: string;
  PROVIDER: Provider;
}

export const env: Env = {
  OPENAI_API_KEY: process.env.OPENAI_API_KEY ?? '',
  GEMINI_API_KEY: process.env.GEMINI_API_KEY ?? '',
  GROQ_API_KEY: process.env.GROQ_API_KEY ?? '',
  PROVIDER: (process.env.PROVIDER as Env['PROVIDER']) ?? 'openai',
};
