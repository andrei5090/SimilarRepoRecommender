<template>

  <v-container>
    <v-form v-model="valid">

      <v-row>
        <v-col cols="12">
          <v-card elevation="5" class="search-bar">
            <v-card-title>
              <v-row justify="space-between" align="center">

                <v-col cols="7" class="text-center" align="center">
                  <div class="pt-7"></div>
                  <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field v-model="queryText" label="Search" prepend-icon="mdi-magnify" outlined
                                    v-bind="attrs"
                                    v-on="on" class="justify-center" single-line rounded clearable
                                    :rules="queryText.length === 0 ? [() => true] : queryRules" counter>
                      </v-text-field>
                    </template>
                    Your Search Query
                  </v-tooltip>
                </v-col>

                <v-col cols="4" class="ma-0 pa-0">
                  <div class="pt-7"></div>
                  <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                      <v-autocomplete
                          auto-select-first
                          clearable
                          deletable-chips
                          multiple
                          v-model="chosenTags"
                          :items="getItems"
                          outlined
                          label="Input Tags"
                          v-bind="attrs"
                          v-on="on"
                          single-line
                          rounded
                          prepend-inner-icon="mdi-label"
                          :rules="chosenTags.length === 0 && queryText.length === 0 ? [() => false] : tagsRules"
                          no-data-text="There is no match between your search and the available tags."
                      >

                        <template v-slot:selection="data">
                          <v-chip color="tag" close
                                  @click:close="remove(data)">
                            {{ data.item }}
                          </v-chip>
                        </template>


                        <template v-slot:item="data">
                          <template v-if="typeof data.item !== 'object'">
                            <v-chip color="tag">
                              {{ data.item }}
                            </v-chip>
                          </template>
                        </template>


                        <!--  Suggest Button -->
                        <template v-slot:append-outer>
                          <v-tooltip top>
                            <template v-slot:activator="{ on, attrs }">
                              <v-slide-x-reverse-transition
                                  mode="out-in"
                              >
                                <div v-bind="attrs"
                                     v-on="on"
                                     :key="`icon-${isSuggesting}`" @click="toggleHierarchy">
                                  <v-icon
                                      :color="isSuggesting || evaluationMode ? 'success' : 'error'"
                                      @click="!evaluationMode ? isSuggesting = !isSuggesting : ''"
                                      v-text="'mdi-graph'"
                                  ></v-icon>
                                </div>
                              </v-slide-x-reverse-transition>
                            </template>
                            {{
                              evaluationMode ? 'The Suggestions are turned on!' : isSuggesting ? 'Do not suggest Tags based on the Hierarchy' : 'Suggest tags based on the Hierarchy'
                            }}
                          </v-tooltip>
                        </template>
                      </v-autocomplete>

                    </template>
                    The tags/topics you are interested with
                  </v-tooltip>

                </v-col>

                <!--          Search Button    -->
                <v-col cols="1" align="right">
                  <v-btn color="primary" x-large elevation="8" fab
                         @click="$emit('search', {text : queryText, tags: chosenTags})" :disabled="!valid"
                         :loading="loading">
                    <v-icon>
                      mdi-magnify
                    </v-icon>
                  </v-btn>
                </v-col>

              </v-row>

            </v-card-title>

          </v-card>
        </v-col>
      </v-row>

      <v-card elevation="5" class="hierarchy-chooser" :disabled="evaluationMode">
        <v-fab-transition>
          <v-row class="mt-5" v-show="isSuggesting || evaluationMode">
            <v-col cols="12">
              <HierarchyChooser @compute-hierarchy="retrieveHierarchy"
                                :evaluation-mode="evaluationMode"></HierarchyChooser>
            </v-col>
          </v-row>
        </v-fab-transition>

      </v-card>
    </v-form>

  </v-container>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
import HierarchyChooser from "./HierarchyChooser";

export default {
  name: 'SearchBar',
  components: {HierarchyChooser},
  props: {
    loading: {
      default: false,
      required: true
    },
    evaluationMode: {
      default: false
    }
  },
  data() {
    return {
      chosenTags: [],
      queryText: '',
      valid: false,
      isSuggesting: false,
      queryRules: [(text) => text.length < 300 || 'The maximum textual search should have at most 100 characters',
        (text) => text.length > 0 || 'The minimum textual information should have at least 1 characters'],
      tagsRules: [(tags) => tags.length < 5 || 'The maximum query can have up to 5 tags',
        (tags) => tags.length > -1 || 'The minimum query can have at least 1 tag']

    }
  },
  methods: {
    remove(item) {
      const index = this.chosenTags.indexOf(item.item)
      if (index >= 0) this.chosenTags.splice(index, 1)
    },
    toggleHierarchy() {
      this.$emit('toggle-hierarchy-chooser')
      if (this.isSuggesting && !this.evaluationMode)
        this.$toast.warning('Before getting suggestions, you have to generate a hierarchy based on the selectors below.', 'Search Info', {position: "topCenter"});
    },
    ...mapActions(['computeRecommendation', 'retrieveAvailableTags', 'retrieveHierarchy', 'resetSearch'])
  },
  computed: {
    ...mapGetters(['getRecommendedTags', 'getAvailableTags', 'getComputedHierarchy', 'getSearchData']),
    getItems() {
      if (!this.isSuggesting || this.chosenTags.length === 0)
        return this.getAvailableTags
      else if (this.getComputedHierarchy) {
        this.computeRecommendation(this.chosenTags)
        return this.getRecommendedTags
      } else return this.getAvailableTags
    }
  },
  mounted() {
    this.resetSearch()
    this.retrieveAvailableTags()
    if (this.evaluationMode)
      this.isSuggesting = true
  },
  watch: {
    getSearchData(newValue) {
      if (newValue != null) {
        if (newValue.error) {
          this.$toast.error("GithubAPI " + newValue.error, "Search Error", {position: "topCenter"});
        }
      }
    }
  }

}
</script>

<style lang="sass" scoped>
::v-deep .search-bar
  border-radius: 20px 70px 70px 70px !important

::v-deep .hierarchy-chooser
  border-radius: 30px 70px 70px 30px !important

</style>
