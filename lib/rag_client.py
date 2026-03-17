"""
V-AFE API — RAG Client
Интеграция с vortex-afe для поиска по базе знаний
"""

from typing import Dict, List, Optional


class RAGClient:
    """
    Клиент для RAG поиска по базе знаний vortex-afe

    Сейчас: Заглушка (возвращает пустой список)
    Future: Интеграция с vortex-afe embeddings
    """

    def __init__(self, endpoint: str = None):
        self.endpoint = endpoint or "http://localhost:8000"
        self.enabled = False  # Пока отключено

    async def search(
        self,
        query: str,
        mode: str = "general",
        top_k: int = 3
    ) -> List[Dict]:
        """
        Поиск релевантных концептов в базе знаний

        Args:
            query: Запрос пользователя
            mode: Режим (vafe, about, general)
            top_k: Количество результатов

        Returns:
            Список концептов с источниками
        """
        # TODO: Интеграция с vortex-afe
        # Сейчас возвращаем пустой список
        return []

    async def sync_embeddings(self) -> bool:
        """
        Синхронизация embeddings с vortex-afe

        Returns:
            True если успешно
        """
        # TODO: Реализовать синхронизацию
        return False
