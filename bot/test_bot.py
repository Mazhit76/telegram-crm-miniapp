"""Тестирование бота и CRM интеграции"""
import asyncio
from services.crm_client import crm_client
from services.ai_agent import ai_agent

async def test_crm_connection():
    """Тест подключения к CRM"""
    print("Тестирование CRM подключения...")
    
    # Тест аутентификации
    auth_result = await crm_client.authenticate()
    if auth_result:
        print("[OK] CRM аутентификация успешна")
        print(f"Токен получен: {crm_client.token[:20]}...")
        
        # Тест создания обращения
        appeal_result = await crm_client.create_appeal(
            telegram_id=123456789,
            message="Тестовое обращение из бота",
            contact_info="@test_user"
        )
        
        if appeal_result:
            print("[OK] Обращение создано успешно")
            print(f"ID обращения: {appeal_result.get('id', 'N/A')}")
        else:
            print("[ERROR] Ошибка создания обращения")
    else:
        print("[ERROR] Ошибка аутентификации в CRM")

async def test_ai_agent():
    """Тест AI агента"""
    print("\nТестирование AI агента...")
    
    test_messages = [
        "Привет!",
        "Сколько стоит мобильное приложение?",
        "Можете разработать AI бота?",
        "Хочу заказать веб-сайт"
    ]
    
    for message in test_messages:
        print(f"\nПользователь: {message}")
        response = await ai_agent.chat_response(message)
        print(f"Бот: {response}")

async def main():
    """Запуск всех тестов"""
    print("Запуск тестирования Telegram Bot...")
    
    await test_crm_connection()
    await test_ai_agent()
    
    print("\nТестирование завершено!")

if __name__ == "__main__":
    asyncio.run(main())