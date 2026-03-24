"""Проверка GigaChat API."""
import requests

# Вставьте ваш токен здесь
AUTH_KEY = "your_gigachat_auth_key_here"

print("🔍 Проверка GigaChat API...")
print("=" * 50)

headers = {
    "Authorization": f"Bearer {AUTH_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "GigaChat",
    "messages": [
        {"role": "user", "content": "Привет! Ответь кратко, как тебя зовут?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

try:
    response = requests.post(
        "https://gigachat.devices.sberbank.ru/api/v2/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        print(f"✅ GigaChat работает!")
        print(f"💬 Ответ: {answer}")
    else:
        print(f"❌ Ошибка: {response.status_code}")
        print(f"📄 Ответ: {response.text}")
        
        if response.status_code == 401:
            print("\n⚠️ Неверный токен!")
            print("Получите новый на: https://developers.sber.ru/gigachat")
        
except requests.exceptions.ConnectionError:
    print("❌ Нет подключения к серверу GigaChat")
    print("Проверьте интернет-соединение")
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("=" * 50)
