# 🚀 Деплой Mini App на GitHub Pages

## Шаги для размещения:

### 1. Создайте репозиторий на GitHub
- Название: `telegram-crm-miniapp` (или любое другое)
- Сделайте его публичным

### 2. Загрузите файлы
Загрузите в репозиторий файлы из папки `miniapp/`:
- `index.html`
- `business-brief.html`

### 3. Включите GitHub Pages
1. Зайдите в Settings репозитория
2. Найдите раздел "Pages"
3. В Source выберите "Deploy from a branch"
4. Выберите ветку `main` и папку `/ (root)`
5. Нажмите Save

### 4. Получите URL
После активации Pages URL будет:
```
https://ВАШ_USERNAME.github.io/telegram-crm-miniapp/business-brief.html
```

### 5. Обновите бота
В файле `bot/handlers/start.py` замените URL:

```python
[InlineKeyboardButton(text="📋 Заполнить бриф", 
 web_app=WebAppInfo(url="https://ВАШ_USERNAME.github.io/telegram-crm-miniapp/business-brief.html"))]
```

### 6. Перезапустите бота
```bash
cd bot
python main.py
```

## ✅ Готовые файлы для загрузки:
- `miniapp/index.html` - главная страница
- `miniapp/business-brief.html` - форма брифа

## 🔧 Альтернативный URL (временно)
Пока настраиваете GitHub Pages, можете использовать:
```python
web_app=WebAppInfo(url="https://raw.githubusercontent.com/ВАШ_USERNAME/telegram-crm-miniapp/main/business-brief.html")
```

**Примечание:** Raw GitHub файлы могут не работать с Telegram WebApp из-за CORS. Лучше использовать GitHub Pages.