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
  GROQ_API_KEY: string;
  GEMINI_API_KEY: string;
  OPENAI_API_KEY: string;
  MODEL_PROVIDER: Provider;

  PORT: number;
  CORS_ORIGINS: string[];
  NODE_ENV: string;

  OPENAI_MODEL: string;
  GEMINI_MODEL: string;
  GROQ_MODEL: string;
}

const port = Number(process.env.PORT);

export const env: Env = {
  GROQ_API_KEY: process.env.GROQ_API_KEY ?? '',
  GEMINI_API_KEY: process.env.GEMINI_API_KEY ?? '',
  OPENAI_API_KEY: process.env.OPENAI_API_KEY ?? '',
  MODEL_PROVIDER: (process.env.MODEL_PROVIDER as Provider) ?? 'openai',

  PORT: Number.isNaN(port) ? 8080 : port,
  CORS_ORIGINS: process.env.CORS_ORIGINS
    ? process.env.CORS_ORIGINS.split(',').map(origin => origin.trim())
    : [],
  NODE_ENV: process.env.NODE_ENV || 'development',

  OPENAI_MODEL: process.env.OPENAI_MODEL ?? '',
  GEMINI_MODEL: process.env.GEMINI_MODEL ?? '',
  GROQ_MODEL: process.env.GROQ_MODEL ?? '',
};
