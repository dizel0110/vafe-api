# V-AFE API — Tests

## 🧪 Запуск тестов

### Тест API (Vercel + Local)

```powershell
cd d:\ai\vafe-api
.\venv\Scripts\Activate.ps1
python tests\test_api.py
```

**Что проверяет:**
- ✅ `/` — главная страница
- ✅ `/api/v1/chat/health` — health check
- ✅ `POST /api/v1/chat` — чат с Gemini

---

### Локальный запуск сервера

```powershell
cd d:\ai\vafe-api
.\venv\Scripts\Activate.ps1
uvicorn api.handler:app --host 0.0.0.0 --port 8000 --reload
```

После запуска:
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs (Swagger UI)

---

## 📊 Тесты

| Тест | URL | Метод |
|------|-----|-------|
| Root | `/` | GET |
| Health | `/api/v1/chat/health` | GET |
| Chat | `/api/v1/chat` | POST |

---

## 🔧 Git

**Нужно ли пушить тесты?**

- ✅ `tests/test_api.py` — **пушить** (полезно для CI/CD)
- ❌ Локальные тесты — **не пушить** (добавь в `.gitignore`)
