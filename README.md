# 🤖 AI ChatBot на базе Google Gemini

AI-чатбот для **Telegram** и **ВКонтакте** с использованием бесплатного API Google Gemini.

## 📋 Возможности

- ✅ Работа с Telegram и ВКонтакте одновременно
- ✅ Бесплатная модель Google Gemini (gemini-2.0-flash-exp / gemini-1.5-flash)
- ✅ Поддержка контекста диалога (помнит историю сообщений)
- ✅ Команды: /start, /clear, /about, /help
- ✅ Inline-кнопки для управления
- ✅ Асинхронная обработка запросов
- ✅ Готов к развёртыванию на Railway/Render

---

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
cd ai_chatbot_bot
pip install -r requirements.txt
```

### 2. Получение API ключей

#### Google Gemini API (бесплатно)
1. Перейдите на https://makersuite.google.com/app/apikey
2. Войдите через Google аккаунт
3. Нажмите **Create API Key**
4. Скопируйте ключ

#### Telegram Bot Token
1. Откройте @BotFather в Telegram
2. Отправьте `/newbot`
3. Придумайте имя и username для бота
4. Скопируйте полученный токен

#### ВКонтакте токен
1. Откройте https://vk.com/editapp?act=create
2. Создайте приложение типа **Bot**
3. В настройках сообщества → Работа с API → Создать ключ
4. Скопируйте токен (формата `vk..._...`)

### 3. Настройка конфигурации

Создайте файл `.env` в папке проекта:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Откройте `.env` и вставьте ваши ключи:

```env
TELEGRAM_TOKEN=1234567890:AABBccDDeeFFggHHiiJJkkLLmmNNooP
VK_TOKEN=vk1.A...your_vk_token...
GEMINI_API_KEY=AIzaSy...your_gemini_key...
```

### 4. Запуск бота

```bash
# Запуск обоих ботов
python main.py

# Или только Telegram (для Railway)
python railway_bot.py

# Или только Telegram
python telegram_bot.py

# Или только ВКонтакте
python vk_bot.py
```

---

## 📁 Структура проекта

```
ai_chatbot_bot/
├── main.py              # Главный файл запуска
├── telegram_bot.py      # Telegram бот
├── vk_bot.py           # ВКонтакте бот
├── gemini_client.py    # Клиент для Gemini API
├── requirements.txt    # Зависимости
├── .env.example        # Пример конфигурации
└── README.md           # Эта инструкция
```

---

## ⚙️ Настройки

### Изменение системного промпта

Откройте `telegram_bot.py` или `vk_bot.py` и измените переменную `SYSTEM_PROMPT`:

```python
SYSTEM_PROMPT = """Ты полезный ассистент AI. Отвечай на вопросы пользователей кратко и по делу."""
```

### Выбор модели Gemini

В `gemini_client.py` измените `model_name`:

```python
# Доступные бесплатные модели:
self.model_name = "gemini-2.0-flash-exp"  # Новая экспериментальная
self.model_name = "gemini-1.5-flash"      # Стабильная быстрая
```

---

## 🎮 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Запустить бота, приветственное сообщение |
| `/clear` | Очистить историю чата |
| `/about` | Информация о боте и модели |
| `/help` | Справка по использованию |

---

## 🌐 Бесплатный хостинг

### Вариант 1: PythonAnywhere (бесплатно)
1. Зарегистрируйтесь на https://www.pythonanywhere.com
2. Загрузите файлы проекта
3. Установите зависимости: `pip install -r requirements.txt`
4. Добавьте переменные окружения в настройках
5. Запустите через консоль

### Вариант 2: Render (бесплатно)
1. Зарегистрируйтесь на https://render.com
2. Создайте новый **Web Service** или **Background Worker**
3. Подключите GitHub репозиторий
4. Добавьте переменные окружения
5. Deploy!

### Вариант 3: Hugging Face Spaces
1. Создайте Space на https://huggingface.co/spaces
2. Выберите **Docker** как среду
3. Загрузите файлы и Dockerfile
4. Добавьте secrets для API ключей

### Вариант 4: VPS (Oracle Cloud Free Tier)
1. Зарегистрируйтесь на https://www.oracle.com/cloud/free
2. Создайте бесплатный VPS (всегда бесплатно)
3. Подключитесь по SSH
4. Установите Python и зависимости
5. Запустите через `systemd` или `screen`

---

## 🔧 Docker (опционально)

Создайте `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Запуск:

```bash
docker build -t ai-chatbot .
docker run -d --env-file .env ai-chatbot
```

---

## ❓ Решение проблем

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt --upgrade
```

### "Gemini API key invalid"
- Проверьте ключ в личном кабинете Google
- Убедитесь, что нет лишних пробелов в `.env`

### "VK Token invalid"
- Токен должен начинаться с `vk` или быть в формате `..._...`
- Проверьте права доступа токена (должен быть доступ к сообщениям)

### Бот не отвечает
- Проверьте логи на наличие ошибок
- Убедитесь, что токены правильные
- Проверьте интернет-соединение

---

## 📊 Лимиты API

| API | Лимит |
|-----|-------|
| Google Gemini | 15 запросов/мин (бесплатно) |
| Telegram | 30 сообщений/сек |
| ВКонтакте | 20 сообщений/сек |

---

## 📝 Лицензия

MIT License - используйте свободно!

---

## 🤝 Поддержка

Если возникли вопросы - создайте issue в репозитории.

**Приятного использования! 🎉**
