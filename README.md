# V-AFE API

Multi-platform AI API for V-AFE Ecosystem.

## 🏗️ Архитектура

```
┌─────────────────────────────────────────┐
│  vafe-api (Vercel)                      │
│                                         │
│  /api/v1/chat      ← Чат                │
│  /api/v1/insight   ← Инсайты            │
│  /api/v1/sync      ← Синхронизация      │
│  /api/v1/analytics ← Аналитика          │
│                                         │
│  Provider Router:                       │
│  • Gemini (active)                      │
│  • OpenAI (future)                      │
│  • Anthropic (future)                   │
│  • Local LLM (future)                   │
└─────────────────────────────────────────┘
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка окружения

```bash
# .env.local
GEMINI_API_KEY=AIza...
```

### 3. Локальный запуск

```bash
vercel dev
```

### 4. Деплой

```bash
vercel --prod
```

## 📊 API Endpoints

### POST /api/v1/chat

```json
{
  "message": "Что такое вымпельный ветер?",
  "mode": "vafe",
  "context": []
}
```

**Ответ:**
```json
{
  "answer": "Вымпельный ветер — это...",
  "sources": [...],
  "provider": "gemini"
}
```

### POST /api/v1/insight

```json
{
  "session": "YAML сессия",
  "extract_insights": true
}
```

### POST /api/v1/sync

```json
{
  "sync_embeddings": true
}
```

### GET /api/v1/analytics

```json
{
  "total_requests": 1000,
  "active_users": 50
}
```

## 🔧 Конфигурация

### config/providers.json

```json
{
  "active": "gemini",
  "providers": {
    "gemini": {
      "enabled": true,
      "model": "gemini-pro",
      "rate_limit": 60
    },
    "openai": {
      "enabled": false,
      "model": "gpt-4-turbo",
      "rate_limit": 10
    }
  }
}
```

## 📁 Структура

```
vafe-api/
├── api/v1/           # API endpoints
├── lib/              # Бизнес-логика
├── config/           # Конфигурация
├── tests/            # Тесты
├── .internal/        # Внутренняя документация
└── vercel.json       # Vercel конфиг
```

## 📈 Roadmap

- [x] Создание репозитория
- [ ] Gemini интеграция
- [ ] RAG поиск
- [ ] Деплой на Vercel
- [ ] OpenAI провайдер
- [ ] Session Parser
- [ ] Analytics API

## 🔗 Связь с проектами

- **vortex-afe** — ML Core (RAG, embeddings)
- **dizel0110.github.io** — Frontend (chat widget)

## 📄 Лицензия

MIT
