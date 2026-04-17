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
  NODE_ENV: string;
  PORT: number;
  CORS_ORIGINS: string[];

  OPENAI_API_KEY: string;
  GROQ_API_KEY: string;
  GEMINI_API_KEY: string;

  MODEL_PROVIDER: Provider;

  OPENAI_MODEL: string;
  GEMINI_MODEL: string;
  GROQ_MODEL: string;

  SEARCH_PROVIDER: string;
  TAVILY_API_KEY: string;
}

const port = Number(process.env.PORT);

export const env: Env = {
  NODE_ENV: process.env.NODE_ENV || 'development',
  PORT: Number.isNaN(port) ? 8080 : port,
  CORS_ORIGINS: process.env.CORS_ORIGINS
    ? process.env.CORS_ORIGINS.split(',').map(origin => origin.trim())
    : [],

  OPENAI_API_KEY: process.env.OPENAI_API_KEY ?? '',
  GROQ_API_KEY: process.env.GROQ_API_KEY ?? '',
  GEMINI_API_KEY: process.env.GEMINI_API_KEY ?? '',

  MODEL_PROVIDER: (process.env.MODEL_PROVIDER as Provider) ?? 'openai',

  OPENAI_MODEL: process.env.OPENAI_MODEL ?? '',
  GEMINI_MODEL: process.env.GEMINI_MODEL ?? '',
  GROQ_MODEL: process.env.GROQ_MODEL ?? '',

  SEARCH_PROVIDER: process.env.SEARCH_PROVIDER ?? '',
  TAVILY_API_KEY: process.env.TAVILY_API_KEY ?? '',
};
