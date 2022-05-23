import Vue from 'vue'
import Vuex from 'vuex'
import {Octokit} from "octokit";



Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        clusters: null,
        labels: {},
        searchData: null
    },
    mutations: {
        addClusters(state, data) {
            state.clusters = data
        },
        addLabels(state, data) {
            state.labels = data
        },
        addLabel(state, data) {
            state.labels[data.id]['label'] = data.label
        },
        addWeight(state, data) {
            state.labels[data.id]['weight'] = data.weight
        },
        storeSearchData(state, data) {
            state.searchData = data
        }
    },
    actions: {
        storeCluster({commit}, data) {
            commit('addClusters', data)
        },
        storeLabels({commit}, data) {
            commit('addLabels', data)
        },
        modifyLabel({commit}, data) {
            commit('addLabel', data)
        },
        async testOctokit({commit}) {

            const octokit = new Octokit({
                auth: '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'
            })

            const res = await octokit.request('GET /search/topics', {q : 'ruby+is:featured'})

            commit('storeSearchData', res)



        }


    },
    getters: {
        getCluster(state) {
            return state.clusters
        }
        ,
        getLabels(state) {
            return state.labels
        },
        getSearchData(state) {
            return state.searchData
        }
    }
    ,
    modules: {}
})
