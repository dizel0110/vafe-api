"""
V-AFE API — RAG Client
Заглушка для RAG поиска

Future: Интеграция с vortex-afe сервисом
"""

from typing import Dict, List


class RAGClient:
    """
    RAG клиент-заглушка

    Сейчас: Возвращает пустой список
    Future: HTTP запрос к vortex-afe API
    """

    def __init__(self, endpoint: str = None):
        self.endpoint = endpoint
        self.enabled = False

    async def search(
        self,
        query: str,
        mode: str = "general",
        top_k: int = 3
    ) -> List[Dict]:
        """
        Поиск концептов (заглушка)

        Returns:
            Пустой список (RAG отключён)
        """
        # TODO: Интеграция с vortex-afe
        return []

    async def sync_embeddings(self) -> bool:
        """Синхронизация embeddings (заглушка)"""
        return False
