import Vue from 'vue'
import App from './App.vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'
import axios from 'axios'
Vue.config.productionTip = false
Vue.use(Antd)
Vue.prototype.$http = axios.create({
  baseURL: "http://127.0.0.1:5000",
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' }
})
new Vue({
  render: h => h(App),
}).$mount('#app')
