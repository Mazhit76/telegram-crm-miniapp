"""Тест передачи реальных данных пользователя"""
import asyncio
from services.crm_client import crm_client

async def test_real_telegram_data():
    """Тест с реальными данными Telegram пользователя"""
    
    # Симуляция данных реального пользователя Telegram
    telegram_id = 123456789
    message = "Хочу заказать мобильное приложение для доставки еды"
    contact_info = "@test_user_real"
    
    print("Создаю обращение с реальными данными Telegram...")
    print(f"Telegram ID: {telegram_id}")
    print(f"Сообщение: {message}")
    print(f"Контакт: {contact_info}")
    
    result = await crm_client.create_appeal(
        telegram_id=telegram_id,
        message=message, 
        contact_info=contact_info
    )
    
    if result:
        print(f"\n[OK] Обращение создано!")
        print(f"ID: {result['id']}")
        print(f"Объект: {result['object']}")
        print(f"Информация: {result['info']}")
        print(f"Клиент: {result['client_name']} {result['client_surname']}")
    else:
        print("[ERROR] Ошибка создания обращения")

if __name__ == "__main__":
    asyncio.run(test_real_telegram_data())