from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn

from healthcare_chatbot import HealthcareChatbot

app = FastAPI(
    title="MediCare AI - Healthcare Chatbot API",
    description="AI-powered healthcare chatbot with RAG and conversation memory",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = HealthcareChatbot()


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict]
    query_type: str
    has_disclaimer: bool

class ConversationSummary(BaseModel):
    total_messages: int
    user_messages: int
    assistant_messages: int
    has_history: bool


@app.get("/")
def root():
    return {
        "name": "MediCare AI Healthcare Chatbot API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "POST /chat": "Send a health question",
            "GET /health": "Check API health",
            "GET /summary": "Get conversation summary",
            "POST /clear": "Clear conversation history",
            "GET /docs": "API documentation (Swagger UI)"
        }
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy" if chatbot.is_initialized else "unhealthy",
        "model": chatbot.model_name,
        "initialized": chatbot.is_initialized,
        "error": chatbot.initialization_error
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    result = chatbot.chat(request.message)

    if result["query_type"] == "error":
        raise HTTPException(status_code=503, detail=result["response"])

    return ChatResponse(
        response=result["response"],
        sources=result["sources"],
        query_type=result["query_type"],
        has_disclaimer=result["has_disclaimer"]
    )


@app.get("/summary", response_model=ConversationSummary)
def get_summary():
    return chatbot.get_conversation_summary()


@app.post("/clear")
def clear_conversation():
    chatbot.clear_conversation()
    return {"status": "success", "message": "Conversation cleared"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
