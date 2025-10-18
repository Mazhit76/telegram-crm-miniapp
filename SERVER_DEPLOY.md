# 🖥️ Деплой на свой сервер

## 📋 Подготовка сервера

### 1. Установка зависимостей
```bash
# Python 3.11+
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv

# Git
sudo apt install git
```

### 2. Создание пользователя для бота
```bash
sudo useradd -m -s /bin/bash telegram-bot
sudo su - telegram-bot
```

## 📦 Установка проекта

### 1. Клонирование репозитория
```bash
cd /home/telegram-bot
git clone https://github.com/ВАШ_USERNAME/telegram-crm.git
cd telegram-crm
```

### 2. Виртуальное окружение
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
```bash
cd bot
cp .env.example .env
nano .env
```

Заполните:
```env
BOT_TOKEN=ваш_токен_бота
OPENAI_API_KEY=ваш_ключ_openai
CRM_API_URL=https://testcrm.ananas.guru/api
CRM_USERNAME=newsbot1
CRM_PASSWORD=BotPass123
```

## 🔧 Настройка systemd сервиса

### 1. Создание сервиса
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

### 2. Содержимое файла:
```ini
[Unit]
Description=Telegram CRM Bot
After=network.target

[Service]
Type=simple
User=telegram-bot
WorkingDirectory=/home/telegram-bot/telegram-crm/bot
Environment=PATH=/home/telegram-bot/telegram-crm/venv/bin
ExecStart=/home/telegram-bot/telegram-crm/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Запуск сервиса
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

## 🌐 Настройка Mini App

### 1. Nginx конфиг для Mini App
```bash
sudo nano /etc/nginx/sites-available/telegram-miniapp
```

### 2. Содержимое:
```nginx
server {
    listen 80;
    server_name ваш-домен.com;
    
    location /miniapp/ {
        root /home/telegram-bot/telegram-crm;
        try_files $uri $uri/ =404;
    }
}
```

### 3. Активация
```bash
sudo ln -s /etc/nginx/sites-available/telegram-miniapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. SSL сертификат (опционально)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ваш-домен.com
```

## 📱 Обновление URL в боте

В файле `bot/handlers/start.py`:
```python
web_app=WebAppInfo(url="https://ваш-домен.com/miniapp/business-brief.html")
```

## 🔄 Управление ботом

### Команды systemctl:
```bash
# Статус
sudo systemctl status telegram-bot

# Перезапуск
sudo systemctl restart telegram-bot

# Остановка
sudo systemctl stop telegram-bot

# Логи
sudo journalctl -u telegram-bot -f
```

### Обновление кода:
```bash
cd /home/telegram-bot/telegram-crm
git pull
sudo systemctl restart telegram-bot
```

## 🔒 Безопасность

### 1. Firewall
```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

### 2. Права доступа
```bash
chmod 600 /home/telegram-bot/telegram-crm/bot/.env
```

## ✅ Проверка работы

1. **Бот**: `sudo systemctl status telegram-bot`
2. **Mini App**: откройте `https://ваш-домен.com/miniapp/business-brief.html`
3. **Telegram**: нажмите "Заполнить бриф" в боте

## 🎯 Преимущества своего сервера:
- ✅ Полный контроль
- ✅ Нет ограничений по времени
- ✅ Рядом с CRM (быстрая связь)
- ✅ Бесплатно (если сервер уже есть)
- ✅ Легкое обслуживание