<template>
  <div class="">
    <v-card :class="padding ? 'mt-5' : ''" elevation="10" v-for="(cluster,index) in clusters" :key="index">
      <v-card-text>
        <v-chip class="ma-1" color="deep-purple lighten-4" v-for="(el, index) in cluster" :key="index"> {{ filterElement(el) }}</v-chip>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>


export default {
  name: 'ClusterRepresentation',
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
    return {}
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
