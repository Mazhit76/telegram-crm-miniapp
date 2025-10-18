"""Тест создания обращения"""
import asyncio
import httpx
from config import settings

async def test_create_appeal():
    """Создать тестовое обращение"""
    
    async with httpx.AsyncClient() as client:
        try:
            # Аутентификация
            auth_response = await client.post(
                f"{settings.crm_api_url}/users/signin",
                data={
                    "username": settings.crm_username,
                    "password": settings.crm_password
                }
            )
            
            token = auth_response.json().get("access_token")
            print(f"Auth OK: {token[:20]}...")
            
            # Создать обращение
            appeal_data = {
                "type": "site",
                "client_id": "8c008860-e04b-4091-a2eb-e027d79d228c",
                "object": "Тест Telegram Bot",
                "info": "Тестовое обращение из Telegram бота",
                "price": 0,
                "city": "Москва",
                "street": "Не указана",
                "apart": "Не указана"
            }
            
            create_response = await client.post(
                f"{settings.crm_api_url}/appeals/",
                headers={"Authorization": f"Bearer {token}"},
                json=appeal_data
            )
            
            print(f"Create response: {create_response.status_code}")
            print(f"Response body: {create_response.text}")
            
            if create_response.status_code == 201:
                appeal = create_response.json()
                print(f"SUCCESS! Appeal created with ID: {appeal.get('id')}")
            else:
                print("FAILED to create appeal")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_create_appeal())