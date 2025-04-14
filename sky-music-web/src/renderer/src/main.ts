import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import naive from 'naive-ui'
import i18n from './i18n'

const app = createApp(App)
app.use(store)
app.use(router)
app.use(naive)
app.use(i18n)
app.mount('#app')
