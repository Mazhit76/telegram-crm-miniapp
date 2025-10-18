"""Получить список пользователей CRM"""
import asyncio
import httpx
from config import settings

async def get_users():
    """Получить пользователей из CRM"""
    
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
            
            # Получить пользователей
            users_response = await client.get(
                f"{settings.crm_api_url}/users/",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            print(f"Users response: {users_response.status_code}")
            
            if users_response.status_code == 200:
                users = users_response.json()
                print(f"Found {len(users)} users:")
                
                for user in users[:5]:  # Первые 5
                    print(f"- ID: {user.get('id')}")
                    print(f"  Username: {user.get('username')}")
                    print(f"  Name: {user.get('name')} {user.get('surname')}")
                    print(f"  Is Client: {user.get('is_client')}")
                    print()
                    
                # Найдем клиента для использования
                client_users = [u for u in users if u.get('is_client')]
                if client_users:
                    print(f"First client ID: {client_users[0]['id']}")
                    return client_users[0]['id']
            else:
                print(f"Error: {users_response.text}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(get_users())