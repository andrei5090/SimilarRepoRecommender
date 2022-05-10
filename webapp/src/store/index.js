import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        clusters: null,
        labels: null
    },
    mutations: {
        addClusters(state, data) {
            state.clusters = data
        },
        addLabels(state, data) {
            state.labels = data
        },
        addLabel(state,data){
            state.labels[data.id] = data.label
        }
    },
    actions: {
        storeCluster({commit}, data) {
            commit('addClusters', data)
        },
        storeLabels({commit}, data) {
            commit('addLabels', data)
        },
        modifyLabel({commit}, data){
            commit.addLabel(data)
        }
    },
    getters: {
        getCluster(state) {
            return state.clusters
        },
        getLabels(state) {
            return state.labels
        }
    },
    modules: {}
})
