# 🐳 Docker деплой опции

## ❌ Docker Hub - НЕ хостинг!
Docker Hub только хранит образы, не запускает их.

## ✅ Платформы с Docker поддержкой:

### 🥇 Fly.io (рекомендуется)
```bash
# 1. Установите flyctl
# 2. Зарегистрируйтесь
flyctl auth signup

# 3. Деплой
flyctl launch
flyctl deploy
```

**Плюсы:**
- Бесплатно до 160 часов/мес
- Быстрый деплой
- Автоскейлинг
- Глобальная сеть

### 🥈 Railway
```bash
# 1. Подключите GitHub репо
# 2. Railway автоматически найдет Dockerfile
# 3. Настройте переменные окружения
```

### 🥉 Render
```bash
# 1. Создайте Web Service
# 2. Выберите Docker
# 3. Укажите Dockerfile
```

## 📦 Готовые файлы:
- `Dockerfile` - образ для бота
- `fly.toml` - конфиг Fly.io
- `requirements.txt` - зависимости

## 🚀 Команды для деплоя:

### Fly.io
```bash
flyctl launch --name telegram-crm-bot
flyctl secrets set BOT_TOKEN=ваш_токен
flyctl secrets set OPENAI_API_KEY=ваш_ключ
flyctl deploy
```

### Railway
```bash
railway login
railway new
railway up
```

## 💰 Стоимость:
- **Fly.io**: Бесплатно (160ч/мес)
- **Railway**: $5/мес
- **Render**: Бесплатно (засыпает)

## 🎯 Рекомендация:
**Fly.io** - лучший баланс цены и качества для Docker деплоя.