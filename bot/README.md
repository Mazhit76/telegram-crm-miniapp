# Telegram AI Bot для CRM

## Установка

1. Установить зависимости:
```bash
pip install -r requirements.txt
```

2. Создать `.env` файл:
```bash
cp .env.example .env
```

3. Заполнить переменные в `.env`:
- `BOT_TOKEN` - токен Telegram бота от @BotFather
- `OPENAI_API_KEY` - ключ OpenAI API
- `CRM_USERNAME` и `CRM_PASSWORD` - данные для CRM

## Запуск

```bash
python main.py
```

## Функции

- 🤖 AI чат-консультант
- 📱 Лидогенерация в CRM
- 🚀 Презентация услуг
- 📞 Сбор заявок

## Структура

```
bot/
├── main.py              # Запуск бота
├── config.py            # Конфигурация
├── handlers/            # Обработчики команд
│   ├── start.py         # Команда /start и меню
│   └── chat.py          # AI чат
└── services/            # Сервисы
    ├── ai_agent.py      # OpenAI интеграция
    └── crm_client.py    # CRM API клиент
```