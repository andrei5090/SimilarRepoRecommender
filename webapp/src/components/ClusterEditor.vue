<template>
  <div class="">
    <v-card>

      <v-card-text>
        <v-row justify="center">
          <v-col cols="5">
            <v-text-field v-model="getLabels[id]"/>
          </v-col>
        </v-row>
      </v-card-text>

<!--      <v-card-actions>-->
<!--        <v-btn rounded left size color="indigo lighten-3">-->
<!--          <v-icon small>mdi-arrow-down-circle</v-icon>-->
<!--          Save-->
<!--        </v-btn>-->
<!--      </v-card-actions>-->

      <v-card-text class="mt-3">
        <ClusterRepresentation :clusters="clusters" :padding="padding"/>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>


import ClusterRepresentation from "./ClusterRepresentation";
import {mapGetters} from "vuex";

export default {
  name: 'ClusterEditor',
  components: {ClusterRepresentation},
  props: {
    clusters: {
      type: Array,
      required: true
    },
    padding: {
      type: Boolean,
      default: false
    },
    id: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      clusterName: ''
    }
  },
  methods: {
    filterElement(el) {
      delete el['_key']
      let val = ""
      Object.values(el).forEach(el => val += el)
      return val
    }
  },
  computed: {
    ...mapGetters(['getLabels'])
  }
}
</script>

<style scoped lang="sass">
</style>
