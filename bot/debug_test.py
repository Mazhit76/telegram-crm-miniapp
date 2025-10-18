# -*- coding: utf-8 -*-
"""Детальный тест с полным логированием"""

import asyncio
import httpx
from config import settings

async def test_direct_api():
    """Прямой тест API без обёрток"""
    
    print("=== Тест прямого API ===")
    
    # 1. Аутентификация
    async with httpx.AsyncClient() as client:
        try:
            print("1. Аутентификация...")
            response = await client.post(
                f"{settings.crm_api_url}/users/signin",
                data={
                    "username": settings.crm_username,
                    "password": settings.crm_password
                }
            )
            print(f"Auth status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                print(f"Token получен: {token[:20]}...")
            else:
                print(f"Auth failed: {response.text}")
                return
            
            # 2. Создание обращения
            print("\n2. Создание обращения...")
            appeal_data = {
                "type": "site",
                "client_id": "8c008860-e04b-4091-a2eb-e027d79d228c",
                "object": "Test appeal",
                "info": "Test message",
                "price": 0,
                "city": "Moscow",
                "street": "Not specified",
                "apart": "Not specified"
            }
            
            print(f"Request data: {appeal_data}")
            
            response = await client.post(
                f"{settings.crm_api_url}/appeals/",
                headers={"Authorization": f"Bearer {token}"},
                json=appeal_data
            )
            
            print(f"Appeal status: {response.status_code}")
            print(f"Response: {response.text}")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_direct_api())