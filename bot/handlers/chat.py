from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from services.ai_agent import ai_agent
from services.crm_client import crm_client
from services.telegram_client import telegram_client_service
from utils.security import SecurityValidator
from utils.safe_print import safe_print

router = Router()

@router.message(F.contact)
async def contact_handler(message: Message):
    """Обработка контактов"""
    contact = message.contact
    user = message.from_user
    
    try:
        # Обновляем контактные данные в CRM
        await telegram_client_service.update_client_contact(
            telegram_id=user.id,
            phone=contact.phone_number,
            name=f"{contact.first_name} {contact.last_name or ''}".strip()
        )
        
        await message.answer(
            f"✅ Спасибо! Контакт сохранен:\n"
            f"📞 {contact.phone_number}\n"
            f"👤 {contact.first_name} {contact.last_name or ''}\n\n"
            "Менеджер свяжется с вами в ближайшее время!",
            reply_markup=ReplyKeyboardRemove()
        )
        
    except Exception as e:
        safe_print(f"Contact handler error: {e}")
        await message.answer(
            "✅ Контакт получен! Менеджер свяжется с вами.",
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(F.text)
async def chat_handler(message: Message):
    """Обработка текстовых сообщений через AI"""
    user = message.from_user
    
    try:
        # Валидация и очистка входных данных
        if not SecurityValidator.validate_telegram_id(user.id):
            return
        
        text = SecurityValidator.sanitize_text(message.text)
        username = SecurityValidator.sanitize_username(user.username)
        
        if not text:
            await message.answer("Пожалуйста, отправьте текстовое сообщение.")
            return
        
        # Проверяем номер телефона в сообщении
        import re
        phone_pattern = r'\+?[78][-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}'
        phone_match = re.search(phone_pattern, text)
        
        if phone_match:
            phone_number = phone_match.group()
            await telegram_client_service.update_client_contact(
                telegram_id=user.id,
                phone=phone_number
            )
            await message.answer(f"📞 Номер {phone_number} сохранен!")
        
        # Проверяем на ключевые слова для лидогенерации
        lead_keywords = ["заказать", "разработка", "сделать", "создать", "цена", "стоимость", "консультация"]
        is_potential_lead = any(keyword in text.lower() for keyword in lead_keywords)
        
        # Получаем ответ от AI
        ai_response = await ai_agent.chat_response(text, {"user_id": user.id, "username": username})
        
        await message.answer(ai_response)
        
        # Если потенциальный лид - создаем обращение в CRM
        if is_potential_lead:
            # Создаем/обновляем Telegram клиента
            telegram_client = await telegram_client_service.create_or_update_client(user)
            
            if telegram_client:
                # Создаем обращение для клиента
                appeal_result = await crm_client.create_appeal_for_client(
                    telegram_client_id=telegram_client["id"],
                    message=f"Сообщение: {text}\nКонтакт: @{username if username != 'anonymous' else 'ID: ' + str(user.id)}",
                    object_title="Консультация по разработке"
                )
                
                if appeal_result:
                    from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
                    
                    contact_kb = ReplyKeyboardMarkup(
                        keyboard=[[KeyboardButton(text="📞 Поделиться контактом", request_contact=True)]],
                        resize_keyboard=True,
                        one_time_keyboard=True
                    )
                    
                    await message.answer(
                        f"✅ Заявка передана менеджеру!\n\n"
                        f"🆔 ID: `{appeal_result.get('id', 'N/A')}`\n\n"
                        "📞 Поделитесь контактом для быстрой связи:",
                        parse_mode="Markdown",
                        reply_markup=contact_kb
                    )
                else:
                    # Fallback к старому методу
                    contact_info = f"@{username}" if username != "anonymous" else f"ID: {user.id}"
                    await crm_client.create_appeal(
                        telegram_id=user.id,
                        message=text,
                        contact_info=contact_info
                    )
                    
                    from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
                    
                    contact_kb = ReplyKeyboardMarkup(
                        keyboard=[[KeyboardButton(text="📞 Поделиться контактом", request_contact=True)]],
                        resize_keyboard=True,
                        one_time_keyboard=True
                    )
                    
                    await message.answer(
                        "✅ Заявка передана!\n\n"
                        "📞 Поделитесь контактом:",
                        reply_markup=contact_kb
                    )
            else:
                # Fallback к старому методу
                contact_info = f"@{username}" if username != "anonymous" else f"ID: {user.id}"
                await crm_client.create_appeal(
                    telegram_id=user.id,
                    message=text,
                    contact_info=contact_info
                )
                await message.answer(
                    "Я передал вашу заявку менеджеру. Мы свяжемся с вами!"
                )
    
    except Exception as e:
        safe_print(f"Chat handler error: {e}")
        await message.answer("Произошла ошибка. Попробуйте еще раз или напишите на admin@ananas.guru")