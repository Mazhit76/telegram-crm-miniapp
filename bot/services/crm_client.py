import httpx
from typing import Dict, Any, Optional
from config import settings
from utils.security import SecurityValidator
from utils.safe_print import safe_print

class CRMClient:
    def __init__(self):
        self.base_url = settings.crm_api_url
        self.token: Optional[str] = None
    
    async def authenticate(self) -> bool:
        """Аутентификация в CRM"""
        async with httpx.AsyncClient(timeout=30.0) as client:
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
    
    async def create_appeal_for_client(self, telegram_client_id: str, message: str, object_title: str = "Телеграм заявка", price: int = 0) -> Optional[Dict[str, Any]]:
        """Создание обращения для Telegram клиента"""
        # Очистка данных
        safe_message = SecurityValidator.sanitize_text(message)
        safe_object = SecurityValidator.sanitize_text(object_title)
        
        if not safe_message:
            safe_print("Empty or invalid message")
            return None
        
        if not self.token:
            await self.authenticate()
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/appeals/",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json={
                        "client_id": "8c008860-e04b-4091-a2eb-e027d79d228c",
                        "telegram_client_id": telegram_client_id,
                        "type": "site",
                        "object": safe_object,
                        "info": safe_message,
                        "price": price,
                        "city": "Москва",
                        "street": "Не указана",
                        "apart": "Не указана"
                    }
                )
                if response.status_code == 201:
                    return response.json()
                else:
                    safe_print(f"Appeal creation failed: {response.status_code} - {response.text}")
                    return None
            except Exception as e:
                safe_print(f"Create appeal error: {e}")
                return None
    
    async def create_appeal(self, telegram_id: int, message: str, contact_info: str) -> Optional[Dict[str, Any]]:
        """Старый метод для обратной совместимости"""
        # Валидация входных данных
        if not SecurityValidator.validate_telegram_id(telegram_id):
            safe_print(f"Invalid telegram_id: {telegram_id}")
            return None
        
        # Очистка данных
        safe_message = SecurityValidator.sanitize_text(message)
        safe_contact = SecurityValidator.sanitize_text(contact_info)
        
        if not safe_message:
            safe_print("Empty or invalid message")
            return None
        
        if not self.token:
            await self.authenticate()
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/appeals/",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json={
                        "type": "site",
                        "client_id": "8c008860-e04b-4091-a2eb-e027d79d228c",
                        "object": "Telegram заявка",
                        "info": f"Сообщение: {safe_message}\nКонтакт: {safe_contact}\nTelegram ID: {telegram_id}",
                        "price": 0,
                        "city": "Москва",
                        "street": "Не указана",
                        "apart": "Не указана"
                    }
                )
                if response.status_code == 201:
                    return response.json()
                else:
                    safe_print(f"Appeal creation failed: {response.status_code} - {response.text}")
                    return None
            except Exception as e:
                safe_print(f"Create appeal error: {e}")
                safe_print(f"Request data: telegram_id={telegram_id}")
                return None

crm_client = CRMClient()