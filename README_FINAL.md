# 🤖 AI TELEGRAM BOT - Gemini + GigaChat

## ✅ Что сделано:

1. **Telegram бот** с вашим токеном
2. **AI:** Gemini (основной) + GigaChat/Groq (резерв)
3. **Готов к деплою** на Railway

---

## ⚙️ Настройка AI

### Вариант 1: Google Gemini (основной)

**Получите ключ:**
1. Откройте https://aistudio.google.com/app/apikey
2. Войдите через Google
3. Нажмите **Create API Key**
4. Скопируйте ключ

**Вставьте в `.env`:**
```env
GEMINI_API_KEY=AIzaSy...ваш_ключ...
```

**Примечание:** Gemini может требовать прокси в РФ. Если не работает - используйте GigaChat.

---

### Вариант 2: GigaChat (для РФ)

**Получите токен:**
1. Откройте https://developers.sber.ru/gigachat
2. Войдите через Sber ID
3. Создайте приложение → GigaChat
4. Скопируйте Auth Key

**Вставьте в `.env`:**
```env
GIGACHAT_AUTH_KEY=ваш_токен...
```

---

### Вариант 3: Groq (быстрый, для РФ)

**Получите ключ:**
1. Откройте https://console.groq.com/keys
2. Войдите через GitHub/Google
3. Создайте ключ
4. Скопируйте (начинается с `gsk_`)

**Вставьте в `.env`:**
```env
GROQ_API_KEY=gsk_...
```

---

## 🚀 Деплой

### 1. Загрузите на GitHub

```bash
cd C:\Users\Dell\ai_chatbot_bot
deploy-to-github.bat
```

### 2. Deploy на Railway

1. https://railway.app → Login with GitHub
2. New Project → Ваш репозиторий
3. Variables → Добавьте:
   - `TELEGRAM_TOKEN` = `8547446073:AAEngENBF0JU--W7j328G9QCwsw5G49OCWQ`
   - `GEMINI_API_KEY` = `AIzaSyAPtmCeedAupDyGnZedjKHrQbiID3aBCCI`
4. Deploy!

---

## 📁 Файлы

| Файл | Описание |
|------|----------|
| `railway_bot.py` | Telegram бот с AI |
| `ai_client.py` | AI клиент (Gemini/GigaChat/Groq) |
| `.env` | Конфигурация |
| `test_gemini_final.py` | Тест Gemini |
| `test_gigachat.py` | Тест GigaChat |

---

## 🔧 Переключение AI

В `railway_bot.py` измените:

```python
# Gemini
init_ai(provider="gemini", api_key=GEMINI_API_KEY)

# Или GigaChat
init_ai(provider="gigachat", auth_key=GIGACHAT_AUTH_KEY)

# Или Groq
init_ai(provider="groq", api_key=GROQ_API_KEY)
```

---

## 💰 Бесплатные лимиты

| AI | Лимит |
|----|-------|
| Gemini | 15 запросов/мин |
| GigaChat | 100K токенов/мес |
| Groq | 30 запросов/мин |

---

## ❓ Проблемы

### Gemini не отвечает
- API может требовать прокси в РФ
- Используйте GigaChat или Groq

### "Module not found"
```bash
pip install -r requirements.txt
```

---

**Готово!** 🎉
