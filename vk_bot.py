"""
ВКонтакте бот с AI на базе Google Gemini.
Использует Long Polling API для получения сообщений.
"""

import asyncio
import logging
import os
import time
from typing import Optional

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotMessageEvent
from vk_api.utils import get_random_id

from gemini_client import init_gemini, get_gemini_client

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("VKBot")

# Конфигурация
VK_TOKEN = os.getenv("VK_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Системный промпт
SYSTEM_PROMPT = """Ты полезный ассистент AI. Отвечай на вопросы пользователей кратко и по делу.
Если не знаешь ответа - так и скажи. Поддерживай дружелюбный тон."""


class VKBot:
    """Класс ВКонтакте бота."""
    
    def __init__(self, token: str):
        """
        Инициализация бота.
        
        Args:
            token: Токен сообщества ВКонтакте
        """
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.longpoll: Optional[VkBotLongPoll] = None
        self.group_id = None
        
    def get_group_id(self) -> int:
        """Получить ID группы."""
        if self.group_id is None:
            try:
                groups = self.vk.method("groups.getMembers", {"group_id": self.token.split('_')[-1] if '_' in self.token else self.token})
                # Или используем метод groups.getById для получения ID
                groups_info = self.vk.method("groups.getById")
                self.group_id = groups_info['items'][0]['id']
                logger.info(f"✅ ID группы: {self.group_id}")
            except Exception as e:
                logger.warning(f"Не удалось получить ID группы автоматически: {e}")
                self.group_id = 0  # Будет установлено вручную
        return self.group_id
    
    def send_message(self, user_id: int, message: str, peer_id: Optional[int] = None):
        """
        Отправить сообщение пользователю.
        
        Args:
            user_id: ID пользователя
            message: Текст сообщения
            peer_id: ID диалога (опционально)
        """
        try:
            self.vk.method("messages.send", {
                "user_id": user_id,
                "message": message,
                "random_id": get_random_id(),
                **( {"peer_id": peer_id} if peer_id else {} )
            })
            logger.info(f"✅ Сообщение отправлено пользователю {user_id}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
    
    def send_keyboard_message(self, user_id: int, message: str, keyboard: dict):
        """Отправить сообщение с клавиатурой."""
        try:
            self.vk.method("messages.send", {
                "user_id": user_id,
                "message": message,
                "keyboard": keyboard,
                "random_id": get_random_id()
            })
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения с клавиатурой: {e}")
    
    def create_main_keyboard(self) -> dict:
        """Создать основную клавиатуру."""
        keyboard = {
            "one_time": False,
            "inline": False,
            "buttons": [
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "💬 Задать вопрос"
                        },
                        "color": "primary"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "🗑 Очистить историю"
                        },
                        "color": "negative"
                    },
                    {
                        "action": {
                            "type": "text",
                            "label": "ℹ️ О боте"
                        },
                        "color": "secondary"
                    }
                ]
            ]
        }
        return keyboard
    
    def create_inline_keyboard(self) -> dict:
        """Создать inline клавиатуру."""
        keyboard = {
            "one_time": False,
            "inline": True,
            "buttons": [
                [
                    {
                        "action": {
                            "type": "callback",
                            "label": "🗑 Очистить историю"
                        },
                        "color": "negative"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "callback",
                            "label": "ℹ️ О боте"
                        },
                        "color": "secondary"
                    }
                ]
            ]
        }
        return keyboard
    
    async def process_message(self, event: VkBotMessageEvent):
        """
        Обработка входящего сообщения.
        
        Args:
            event: Событие сообщения
        """
        user_id = event.user_id
        user_text = event.text
        
        logger.info(f"💬 Пользователь {user_id}: {user_text[:50]}...")
        
        # Команды
        if user_text.lower() in ['/start', 'старт', 'начать']:
            message = (
                f"👋 Привет! Я AI-бот на базе Google Gemini 🤖\n\n"
                f"Могу ответить на ваши вопросы, помочь с идеями или просто поболтать!\n\n"
                f"Команды:\n"
                f"/start - Запустить бота\n"
                f"/clear - Очистить историю чата\n"
                f"/about - Информация о боте\n"
                f"/help - Помощь\n\n"
                f"Просто отправьте мне сообщение, и я отвечу! 💬"
            )
            self.send_keyboard_message(user_id, message, self.create_main_keyboard())
            return
        
        if user_text.lower() in ['/clear', 'очистить', 'сброс']:
            try:
                client = get_gemini_client()
                client.clear_session(user_id)
                self.send_message(user_id, "🗑 История чата очищена!")
                logger.info(f"Пользователь {user_id} очистил историю")
            except Exception as e:
                logger.error(f"Ошибка при очистке истории: {e}")
                self.send_message(user_id, "❌ Произошла ошибка при очистке истории")
            return
        
        if user_text.lower() in ['/about', 'о боте', 'инфо']:
            try:
                client = get_gemini_client()
                stats = client.get_stats()
                message = (
                    f"🤖 AI ChatBot на базе Google Gemini\n\n"
                    f"Модель: {stats['model']}\n"
                    f"Активных сессий: {stats['active_sessions']}\n\n"
                    f"Бот использует бесплатное API Google Gemini."
                )
                self.send_message(user_id, message)
            except Exception as e:
                logger.error(f"Ошибка в /about: {e}")
                self.send_message(user_id, "ℹ️ AI-бот на базе Google Gemini")
            return
        
        if user_text.lower() in ['/help', 'помощь']:
            message = (
                f"💡 Как пользоваться ботом:\n\n"
                f"1️⃣ Просто отправьте любое сообщение - я отвечу!\n"
                f"2️⃣ Используйте '🗑 Очистить историю' для сброса контекста\n"
                f"3️⃣ Бот помнит контекст диалога для более точных ответов\n\n"
                f"Примеры запросов:\n"
                f"• Расскажи интересную историю\n"
                f"• Помоги решить задачу по математике\n"
                f"• Объясни квантовую физику простыми словами\n\n"
                f"Бот бесплатный и использует Google Gemini API"
            )
            self.send_message(user_id, message)
            return
        
        # Обработка обычного сообщения
        try:
            client = get_gemini_client()
            
            # Отправляем сообщение о наборе текста (через 1 секунду)
            await asyncio.sleep(0.5)
            
            response = await client.ask(
                user_id=user_id,
                message=user_text,
                system_prompt=SYSTEM_PROMPT
            )
            
            # Отправляем ответ с inline клавиатурой
            self.send_keyboard_message(user_id, response, self.create_inline_keyboard())
            
            logger.info(f"✅ Ответ отправлен пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения: {e}")
            self.send_message(
                user_id,
                "❌ Произошла ошибка при обработке запроса.\n"
                "Попробуйте позже или используйте /clear для сброса."
            )
    
    async def process_callback(self, event: VkBotMessageEvent):
        """
        Обработка callback запросов от inline клавиатуры.
        
        Args:
            event: Событие callback
        """
        user_id = event.user_id
        payload = event.payload
        
        if not payload:
            return
        
        action = payload.get('action')
        
        if action == 'clear_history':
            try:
                client = get_gemini_client()
                client.clear_session(user_id)
                self.send_message(user_id, "🗑 История очищена!")
                logger.info(f"Пользователь {user_id} очистил историю (callback)")
            except Exception as e:
                logger.error(f"Ошибка при очистке истории: {e}")
                self.send_message(user_id, "❌ Ошибка при очистке")
        
        elif action == 'about':
            try:
                client = get_gemini_client()
                stats = client.get_stats()
                message = (
                    f"🤖 AI ChatBot\n\n"
                    f"Модель: {stats['model']}\n"
                    f"Сессий: {stats['active_sessions']}\n\n"
                    f"Google Gemini API"
                )
                self.send_message(user_id, message)
            except Exception as e:
                logger.error(f"Ошибка в about callback: {e}")
    
    def run(self):
        """Запуск бота (синхронная версия)."""
        logger.info("🚀 Запуск ВКонтакте бота...")
        
        self.longpoll = VkBotLongPoll(self.vk, self.get_group_id())
        
        logger.info("✅ ВКонтакте бот запущен (Long Polling)")
        
        try:
            for event in self.longpoll.listen():
                if event.type == VkBotLongPoll.MESSAGE_NEW:
                    # Создаём asyncio event loop для обработки
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(self.process_message(event))
                    finally:
                        loop.close()
                        
                elif event.type == VkBotLongPoll.MESSAGE_EVENT:
                    # Обработка callback
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(self.process_callback(event))
                    finally:
                        loop.close()
                        
        except KeyboardInterrupt:
            logger.info("🛑 Бот остановлен пользователем")
        except Exception as e:
            logger.error(f"Ошибка в Long Polling: {e}")


async def main():
    """Основная функция запуска бота."""
    
    # Проверка токенов
    if not VK_TOKEN:
        logger.error("❌ VK_TOKEN не найден в переменных окружения")
        return
    
    if not GEMINI_API_KEY:
        logger.error("❌ GEMINI_API_KEY не найден в переменных окружения")
        return
    
    # Инициализация Gemini
    init_gemini(GEMINI_API_KEY)
    
    # Создание и запуск бота
    bot = VKBot(VK_TOKEN)
    
    # Запускаем в отдельном потоке
    import threading
    bot_thread = threading.Thread(target=bot.run, daemon=True)
    bot_thread.start()
    
    # Держим основной поток активным
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
