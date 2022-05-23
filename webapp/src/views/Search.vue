<template>
  <v-container>

    <v-row justify="center" class="ma-4">
      <v-col cols="2" class="justify-center text-center">
        <v-btn class="text-center" rounded x-large color="black"><span class="white--text" @click="testOctokit"> TEST </span></v-btn>
      </v-col>
    </v-row>

    <v-card shaped>
      <v-card-title>Test Result</v-card-title>
      <v-card-text>
        <v-list rounded>
          <v-list-item-group>
            <v-list-item v-for="(res,index) in searchData" :key="index">
              <v-list-item-content>
                <v-list-item-title>
                  {{ res.name }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ res.short_description }}
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

export default {
  name: 'Search',
  components: {},
  methods: {
    ...mapActions(['testOctokit'])
  },
  computed: {
    ...mapGetters(['getSearchData']),
    searchData() {
      return this.getSearchData ? this.getSearchData.data.items ? this.getSearchData.data.items : [] : []
    }
  }
}
</script>
