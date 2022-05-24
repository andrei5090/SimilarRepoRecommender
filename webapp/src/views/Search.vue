<template>
  <v-container>

    <v-row>
      <SearchBar :items="getAvailableTags"></SearchBar>
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

    <v-row justify="center" class="ma-4">
      <v-col cols="2" class="justify-center text-center">
        <v-btn class="text-center" rounded x-large color="black"><span class="white--text"
                                                                       @click="testOctokit"> TEST </span></v-btn>
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
import SearchBar from "../components/SearchBar";

export default {
  name: 'Search',
  components: {SearchBar},
  methods: {
    ...mapActions(['testOctokit', 'retrieveAvailableTags'])
  },
  computed: {
    ...mapGetters(['getSearchData', 'getAvailableTags']),
    searchData() {
      return this.getSearchData ? this.getSearchData.data.items ? this.getSearchData.data.items : [] : []
    }
  },
  mounted() {
    this.retrieveAvailableTags()
  }
}
</script>
