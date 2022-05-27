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
<v-btn @click="computeHierarchyLevels">click</v-btn>
    <v-card shaped class="search-card mt-7" elevation="5" v-if="getSearchData">
      <v-card-title>Search Results</v-card-title>
      <v-card-text v-if="searchData.length === 0">

        <v-row align="center" justify="center">
          <v-col cols="4" class="justify-center text-center">
            <span class="subtitle-1">No items found based on your search.</span>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-text>
        <v-list rounded>
          <v-list-item-group>
            <v-list-item v-for="(res,index) in searchData" :key="index" :href="res.html_url" target="_blank" dense>
              <v-list-item-content>
                <v-list-item-title>
                  {{ res.full_name }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  <span class="subtitle-2">{{ res.description }}</span>
                </v-list-item-subtitle>
                <v-list-item-subtitle>
                  <v-chip v-for="(tag,index) in res.topics" small color="tag" :key="index" class="ma-1">
                    {{ tag }}
                  </v-chip>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>

      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>

import {mapActions, mapGetters} from "vuex";
import SearchBar from "../components/SearchBar";
import HierarchyChooser from "../components/HierarchyChooser";

export default {
  name: 'Search',
  components: {HierarchyChooser, SearchBar},
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
  mounted() {
    this.retrieveAvailableTags()
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
