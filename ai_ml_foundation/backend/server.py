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
    thread_id: str


@app.get("/")
def read_root():
    return {"message": "Welcome to ChatGPT"}


@app.post("/chat")
def chat(payload: ChatRequest):
    if not payload.thread_id.strip():
        raise HTTPException(status_code=400, detail="threadId cannot be empty.")

    print(f"Thread ID: {payload.thread_id}")
    print(f"Message: {payload.message}")

    reply = generate(user_message=payload.message, thread_id=payload.thread_id)

    return {"reply": reply or "No response generated."}
