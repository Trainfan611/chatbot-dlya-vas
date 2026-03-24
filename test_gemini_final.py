"""Проверка Gemini API с авто-выбором модели."""
import asyncio
import google.generativeai as genai

API_KEY = "AIzaSyAPtmCeedAupDyGnZedjKHrQbiID3aBCCI"

print("🔍 Проверка Gemini API...")
print("=" * 50)

genai.configure(api_key=API_KEY)

# Проверяем доступные модели
print("\n📋 Проверка моделей...\n")

models_to_try = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b", 
    "gemini-pro"
]

selected_model = None

for model_name in models_to_try:
    try:
        print(f"  Проверяю {model_name}...", end=" ")
        model = genai.GenerativeModel(model_name)
        # Пробуем сделать тестовый запрос
        response = model.generate_content("Hi", generation_config=genai.types.GenerationConfig(max_output_tokens=10))
        print(f"✅ OK")
        selected_model = model_name
        break
    except Exception as e:
        print(f"❌ Недоступна")

if not selected_model:
    print("\n❌ Ни одна модель не доступна!")
    print("\nВозможные причины:")
    print("  1. API ключ неверный")
    print("  2. API не активирован в Google Cloud")
    print("  3. Регион не поддерживается (нужен прокси)")
else:
    print(f"\n✅ Выбрана модель: {selected_model}")
    print("\n📝 Тестовый запрос...")
    
    model = genai.GenerativeModel(selected_model)
    chat = model.start_chat()
    response = chat.send_message("Привет! Напиши краткое приветствие.")
    print(f"💬 Ответ: {response.text}")
    
    print("\n" + "=" * 50)
    print("✅ Gemini готов к работе!")
    print(f"   Модель: {selected_model}")
    print(f"   API Key: {API_KEY[:20]}...")
