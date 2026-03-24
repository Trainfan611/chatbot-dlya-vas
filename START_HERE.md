# 🤖 AI TELEGRAM BOT - ГОТОВО К ЗАПУСКУ

## ✅ Что сделано:

1. **Telegram бот** создан с вашим токеном
2. **AI интеграция** через **GigaChat (Сбер)** - работает в России!
3. **Готов к деплою** на Railway/Render

---

## 🚀 СРОЧНО: Получите GigaChat токен

### Получение токена GigaChat (5 минут):

1. Перейдите на https://developers.sber.ru/
2. Войдите через **Sber ID** (телефон/email)
3. **Личный кабинет** → **Создать приложение**
4. Выберите **GigaChat** → **Подключить**
5. Скопируйте **Auth Key** (длинная строка)

**Подробная инструкция:** GIGACHAT_SETUP.md

---

## 📋 Шаг 1: Вставьте токен GigaChat

Откройте файл `.env` и вставьте ваш токен:

```
GIGACHAT_AUTH_KEY=ваш_токен_здесь
```

Или скажите мне токен, и я вставлю его.

---

## 📋 Шаг 2: Загрузите на GitHub

Запустите скрипт:
```
deploy-to-github.bat
```

Или вручную:
```bash
cd C:\Users\Dell\ai_chatbot_bot
git init
git add .
git commit -m "AI Bot with GigaChat"
git remote add origin https://github.com/ВАШ_USERNAME/ai-bot.git
git push -u origin main
```

---

## 📋 Шаг 3: Deploy на Railway

1. https://railway.app → Login with GitHub
2. New Project → Deploy from GitHub
3. Выберите репозиторий `ai-bot`
4. Variables → Добавьте:
   - `TELEGRAM_TOKEN` = `8547446073:AAEngENBF0JU--W7j328G9QCwsw5G49OCWQ`
   - `GIGACHAT_AUTH_KEY` = `ваш_токен`
5. Ждите деплой (2-5 минут)

---

## 📋 Шаг 4: Проверка

1. Откройте Telegram
2. Найдите бота по @username
3. Отправьте `/start`
4. Бот ответит!

---

## 📁 Файлы проекта

| Файл | Описание |
|------|----------|
| `railway_bot.py` | Основная версия для Railway |
| `telegram_bot.py` | Полная версия Telegram |
| `vk_bot.py` | Версия для ВКонтакте |
| `ai_client.py` | AI клиент (GigaChat/Groq/Yandex) |
| `.env` | Конфигурация |
| `requirements.txt` | Зависимости |
| `GIGACHAT_SETUP.md` | Инструкция по GigaChat |

---

## 💰 Бесплатные лимиты

| Сервис | Лимит |
|--------|-------|
| GigaChat | 100 000 токенов/мес (бесплатно) |
| Railway | $5 кредитов/месяц |
| Telegram | Безлимитно |

**100K токенов** ≈ 50 000 сообщений в месяц!

---

## 🔧 Команды бота

- `/start` - Запустить
- `/clear` - Очистить историю
- `/about` - О боте

---

## ❓ Если проблемы

### "GIGACHAT_AUTH_KEY не найден"
- Получите токен на https://developers.sber.ru/gigachat
- Вставьте в `.env`

### Бот не отвечает
- Проверьте логи Railway
- Убедитесь в правильности токена

### GigaChat ошибка
- Проверьте токен
- Убедитесь, что приложение активно

---

## 📞 Следующие шаги

1. ✅ Получите GigaChat токен
2. ✅ Вставьте в `.env`
3. ✅ Загрузите на GitHub
4. ✅ Deploy на Railway
5. ✅ Готово!

**Вопросы?** Спрашивайте! 🚀
