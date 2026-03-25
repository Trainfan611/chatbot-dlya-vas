"""
AI ChatBot для Railway - Telegram бот.
Использует GigaChat (Россия) + Groq (США) - работает в РФ!
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Добавляем корень проекта в path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("RailwayBot")

# Проверка переменных
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
GIGACHAT_AUTH_KEY = os.getenv("GIGACHAT_AUTH_KEY", "")
GIGACHAT_CLIENT_ID = os.getenv("GIGACHAT_CLIENT_ID", "")
GIGACHAT_SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not TELEGRAM_TOKEN:
    logger.error("❌ TELEGRAM_TOKEN не найден!")
    sys.exit(1)

# Импорты после проверки
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from ai_client import init_ai, get_ai_client

# Инициализация AI - GigaChat (основной) + Groq (резерв)
if GIGACHAT_AUTH_KEY and GIGACHAT_CLIENT_ID:
    init_ai(
        provider="gigachat",
        auth_key=GIGACHAT_AUTH_KEY,
        client_id=GIGACHAT_CLIENT_ID,
        scope=GIGACHAT_SCOPE
    )
    logger.info("✅ GigaChat (Россия) инициализирован - основная модель")
elif GROQ_API_KEY:
    init_ai(
        provider="groq",
        api_key=GROQ_API_KEY
    )
    logger.info("✅ Groq (США) инициализирован - резервная модель")
else:
    logger.error("❌ Нет доступных AI моделей!")
    sys.exit(1)

ai = get_ai_client()
logger.info(f"✅ AI модель {ai.model} ({ai.provider}) активна")

# Хранилище сессий
chat_sessions = {}

SYSTEM_PROMPT = "Ты полезный ассистент AI. Отвечай кратко и по делу. Поддерживай дружелюбный тон."

def create_main_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="🗑 Очистить историю")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def create_inline_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🗑 Очистить историю", callback_data="clear_history"))
    return builder.as_markup()

async def ask_ai(user_id: int, message: str) -> str:
    """Запрос к AI (Groq основной, GigaChat резерв)."""
    try:
        client = get_ai_client()
        
        # Groq использует асинхронный запрос через requests
        if client.provider == "groq":
            return client._ask_groq(
                client.get_session(user_id),
                message,
                SYSTEM_PROMPT
            )
        else:
            # GigaChat синхронный
            return client.ask(user_id, message, SYSTEM_PROMPT)
            
    except Exception as e:
        logger.error(f"Ошибка AI: {e}")
        return "Произошла ошибка. Попробуйте позже или используйте /clear"

async def main():
    """Запуск бота."""
    logger.info("=" * 50)
    logger.info("🤖 AI ChatBot на базе Google Gemini")
    logger.info("=" * 50)
    
    bot = Bot(
        token=TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        user = message.from_user
        logger.info(f"👤 {user.username} запустил бота")
        
        # Получаем информацию о модели
        ai_client = get_ai_client()
        model_info = ai_client.get_stats()
        
        # Определяем описание модели
        if model_info['provider'] == 'groq':
            model_desc = "Groq (США) 🇺🇸"
        else:
            model_desc = "GigaChat (Россия) 🇷🇺"

        text = (
            f"👋 <b>Привет, {user.first_name}!</b>\n\n"
            f"Я AI-бот на базе <b>{model_desc}</b> 🤖\n\n"
            f"Могу ответить на вопросы, помочь с идеями или просто поболтать!\n\n"
            f"<b>Команды:</b>\n"
            f"/clear - Очистить историю чата\n\n"
            f"💬 <b>Просто напишите сообщение - я отвечу!</b>"
        )
        await message.answer(text, reply_markup=create_main_keyboard())
    
    @dp.message(Command("clear"))
    async def cmd_clear(message: types.Message):
        # Очищаем историю пользователя
        chat_sessions[message.from_user.id] = []
        
        # Также очищаем в AI клиенте
        try:
            ai_client = get_ai_client()
            ai_client.clear_session(message.from_user.id)
        except:
            pass
        
        await message.answer("🗑 История чата очищена! Контекст сброшен.", reply_markup=create_main_keyboard())
        logger.info(f"Пользователь {message.from_user.id} очистил историю")
    
    @dp.callback_query(F.data == "clear_history")
    async def cb_clear(callback: types.CallbackQuery):
        # Очищаем историю пользователя
        chat_sessions[callback.from_user.id] = []
        
        # Также очищаем в AI клиенте
        try:
            ai_client = get_ai_client()
            ai_client.clear_session(callback.from_user.id)
        except:
            pass
        
        await callback.answer("🗑 История и контекст сброшены!", show_alert=True)
        logger.info(f"Пользователь {callback.from_user.id} очистил историю (кнопка)")
    
    @dp.message(F.text)
    async def handle_message(message: types.Message):
        user = message.from_user
        user_text = message.text

        logger.info(f"💬 {user.username}: {user_text[:50]}...")

        await bot.send_chat_action(chat_id=message.chat.id, action="typing")

        # Вызываем AI
        try:
            client = get_ai_client()
            response = client.ask(user.id, user_text, SYSTEM_PROMPT)
        except Exception as e:
            logger.error(f"Ошибка AI: {e}")
            response = "Произошла ошибка. Используйте /clear"

        # Разбиваем длинные ответы
        max_len = 4000
        for i in range(0, len(response), max_len):
            chunk = response[i:i + max_len]
            await message.answer(chunk, reply_markup=create_inline_keyboard())

        logger.info(f"✅ Ответ отправлен")
    
    # Запуск
    logger.info("🚀 Запуск бота (polling mode)...")
    
    # Для Railway: пробуем webhook, если не получится - polling
    webhook_url = os.getenv("RAILWAY_PUBLIC_URL", "")
    
    if webhook_url:
        logger.info(f"📡 Настройка webhook: {webhook_url}")
        await bot.set_webhook(webhook_url)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    else:
        logger.info("📡 Запуск в режиме polling...")
        await bot.delete_webhook()
        await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n🛑 Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
