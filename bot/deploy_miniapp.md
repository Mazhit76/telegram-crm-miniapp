# Развертывание Mini App

## Варианты размещения

### 1. GitHub Pages (бесплатно)

1. Создайте репозиторий на GitHub
2. Загрузите файл `business-brief.html`
3. Включите GitHub Pages в настройках
4. URL будет: `https://username.github.io/repository-name/business-brief.html`

### 2. Netlify (бесплатно)

1. Зарегистрируйтесь на netlify.com
2. Перетащите файл `business-brief.html` в Netlify
3. Получите URL вида: `https://random-name.netlify.app/business-brief.html`

### 3. Vercel (бесплатно)

1. Зарегистрируйтесь на vercel.com
2. Загрузите файл через интерфейс
3. Получите URL вида: `https://project-name.vercel.app/business-brief.html`

### 4. Собственный сервер

Разместите файл на вашем домене:
```
https://ananas.guru/miniapp/business-brief.html
```

## Обновление URL в боте

После размещения обновите URL в файле `handlers/start.py`:

```python
[InlineKeyboardButton(text="📋 Заполнить бриф", web_app=WebAppInfo(url="ВАШ_РЕАЛЬНЫЙ_URL"))]
```

## Тестирование

1. Разместите файл по любому из вариантов
2. Обновите URL в боте
3. Перезапустите бота
4. Протестируйте кнопку "Заполнить бриф"

## Безопасность

- Telegram проверяет HTTPS сертификаты
- Используйте только HTTPS URL
- Все перечисленные сервисы предоставляют HTTPS автоматически