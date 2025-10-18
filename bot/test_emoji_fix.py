"""Тест исправления проблемы с эмодзи"""
from utils.safe_print import safe_print, setup_console_utf8
from utils.security import SecurityValidator

def test_emoji_handling():
    """Тест обработки эмодзи"""
    
    # Настройка консоли
    setup_console_utf8()
    
    test_messages = [
        "Привет! 👋",
        "Хочу заказать приложение 📱💰",
        "🚀🎯💻🔥⭐️🌟✨💎🎨🎪",
        "Обычный текст без эмодзи",
    ]
    
    safe_print("=== ТЕСТ ОБРАБОТКИ ЭМОДЗИ ===")
    
    for i, message in enumerate(test_messages):
        safe_print(f"\nТест {i+1}: {repr(message)}")
        
        # Проверяем санитизацию
        sanitized = SecurityValidator.sanitize_text(message)
        safe_print(f"Очищено: {repr(sanitized)}")
        
        # Проверяем что данные корректны для передачи
        safe_print(f"Длина: {len(sanitized)} символов")
        safe_print(f"Безопасно: {'Да' if sanitized else 'Нет'}")

if __name__ == "__main__":
    test_emoji_handling()