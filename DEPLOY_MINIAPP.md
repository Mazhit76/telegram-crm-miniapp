# 🚀 Быстрый деплой Mini App

## Проблема: 404 при нажатии "Заполнить бриф"

**Причина:** Файл `business-brief.html` не размещен в интернете

## ⚡ Быстрое решение (5 минут)

### Вариант 1: Netlify Drop (самый быстрый)

1. Откройте https://app.netlify.com/drop
2. Перетащите файл `miniapp/business-brief.html` в окно браузера
3. Скопируйте полученный URL (например: `https://amazing-name-123456.netlify.app/business-brief.html`)
4. Обновите URL в `bot/handlers/start.py`:

```python
[InlineKeyboardButton(text="📋 Заполнить бриф", web_app=WebAppInfo(url="ВАШ_URL_ИЗ_NETLIFY"))]
```

5. Перезапустите бота: `python main.py`

### Вариант 2: GitHub Pages

1. Создайте репозиторий на GitHub
2. Загрузите файл `business-brief.html`
3. Включите Pages в Settings → Pages
4. URL: `https://username.github.io/repo-name/business-brief.html`

### Вариант 3: Временное решение

Используйте готовый тестовый URL:
```python
web_app=WebAppInfo(url="https://telegram-crm-demo.netlify.app/business-brief.html")
```

## ✅ Проверка

1. Запустите бота
2. Нажмите /start
3. Нажмите "📋 Заполнить бриф"
4. Должна открыться форма брифа

## 🔧 Если не работает

- Проверьте, что URL начинается с `https://`
- Убедитесь, что файл доступен по прямой ссылке
- Перезапустите бота после изменения URL

## 📱 Текущий статус

- ✅ Файл брифа готов: `miniapp/business-brief.html`
- ❌ Не размещен в интернете
- ❌ URL в боте указывает на несуществующий адрес

**Нужно:** Разместить файл и обновить URL в коде бота.