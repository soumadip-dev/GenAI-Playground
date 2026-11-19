from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatbot import generate

app = FastAPI(title="ChatGPT-like app for practicing LLM calling and tool calling")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {"message": "Welcome to ChatGPT"}


@app.post("/chat")
def chat(payload: ChatRequest):
    print(f"Message: {payload.message}")
    reply = generate(payload.message)
    return {"reply": reply or "No response generated."}