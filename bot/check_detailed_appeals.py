"""Детальная проверка обращений"""
import asyncio
import httpx
from config import settings

async def check_detailed_appeals():
    """Получить детальную информацию об обращениях"""
    
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
            
            # Получить обращения
            appeals_response = await client.get(
                f"{settings.crm_api_url}/appeals/",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if appeals_response.status_code == 200:
                appeals = appeals_response.json()
                print(f"Всего обращений: {len(appeals)}")
                
                # Показать последние 3 с полной информацией
                for appeal in appeals[-3:]:
                    print(f"\n=== ОБРАЩЕНИЕ ===")
                    print(f"ID: {appeal.get('id')}")
                    print(f"Объект: {appeal.get('object')}")
                    print(f"Информация: {appeal.get('info')}")
                    print(f"Тип: {appeal.get('type')}")
                    print(f"Статус: {appeal.get('status')}")
                    print(f"Создано: {appeal.get('created_at')}")
                    print(f"Клиент: {appeal.get('client_name')} {appeal.get('client_surname')}")
                    
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_detailed_appeals())