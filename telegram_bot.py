"""
Telegram бот с AI на базе Google Gemini.
"""

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from gemini_client import init_gemini, get_gemini_client

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TelegramBot")

# Конфигурация
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Системный промпт (можно изменить)
SYSTEM_PROMPT = """Ты полезный ассистент AI. Отвечай на вопросы пользователей кратко и по делу. 
Если не знаешь ответа - так и скажи. Поддерживай дружелюбный тон."""


def create_main_keyboard() -> types.ReplyKeyboardMarkup:
    """Создать основную клавиатуру."""
    kb = [
        [types.KeyboardButton(text="💬 Задать вопрос")],
        [types.KeyboardButton(text="🗑 Очистить историю"), types.KeyboardButton(text="ℹ️ О боте")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def create_inline_keyboard() -> types.InlineKeyboardMarkup:
    """Создать inline клавиатуру для ответов."""
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🗑 Очистить историю", callback_data="clear_history"))
    builder.row(types.InlineKeyboardButton(text="ℹ️ О боте", callback_data="about"))
    return builder.as_markup()


async def main():
    """Основная функция запуска бота."""
    
    # Проверка токенов
    if not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN не найден в переменных окружения")
        return
    
    if not GEMINI_API_KEY:
        logger.error("❌ GEMINI_API_KEY не найден в переменных окружения")
        return
    
    # Инициализация Gemini
    init_gemini(GEMINI_API_KEY)
    
    # Инициализация бота
    bot = Bot(
        token=TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    logger.info("✅ Telegram бот инициализирован")
    
    # ==================== ОБРАБОТЧИКИ ====================
    
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        """Команда /start."""
        user = message.from_user
        logger.info(f"👤 Пользователь {user.username} запустил бота")
        
        text = (
            f"👋 <b>Привет, {user.first_name}!</b>\n\n"
            f"Я AI-бот на базе <b>Google Gemini</b> 🤖\n\n"
            f"Могу ответить на ваши вопросы, помочь с идеями или просто поболтать!\n\n"
            f"<b>Команды:</b>\n"
            f"/start - Запустить бота\n"
            f"/clear - Очистить историю чата\n"
            f"/about - Информация о боте\n"
            f"/help - Помощь\n\n"
            f"Просто отправьте мне сообщение, и я отвечу! 💬"
        )
        
        await message.answer(text, reply_markup=create_main_keyboard())
    
    @dp.message(Command("clear"))
    async def cmd_clear(message: types.Message):
        """Команда /clear - очистка истории."""
        try:
            client = get_gemini_client()
            client.clear_session(message.from_user.id)
            await message.answer("🗑 История чата очищена!", reply_markup=create_main_keyboard())
            logger.info(f"Пользователь {message.from_user.id} очистил историю")
        except Exception as e:
            logger.error(f"Ошибка при очистке истории: {e}")
            await message.answer("❌ Произошла ошибка при очистке истории")
    
    @dp.message(Command("about"))
    async def cmd_about(message: types.Message):
        """Команда /about - информация о боте."""
        try:
            client = get_gemini_client()
            stats = client.get_stats()
            
            text = (
                f"<b>🤖 AI ChatBot на базе Google Gemini</b>\n\n"
                f"<b>Модель:</b> {stats['model']}\n"
                f"<b>Активных сессий:</b> {stats['active_sessions']}\n\n"
                f"Бот использует бесплатное API Google Gemini для генерации ответов.\n\n"
                f"<i>Создано для Telegram и ВКонтакте</i>"
            )
            
            await message.answer(text)
        except Exception as e:
            logger.error(f"Ошибка в /about: {e}")
            await message.answer("ℹ️ AI-бот на базе Google Gemini")
    
    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        """Команда /help - помощь."""
        text = (
            f"<b>💡 Как пользоваться ботом:</b>\n\n"
            f"1️⃣ Просто отправьте любое сообщение - я отвечу!\n"
            f"2️⃣ Используйте кнопку '🗑 Очистить историю' для сброса контекста\n"
            f"3️⃣ Бот помнит контекст диалога для более точных ответов\n\n"
            f"<b>Примеры запросов:</b>\n"
            f"• Расскажи интересную историю\n"
            f"• Помоги решить задачу по математике\n"
            f"• Объясни квантовую физику простыми словами\n"
            f"• Напиши код для...\n\n"
            f"<i>Бот бесплатный и использует Google Gemini API</i>"
        )
        await message.answer(text)
    
    @dp.callback_query(F.data == "clear_history")
    async def cb_clear_history(callback: types.CallbackQuery):
        """Очистка истории через inline кнопку."""
        try:
            client = get_gemini_client()
            client.clear_session(callback.from_user.id)
            await callback.answer("🗑 История очищена!", show_alert=True)
            logger.info(f"Пользователь {callback.from_user.id} очистил историю (inline)")
        except Exception as e:
            logger.error(f"Ошибка при очистке истории: {e}")
            await callback.answer("❌ Ошибка при очистке", show_alert=True)
    
    @dp.callback_query(F.data == "about")
    async def cb_about(callback: types.CallbackQuery):
        """Инфо через inline кнопку."""
        try:
            client = get_gemini_client()
            stats = client.get_stats()
            
            text = (
                f"<b>🤖 AI ChatBot</b>\n\n"
                f"Модель: {stats['model']}\n"
                f"Сессий: {stats['active_sessions']}\n\n"
                f"<i>Google Gemini API</i>"
            )
            await callback.message.answer(text)
        except Exception as e:
            logger.error(f"Ошибка в about callback: {e}")
    
    @dp.message(F.text)
    async def handle_message(message: types.Message):
        """Обработка обычных сообщений."""
        user = message.from_user
        user_text = message.text
        
        logger.info(f"💬 Пользователь {user.id}: {user_text[:50]}...")
        
        # Отправляем индикатор набора текста
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        try:
            # Получаем ответ от Gemini
            client = get_gemini_client()
            response = await client.ask(
                user_id=user.id,
                message=user_text,
                system_prompt=SYSTEM_PROMPT
            )
            
            # Отправляем ответ (разбиваем на части если длинный)
            max_length = 4000
            for i in range(0, len(response), max_length):
                chunk = response[i:i + max_length]
                await message.answer(chunk, reply_markup=create_inline_keyboard())
            
            logger.info(f"✅ Ответ отправлен пользователю {user.id}")
            
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения: {e}")
            await message.answer(
                "❌ Произошла ошибка при обработке запроса.\n"
                "Попробуйте позже или используйте /clear для сброса.",
                reply_markup=create_main_keyboard()
            )
    
    # ==================== ЗАПУСК ====================
    
    logger.info("🚀 Запуск Telegram бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
