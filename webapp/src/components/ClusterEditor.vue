<template>
  <div class="">
    <v-card>

      <v-card-text>
        <v-row justify="center">
          <v-col cols="5">
            <v-text-field v-model="clusterName"/>
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
  }
}
</script>

<style scoped lang="sass">
</style>
