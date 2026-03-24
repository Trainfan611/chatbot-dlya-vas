"""Проверка Gemini API ключа."""
import google.generativeai as genai

API_KEY = "AIzaSyAPtmCeedAupDyGnZedjKHrQbiID3aBCCI"

print("🔍 Проверка Gemini API ключа...")
print("=" * 50)

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    print("✅ Модель gemini-2.0-flash-exp доступна!")
    
    # Тестовый запрос
    print("\n📝 Тестовый запрос...")
    response = model.generate_content("Привет! Это тестовый запрос. Ответь кратко.")
    print(f"💬 Ответ: {response.text}")
    
    print("\n" + "=" * 50)
    print("✅ Ключ работает корректно!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("\nПопробуем запасную модель...")
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Привет! Это тестовый запрос.")
        print(f"✅ Модель gemini-1.5-flash работает!")
        print(f"💬 Ответ: {response.text}")
    except Exception as e2:
        print(f"❌ Ошибка с запасной моделью: {e2}")
        print("\n⚠️ Проверьте ключ на странице:")
        print("https://makersuite.google.com/app/apikey")
