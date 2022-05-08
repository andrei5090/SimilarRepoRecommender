import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueTree from '@ssthouse/vue-tree-chart'

Vue.config.productionTip = false

Vue.component('vue-tree', VueTree)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
