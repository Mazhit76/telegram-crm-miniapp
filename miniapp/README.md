# Telegram Mini App - Форма заказа разработки

## Функции
- 📋 Детальная форма проекта
- 💰 Калькулятор стоимости
- 📱 Выбор типа разработки
- 📎 Загрузка файлов ТЗ
- 🎨 Telegram UI/UX

## Установка

```bash
cd miniapp
npm install
```

## Разработка

```bash
npm run dev
```

## Сборка

```bash
npm run build
```

## Интеграция с ботом

1. Разместить на сервере (например, GitHub Pages)
2. Добавить Web App кнопку в бота:

```python
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="📱 Заказать разработку", 
        web_app=WebAppInfo(url="https://your-domain.com/miniapp")
    )]
])
```

## Структура

```
miniapp/
├── src/
│   ├── components/
│   │   └── ProjectForm.vue    # Основная форма
│   ├── App.vue               # Главный компонент
│   ├── main.js              # Точка входа
│   └── style.css            # Стили
├── index.html               # HTML шаблон
├── package.json            # Зависимости
└── vite.config.js          # Конфигурация сборки
```# telegram-crm-miniapp
