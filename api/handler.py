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
import httpx  # Для запросов к Tavily API

# Добавляем корень проекта в path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.provider_router import ProviderRouter
from lib.rag_client import RAGClient
from lib.web_search import search_web

# Инициализация FastAPI
app = FastAPI(title="V-AFE API", version="1.0.0")

# CORS для конкретных доменов
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",       # Локальная разработка
        "https://dizel0110.github.io", # Production
        "https://dizel0110.github.io",
    ],
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
    search_provider: Optional[str] = "tavily"  # tavily|concepts|hybrid


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
        # 1. Определяем поисковик
        provider = request.search_provider or "tavily"

        # 2. Поиск источников (зависит от поисковика)
        sources = []

        if provider == "concepts":
            # Только концепты (RAG)
            if request.use_rag:
                sources = await rag_client.search(
                    query=request.message,
                    mode=request.mode,
                    top_k=5
                )

        elif provider == "hybrid":
            # Гибридный: Концепты + Веб
            hybrid_sources = []

            # Концепты
            if request.use_rag:
                hybrid_sources.extend(await rag_client.search(
                    query=request.message,
                    mode=request.mode,
                    top_k=2
                ))

            # Веб (Tavily)
            web_sources = search_web(request.message, max_results=2)
            hybrid_sources.extend(web_sources)

            sources = hybrid_sources[:5]

        elif provider == "tavily":
            # Tavily AI (по умолчанию)
            if request.mode == "general" and not request.use_rag:
                sources = search_web(request.message, max_results=3)
            elif request.use_rag:
                sources = await rag_client.search(
                    query=request.message,
                    mode=request.mode,
                    top_k=3
                )

        # 3. Генерация ответа через Gemini
        response = await provider_router.generate(
            prompt=request.message,
            context=sources,
            mode=request.mode
        )

        # 4. Формируем metadata
        search_type = "hybrid" if provider == "hybrid" else ("local" if provider == "concepts" else "web")

        metadata = {
            "sources_count": len(sources),
            "search_provider": "Tavily AI" if provider in ["tavily", "hybrid"] else "Local Concepts",
            "search_type": search_type,
            "llm_model": response['model'],
            "mode": request.mode,
            "rag_enabled": request.use_rag,
            "multi_language": True,
            "interactive_links": True
        }

        return ChatResponse(
            answer=response['answer'],
            sources=sources,
            provider=response['provider'],
            model=response['model'],
            mode=request.mode,
            metadata=metadata
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


class UsageResponse(BaseModel):
    """Статистика использования Tavily"""
    requests_this_month: int
    requests_limit: int
    percentage_used: float
    remaining: int
    plan: str = "free"
    source: str = "Tavily API"


@app.get("/api/v1/usage")
async def get_usage():
    """
    Получить статистику использования Tavily API

    Returns:
        UsageResponse с реальной статистикой
    """
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    TAVILY_API_URL = "https://api.tavily.com/user/usage"

    if not TAVILY_API_KEY:
        return UsageResponse(
            requests_this_month=0,
            requests_limit=1000,
            percentage_used=0.0,
            remaining=1000,
            source="TAVILY_API_KEY not configured"
        )

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                TAVILY_API_URL,
                headers={"Authorization": f"Bearer {TAVILY_API_KEY}"}
            )

            if response.status_code == 200:
                data = response.json()
                usage = data.get("usage", {})
                requests_this_month = usage.get("requests_this_month", 0)
                requests_limit = usage.get("requests_limit", 1000)

                return UsageResponse(
                    requests_this_month=requests_this_month,
                    requests_limit=requests_limit,
                    percentage_used=round((requests_this_month / requests_limit) * 100, 1),
                    remaining=requests_limit - requests_this_month,
                    plan=usage.get("plan", "free"),
                    source="Tavily API"
                )
    except Exception as e:
        pass

    # Fallback при ошибке
    return UsageResponse(
        requests_this_month=0,
        requests_limit=1000,
        percentage_used=0.0,
        remaining=1000,
        source="Fallback (Tavily API unavailable)"
    )


@app.get("/api/v1/usage/health")
async def usage_health():
    """Проверка доступности usage endpoint"""
    return {
        "status": "healthy",
        "endpoint": "/api/v1/usage",
        "tavily_configured": bool(os.getenv("TAVILY_API_KEY"))
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "V-AFE API",
        "version": "1.0.0",
        "status": "running",
        "search_providers": ["tavily", "concepts", "hybrid"]
    }
