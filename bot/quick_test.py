"""Быстрый тест запуска бота"""
import asyncio
from aiogram import Bot
from config import settings

async def test_bot_token():
    """Тест токена бота"""
    try:
        bot = Bot(token=settings.bot_token)
        me = await bot.get_me()
        print(f"Bot OK: @{me.username} ({me.first_name})")
        await bot.session.close()
        return True
    except Exception as e:
        print(f"Bot Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_bot_token())