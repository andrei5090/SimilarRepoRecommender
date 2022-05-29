<template>
  <div>
    <v-row justify="space-around">
      <v-col cols="4">
        <v-row>
          <v-subheader>
            The minimum number of clusters in the Hierarchy
          </v-subheader>
        </v-row>
        <v-row class="mt-8">
          <v-slider
              class="ml-5"
              thumb-label="always"
              v-model="cuts"
              :step="step"
              :min="minCuts"
              :max="maxCuts"
              :color="getProgressColor"
          >
            <template #prepend>
              <v-icon :color="getProgressColor">mdi-chart-timeline-variant-shimmer</v-icon>
            </template>
          </v-slider>
        </v-row>
      </v-col>

      <v-col cols="3">
        <div class="mt-8"/>
        <v-select
            class="text-capitalize"
            v-model="methodSelection"
            :items="methods"
            label="Method"
            dense
            outlined
            rounded
        >
        </v-select>
      </v-col>


      <v-col cols="3">
        <div class="mt-8"/>
        <v-select
            class="text-capitalize"
            v-model="metricsSelection"
            :items="metrics"
            label="Metric"
            dense
            outlined
            rounded
        ></v-select>
      </v-col>

      <v-col cols="1" align="right">
        <div class="mt-4"/>
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn :color="getComputedHierarchy && !newData ? 'success' : 'primary'" x-large elevation="8" fab
                   :loading="loading"
                   align="right"
                   v-on="on"
                   v-bind="attrs"
                   @click="$emit('compute-hierarchy',{cuts: cuts, method:methodSelection, metric:metricsSelection}); loading = true">

              <v-fade-transition>
                <v-icon v-if="!getComputedHierarchy || newData">
                  mdi-graph
                </v-icon>
                <v-icon v-else>
                  mdi-check-outline
                </v-icon>
              </v-fade-transition>
            </v-btn>
          </template>
          Generate Hierarchy
        </v-tooltip>
      </v-col>

    </v-row>
  </div>
</template>

<script>


import {mapGetters} from "vuex";

export default {
  name: 'HierarchyChooser',
  props: {
  },
  data() {
    return {
      cuts: 0,
      minCuts: 1,
      maxCuts: 525,
      step: 1,
      methods: ['ward', 'single', 'complete', 'average', 'weighted', 'centroid', 'median'],
      metrics: ['euclidean', 'minkowski', 'cityblock', 'seuclidean', 'sqeuclidean',
        'cosine', 'correlation', 'hamming',
        'jaccard', 'jensenshannon', 'chebyshev', 'canberra',
        'braycurtis', 'mahalanobis', 'yule', 'dice', 'kulsinski', 'rogerstanimoto',
        'russellrao', 'sokalmichener', 'sokalsneath', 'kulczynski1'],
      methodSelection: 'ward',
      metricsSelection: 'euclidean',
      loading: false,
      newData: false
    }
  },
  computed: {
    getProgressColor() {
      let colors = ['blue', 'yellow darken-2', 'red']
      let p = 0
      if (this.cuts > this.maxCuts / 3)
        p = 1
      if (this.cuts > this.maxCuts * 2 / 3)
        p = 2
      let color = colors[p]
      return color
    },
    ...mapGetters(['getComputedHierarchy'])
  },
  methods: {},
  watch: {
    getComputedHierarchy(newValue) {

      if (newValue && newValue.error != null)
        this.$toast.error(newValue.error, 'Hierarchy Generation Error', {position: "topCenter"});
      else
        this.$toast.success('The hierarchy was successfully generated!', 'Hierarchy Info', {position: "topCenter"});

      this.newData = false
      this.loading = false

    },
    cuts() {
      this.newData = true
    },
    methodSelection() {
      this.newData = true
    },
    metricsSelection() {
      this.newData = true
    }
  }
}
</script>

<style scoped lang="sass">
</style>
