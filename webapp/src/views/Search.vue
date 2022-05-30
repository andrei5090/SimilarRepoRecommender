<template>
  <v-container>

    <v-row>
      <SearchBar @search="search" :loading="loading"></SearchBar>
    </v-row>

    <!--    <v-row class="ma-5" justify="center" v-if="getAvailableTags">-->
    <!--      <v-col cols="10">-->
    <!--        <v-card>-->
    <!--          <v-chip class="ma-1" color="deep-purple lighten-4" v-for="(el, index) in getAvailableTags" :key="index">-->
    <!--            {{ el }}-->
    <!--          </v-chip>-->
    <!--        </v-card>-->
    <!--      </v-col>-->

    <!--    </v-row>-->
    <!--TEST BUTTON-->
    <!--    <v-row justify="center" class="ma-4">-->
    <!--      <v-col cols="2" class="justify-center text-center">-->
    <!--        <v-btn class="text-center" rounded x-large color="black"><span class="white&#45;&#45;text"-->
    <!--                                                                       @click="testOctokit"> TEST </span></v-btn>-->
    <!--      </v-col>-->
    <!--    </v-row>-->
    <v-row justify="space-around">
      <v-col cols="12">
        <v-fade-transition>
          <SearchResult :search-data="searchData" v-if="getSearchData"/>
        </v-fade-transition>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

import {mapActions, mapGetters} from "vuex";
import SearchBar from "../components/SearchBar";
import SearchResult from "../components/SearchResult";

export default {
  name: 'Search',
  components: {SearchResult, SearchBar},
  data() {
    return {
      loading: false
    }
  },
  methods: {
    ...mapActions(['testOctokit', 'searchTextAndTags', 'retrieveHierarchy', 'computeHierarchyLevels']),
    search(searchQuery) {
      this.loading = true
      this.searchTextAndTags(searchQuery)
    }
  },
  computed: {
    ...mapGetters(['getSearchData', 'getSearchData']),
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
  watch: {
    getSearchData(newValue) {
      if (newValue && newValue.status >= 400)
        this.$toast.error('Your search query is not valid', 'Search Error', {position: "topCenter"});

      this.loading = false
    }

  }
}
</script>

<style scoped lang="sass">
::v-deep .search-card
  border-radius: 30px 30px 30px 30px !important
</style>
