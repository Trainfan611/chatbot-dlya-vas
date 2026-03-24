# 🚀 Развёртывание на Railway (бесплатно)

## Шаг 1: Подготовка проекта на GitHub

1. **Создайте репозиторий на GitHub:**
   - Зайдите на https://github.com
   - Нажмите **New** → Создайте репозиторий (например, `ai-telegram-bot`)
   - Сделайте его **Public**

2. **Загрузите файлы проекта:**

   ```bash
   cd C:\Users\Dell\ai_chatbot_bot
   
   # Инициализация git
   git init
   git add .
   git commit -m "Initial commit - AI Telegram Bot"
   
   # Подключите ваш репозиторий (замените URL на свой)
   git remote add origin https://github.com/ВАШ_USERNAME/ai-telegram-bot.git
   git push -u origin main
   ```

   **Или через GitHub Desktop:**
   - Скачайте https://desktop.github.com
   - Добавьте папку `ai_chatbot_bot`
   - Сделайте commit и push

---

## Шаг 2: Развёртывание на Railway

### Вариант A: Через GitHub (рекомендуется)

1. **Зайдите на Railway:**
   - Перейдите на https://railway.app
   - Войдите через GitHub

2. **Создайте новый проект:**
   - Нажмите **New Project**
   - Выберите **Deploy from GitHub repo**
   - Найдите ваш репозиторий `ai-telegram-bot`

3. **Настройте переменные окружения:**
   - В панели проекта нажмите **Variables**
   - Добавьте переменные:
     ```
     TELEGRAM_TOKEN=8547446073:AAEngENBF0JU--W7j328G9QCwsw5G49OCWQ
     GEMINI_API_KEY=AIzaSyAPtmCeedAupDyGnZedjKHrQbiID3aBCCI
     ```

4. **Запустите деплой:**
   - Railway автоматически начнёт сборку
   - Дождитесь статуса **Deployed**

### Вариант B: Через Railway CLI

```bash
# Установите Railway CLI
npm install -g @railway/cli

# Войдите
railway login

# Инициализируйте проект
cd C:\Users\Dell\ai_chatbot_bot
railway init

# Создайте сервис
railway up

# Добавьте переменные
railway variables set TELEGRAM_TOKEN=8547446073:AAEngENBF0JU--W7j328G9QCwsw5G49OCWQ
railway variables set GEMINI_API_KEY=AIzaSyAPtmCeedAupDyGnZedjKHrQbiID3aBCCI

# Деплой
railway up --detach
```

---

## Шаг 3: Проверка работы

1. **Найдите URL вашего бота:**
   - В панели Railway → Settings → **Public URL**
   - Или в вкладке **Deployments**

2. **Проверьте логи:**
   - В панели Railway → **Deployments** → **View Logs**

3. **Протестируйте бота:**
   - Откройте вашего бота в Telegram
   - Отправьте `/start`
   - Задайте любой вопрос

---

## 🔧 Настройка домена (опционально)

Railway предоставляет бесплатный домен вида:
```
your-project-production.up.railway.app
```

Для кастомного домена:
1. Settings → **Domains**
2. Добавьте свой домен
3. Настройте DNS записи

---

## 💰 Бесплатный тариф Railway

- **$5 кредитов в месяц** (хватает для небольшого бота)
- **500 часов работы** в месяц
- **1 ГБ RAM**
- **1 CPU**

**Важно:** Railway больше не предоставляет полностью бесплатный тариф без привязки карты. 
Но $5 кредитов хватает на ~2-3 недели работы бота.

---

## 🆓 Альтернативы Railway (полностью бесплатно)

### 1. Render.com
- Бесплатный тариф без карты
- Web-сервисы + Background Workers
- https://render.com

### 2. Fly.io
- 3 бесплатных VM (shared CPU)
- Требуется карта
- https://fly.io

### 3. Hugging Face Spaces
- Полностью бесплатно
- Docker-контейнеры
- https://huggingface.co/spaces

### 4. Oracle Cloud Free Tier
- Всегда бесплатный VPS
- Требуется карта
- https://oracle.com/cloud/free

### 5. PythonAnywhere
- Бесплатный хостинг Python
- Ограничения по времени
- https://pythonanywhere.com

---

## 📝 Решение проблем

### Бот не запускается
- Проверьте логи в Railway
- Убедитесь, что переменные окружения установлены
- Проверьте `requirements.txt`

### Ошибка "Module not found"
```bash
# Убедитесь, что requirements.txt содержит:
pip install -r requirements.txt
```

### Бот не отвечает
- Проверьте, что токен правильный
- Проверьте логи на ошибки API
- Убедитесь, что бот добавлен в Telegram через @BotFather

### Railway требует карту
- Это нормально для Railway
- $5 кредитов даётся сразу
- Можно использовать альтернативы выше

---

## 🎉 Готово!

Ваш бот работает на бесплатном сервере Railway!

**URL бота:** https://your-project.up.railway.app

**Telegram:** @your_bot_username
