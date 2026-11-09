from typing import TypedDict

import httpx

from env import Provider, env


class HelloResponse(TypedDict):
    ok: bool
    provider: Provider
    model: str
    message: str


# Response shape returned by Gemini
class GeminiGenerateContentResponse(TypedDict, total=False):
    candidates: list[dict]


# Response shape returned by OpenAI-compatible APIs
class OpenAIChatCompletionResponse(TypedDict, total=False):
    choices: list[dict]


# Sends a greeting prompt to Gemini
async def hello_gemini() -> HelloResponse:

    gemini_api_key = env["GEMINI_API_KEY"]

    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    model = "gemini-2.5-flash-lite"

    endpoint_url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model}:generateContent?key={gemini_api_key}"
    )

    async with httpx.AsyncClient(timeout=30.0) as client:

        api_response = await client.post(
            endpoint_url,
            headers={
                "Content-Type": "application/json",
            },
            json={"contents": [{"parts": [{"text": "Say hello to the world!"}]}]},
        )

    if api_response.is_error:
        raise RuntimeError(
            f"Gemini API request failed with status "
            f"{api_response.status_code}: {api_response.text}"
        )

    response_data = api_response.json()

    generated_text = (
        response_data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text")
        or "Gemini returned a successful response, but no text content was found."
    )

    return {
        "ok": True,
        "provider": "gemini",
        "model": model,
        "message": str(generated_text).strip(),
    }


# Sends a greeting prompt to Groq
async def hello_groq() -> HelloResponse:

    groq_api_key = env["GROQ_API_KEY"]

    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is not configured.")

    model = "llama-3.1-8b-instant"

    endpoint_url = "https://api.groq.com/openai/v1/chat/completions"

    async with httpx.AsyncClient(timeout=30.0) as client:

        api_response = await client.post(
            endpoint_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {groq_api_key}",
            },
            json={
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": "Say hello to the world!",
                    }
                ],
                "temperature": 0,
            },
        )

    if api_response.is_error:
        raise RuntimeError(
            f"Groq API request failed with status "
            f"{api_response.status_code}: {api_response.text}"
        )

    response_data = api_response.json()

    generated_message = (
        response_data.get("choices", [{}])[0].get("message", {}).get("content")
        or "Groq returned a successful response, but no text content was available."
    )

    return {
        "ok": True,
        "provider": "groq",
        "model": model,
        "message": str(generated_message).strip(),
    }


# Sends a greeting prompt to OpenAI
async def hello_openai() -> HelloResponse:

    openai_api_key = env["OPENAI_API_KEY"]

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured.")

    model = "gpt-5-nano"

    endpoint_url = "https://api.openai.com/v1/chat/completions"

    async with httpx.AsyncClient(timeout=30.0) as client:

        api_response = await client.post(
            endpoint_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}",
            },
            json={
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": "Say hello to the world!",
                    }
                ],
                "temperature": 0,
            },
        )

    if api_response.is_error:
        raise RuntimeError(
            f"OpenAI API request failed with status "
            f"{api_response.status_code}: {api_response.text}"
        )

    response_data = api_response.json()

    generated_message = (
        response_data.get("choices", [{}])[0].get("message", {}).get("content")
        or "OpenAI returned a successful response, but no message content was found."
    )

    return {
        "ok": True,
        "provider": "openai",
        "model": model,
        "message": str(generated_message).strip(),
    }


# Selects the provider based on environment configuration
async def select_and_hello() -> HelloResponse:

    configured_provider = env["PROVIDER"].lower()

    # Use explicitly configured provider
    if configured_provider == "gemini":
        return await hello_gemini()

    if configured_provider == "groq":
        return await hello_groq()

    if configured_provider == "openai":
        return await hello_openai()

    if configured_provider:
        raise ValueError(
            f'Unsupported provider "{configured_provider}". '
            "Supported values are: openai, gemini, and groq."
        )

    # Try Gemini first
    if env["GEMINI_API_KEY"]:
        try:
            return await hello_gemini()
        except Exception as error:
            print(f"Gemini request failed: {error}")

    # Fall back to Groq
    if env["GROQ_API_KEY"]:
        try:
            return await hello_groq()
        except Exception as error:
            print(f"Groq request failed: {error}")

    # Fall back to OpenAI
    if env["OPENAI_API_KEY"]:
        try:
            return await hello_openai()
        except Exception as error:
            print(f"OpenAI request failed: {error}")

    raise RuntimeError(
        "No AI provider is configured. "
        "Set GEMINI_API_KEY, GROQ_API_KEY, or OPENAI_API_KEY."
    )
