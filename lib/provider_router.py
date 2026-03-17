"""
V-AFE API — Provider Router
Маршрутизация запросов к разным LLM провайдерам
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class ProviderRouter:
    """
    Роутер для LLM провайдеров
    
    Поддерживает:
    - Google Gemini (active)
    - OpenAI (future)
    - Anthropic (future)
    - Local LLM (future)
    """
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "providers.json"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.active_provider = self.config['active']
        self.clients: Dict[str, Any] = {}
        
        # Инициализация клиентов
        self._init_clients()
    
    def _init_clients(self):
        """Инициализация клиентов для всех включённых провайдеров"""
        for name, provider in self.config['providers'].items():
            if provider.get('enabled', False):
                client = self._create_client(name, provider)
                if client:
                    self.clients[name] = client
    
    def _create_client(self, name: str, config: Dict) -> Optional[Any]:
        """Создание клиента для провайдера"""
        if name == 'gemini':
            from .gemini_client import GeminiClient
            return GeminiClient(config)
        elif name == 'openai':
            from .openai_client import OpenAIClient
            return OpenAIClient(config)
        elif name == 'anthropic':
            from .anthropic_client import AnthropicClient
            return AnthropicClient(config)
        elif name == 'local':
            from .local_client import LocalClient
            return LocalClient(config)
        return None
    
    async def generate(self, prompt: str, context: list = None, **kwargs) -> Dict:
        """
        Генерация ответа через активного провайдера
        
        Args:
            prompt: Запрос пользователя
            context: Контекст из RAG
            **kwargs: Дополнительные параметры
        
        Returns:
            Dict с ответом и метаданными
        """
        provider_name = self.active_provider
        
        if provider_name not in self.clients:
            raise ValueError(f"Provider {provider_name} not initialized")
        
        client = self.clients[provider_name]
        
        try:
            response = await client.generate(prompt, context, **kwargs)
            return {
                'answer': response['text'],
                'provider': provider_name,
                'model': self.config['providers'][provider_name]['model'],
                'sources': context or [],
                'metadata': response.get('metadata', {})
            }
        except Exception as e:
            # Fallback к другому провайдеру
            if self.config.get('fallback', {}).get('enabled', False):
                return await self._fallback_generate(prompt, context, **kwargs)
            raise e
    
    async def _fallback_generate(self, prompt: str, context: list = None, **kwargs) -> Dict:
        """Генерация через fallback провайдеры"""
        fallback_order = self.config['fallback'].get('order', [])
        retry_count = self.config['fallback'].get('retry_count', 3)
        
        for provider_name in fallback_order:
            if provider_name == self.active_provider:
                continue
            
            if provider_name not in self.clients:
                continue
            
            try:
                client = self.clients[provider_name]
                response = await client.generate(prompt, context, **kwargs)
                return {
                    'answer': response['text'],
                    'provider': provider_name,
                    'model': self.config['providers'][provider_name]['model'],
                    'sources': context or [],
                    'metadata': response.get('metadata', {})
                }
            except Exception as e:
                retry_count -= 1
                if retry_count <= 0:
                    raise e
                continue
        
        raise Exception("All providers failed")
    
    def get_active_provider(self) -> str:
        """Получить имя активного провайдера"""
        return self.active_provider
    
    def get_available_providers(self) -> list:
        """Получить список доступных провайдеров"""
        return [
            name for name, config in self.config['providers'].items()
            if config.get('enabled', False)
        ]
