<template>
  <div>
    <v-card shaped class="search-card mt-7" elevation="5" v-if="searchData" :loading="loading">
      <v-card-title>{{ searchTitle }}</v-card-title>
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
              <v-list-item-action v-if="evaluationMode">
                <v-checkbox @click.prevent v-model="res.checked"></v-checkbox>
              </v-list-item-action>
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
  </div>
</template>

<script>

export default {
  name: 'SearchResult',
  props: {
    searchData: {
      required: true,
      default: () => {
        return []
      },
    },
    searchTitle: {
      type: String,
      required: false,
      default: "Search Results"
    },
    evaluationMode: {
      type: Boolean,
      default: false
    },
    loading:{
      type: Boolean,
      default: false
    }
  },
  data() {
    return {}
  },
  methods: {
    collectData(){
      return this.searchData
    }
  },
  computed: {},
  watch: {}
}
</script>

<style scoped lang="sass">
</style>
