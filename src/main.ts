import { createApp } from 'vue'
import './style/reset.scss'
import App from './App.vue'
import router from './router';
// 引入element-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

import { createPinia } from 'pinia';
// import dialog from './components/dialog.vue';
const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
// app.component('dialog', dialog)
app.use(ElementPlus, { locale: zhCn })
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(router)
app.mount('#app')