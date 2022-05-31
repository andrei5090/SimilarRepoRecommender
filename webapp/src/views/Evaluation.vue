<template>
  <div>
    <!--   Start Button   -->
    <div v-if="!started" class="center-align">
      <v-row align="center" justify="center">
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
      </v-row>

    </div>
    <div v-else>
      <!--      Scenario -->
      <v-row justify="center">
        <v-col cols="6">
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
          <v-col cols="1">
            <v-btn rounded color="primary" @click="searchCompleted = false">Search Again
              <v-icon right>mdi-magnify</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-fab-transition>


      <v-row justify="space-around" v-if="searchData.length > 0">
        <v-col cols="4" class="">
          <SearchResult :search-data="searchData" v-if="searchData" search-title="Search Results 1"/>
        </v-col>

        <v-col cols="4" class="">
          <SearchResult :search-data="searchData" v-if="searchData" search-title="Search Results 2"/>
        </v-col>


        <v-col cols="4" class="">
          <SearchResult :search-data="searchData" v-if="searchData" search-title="Search Results 3"/>
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
      scenario: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In mollis purus non ipsum accumsan iaculis. Aliquam convallis ante quam, sed rhoncus turpis cursus ac. Maecenas at pretium enim, a facilisis ipsum. Etiam eleifend lacus sit amet odio pellentesque consectetur. Quisque id dui tincidunt, laoreet massa dignissim, fermentum odio. Sed efficitur arcu pharetra quam imperdiet, quis imperdiet eros scelerisque. Proin eu posuere dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque ex diam, euismod sed felis quis, tempus tempor nunc. Sed dapibus quam eget dolor fermentum, a placerat ligula fringilla. Quisque semper magna et justo blandit accumsan. Phasellus in porta dolor, a accumsan felis. In vitae elit auctor, tempor purus eget, sollicitudin risus.',
      lorem: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In mollis purus non ipsum accumsan iaculis. Aliquam convallis ante quam, sed rhoncus turpis cursus ac. Maecenas at pretium enim, a facilisis ipsum. Etiam eleifend lacus sit amet odio pellentesque consectetur. Quisque id dui tincidunt, laoreet massa dignissim, fermentum odio. Sed efficitur arcu pharetra quam imperdiet, quis imperdiet eros scelerisque. Proin eu posuere dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque ex diam, euismod sed felis quis, tempus tempor nunc. Sed dapibus quam eget dolor fermentum, a placerat ligula fringilla. Quisque semper magna et justo blandit accumsan. Phasellus in porta dolor, a accumsan felis. In vitae elit auctor, tempor purus eget, sollicitudin risus.'
    }
  },
  methods: {
    ...mapActions(['searchTextAndTags', 'resetSearch']),
    search(searchQuery) {
      this.loading = true
      this.searchTextAndTags(searchQuery)
    }
  },
  computed: {
    ...mapGetters(['getSearchData']),
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
  },
  watch: {
    getSearchData() {
      this.searchCompleted = true
      this.loading = false
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
