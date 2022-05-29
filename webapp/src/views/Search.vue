<template>
  <v-container>

    <v-row>
      <SearchBar :items="getAvailableTags" @search="search" :loading="loading"
                 @toggle-hierarchy-chooser="showHierarchyChooser = !showHierarchyChooser"></SearchBar>
    </v-row>

    <v-fade-transition>
      <v-row class="mt-5" v-if="showHierarchyChooser">
        <v-col cols="12">
          <v-card elevation="5" class="hierarchy-chooser">
            <HierarchyChooser @compute-hierarchy="retrieveHierarchy"></HierarchyChooser>
          </v-card>
        </v-col>
      </v-row>
    </v-fade-transition>

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
    <v-fade-transition>
      <SearchResult :search-data="searchData" v-if="getSearchData"/>
    </v-fade-transition>
  </v-container>
</template>

<script>

import {mapActions, mapGetters} from "vuex";
import SearchBar from "../components/SearchBar";
import HierarchyChooser from "../components/HierarchyChooser";
import SearchResult from "../components/SearchResult";

export default {
  name: 'Search',
  components: {SearchResult, HierarchyChooser, SearchBar},
  data() {
    return {
      loading: false,
      showHierarchyChooser: false
    }
  },
  methods: {
    ...mapActions(['testOctokit', 'retrieveAvailableTags', 'searchTextAndTags', 'retrieveHierarchy', 'computeHierarchyLevels']),
    search(searchQuery) {
      this.loading = true
      this.searchTextAndTags(searchQuery)
    }
  },
  computed: {
    ...mapGetters(['getSearchData', 'getAvailableTags', 'getSearchData']),
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
::v-deep .hierarchy-chooser
  border-radius: 30px 70px 70px 30px !important

::v-deep .search-card
  border-radius: 30px 30px 30px 30px !important
</style>
