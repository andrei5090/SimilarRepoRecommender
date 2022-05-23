<template>
  <div class="">
    <v-card>
      <v-card-title>
        Cluster {{ id }}
      </v-card-title>
      <v-card-text>
        <v-row justify="center">
          <v-col cols="5">
            <v-text-field v-model="getLabels[id].label" label="Label" prepend-icon="mdi-label"/>
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col cols="5">
            <v-text-field v-model="getLabels[id].weight" label="Weight" prepend-icon="mdi-numeric"/>
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
import {mapActions, mapGetters} from "vuex";

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
      clusterName: '',
    }
  },
  methods: {
    ...mapActions(['modifyLabel']),
    filterElement(el) {
      delete el['_key']
      let val = ""
      Object.values(el).forEach(el => val += el)
      return val
    }
  },
  computed: {
    ...mapGetters(['getLabels'])
  },
  created() {
    if (!this.getLabels[this.id])
      this.getLabels[this.id] = {}

    if (!this.getLabels[this.id]['label'])
      this.getLabels[this.id]['label'] = null

    if (!this.getLabels[this.id]['weight'])
      this.getLabels[this.id]['weight'] = null
  },
  watch: {
    id(newValue) {
      if (!this.getLabels[newValue])
        this.getLabels[newValue] = {}

      if (!this.getLabels[newValue]['label'])
        this.getLabels[newValue]['label'] = null

      if (!this.getLabels[newValue]['weight'])
        this.getLabels[newValue]['weight'] = null


    }
  }
}
</script>

<style scoped lang="sass">
</style>
