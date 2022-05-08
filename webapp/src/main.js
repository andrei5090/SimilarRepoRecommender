import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueTree from '@ssthouse/vue-tree-chart'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false

Vue.component('vue-tree', VueTree)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
