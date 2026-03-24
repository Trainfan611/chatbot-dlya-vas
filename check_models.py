"""Проверка доступных моделей Gemini."""
import google.generativeai as genai

API_KEY = "AIzaSyAPtmCeedAupDyGnZedjKHrQbiID3aBCCI"

print("🔍 Проверка доступных моделей...")
print("=" * 50)

genai.configure(api_key=API_KEY)

# Получаем список моделей
print("📋 Доступные модели:\n")

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
except Exception as e:
    print(f"Ошибка: {e}")

print("\n" + "=" * 50)

# Пробуем использовать gemini-pro
print("\n📝 Тест с gemini-pro...")
try:
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Привет! Ответь кратко.")
    print(f"✅ gemini-pro работает!")
    print(f"💬 Ответ: {response.text}")
except Exception as e:
    print(f"❌ gemini-pro: {e}")
