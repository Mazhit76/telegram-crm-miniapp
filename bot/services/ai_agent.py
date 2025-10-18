import openai
from typing import List, Dict, Any
from config import settings
from utils.security import SecurityValidator

class AIAgent:
    def __init__(self):
        if settings.openai_api_key != "sk-test-key-placeholder":
            openai.api_key = settings.openai_api_key
            self.client = openai.OpenAI(api_key=settings.openai_api_key)
        else:
            self.client = None
    
    async def chat_response(self, message: str, user_context: Dict[str, Any] = None) -> str:
        """AI ответ в чате"""
        # Валидация сообщения
        safe_message = SecurityValidator.sanitize_text(message)
        if not safe_message:
            return "Пожалуйста, отправьте корректное сообщение."
        
        # Проверяем наличие реального API ключа
        if settings.openai_api_key == "sk-test-key-placeholder":
            return self._mock_response(safe_message)
        
        system_prompt = """Ты - AI консультант IT-компании ananas.guru. 
        Мы разрабатываем мобильные приложения, веб-сайты и AI решения.
        
        Твоя задача:
        1. Отвечать на вопросы о наших услугах
        2. Квалифицировать потенциальных клиентов
        3. Предлагать консультацию при интересе к разработке
        
        Услуги:
        - Мобильные приложения (iOS/Android/Flutter)
        - Веб-приложения (Vue.js, React, FastAPI)
        - AI агенты и чат-боты
        - Интеграции с внешними системами
        
        Отвечай дружелюбно, профессионально, кратко."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": safe_message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Извините, произошла ошибка. Напишите нам на admin@ananas.guru"
    
    def _mock_response(self, message: str) -> str:
        """Заглушка для тестирования без OpenAI"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["привет", "hello", "hi"]):
            return "👋 Привет! Я AI-консультант ananas.guru. Мы создаем мобильные приложения, веб-сайты и AI решения. Чем могу помочь?"
        
        elif any(word in message_lower for word in ["цена", "стоимость", "сколько"]):
            return "💰 Стоимость разработки:\n• Мобильные приложения: от 100,000₽\n• Веб-сайты: от 50,000₽\n• AI решения: от 80,000₽\n\nХотите получить точную оценку вашего проекта?"
        
        elif any(word in message_lower for word in ["мобильное", "приложение", "app"]):
            return "📱 Мы разрабатываем мобильные приложения на iOS и Android. Используем Swift, Kotlin и Flutter для кроссплатформенной разработки. Расскажите о вашей идее!"
        
        elif any(word in message_lower for word in ["сайт", "веб", "website"]):
            return "🌐 Создаем современные веб-сайты и приложения на Vue.js, React, FastAPI. От лендингов до сложных порталов. Какой сайт вам нужен?"
        
        elif any(word in message_lower for word in ["ai", "ии", "бот", "искусственный"]):
            return "🤖 Разрабатываем AI решения: чат-боты, автоматизация процессов, интеграции с OpenAI. Как AI может помочь вашему бизнесу?"
        
        else:
            return "Спасибо за вопрос! Мы специализируемся на разработке мобильных приложений, веб-сайтов и AI решений. Расскажите подробнее о вашей задаче, и я помогу найти лучшее решение!"
    
    async def generate_it_article(self, news_data: Dict[str, Any]) -> str:
        """Генерация IT статьи на основе новостей"""
        prompt = f"""Создай интересную статью на основе IT новости:
        
        Заголовок: {news_data.get('title', '')}
        Описание: {news_data.get('description', '')}
        
        Требования:
        1. Объем 200-300 слов
        2. Простым языком для бизнеса
        3. В конце подводка к нашим услугам разработки
        4. Добавь призыв к действию
        
        Наши услуги: мобильная разработка, веб-приложения, AI решения."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            return None

ai_agent = AIAgent()