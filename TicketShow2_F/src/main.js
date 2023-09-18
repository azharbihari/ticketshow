import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import Spinner from "@/components/PageSpinner.vue";
import AlertMessage from "@/components/AlertMessage.vue";


const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('PageSpinner', Spinner);
app.component('AlertMessage', AlertMessage);
app.mount('#app')