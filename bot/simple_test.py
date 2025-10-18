# -*- coding: utf-8 -*-
"""Простой тест исправлений"""

import asyncio
from services.crm_client import crm_client

async def test_appeal():
    """Тест создания обращения"""
    
    print("Тестируем создание обращения...")
    
    # Аутентификация
    auth_ok = await crm_client.authenticate()
    if not auth_ok:
        print("Ошибка аутентификации")
        return
    
    print("Аутентификация OK")
    
    # Создание обращения
    result = await crm_client.create_appeal(
        telegram_id=1140537573,
        message="Хочу заказать приложение",
        contact_info="@img76"
    )
    
    if result:
        print(f"Обращение создано: {result.get('id')}")
    else:
        print("Ошибка создания обращения")

if __name__ == "__main__":
    asyncio.run(test_appeal())