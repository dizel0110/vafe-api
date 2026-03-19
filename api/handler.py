"""
V-AFE API — Vercel Handler
Точка входа для Vercel Serverless Functions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import sys

# Добавляем корень проекта в path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.provider_router import ProviderRouter
from lib.rag_client import RAGClient

# Инициализация FastAPI
app = FastAPI(title="V-AFE API", version="1.0.0")

# CORS для всех источников (безопасно для serverless)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация клиентов
provider_router = ProviderRouter()
rag_client = RAGClient()


class ChatRequest(BaseModel):
    """Запрос к чату"""
    message: str
    mode: Optional[str] = "general"
    context: Optional[List[Dict]] = []
    use_rag: Optional[bool] = True
    stream: Optional[bool] = False


class ChatResponse(BaseModel):
    """Ответ чата"""
    answer: str
    sources: List[Dict] = []
    provider: str
    model: str
    mode: str
    metadata: Dict = {}


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Основной endpoint для чата"""
    try:
        sources = []
        if request.use_rag:
            sources = await rag_client.search(
                query=request.message,
                mode=request.mode,
                top_k=3
            )

        response = await provider_router.generate(
            prompt=request.message,
            context=sources,
            mode=request.mode
        )

        return ChatResponse(
            answer=response['answer'],
            sources=sources,
            provider=response['provider'],
            model=response['model'],
            mode=request.mode,
            metadata=response.get('metadata', {})
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )


@app.get("/api/v1/chat/health")
async def health_check():
    """Проверка здоровья endpoint"""
    return {
        "status": "healthy",
        "provider": provider_router.get_active_provider(),
        "available_providers": provider_router.get_available_providers()
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "V-AFE API",
        "version": "1.0.0",
        "status": "running"
    }
