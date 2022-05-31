<template>
  <div>
    <!--   Start Button   -->
    <div v-if="!started" class="center-align">
      <v-row align="center" justify="center">
        <v-col cols="12" md="10" class="text-center">
          <v-card>
            <v-card-title>Your task</v-card-title>
            <v-card-text>{{ lorem }}</v-card-text>
            <v-card-actions class="justify-center">
              <v-btn @click="started = true" color="primary" x-large>
                Start
                <v-icon right>mdi-arrow-right-bold-circle</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

    </div>
    <div v-else>
      <!-- Scenario -->
      <v-row justify="center">
        <v-col cols="11" md="6">
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <v-progress-linear
                  color="light-blue darken-3"
                  striped
                  height="10"
                  :value="(progressIndex + 1) * 100 / scenarios.length"
                  v-bind="attrs"
                  v-on="on"
              >
              </v-progress-linear>
            </template>
            <span>Your progress</span>
          </v-tooltip>
          <v-card rounded>
            <v-card-title>Your current search scenario</v-card-title>
            <v-card-text>{{ scenario }}</v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-fab-transition>
        <v-row v-show="!searchCompleted">
          <v-col cols="12">
            <SearchBar :evaluation-mode="true" :loading="loading" @search="search"/>
          </v-col>
        </v-row>
      </v-fab-transition>
      <v-fab-transition>
        <v-row justify="center" align="center" v-show="searchCompleted">
          <v-col cols="12" class="text-center">
            <v-btn rounded color="primary" @click="searchCompleted = false; evalStatus=false">
              Search Again
              <v-icon right>mdi-magnify</v-icon>
            </v-btn>
          </v-col>


          <v-col cols="11" md="6" class="text-center">
            <v-card shaped elevation="5">
              <div v-if="evalStatus">
                <v-card-text class="text-center success--text font-weight-bold text-h6">
                  Please check the results that you find more relevant in all the Search Results below given the current
                  scenario.
                </v-card-text>
                <v-card-text class="text-center font-weight-bold">
                  When you are done, press the submit button.
                </v-card-text>


              </div>
              <div v-else>
                <v-card-text class="text-center success--text font-weight-bold text-h6">
                  Please analyze all the results and when you are finished, press the Start Evaluation button.
                </v-card-text>

                <v-card-actions class="text-center justify-center">
                  <v-btn x-large rounded color="primary" @click="evalStatus = true">Start Evaluation
                    <v-icon right>mdi-podium</v-icon>
                  </v-btn>
                </v-card-actions>
              </div>
            </v-card>
          </v-col>
        </v-row>

      </v-fab-transition>


      <v-row justify="space-around" v-if="searchData.length > 0">
        <v-col cols="11" md="4" class="">
          <SearchResult :evaluation-mode="evalStatus" :search-data="searchData" v-if="searchData"
                        search-title="Search Results 1"/>
        </v-col>

        <v-col cols="11" md="4" class="">
          <SearchResult :evaluation-mode="evalStatus" :search-data="searchData" v-if="searchData"
                        search-title="Search Results 2"/>
        </v-col>

        <v-col cols="11" md="4" class="">
          <SearchResult :evaluation-mode="evalStatus" :search-data="searchData" v-if="searchData"
                        search-title="Search Results 3"/>
        </v-col>

      </v-row>
    </div>
  </div>
</template>

<script>


import SearchBar from "../components/SearchBar";
import SearchResult from "../components/SearchResult";
import {mapActions, mapGetters} from "vuex";

export default {
  name: 'Evaluation',
  components: {SearchResult, SearchBar},
  data() {
    return {
      loading: false,
      started: false,
      searchCompleted: false,
      progressIndex: 0,
      scenarios: ['', '', '', '', ''],
      evalStatus: false,
      scenario: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In mollis purus non ipsum accumsan iaculis. Aliquam convallis ante quam, sed rhoncus turpis cursus ac. Maecenas at pretium enim, a facilisis ipsum. Etiam eleifend lacus sit amet odio pellentesque consectetur. Quisque id dui tincidunt, laoreet massa dignissim, fermentum odio. Sed efficitur arcu pharetra quam imperdiet, quis imperdiet eros scelerisque. Proin eu posuere dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque ex diam, euismod sed felis quis, tempus tempor nunc. Sed dapibus quam eget dolor fermentum, a placerat ligula fringilla. Quisque semper magna et justo blandit accumsan. Phasellus in porta dolor, a accumsan felis. In vitae elit auctor, tempor purus eget, sollicitudin risus.',
      lorem: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In mollis purus non ipsum accumsan iaculis. Aliquam convallis ante quam, sed rhoncus turpis cursus ac. Maecenas at pretium enim, a facilisis ipsum. Etiam eleifend lacus sit amet odio pellentesque consectetur. Quisque id dui tincidunt, laoreet massa dignissim, fermentum odio. Sed efficitur arcu pharetra quam imperdiet, quis imperdiet eros scelerisque. Proin eu posuere dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque ex diam, euismod sed felis quis, tempus tempor nunc. Sed dapibus quam eget dolor fermentum, a placerat ligula fringilla. Quisque semper magna et justo blandit accumsan. Phasellus in porta dolor, a accumsan felis. In vitae elit auctor, tempor purus eget, sollicitudin risus.'
    }
  },
  methods: {
    ...mapActions(['searchTextAndTags', 'resetSearch', 'sendFeedback']),
    search(searchQuery) {
      this.loading = true
      this.searchTextAndTags(searchQuery)
    }
  },
  computed: {
    ...mapGetters(['getSearchData', 'getFeedbackStatus']),
    searchData() {
      try {
        return this.getSearchData ? this.getSearchData.data.items ? this.getSearchData.data.items : [] : []
      } catch (e) {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        this.loading = false
        return []
      }
    }
  },
  mounted() {
    this.resetSearch()
    this.evalStatus = false
    this.searchCompleted = false
  },
  watch: {
    getSearchData() {
      this.searchCompleted = true
      this.loading = false
    },
    getFeedbackStatus(newValue) {
      if (newValue.error)
        this.$toast.error(newValue.message, newValue.title, {position: "topCenter"});
      else
        this.$toast.success(newValue.message, newValue.title, {position: "topCenter"});


    }
  }
}
</script>

<style scoped lang="sass">

.center-align
  position: fixed
  top: 50%
  left: 50%
  transform: translate(-50%, -50%)

</style>
