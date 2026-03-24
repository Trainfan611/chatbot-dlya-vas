"""
Основной файл запуска для AI ChatBot.
Запускает Telegram и ВКонтакте ботов одновременно.
Поддерживает режим Railway (webhook + polling fallback).
"""

import asyncio
import logging
import os
import sys
from typing import Optional

from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("MainBot")

# Импортируем ботов
from gemini_client import init_gemini, get_gemini_client

# Проверка доступности ботов
TELEGRAM_AVAILABLE = False
VK_AVAILABLE = False

try:
    from telegram_bot import run_telegram_bot
    TELEGRAM_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Telegram бот не доступен: {e}")

try:
    from vk_bot import run_vk_bot
    VK_AVAILABLE = True
except ImportError as e:
    logger.warning(f"VK бот не доступен: {e}")


async def run_telegram_bot():
    """Запуск Telegram бота."""
    logger.info("=" * 50)
    logger.info("📱 Запуск Telegram бота...")
    logger.info("=" * 50)
    await telegram_main()


async def run_vk_bot():
    """Запуск ВКонтакте бота."""
    logger.info("=" * 50)
    logger.info("👁 Запуск ВКонтакте бота...")
    logger.info("=" * 50)
    await vk_main()


async def main():
    """Основная функция запуска."""
    
    # Проверка переменных окружения
    telegram_token = os.getenv("TELEGRAM_TOKEN", "")
    vk_token = os.getenv("VK_TOKEN", "")
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    
    logger.info("🤖 AI ChatBot - Google Gemini")
    logger.info("=" * 50)
    
    if not gemini_api_key:
        logger.error("❌ GEMINI_API_KEY не найден!")
        logger.info("Получите ключ здесь: https://makersuite.google.com/app/apikey")
        return
    
    # Инициализация Gemini
    init_gemini(gemini_api_key)
    logger.info("✅ Google Gemini инициализирован")
    
    # Проверяем, какие боты запускать
    run_telegram = bool(telegram_token)
    run_vk = bool(vk_token)
    
    if not run_telegram and not run_vk:
        logger.error("❌ Не найдены токены для ботов!")
        logger.info("Установите TELEGRAM_TOKEN и/или VK_TOKEN в .env файле")
        return
    
    logger.info(f"Telegram бот: {'✅' if run_telegram else '❌'}")
    logger.info(f"ВКонтакте бот: {'✅' if run_vk else '❌'}")
    logger.info("=" * 50)
    
    # Запускаем выбранные задачи
    tasks = []
    
    if run_telegram:
        tasks.append(run_telegram_bot())
    
    if run_vk:
        tasks.append(run_vk_bot())
    
    # Запускаем все задачи параллельно
    if tasks:
        logger.info("🚀 Запуск всех ботов...")
        await asyncio.gather(*tasks, return_exceptions=True)
    else:
        logger.error("❌ Нет активных ботов для запуска")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n🛑 Боты остановлены пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
