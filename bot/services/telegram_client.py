"""Клиент для работы с Telegram клиентами в CRM"""
import httpx
from typing import Dict, Any, Optional
from config import settings
from utils.security import SecurityValidator
from utils.safe_print import safe_print

class TelegramClientService:
    """Сервис для управления Telegram клиентами в CRM"""
    
    def __init__(self):
        self.base_url = settings.crm_api_url
        self.token: Optional[str] = None
    
    async def authenticate(self) -> bool:
        """Аутентификация в CRM"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/users/signin",
                    data={
                        "username": settings.crm_username,
                        "password": settings.crm_password
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    self.token = data.get("access_token")
                    return True
                return False
            except Exception as e:
                safe_print(f"CRM auth error: {e}")
                return False
    
    async def create_or_update_client(self, telegram_user) -> Optional[Dict[str, Any]]:
        """Создание или обновление Telegram клиента"""
        if not SecurityValidator.validate_telegram_id(telegram_user.id):
            safe_print(f"Invalid telegram_id: {telegram_user.id}")
            return None
        
        if not self.token:
            await self.authenticate()
        
        # Подготовка данных клиента
        client_data = {
            "telegram_id": telegram_user.id,
            "source": "telegram_bot"
        }
        
        # Добавляем опциональные поля если есть
        if telegram_user.username:
            client_data["username"] = SecurityValidator.sanitize_username(telegram_user.username)
        
        if telegram_user.first_name:
            client_data["first_name"] = SecurityValidator.sanitize_text(telegram_user.first_name)
        
        if telegram_user.last_name:
            client_data["last_name"] = SecurityValidator.sanitize_text(telegram_user.last_name)
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/telegram-clients/",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=client_data
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    safe_print(f"Telegram client created/updated: {result.get('id')}")
                    return result
                else:
                    safe_print(f"Failed to create client: {response.status_code} - {response.text}")
                    return None
                    
            except Exception as e:
                safe_print(f"Create client error: {e}")
                return None
    
    async def get_client_by_telegram_id(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Получение клиента по Telegram ID"""
        if not SecurityValidator.validate_telegram_id(telegram_id):
            return None
        
        if not self.token:
            await self.authenticate()
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/telegram-clients/by-telegram-id/{telegram_id}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    safe_print(f"Client not found: {telegram_id}")
                    return None
                else:
                    safe_print(f"Get client error: {response.status_code}")
                    return None
                    
            except Exception as e:
                safe_print(f"Get client error: {e}")
                return None
    
    async def update_client_contact(self, telegram_id: int, phone: str = None, name: str = None) -> Optional[Dict[str, Any]]:
        """Обновление контактных данных клиента"""
        if not SecurityValidator.validate_telegram_id(telegram_id):
            return None
        
        if not self.token:
            await self.authenticate()
        
        update_data = {}
        
        if phone:
            update_data["phone"] = SecurityValidator.sanitize_text(phone)
        
        if name:
            # Разделяем имя на части
            name_parts = SecurityValidator.sanitize_text(name).split()
            if len(name_parts) >= 1:
                update_data["first_name"] = name_parts[0]
            if len(name_parts) >= 2:
                update_data["last_name"] = " ".join(name_parts[1:])
        
        if not update_data:
            return None
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.patch(
                    f"{self.base_url}/telegram-clients/by-telegram-id/{telegram_id}",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=update_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    safe_print(f"Client updated: {telegram_id}")
                    return result
                else:
                    safe_print(f"Update client error: {response.status_code}")
                    return None
                    
            except Exception as e:
                safe_print(f"Update client error: {e}")
                return None

telegram_client_service = TelegramClientService()