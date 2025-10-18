from aiogram import Router, F
from aiogram.types import Message
import json
from services.crm_client import crm_client
from services.telegram_client import telegram_client_service
from utils.safe_print import safe_print
from utils.brief_helpers import get_project_type_title, parse_budget

router = Router()

@router.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    """Обработка данных из Web App"""
    try:
        # Получаем данные из Web App
        webapp_data = json.loads(message.web_app_data.data)
        user = message.from_user
        
        safe_print(f"Received webapp data from user {user.id}: {webapp_data}")
        
        # Создаем/обновляем Telegram клиента с контактными данными
        telegram_client = await telegram_client_service.create_or_update_client(user)
        
        # Обновляем контактные данные из брифа
        if telegram_client and (webapp_data.get('clientName') or webapp_data.get('phone')):
            await telegram_client_service.update_client_contact(
                telegram_id=user.id,
                phone=webapp_data.get('phone'),
                name=webapp_data.get('clientName')
            )
        
        # Формируем детальное описание для CRM
        brief_description = format_brief_for_crm(webapp_data)
        
        # Определяем тип проекта и бюджет
        project_type = get_project_type_title(webapp_data.get('appTypes', []))
        budget_amount = parse_budget(webapp_data.get('budget', '0'))
        
        # Создаем обращение в CRM
        appeal_result = None
        if telegram_client:
            appeal_result = await crm_client.create_appeal_for_client(
                telegram_client_id=telegram_client["id"],
                message=brief_description,
                object_title=project_type or "Разработка приложения",
                price=budget_amount
            )
        
        # Fallback к старому методу если новый не сработал
        if not appeal_result:
            contact_info = f"@{user.username}" if user.username else f"ID: {user.id}"
            if webapp_data.get('phone'):
                contact_info += f", тел: {webapp_data['phone']}"
            
            appeal_result = await crm_client.create_appeal(
                telegram_id=user.id,
                message=brief_description,
                contact_info=contact_info
            )
        
        if appeal_result:
            # Успешно создано обращение
            await message.answer(
                f"✅ **Бриф получен!**\n\n"
                f"Спасибо, {webapp_data.get('clientName', 'за заявку')}!\n\n"
                f"📋 Ваш бриф передан нашим экспертам\n"
                f"📞 Мы свяжемся с вами в течение 2 часов\n"
                f"💼 ID заявки: `{appeal_result.get('id', 'N/A')}`\n\n"
                f"Если у вас есть дополнительные вопросы, просто напишите их в этом чате.",
                parse_mode="Markdown"
            )
        else:
            # Ошибка создания обращения
            await message.answer(
                "❌ Произошла ошибка при сохранении брифа.\n\n"
                "Пожалуйста, свяжитесь с нами напрямую:\n"
                "📧 admin@ananas.guru\n"
                "📞 +7 (XXX) XXX-XX-XX"
            )
            
    except Exception as e:
        safe_print(f"WebApp data processing error: {e}")
        await message.answer(
            "❌ Ошибка обработки данных.\n\n"
            "Попробуйте отправить бриф еще раз или свяжитесь с нами напрямую."
        )

def format_brief_for_crm(data):
    """Форматирование данных брифа для CRM"""
    
    # Типы приложений
    app_types = ", ".join(data.get('appTypes', []))
    if data.get('customAppType'):
        app_types += f", {data['customAppType']}"
    
    # Аналоги
    analogs = ", ".join(data.get('analogs', []))
    
    # Технические фишки
    tech_features = ", ".join(data.get('techFeatures', []))
    
    # Бизнес-цели
    business_goals = ", ".join(data.get('businessGoals', []))
    
    # Файлы
    files_info = ""
    if data.get('files'):
        files_list = [f['name'] for f in data['files']]
        files_info = f"\nПриложенные файлы: {', '.join(files_list)}"
    
    brief_text = f"""
БРИФ НА РАЗРАБОТКУ ПРИЛОЖЕНИЯ

Клиент: {data.get('clientName', 'Не указано')}
Телефон: {data.get('phone', 'Не указан')}

Тип приложения: {app_types or 'Не указано'}

Похожие приложения: {analogs or 'Не указано'}

Технические функции: {tech_features or 'Не указано'}

Бизнес-цели: {business_goals or 'Не указано'}

Описание проекта:
{data.get('projectDescription', 'Не указано')}

Бюджет: {data.get('budget', 'Не указан')}
Сроки: {data.get('timeline', 'Не указаны')}{files_info}

Дата подачи: {data.get('submitted_at', 'Не указана')}
Источник: Telegram Mini App
"""
    
    return brief_text.strip()