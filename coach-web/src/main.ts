import { createApp } from "vue"
import { createPinia } from "pinia"
import ElementPlus from "element-plus"
import "element-plus/dist/index.css"
import "element-plus/theme-chalk/dark/css-vars.css"  // v7 暗色
import "./assets/design-tokens.css"                   // v7 令牌 + Element 覆写
import App from "./App.vue"
import router from "./router"

document.documentElement.classList.add("dark")        // 启用 Element 暗色

createApp(App).use(createPinia()).use(router).use(ElementPlus).mount("#app")
