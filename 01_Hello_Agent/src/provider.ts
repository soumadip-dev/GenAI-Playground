import { env, type Provider } from './env';

type HelloResponse = {
  ok: true;
  provider: Provider;
  model: string;
  message: string;
};

//* Response shape returned by the Gemini generateContent API.
type GeminiGenerateContentResponse = {
  candidates?: Array<{
    content?: {
      parts?: Array<{
        text?: string;
      }>;
    };
  }>;
};

//* Response shape returned by OpenAI-compatible APIs such as Groq.
type OpenAIChatCompletionResponse = {
  choices?: Array<{ message?: { content?: string } }>;
};

//* Sends a simple greeting prompt to the Gemini API.
async function helloGemini(): Promise<HelloResponse> {
  const geminiApiKey = env.GEMINI_API_KEY;

  if (!geminiApiKey) {
    throw new Error('GEMINI_API_KEY is not configured.');
  }

  const model = 'gemini-2.5-flash-lite';

  const endpointUrl = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`;

  const apiResponse = await fetch(endpointUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      contents: [
        {
          parts: [
            {
              text: 'Say hello to the world!',
            },
          ],
        },
      ],
    }),
  });

  if (!apiResponse.ok) {
    throw new Error(
      `Gemini API request failed with status ${apiResponse.status}: ${await apiResponse.text()}`
    );
  }
  const responseData = (await apiResponse.json()) as GeminiGenerateContentResponse;

  const generatedText =
    responseData.candidates?.[0]?.content?.parts?.[0]?.text ??
    'Gemini returned a successful response, but no text content was found.';

  return {
    ok: true,
    provider: 'gemini',
    model,
    message: String(generatedText).trim(),
  };
}

//* Sends a simple greeting prompt to the Groq API.
async function helloGroq(): Promise<HelloResponse> {
  const groqApiKey = env.GROQ_API_KEY;

  if (!groqApiKey) {
    throw new Error('GROQ_API_KEY is not configured.');
  }

  const model = 'llama-3.1-8b-instant';

  const endpointUrl = 'https://api.groq.com/openai/v1/chat/completions';

  const apiResponse = await fetch(endpointUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${groqApiKey}`,
    },
    body: JSON.stringify({
      model,
      messages: [
        {
          role: 'user',
          content: 'Say hello to the world!',
        },
      ],
      temperature: 0,
    }),
  });

  if (!apiResponse.ok) {
    throw new Error(
      `Groq API request failed with status ${apiResponse.status}: ${await apiResponse.text()}`
    );
  }

  const responseData = (await apiResponse.json()) as OpenAIChatCompletionResponse;

  const generatedMessage =
    responseData.choices?.[0]?.message?.content ??
    'Groq returned a successful response, but no text content was available.';

  return {
    ok: true,
    provider: 'groq',
    model,
    message: String(generatedMessage).trim(),
  };
}

//* Sends a simple greeting prompt to the OpenAI API.
async function helloOpenAI(): Promise<HelloResponse> {
  const openaiApiKey = env.OPENAI_API_KEY;

  if (!openaiApiKey) {
    throw new Error('OPENAI_API_KEY is not configured.');
  }

  const model = 'gpt-5-nano';

  // OpenAI chat completion endpoint.
  const endpointUrl = 'https://api.openai.com/v1/chat/completions';

  const apiResponse = await fetch(endpointUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${openaiApiKey}`,
    },
    body: JSON.stringify({
      model,
      messages: [
        {
          role: 'user',
          content: 'Say hello to the world!',
        },
      ],
      temperature: 0,
    }),
  });

  if (!apiResponse.ok) {
    throw new Error(
      `OpenAI API request failed with status ${apiResponse.status}: ${await apiResponse.text()}`
    );
  }

  const responseBody = (await apiResponse.json()) as OpenAIChatCompletionResponse;

  // Extract the generated message from the first completion choice.
  const generatedMessage =
    responseBody.choices?.[0]?.message?.content ??
    'OpenAI returned a successful response, but no message content was found.';

  return {
    ok: true,
    provider: 'openai',
    model,
    message: String(generatedMessage).trim(),
  };
}
