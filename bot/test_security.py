"""Тест системы безопасности"""
import asyncio
from utils.security import SecurityValidator
from services.ai_agent import ai_agent

async def test_security():
    """Тест защиты от атак и эмодзи"""
    
    test_cases = [
        # Обычные сообщения
        "Привет!",
        "Хочу заказать приложение",
        "Сколько стоит разработка?",
        
        # Длинные сообщения
        "А" * 5000,
        
        # Попытки инъекций
        "<script>alert('xss')</script>",
        "SELECT * FROM users",
        "javascript:alert(1)",
        "DROP TABLE users",
        
        # Эмодзи и Unicode
        "emoji_test_string",
        "Привет мир! Как дела?",
        
        # Пустые и None
        "",
        None,
    ]
    
    print("=== ТЕСТ СИСТЕМЫ БЕЗОПАСНОСТИ ===\n")
    
    for i, test_input in enumerate(test_cases):
        print(f"Тест {i+1}: {repr(test_input)}")
        
        try:
            # Тест валидатора
            if test_input is not None:
                sanitized = SecurityValidator.sanitize_text(test_input)
                print(f"  Очищено: {repr(sanitized)}")
                
                # Тест AI агента
                if sanitized:
                    response = await ai_agent.chat_response(sanitized)
                    print(f"  AI ответ: {response[:50]}...")
                else:
                    print("  AI ответ: [пустое сообщение]")
            else:
                print("  Результат: None обработан")
                
        except Exception as e:
            print(f"  ОШИБКА: {e}")
        
        print()

if __name__ == "__main__":
    asyncio.run(test_security())