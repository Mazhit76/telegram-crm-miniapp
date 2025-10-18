from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    """Обработчик команды /start"""
    user = message.from_user
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Наши услуги", callback_data="services")],
        [InlineKeyboardButton(text="💬 Задать вопрос AI", callback_data="ask_ai")],
        [InlineKeyboardButton(text="📱 Заказать разработку", callback_data="order")],
        [InlineKeyboardButton(text="📋 Заполнить бриф", web_app=WebAppInfo(url="https://testcrm.ananas.guru/miniapp/business-brief.html"))]
    ])
    
    welcome_text = f"""👋 Привет, {user.first_name}!

Я AI-консультант компании ananas.guru - мы создаем:
• 📱 Мобильные приложения
• 🌐 Веб-сайты и сервисы  
• 🤖 AI решения и боты

Чем могу помочь?"""
    
    await message.answer(welcome_text, reply_markup=keyboard)

@router.callback_query(F.data == "services")
async def services_handler(callback):
    """Показать услуги"""
    services_text = """🚀 **Наши услуги:**

📱 **Мобильные приложения** - от 100,000₽
🌐 **Веб-разработка** - от 50,000₽  
🤖 **AI решения** - от 80,000₽
🔗 **Интеграции** - от 30,000₽"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📞 Консультация", callback_data="consultation")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])
    
    await callback.message.edit_text(services_text, reply_markup=keyboard, parse_mode="Markdown")

@router.callback_query(F.data == "ask_ai")
async def ask_ai_handler(callback):
    """Режим вопросов AI"""
    await callback.message.edit_text(
        "🤖 Задайте любой вопрос о разработке, технологиях или наших услугах.\n\nЯ отвечу с помощью AI!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ])
    )

@router.callback_query(F.data == "order")
async def order_handler(callback):
    """Заказ разработки"""
    await callback.message.edit_text(
        "📱 Опишите вашу задачу и мы свяжемся с вами!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ])
    )

@router.callback_query(F.data == "consultation")
async def consultation_handler(callback):
    """Консультация"""
    await callback.message.edit_text(
        "📞 **Бесплатная консультация**\n\nОпишите вашу задачу в чате, и наш менеджер свяжется с вами в течение часа!\n\nИли звоните: +7 (XXX) XXX-XX-XX",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ]),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "back")
async def back_handler(callback):
    """Возврат в главное меню"""
    await start_handler(callback.message)