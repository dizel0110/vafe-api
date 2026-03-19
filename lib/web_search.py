"""
Web Search via DuckDuckGo
Поиск источников для ответов Gemini
"""

from duckduckgo_search import DDGS
from typing import List, Dict


def search_web(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Поиск в интернете через DuckDuckGo

    Args:
        query: Поисковый запрос
        max_results: Максимальное количество результатов (по умолчанию 3)

    Returns:
        Список источников: [{"title": "...", "url": "...", "snippet": "..."}]
    """
    try:
        with DDGS(headers={"User-Agent": "Mozilla/5.0"}) as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        sources = []
        for result in results[:max_results]:
            sources.append({
                "title": result.get("title", "No title"),
                "url": result.get("href", ""),
                "snippet": result.get("body", "")
            })

        return sources

    except Exception as e:
        print(f"Web search error: {e}")
        # Возвращаем fallback источники при ошибке
        return [{
            "title": "Search unavailable",
            "url": "",
            "snippet": "Web search is currently unavailable"
        }]


# Тест
if __name__ == "__main__":
    query = "Google Gemini AI model"
    sources = search_web(query, max_results=3)

    print(f"🔍 Search: {query}\n")
    for i, source in enumerate(sources, 1):
        print(f"{i}. {source['title']}")
        print(f"   {source['url']}")
        print(f"   {source['snippet']}\n")
