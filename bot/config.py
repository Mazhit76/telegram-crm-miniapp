from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Telegram
    bot_token: str
    
    # OpenAI
    openai_api_key: str
    
    # CRM
    crm_api_url: str = "https://testcrm.ananas.guru/api"
    crm_username: str
    crm_password: str
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # News
    news_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()