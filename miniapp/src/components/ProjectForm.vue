<template>
  <div class="max-w-2xl mx-auto p-4">
    <!-- Заголовок -->
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold text-tg-text mb-2">Заказать разработку</h1>
      <p class="text-tg-hint">Расскажите о вашем проекте и получите расчет стоимости</p>
    </div>

    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- Тип проекта -->
      <div>
        <label class="block text-sm font-medium text-tg-text mb-2">Тип проекта *</label>
        <select v-model="form.projectType" class="form-select" required>
          <option value="">Выберите тип проекта</option>
          <option value="mobile">📱 Мобильное приложение</option>
          <option value="web">🌐 Веб-сайт/приложение</option>
          <option value="ai">🤖 AI решение</option>
          <option value="integration">🔗 Интеграция систем</option>
        </select>
      </div>

      <!-- Название проекта -->
      <div>
        <label class="block text-sm font-medium text-tg-text mb-2">Название проекта *</label>
        <input 
          v-model="form.projectName" 
          type="text" 
          class="form-input" 
          placeholder="Например: Приложение доставки еды"
          required
        >
      </div>

      <!-- Описание -->
      <div>
        <label class="block text-sm font-medium text-tg-text mb-2">Описание проекта *</label>
        <textarea 
          v-model="form.description" 
          class="form-input h-24 resize-none" 
          placeholder="Опишите основную идею и функционал"
          required
        ></textarea>
      </div>

      <!-- Платформы (для мобильных) -->
      <div v-if="form.projectType === 'mobile'">
        <label class="block text-sm font-medium text-tg-text mb-2">Платформы</label>
        <div class="space-y-2">
          <label class="flex items-center">
            <input v-model="form.platforms" type="checkbox" value="ios" class="mr-2">
            <span>iOS (iPhone/iPad)</span>
          </label>
          <label class="flex items-center">
            <input v-model="form.platforms" type="checkbox" value="android" class="mr-2">
            <span>Android</span>
          </label>
          <label class="flex items-center">
            <input v-model="form.platforms" type="checkbox" value="cross" class="mr-2">
            <span>Кроссплатформенное (Flutter/React Native)</span>
          </label>
        </div>
      </div>

      <!-- Функции -->
      <div>
        <label class="block text-sm font-medium text-tg-text mb-2">Основные функции</label>
        <div class="grid grid-cols-2 gap-2">
          <label v-for="feature in availableFeatures" :key="feature.id" class="flex items-center text-sm">
            <input v-model="form.features" type="checkbox" :value="feature.id" class="mr-2">
            <span>{{ feature.name }}</span>
          </label>
        </div>
      </div>

      <!-- Бюджет -->
      <div>
        <label class="block text-sm font-medium text-tg-text mb-2">Планируемый бюджет</label>
        <select v-model="form.budget" class="form-select">
          <option value="">Выберите диапазон</option>
          <option value="50-100">50,000 - 100,000 ₽</option>
          <option value="100-300">100,000 - 300,000 ₽</option>
          <option value="300-500">300,000 - 500,000 ₽</option>
          <option value="500-1000">500,000 - 1,000,000 ₽</option>
          <option value="1000+">Более 1,000,000 ₽</option>
        </select>
      </div>

      <!-- Сроки -->
      <div>
        <label class="block text-sm font-medium text-tg-text mb-2">Желаемые сроки</label>
        <select v-model="form.timeline" class="form-select">
          <option value="">Выберите сроки</option>
          <option value="1-2">1-2 месяца</option>
          <option value="2-4">2-4 месяца</option>
          <option value="4-6">4-6 месяцев</option>
          <option value="6+">Более 6 месяцев</option>
        </select>
      </div>

      <!-- Контакты -->
      <div>
        <label class="block text-sm font-medium text-tg-text mb-2">Контактная информация</label>
        <input 
          v-model="form.contact" 
          type="text" 
          class="form-input" 
          placeholder="Телефон или email для связи"
        >
      </div>

      <!-- Загрузка файлов -->
      <div>
        <label class="block text-sm font-medium text-tg-text mb-2">Техническое задание (опционально)</label>
        <input 
          @change="handleFileUpload" 
          type="file" 
          accept=".pdf,.doc,.docx,.txt"
          class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        >
        <p class="text-xs text-tg-hint mt-1">PDF, DOC, DOCX, TXT до 10MB</p>
      </div>

      <!-- Калькулятор стоимости -->
      <div class="bg-blue-50 p-4 rounded-lg">
        <h3 class="font-medium text-gray-900 mb-2">💰 Предварительная стоимость</h3>
        <div class="text-2xl font-bold text-blue-600">{{ calculatedPrice }} ₽</div>
        <p class="text-sm text-gray-600 mt-1">Точная стоимость определяется после анализа требований</p>
      </div>

      <!-- Кнопка отправки -->
      <button 
        type="submit" 
        :disabled="isSubmitting"
        class="btn-primary w-full disabled:opacity-50"
      >
        {{ isSubmitting ? 'Отправка...' : 'Отправить заявку' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const form = ref({
  projectType: '',
  projectName: '',
  description: '',
  platforms: [],
  features: [],
  budget: '',
  timeline: '',
  contact: '',
  file: null
})

const isSubmitting = ref(false)

const availableFeatures = ref([
  { id: 'auth', name: 'Авторизация' },
  { id: 'payments', name: 'Платежи' },
  { id: 'push', name: 'Push уведомления' },
  { id: 'chat', name: 'Чат/Сообщения' },
  { id: 'maps', name: 'Карты/Геолокация' },
  { id: 'social', name: 'Соцсети' },
  { id: 'admin', name: 'Админ панель' },
  { id: 'api', name: 'API интеграции' }
])

const calculatedPrice = computed(() => {
  let basePrice = 0
  
  // Базовая цена по типу проекта
  switch (form.value.projectType) {
    case 'mobile': basePrice = 150000; break
    case 'web': basePrice = 80000; break
    case 'ai': basePrice = 120000; break
    case 'integration': basePrice = 60000; break
    default: return '0'
  }
  
  // Добавляем за функции
  basePrice += form.value.features.length * 15000
  
  // Добавляем за платформы
  if (form.value.platforms.includes('ios') && form.value.platforms.includes('android')) {
    basePrice += 50000
  }
  
  return basePrice.toLocaleString('ru-RU')
})

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file && file.size <= 10 * 1024 * 1024) { // 10MB
    form.value.file = file
  } else {
    alert('Файл слишком большой. Максимум 10MB')
    event.target.value = ''
  }
}

const submitForm = async () => {
  isSubmitting.value = true
  
  try {
    // Подготовка данных
    const formData = {
      ...form.value,
      telegram_user: window.Telegram?.WebApp?.initDataUnsafe?.user,
      calculated_price: calculatedPrice.value
    }
    
    // Отправка через Telegram WebApp
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.sendData(JSON.stringify(formData))
    } else {
      // Fallback для тестирования
      console.log('Form data:', formData)
      alert('Заявка отправлена! Мы свяжемся с вами в ближайшее время.')
    }
    
  } catch (error) {
    console.error('Submit error:', error)
    alert('Ошибка отправки. Попробуйте еще раз.')
  } finally {
    isSubmitting.value = false
  }
}
</script>