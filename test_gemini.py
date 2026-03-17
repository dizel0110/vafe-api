"""
Проверка Gemini API ключа напрямую
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Загружаем ключ из .env.local
load_dotenv('.env.local')

api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY не найден в .env.local")
    exit(1)

print(f"✅ Ключ найден: {api_key[:15]}...")

# Инициализация
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    print("✅ Модель инициализирована (gemini-2.5-flash)")
except Exception as e:
    print(f"❌ Ошибка инициализации: {e}")
    exit(1)

# Тестовый запрос
print("\n📤 Отправка запроса...")
try:
    response = model.generate_content("Что такое вымпельный ветер? Ответь кратко в 2 предложениях.")
    print("✅ Ответ получен!")
    print(f"\n📝 Текст:\n{response.text}")
except Exception as e:
    print(f"❌ Ошибка запроса: {e}")
