"""
V-AFE API — Тестовый скрипт
Проверка работы API локально и на Vercel
"""

import requests
import json

# URL API
VERCEL_URL = "https://vafe-api.vercel.app"
LOCAL_URL = "http://127.0.0.1:8000"


def test_health(base_url: str, name: str):
    """Проверка health endpoint"""
    print(f"\n{'='*50}")
    print(f"Тест: Health check ({name})")
    print(f"{'='*50}")
    
    try:
        response = requests.get(f"{base_url}/api/v1/chat/health")
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def test_chat(base_url: str, name: str):
    """Проверка chat endpoint"""
    print(f"\n{'='*50}")
    print(f"Тест: Chat ({name})")
    print(f"{'='*50}")
    
    payload = {
        "message": "Что такое вымпельный ветер?",
        "mode": "general",
        "use_rag": False  # RAG отключён
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/chat",
            json=payload,
            timeout=30
        )
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Ответ: {data.get('answer', 'N/A')[:200]}...")
            print(f"Провайдер: {data.get('provider', 'N/A')}")
            print(f"Модель: {data.get('model', 'N/A')}")
            return True
        else:
            print(f"Ошибка: {response.text}")
            return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def test_root(base_url: str, name: str):
    """Проверка root endpoint"""
    print(f"\n{'='*50}")
    print(f"Тест: Root ({name})")
    print(f"{'='*50}")
    
    try:
        response = requests.get(f"{base_url}/")
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def main():
    """Запуск всех тестов"""
    print("\n" + "="*60)
    print("V-AFE API — Тестирование")
    print("="*60)
    
    results = {}
    
    # Тесты Vercel
    print("\n🌐 Тестирование Vercel (продакшен)")
    results['vercel_root'] = test_root(VERCEL_URL, "Vercel")
    results['vercel_health'] = test_health(VERCEL_URL, "Vercel")
    results['vercel_chat'] = test_chat(VERCEL_URL, "Vercel")
    
    # Тесты Local (опционально)
    print("\n🏠 Тестирование Local (локально)")
    print("Пропускаем (нужно запустить uvicorn отдельно)")
    
    # Итоги
    print("\n" + "="*60)
    print("Итоги:")
    print("="*60)
    
    for test, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {test}: {'PASS' if passed else 'FAIL'}")
    
    all_passed = all(results.values())
    print("\n" + "="*60)
    if all_passed:
        print("🎉 Все тесты пройдены!")
    else:
        print("⚠️  Некоторые тесты не прошли")
    print("="*60)


if __name__ == "__main__":
    main()
