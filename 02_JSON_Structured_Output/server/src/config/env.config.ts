import dotenv from 'dotenv';

let loaded = false;

function loadEnv(): void {
  if (loaded) return;

  dotenv.config();
  loaded = true;
}

loadEnv();

export type Provider = 'openai' | 'gemini' | 'groq';

interface EnvConfig {
  PORT: number;
  NODE_ENV: string;
  CORS_ORIGINS: string[];
  OPENAI_API_KEY: string;
  GEMINI_API_KEY: string;
  GROQ_API_KEY: string;
  PROVIDER: Provider;
}

const port = Number(process.env.PORT);

export const env: EnvConfig = {
  PORT: Number.isNaN(port) ? 8080 : port,
  NODE_ENV: process.env.NODE_ENV || 'development',
  CORS_ORIGINS: process.env.CORS_ORIGINS
    ? process.env.CORS_ORIGINS.split(',').map(origin => origin.trim())
    : [],
  OPENAI_API_KEY: process.env.OPENAI_API_KEY ?? '',
  GEMINI_API_KEY: process.env.GEMINI_API_KEY ?? '',
  GROQ_API_KEY: process.env.GROQ_API_KEY ?? '',
  PROVIDER: (process.env.PROVIDER as EnvConfig['PROVIDER']) ?? 'openai',
};
