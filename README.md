# Telegram CRM Bot для IT-услуг

Система лидогенерации и CRM для привлечения клиентов на разработку мобильных и AI приложений.

## Архитектура
- **Backend**: FastAPI + PostgreSQL + Redis
- **Bot**: Python aiogram + OpenAI
- **Mini App**: Vue.js 3 + Tailwind CSS
- **Admin**: Vue.js Dashboard

## Быстрый старт
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Bot  
cd bot
python bot.py

# Frontend
cd frontend
npm install && npm run dev
```

## Структура проекта
```
telegram-crm/
├── backend/          # FastAPI сервер
├── bot/             # Telegram бот
├── frontend/        # Vue.js Mini App + Admin
├── docker-compose.yml
└── README.md
```