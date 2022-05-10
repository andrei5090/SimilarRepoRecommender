import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        clusters: null
    },
    mutations: {
        addClusters(state, data) {
            state.clusters = data
        }
    },
    actions: {
        storeCluster({commit}, data) {
            commit('addClusters', data)
        }
    },
    getters: {
        getCluster(state) {
            return state.clusters
        }
    },
    modules: {}
})
