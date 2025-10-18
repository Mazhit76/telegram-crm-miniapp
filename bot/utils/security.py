"""Модуль безопасности и валидации"""
import re
import html
from typing import Optional

class SecurityValidator:
    """Валидатор безопасности для входящих данных"""
    
    MAX_MESSAGE_LENGTH = 4000
    MAX_USERNAME_LENGTH = 100
    
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'SELECT\s+.*FROM',
        r'INSERT\s+INTO',
        r'DELETE\s+FROM',
        r'DROP\s+TABLE',
        r'UNION\s+SELECT',
    ]
    
    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """Очистка и безопасная обработка текста"""
        if not text:
            return ""
        
        if len(text) > cls.MAX_MESSAGE_LENGTH:
            text = text[:cls.MAX_MESSAGE_LENGTH] + "..."
        
        for pattern in cls.DANGEROUS_PATTERNS:
            text = re.sub(pattern, '[BLOCKED]', text, flags=re.IGNORECASE)
        
        text = html.escape(text)
        
        try:
            text.encode('utf-8').decode('utf-8')
        except UnicodeError:
            text = text.encode('utf-8', errors='replace').decode('utf-8')
        
        return text.strip()
    
    @classmethod
    def sanitize_username(cls, username: Optional[str]) -> str:
        """Очистка username"""
        if not username:
            return "anonymous"
        
        if len(username) > cls.MAX_USERNAME_LENGTH:
            username = username[:cls.MAX_USERNAME_LENGTH]
        
        username = re.sub(r'[<>"\']', '', username)
        return username.strip() or "anonymous"
    
    @classmethod
    def validate_telegram_id(cls, telegram_id: int) -> bool:
        """Валидация Telegram ID"""
        return isinstance(telegram_id, int) and 0 < telegram_id < 10**12