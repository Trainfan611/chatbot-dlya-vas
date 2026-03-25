"""
AI ChatBot для Railway - только Telegram бот.
Использует GigaChat (Сбер) - работает в РФ!
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

if not TELEGRAM_TOKEN:
    logger.error("❌ TELEGRAM_TOKEN не найден!")
    sys.exit(1)

if not GIGACHAT_AUTH_KEY:
    logger.error("❌ GIGACHAT_AUTH_KEY не найден!")
    logger.info("Получите токен: https://developers.sber.ru/gigachat")
    sys.exit(1)

# Импорты после проверки
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from ai_client import init_ai, get_ai_client

# Инициализация GigaChat с OAuth
init_ai(
    provider="gigachat",
    auth_key=GIGACHAT_AUTH_KEY,
    client_id=GIGACHAT_CLIENT_ID,
    scope=GIGACHAT_SCOPE
)
ai = get_ai_client()
logger.info(f"✅ AI модель {ai.model} ({ai.provider}) инициализирована")

# Хранилище сессий
chat_sessions = {}

SYSTEM_PROMPT = "Ты полезный ассистент AI. Отвечай кратко и по делу. Поддерживай дружелюбный тон."

def create_main_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="💬 Задать вопрос")],
        [types.KeyboardButton(text="🗑 Очистить историю"), types.KeyboardButton(text="ℹ️ О боте")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def create_inline_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🗑 Очистить историю", callback_data="clear_history"))
    builder.row(types.InlineKeyboardButton(text="ℹ️ О боте", callback_data="about"))
    return builder.as_markup()

async def ask_ai(user_id: int, message: str) -> str:
    """Запрос к AI (GigaChat)."""
    try:
        client = get_ai_client()
        # GigaChat использует синхронный метод
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

        text = (
            f"👋 <b>Привет, {user.first_name}!</b>\n\n"
            f"Я AI-бот на базе <b>GigaChat (Сбер)</b> 🤖\n\n"
            f"Могу ответить на вопросы, помочь с идеями или просто поболтать!\n\n"
            f"<b>Команды:</b>\n"
            f"/start - Запустить бота\n"
            f"/clear - Очистить историю\n"
            f"/about - О боте\n\n"
            f"Просто отправьте сообщение! 💬"
        )
        await message.answer(text, reply_markup=create_main_keyboard())
    
    @dp.message(Command("clear"))
    async def cmd_clear(message: types.Message):
        chat_sessions[message.from_user.id] = []
        await message.answer("🗑 История очищена!", reply_markup=create_main_keyboard())
        logger.info(f"Пользователь {message.from_user.id} очистил историю")
    
    @dp.message(Command("about"))
    async def cmd_about(message: types.Message):
        ai_client = get_ai_client()
        stats = ai_client.get_stats()
        
        text = (
            f"<b>🤖 AI ChatBot</b>\n\n"
            f"Модель: {stats['model']}\n"
            f"Провайдер: {stats['provider']}\n"
            f"Активных чатов: {len(chat_sessions)}\n\n"
            f"<i>GigaChat API (Сбер, РФ)</i>"
        )
        await message.answer(text)

    @dp.callback_query(F.data == "clear_history")
    async def cb_clear(callback: types.CallbackQuery):
        chat_sessions[callback.from_user.id] = []
        await callback.answer("🗑 История очищена!", show_alert=True)

    @dp.callback_query(F.data == "about")
    async def cb_about(callback: types.CallbackQuery):
        ai_client = get_ai_client()
        stats = ai_client.get_stats()
        text = f"<b>AI ChatBot</b>\n\nМодель: {stats['model']}\nПровайдер: {stats['provider']}\nЧатов: {len(chat_sessions)}"
        await callback.message.answer(text)
    
    @dp.message(F.text)
    async def handle_message(message: types.Message):
        user = message.from_user
        user_text = message.text
        
        logger.info(f"💬 {user.username}: {user_text[:50]}...")
        
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        response = await ask_ai(user.id, user_text)
        
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
