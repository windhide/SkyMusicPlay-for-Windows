import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import naive from 'naive-ui'

const app = createApp(App)
app.use(store)
app.use(router)
app.use(naive)
app.mount('#app')
