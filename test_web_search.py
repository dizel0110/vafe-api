"""Тест веб-поиска и Gemini"""

from dotenv import load_dotenv
load_dotenv('.env.local')

from lib.web_search import search_web
from lib.provider_router import ProviderRouter
import asyncio

print("🔍 Тест 1: Веб-поиск")
sources = search_web("Google Gemini AI", max_results=2)
print(f"Найдено: {len(sources)}")
for s in sources:
    print(f"  • {s['title'][:60]}... → {s['url'][:50]}...")

print("\n🤖 Тест 2: Gemini + источники")

async def test():
    router = ProviderRouter()
    response = await router.generate(
        prompt="Что такое Gemini?",
        context=sources,
        mode="general"
    )
    print(f"Ответ: {response['answer'][:150]}...")
    print(f"Провайдер: {response['provider']}")

asyncio.run(test())
print("\n✅ Тест завершён")
