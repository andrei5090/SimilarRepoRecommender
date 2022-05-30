<template>
  <div>
    <v-row>
      <v-col cols="12">
        <SearchBar :evaluation-mode="true" :loading="loading" @search="search"/>
      </v-col>
    </v-row>

    <v-row justify="space-around">
      <v-col cols="5" class="ma-2">
        <SearchResult :search-data="searchData" v-if="searchData" search-title="Search Results 1"/>
      </v-col>

      <v-col cols="5" class="ma-2">
        <SearchResult :search-data="searchData" v-if="searchData" search-title="Search Results 2"/>
      </v-col>
    </v-row>
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
      loading: false
    }
  },
  methods: {
    ...mapActions(['searchTextAndTags']),
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
  watch: {
    getSearchData(){
      this.loading = false
    }
  }
}
</script>

<style scoped lang="sass">
</style>
