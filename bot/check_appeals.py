"""Проверка обращений в CRM"""
import asyncio
import httpx
from config import settings

async def check_appeals():
    """Получить список обращений из CRM"""
    
    # Аутентификация
    async with httpx.AsyncClient() as client:
        try:
            # Логин
            auth_response = await client.post(
                f"{settings.crm_api_url}/users/signin",
                data={
                    "username": settings.crm_username,
                    "password": settings.crm_password
                }
            )
            
            if auth_response.status_code != 200:
                print(f"Auth failed: {auth_response.status_code}")
                print(auth_response.text)
                return
            
            token = auth_response.json().get("access_token")
            print(f"Auth OK, token: {token[:20]}...")
            
            # Получить обращения
            appeals_response = await client.get(
                f"{settings.crm_api_url}/appeals/",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            print(f"\nAppeals response: {appeals_response.status_code}")
            
            if appeals_response.status_code == 200:
                appeals = appeals_response.json()
                print(f"Found {len(appeals)} appeals:")
                
                for appeal in appeals[-5:]:  # Последние 5
                    print(f"- ID: {appeal.get('id')}")
                    print(f"  Type: {appeal.get('type')}")
                    print(f"  Status: {appeal.get('status')}")
                    print(f"  Description: {appeal.get('description', '')[:100]}...")
                    print(f"  Created: {appeal.get('created_at')}")
                    print()
            else:
                print(f"Error getting appeals: {appeals_response.text}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_appeals())