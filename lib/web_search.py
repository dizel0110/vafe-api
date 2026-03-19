"""
Web Search via Tavily AI
Поиск источников для ответов Gemini

Docs: https://docs.tavily.com/
Free tier: 1000 requests/month
"""

import os
from typing import List, Dict

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None


def search_web(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Поиск в интернете через Tavily AI

    Args:
        query: Поисковый запрос
        max_results: Максимальное количество результатов (по умолчанию 3)

    Returns:
        Список источников: [{"title": "...", "url": "...", "snippet": "..."}]
    """
    # Получаем API ключ
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        print("TAVILY_API_KEY not found, returning empty sources")
        return []

    if TavilyClient is None:
        print("tavily-python not installed, returning empty sources")
        return []

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query, max_results=max_results)

        sources = []
        for result in response.get("results", [])[:max_results]:
            sources.append({
                "title": result.get("title", "No title"),
                "url": result.get("url", ""),
                "snippet": result.get("content", "")
            })

        return sources

    except Exception as e:
        print(f"Tavily search error: {e}")
        return []


# Тест
if __name__ == "__main__":
    query = "Google Gemini AI model"
    sources = search_web(query, max_results=3)

    print(f"🔍 Search: {query}\n")
    for i, source in enumerate(sources, 1):
        print(f"{i}. {source['title']}")
        print(f"   {source['url']}")
        print(f"   {source['snippet']}\n")
