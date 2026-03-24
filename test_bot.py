"""Проверка Telegram токена."""
import asyncio
from aiogram import Bot

async def test():
    token = "8547446073:AAEngENBF0JU--W7j328G9QCwsw5G49OCWQ"
    bot = Bot(token=token)
    
    try:
        info = await bot.get_me()
        print(f"✅ Бот успешно подключён!")
        print(f"   Имя: {info.first_name}")
        print(f"   Username: @{info.username}")
        print(f"   ID: {info.id}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(test())
