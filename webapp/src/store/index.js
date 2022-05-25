import Vue from 'vue'
import Vuex from 'vuex'
import {Octokit} from "octokit";
import axios from "axios";

axios.defaults.baseURL = process.env.VUE_APP_BASE_URL

const octokit = new Octokit({
    auth: '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'
})


Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        clusters: null,
        labels: {},
        searchData: null,
        availableTags: null
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
        },
        storeAvailableTopics(state, data) {
            state.availableTags = data

        },
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


            const res = await octokit.request('GET /search/topics', {q: 'ruby+is:featured'})

            commit('storeSearchData', res)
        },
        async retrieveAvailableTags({commit}) {
            // eslint-disable-next-line no-unused-vars
            const response = await axios.get('/tags')
            commit('storeAvailableTopics', response.data)


        },
        async searchTextAndTags({commit}, data) {
            const method = 'is:featured'
            let query = ''

            if (data.text && data.text.length > 5)
                query += data.text

            if (data.tags && data.tags.length > 0)
                data.tags.forEach((tag) => query += ' ' + method + ' ' + tag)


            const res = await octokit.request('GET /search/repositories', {q: query})

            console.log("res", res)


            commit('storeSearchData', res)


        }


    },
    getters: {
        getCluster(state) {
            return state.clusters
        },
        getLabels(state) {
            return state.labels
        },
        getSearchData(state) {
            return state.searchData
        },
        getAvailableTags(state) {
            if (state.availableTags && state.availableTags.payload)
                return state.availableTags.payload
            return null
        }
    }
    ,
    modules: {}
})
