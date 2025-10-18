"""Тест обработки данных Web App"""
import asyncio
import json
from handlers.webapp import format_brief_for_crm

def test_brief_formatting():
    """Тест форматирования брифа"""
    
    # Тестовые данные из Web App
    test_data = {
        "appTypes": ["chat", "ecommerce"],
        "customAppType": "Доставка еды",
        "analogs": ["delivery", "uber"],
        "techFeatures": ["push", "geo", "payments"],
        "businessGoals": ["ad_revenue", "new_markets"],
        "projectDescription": "Приложение для доставки еды с геолокацией и чатом с курьерами",
        "budget": "500-800",
        "timeline": "4-6",
        "clientName": "Иван Петров",
        "phone": "+7 (999) 123-45-67",
        "files": [
            {"name": "техзадание.pdf", "size": 1024000},
            {"name": "макеты.jpg", "size": 512000}
        ],
        "submitted_at": "2024-01-15T10:30:00Z"
    }
    
    # Форматируем бриф
    formatted_brief = format_brief_for_crm(test_data)
    
    from utils.safe_print import safe_print
    safe_print("=== ТЕСТ ФОРМАТИРОВАНИЯ БРИФА ===")
    safe_print(formatted_brief)
    safe_print("\n=== ДЛИНА ТЕКСТА ===")
    safe_print(f"Символов: {len(formatted_brief)}")
    
    # Проверяем что все данные включены
    assert "Иван Петров" in formatted_brief
    assert "+7 (999) 123-45-67" in formatted_brief
    assert "chat, ecommerce" in formatted_brief
    assert "Доставка еды" in formatted_brief
    assert "техзадание.pdf" in formatted_brief
    
    safe_print("\nВсе проверки пройдены!")

if __name__ == "__main__":
    test_brief_formatting()