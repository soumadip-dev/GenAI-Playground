import { env, type Provider } from './env';

type HelloResponse = {
  ok: true;
  provider: Provider;
  model: string;
  message: string;
};

type GeminiGenerateContentResponse = {
  candidates?: Array<{
    content?: {
      parts?: Array<{
        text?: string;
      }>;
    };
  }>;
};

async function helloGemini(): Promise<HelloResponse> {
  const geminiApiKey = env.GEMINI_API_KEY;

  if (!geminiApiKey) {
    throw new Error('GEMINI_API_KEY is not configured.');
  }

  const model = 'gemini-2.5-flash-lite';

  const endpointUrl = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`;

  const apiResponse = await fetch(endpointUrl, {
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
