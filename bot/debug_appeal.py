"""Отладка создания обращения"""
import asyncio
import httpx
from config import settings

async def debug_appeal_creation():
    """Отладка с подробными логами"""
    
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
            
            # Попробуем разные варианты данных
            appeal_variants = [
                {
                    "type": "site",
                    "client_id": "8c008860-e04b-4091-a2eb-e027d79d228c",
                    "object": "Telegram заявка",
                    "info": "Хочу заказать приложение",
                    "price": 0,
                    "city": "Москва",
                    "street": "Не указана",
                    "apart": "Не указана"
                },
                {
                    "type": "site",
                    "client_id": "8c008860-e04b-4091-a2eb-e027d79d228c",
                    "object": "Telegram заявка",
                    "info": "Хочу заказать приложение",
                    "price": 0,
                    "city": "Москва",
                    "street": "Не указана",
                    "apart": "Не указана",
                    "company": None
                }
            ]
            
            for i, appeal_data in enumerate(appeal_variants):
                print(f"\n--- Вариант {i+1} ---")
                print(f"Данные: {appeal_data}")
                
                response = await client.post(
                    f"{settings.crm_api_url}/appeals/",
                    headers={"Authorization": f"Bearer {token}"},
                    json=appeal_data
                )
                
                print(f"Статус: {response.status_code}")
                print(f"Ответ: {response.text}")
                
                if response.status_code == 201:
                    print("✅ УСПЕХ!")
                    break
                    
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_appeal_creation())