import './assets/css/modern-forms.css' // Import Custom BEM Styles
import './assets/service-registry-bem.css' // Import BEM Component Library
import './assets/css/birth-certificate.css' // Import Birth Certificate BEM Styles
import './assets/css/digital-wallet-card.css' // Import Digital Wallet Card Styles

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './index.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.mount('#app')
