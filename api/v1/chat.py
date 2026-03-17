"""
V-AFE API — Chat Endpoint v1
POST /api/v1/chat
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os

# Импорты для RAG и Gemini
from lib.provider_router import ProviderRouter
from lib.rag_client import RAGClient

router = APIRouter()

# Инициализация
provider_router = ProviderRouter()
rag_client = RAGClient()


class ChatRequest(BaseModel):
    """Запрос к чату"""
    message: str
    mode: Optional[str] = "general"  # vafe, about, general
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


@router.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Основной endpoint для чата
    
    Принимает вопрос пользователя, возвращает ответ с источниками
    """
    try:
        # RAG поиск (если включён)
        sources = []
        if request.use_rag:
            sources = await rag_client.search(
                query=request.message,
                mode=request.mode,
                top_k=3
            )
        
        # Генерация ответа через LLM
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


@router.get("/api/v1/chat/health")
async def health_check():
    """Проверка здоровья endpoint"""
    return {
        "status": "healthy",
        "provider": provider_router.get_active_provider(),
        "available_providers": provider_router.get_available_providers()
    }
