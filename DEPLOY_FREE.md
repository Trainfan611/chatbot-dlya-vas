# 🆓 Бесплатные альтернативы Railway

## 1. Render.com (ЛУЧШИЙ выбор - бесплатно без карты!)

### Преимущества:
- ✅ Не требует карту
- ✅ 750 часов в месяц бесплатно
- ✅ Автоматический деплой из GitHub

### Развёртывание:

1. **Зарегистрируйтесь:** https://render.com

2. **Создайте Web Service:**
   - New → **Web Service**
   - Подключите GitHub репозиторий
   - Настройки:
     ```
     Name: ai-telegram-bot
     Region: Frankfurt (ближе к России)
     Branch: main
     Root Directory: (оставьте пустым)
     Runtime: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: python railway_bot.py
     ```

3. **Добавьте переменные окружения:**
   - Environment → Add Environment Variable
   ```
   TELEGRAM_TOKEN=8547446073:AAEngENBF0JU--W7j328G9QCwsw5G49OCWQ
   GEMINI_API_KEY=AIzaSyAPtmCeedAupDyGnZedjKHrQbiID3aBCCI
   ```

4. **Deploy!**
   - Нажмите **Create Web Service**
   - Ждите ~5 минут

---

## 2. Hugging Face Spaces (полностью бесплатно)

### Преимущества:
- ✅ Полностью бесплатно
- ✅ Не требует карту
- ✅ Docker поддержка

### Развёртывание:

1. **Создайте Space:**
   - https://huggingface.co/new-space
   - Space name: `ai-telegram-bot`
   - License: MIT

2. **Создайте Dockerfile:**
   - Уже есть в проекте!

3. **Загрузите файлы:**
   ```bash
   # Установите huggingface_hub
   pip install huggingface_hub
   
   # Войдите
   huggingface-cli login
   
   # Загрузите файлы
   cd C:\Users\Dell\ai_chatbot_bot
   huggingface-cli upload your-username/ai-telegram-bot .
   ```

4. **Добавьте Secrets:**
   - Settings → **Repository Secrets**
   - Добавьте `TELEGRAM_TOKEN` и `GEMINI_API_KEY`

---

## 3. Fly.io (требуется карта)

### Развёртывание:

```bash
# Установите CLI
curl -L https://fly.io/install.sh | sh

# Войдите
fly auth login

# Инициализируйте
cd C:\Users\Dell\ai_chatbot_bot
fly launch --name ai-telegram-bot

# Установите переменные
fly secrets set TELEGRAM_TOKEN=8547446073:AAEngENBF0JU--W7j328G9QCwsw5G49OCWQ
fly secrets set GEMINI_API_KEY=AIzaSyAPtmCeedAupDyGnZedjKHrQbiID3aBCCI

# Деплой
fly deploy

# Запустите
fly apps open ai-telegram-bot
```

---

## 4. PythonAnywhere (просто, но с ограничениями)

### Развёртывание:

1. **Регистрация:** https://www.pythonanywhere.com

2. **Загрузите код:**
   - Consoles → **Bash**
   ```bash
   git clone https://github.com/your-username/ai-telegram-bot.git
   cd ai-telegram-bot
   pip install -r requirements.txt --user
   ```

3. **Запустите бота:**
   - Создайте **Scheduled Task**
   - Или запустите в консоли:
   ```bash
   python railway_bot.py
   ```

**Ограничения:**
- ❌ Бот работает только 1 час в день (бесплатно)
- ❌ Нужно запускать вручную каждый день

---

## 5. Oracle Cloud Free Tier (VPS навсегда)

### Преимущества:
- ✅ 2 VPS навсегда бесплатно
- ✅ 4 ARM ядра + 24 GB RAM
- ✅ Полноценный сервер

### Развёртывание:

1. **Регистрация:** https://www.oracle.com/cloud/free

2. **Создайте VM:**
   - Compute → Instances → **Create Instance**
   - Image: Ubuntu 22.04
   - Shape: VM.Standard.A1.Flex (бесплатно)

3. **Подключитесь по SSH:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ip
   ```

4. **Установите Python и бота:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git -y
   
   git clone https://github.com/your-username/ai-telegram-bot.git
   cd ai-telegram-bot
   pip3 install -r requirements.txt
   ```

5. **Создайте systemd сервис:**
   ```bash
   sudo nano /etc/systemd/system/telegram-bot.service
   ```
   
   ```ini
   [Unit]
   Description=AI Telegram Bot
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/ai-telegram-bot
   Environment="TELEGRAM_TOKEN=8547446073:AAEngENBF0JU--W7j328G9QCwsw5G49OCWQ"
   Environment="GEMINI_API_KEY=AIzaSyAPtmCeedAupDyGnZedjKHrQbiID3aBCCI"
   ExecStart=/usr/bin/python3 /home/ubuntu/ai-telegram-bot/railway_bot.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

6. **Запустите:**
   ```bash
   sudo systemctl enable telegram-bot
   sudo systemctl start telegram-bot
   sudo systemctl status telegram-bot
   ```

---

## 📊 Сравнение сервисов

| Сервис | Бесплатно | Карта | Лимиты | Сложность |
|--------|-----------|-------|--------|-----------|
| **Render** | ✅ 750 ч/мес | ❌ | 512 MB RAM | ⭐ Легко |
| **Railway** | $5 кредит | ✅ | 1 GB RAM | ⭐ Легко |
| **Hugging Face** | ✅ Навсегда | ❌ | 16 GB RAM | ⭐⭐ Средне |
| **Fly.io** | 3 VM | ✅ | 256 MB RAM | ⭐⭐ Средне |
| **PythonAnywhere** | ✅ 1 ч/день | ❌ | 512 MB RAM | ⭐ Легко |
| **Oracle Cloud** | ✅ Навсегда | ✅ | 24 GB RAM | ⭐⭐⭐ Сложно |

---

## 🏆 Рекомендация

**Для начала:** Используйте **Render.com** - бесплатно, не требует карту, легко настроить.

**Для продакшена:** **Oracle Cloud** - полноценный VPS навсегда.

**Для тестов:** **Hugging Face Spaces** - полностью бесплатно, Docker поддержка.

---

## 🔗 Полезные ссылки

- Render: https://render.com
- Railway: https://railway.app
- Hugging Face: https://huggingface.co/spaces
- Fly.io: https://fly.io
- Oracle Cloud: https://www.oracle.com/cloud/free
- PythonAnywhere: https://www.pythonanywhere.com
