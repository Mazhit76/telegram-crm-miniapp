# -*- coding: utf-8 -*-
"""Тест исправлений API CRM"""

import asyncio
from services.crm_client import crm_client
from services.telegram_client import telegram_client_service

async def test_crm_integration():
    """Тестируем исправленную интеграцию с CRM"""
    
    print("Тестируем исправления CRM интеграции...")
    
    # 1. Тест аутентификации
    print("\n1. Тестируем аутентификацию...")
    auth_result = await crm_client.authenticate()
    if auth_result:
        print("[OK] Аутентификация успешна")
    else:
        print("[ERROR] Ошибка аутентификации")
        return
    
    # 2. Тест создания обращения (старый метод)
    print("\n2. Тестируем старый метод создания обращения...")
    appeal_result = await crm_client.create_appeal(
        telegram_id=1140537573,
        message="Тестовое сообщение: Хочу заказать приложение",
        contact_info="@test_user"
    )
    
    if appeal_result:
        print(f"[OK] Обращение создано: {appeal_result.get('id')}")
    else:
        print("[ERROR] Ошибка создания обращения")
    
    print("\nТест завершен!")

if __name__ == "__main__":
    asyncio.run(test_crm_integration())