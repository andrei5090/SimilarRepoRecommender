import Vue from 'vue'
import Vuex from 'vuex'
import {Octokit} from "octokit";
import axios from "axios";
import {getRecommendation} from "../hierarchy/hierarchy";

axios.defaults.baseURL = process.env.VUE_APP_BASE_URL

const octokit = new Octokit({auth: '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'})


Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        clusters: null,
        labels: {},
        searchData: null,
        githubSearchData: null,
        googleSearchData: null,
        availableTags: null,
        computedHierarchy: null,
        hierarchyLevels: null,
        recommendedTags: null,
        feedbackStatus: null,
        userFeedbackData:null
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
        storeComputedHierarchy(state, data) {
            state.computedHierarchy = data
        },
        resetHierarchyMutation(state) {
            state.computedHierarchy = null
            state.clusters = null
        },
        storeRecommendedTags(state, data) {
            state.recommendedTags = data
        },
        storeFeedbackStatus(state, data) {
            state.feedbackStatus = data
        },
        storeGithubSearchData(state, data) {
            state.githubSearchData = data
        },
        storeGoogleSearchData(state, data) {
            state.googleSearchData = data
        },
        storeUserFeedbackData(state, data){
            state.userFeedbackData = data
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
            const res = await octokit.request('GET /search/topics', {q: 'ruby+is:featured'})

            commit('storeSearchData', res)
        },
        async retrieveAvailableTags({commit}) {
            const response = await axios.get('/tags')
            commit('storeAvailableTopics', response.data)
        },
        async searchTextAndTags({commit}, data) {
            const method = 'is:featured'
            let query = ''

            if (data.text && data.text.length >= 1)
                query += data.text

            if (data.tags && data.tags.length > 0)
                data.tags.forEach((tag) => query += ' ' + tag + ' ' + method)

            try {
                const res = await octokit.request('GET /search/repositories', {q: query})
                commit('storeSearchData', res)
            } catch (e) {
                commit('storeSearchData', {items: [], status: 422, error: e.message})
            }
        },
        async searchTextGithub({commit}, data) {
            let query = ''

            if (data.text && data.text.length >= 1)
                query += data.text

            try {
                const res = await octokit.request('GET /search/repositories', {q: query})

                commit('storeGithubSearchData', res)
            } catch (e) {
                commit('storeGithubSearchData', {items: [], status: 422, error: e.message})
            }
        },
        async retrieveHierarchy({commit}, data) {
            try {
                const response = await axios.get('/hierarchy?method=' + data.method + '&metric=' + data.metric + '&cuts=' + data.cuts)
                commit('storeComputedHierarchy', {error: null, payload: response.data.payload})
            } catch (e) {
                commit('storeComputedHierarchy', {error: e.response.data.detail, payload: null})
            }
        },
        resetHierarchy({commit}) {
            commit('resetHierarchyMutation')
        },
        // eslint-disable-next-line no-unused-vars
        computeRecommendation({commit, state}, data) {
            commit('storeRecommendedTags', getRecommendation(state.computedHierarchy, data))

        },
        resetSearch({commit}) {
            commit('storeSearchData', null)
            commit('storeGithubSearchData', null)
            commit('storeGoogleSearchData', null)
        },
        async sendFeedback({commit}, data) {
            try {
                await axios.post('/feedback', data, {
                    'Content-Type': 'application/json;charset=UTF-8',
                    "Access-Control-Allow-Origin": "*",
                })
                commit('storeFeedbackStatus', {
                    error: null,
                    message: 'Your feedback for this scenario has been recorded. Please continue with the next scenario.',
                    title: 'Feedback Success'
                })

            } catch (e) {
                commit('storeFeedbackStatus', {
                    error: e,
                    message: 'The feedback for this scenario was not recorder. Please contact the developer or try submitting again.',
                    title: 'Feedback Error (' + e.response.status + ')'
                })
            }
        },
        // eslint-disable-next-line no-unused-vars
        async searchRepositoryDataFromGoogle({commit}, data) {
            let result = []
            let query = ''
            try {

                if (data.text && data.text.length >= 1)
                    query += data.text

                if (data.tags && data.tags.length > 0)
                    data.tags.forEach((tag) => query += ' ' + ' ' + tag)

                const response = await axios.get('/search?query=' + query)


                const length = response.data.links.length

                for (let i = 0; i < length; i++) {
                    try {
                        let splitStr = response.data.links[i].split('/')
                        let owner = splitStr[3]
                        let repo = splitStr[4]
                        const res = await octokit.rest.repos.get({owner: owner, repo: repo})

                        result.push(res.data)
                    } // eslint-disable-next-line no-empty
                    catch (e) {

                    }
                }
                //this.getGoogleSearchData.data.items

                commit('storeGoogleSearchData', {data: {items: result}, status: 200})

            } catch (e) {
                commit('storeGoogleSearchData', {items: [], status: 422, error: e.message})
            }
        },
        addUserFeedbackData({commit}, data){
            commit('storeUserFeedbackData', data)
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
        },
        getComputedHierarchy(state) {
            return state.computedHierarchy
        },
        getRecommendedTags(state) {
            return state.recommendedTags
        },
        getFeedbackStatus(state) {
            return state.feedbackStatus
        },
        getGithubSearchData(state) {
            return state.githubSearchData
        },
        getGoogleSearchData(state) {
            return state.googleSearchData
        },
        getUserFeedbackData(state){
            return state.userFeedbackData
        }
    },
    modules: {}
})
