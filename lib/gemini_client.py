"""
V-AFE API — Gemini Client
Клиент для Google Gemini API
"""

import os
from typing import Dict, Any, List, Optional
import google.generativeai as genai


class GeminiClient:
    """
    Клиент для Google Gemini API
    
    Free tier: 60 requests/min, 1500 requests/day
    Model: gemini-pro
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.model_name = config.get('model', 'gemini-2.5-flash')
        
        # Получение API ключа
        api_key_env = config.get('api_key_env', 'GEMINI_API_KEY')
        api_key = os.getenv(api_key_env)
        
        if not api_key:
            raise ValueError(f"API key {api_key_env} not found")
        
        # Инициализация
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    async def generate(
        self,
        prompt: str,
        context: List[Dict] = None,
        **kwargs
    ) -> Dict:
        """
        Генерация ответа
        
        Args:
            prompt: Запрос пользователя
            context: Контекст из RAG базы
            **kwargs: Дополнительные параметры
        
        Returns:
            Dict с текстом ответа и метаданными
        """
        # Формирование промпта с контекстом
        full_prompt = self._build_prompt(prompt, context)
        
        # Генерация
        response = await self._generate_async(full_prompt, **kwargs)
        
        return {
            'text': response.text,
            'metadata': {
                'model': self.model_name,
                'usage': {
                    'prompt_tokens': len(full_prompt.split()),
                    'completion_tokens': len(response.text.split())
                }
            }
        }
    
    def _build_prompt(self, prompt: str, context: List[Dict] = None) -> str:
        """
        Построение промпта с контекстом из RAG
        
        Args:
            prompt: Запрос пользователя
            context: Контекст из базы знаний
        
        Returns:
            Полный промпт
        """
        if not context:
            return prompt
        
        context_text = "\n\n".join([
            f"[{c.get('concept', 'Unknown')}]\n"
            f"Физика: {c.get('physics', '')}\n"
            f"Механика: {c.get('mechanics', '')}"
            for c in context[:3]  # Top 3 релевантных концепта
        ])
        
        full_prompt = f"""Ты — V-AFE AI Instructor, экспертный инструктор по кайтбордингу.

Твои ответы основаны на физической базе знаний VORTEX: APPARENT FLOW ENGINE.

База знаний:
{context_text}

Вопрос пользователя: {prompt}

Отвечай:
- Инженерным, лаконичным языком
- С ссылками на конкретные концепты
- С акцентом на физику и механику
- Без общих фраз и воды

Ответ:"""
        
        return full_prompt
    
    async def _generate_async(self, prompt: str, **kwargs) -> Any:
        """
        Асинхронная генерация
        
        Gemini SDK синхронный, поэтому используем asyncio
        """
        import asyncio
        
        loop = asyncio.get_event_loop()
        
        # Генерация в отдельном потоке
        response = await loop.run_in_executor(
            None,
            lambda: self.model.generate_content(prompt)
        )
        
        return response
    
    def generate_stream(
        self,
        prompt: str,
        context: List[Dict] = None,
        **kwargs
    ):
        """
        Потоковая генерация
        
        Yields:
            Части ответа
        """
        full_prompt = self._build_prompt(prompt, context)
        
        for chunk in self.model.generate_content(full_prompt, stream=True):
            yield chunk.text
