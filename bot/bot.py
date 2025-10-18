import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os
import httpx

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-webapp.com")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Рассчитать проект", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="📞 Связаться с менеджером", callback_data="contact_manager")]
    ])
    
    await message.answer(
        "👋 Привет! Я помогу рассчитать стоимость разработки вашего IT-проекта.\n\n"
        "🔹 Мобильные приложения\n"
        "🔹 AI решения\n"
        "🔹 Web платформы\n\n"
        "Нажмите кнопку ниже для расчета:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "contact_manager")
async def contact_manager(callback: types.CallbackQuery):
    await callback.message.answer(
        "📞 Свяжитесь с нашим менеджером:\n"
        "Telegram: @manager\n"
        "Email: info@company.com\n"
        "Телефон: +7 (999) 123-45-67"
    )

async def create_lead(user_data: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{API_BASE_URL}/leads/", json=user_data)
            return response.json()
        except Exception as e:
            logging.error(f"Error creating lead: {e}")
            return None

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())