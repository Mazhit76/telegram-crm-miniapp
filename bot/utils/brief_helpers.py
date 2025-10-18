"""Вспомогательные функции для обработки брифов"""

def get_project_type_title(app_types):
    """Получить название типа проекта из массива типов"""
    type_mapping = {
        'chat': 'Чат-приложение',
        'ecommerce': 'Интернет-магазин',
        'marketplace': 'Маркетплейс',
        'social': 'Социальная сеть',
        'crm': 'CRM система',
        'news': 'Новостное приложение',
        'media': 'Медиа-плеер',
        'streaming': 'Стриминг-платформа',
        'analytics': 'Аналитическая система',
        'webview': 'WebView приложение',
        'education': 'Образовательная платформа',
        'booking': 'Система бронирования',
        'delivery': 'Служба доставки'
    }
    
    if not app_types:
        return "Мобильное приложение"
    
    # Берем первый тип из списка
    first_type = app_types[0] if isinstance(app_types, list) else app_types
    return type_mapping.get(first_type, "Мобильное приложение")

def parse_budget(budget_str):
    """Парсинг бюджета в числовое значение"""
    if not budget_str:
        return 0
    
    budget_mapping = {
        '100-300': 200000,
        '300-500': 400000,
        '500-800': 650000,
        '800-1500': 1150000,
        '1500-3000': 2250000,
        '3000+': 3000000
    }
    
    return budget_mapping.get(budget_str, 0)