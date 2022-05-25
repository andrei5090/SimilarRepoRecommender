<template>
  <div class="">
    <v-card :class="padding ? 'mt-5' : ''" elevation="10" v-for="(cluster,index) in clusters" :key="index">
      <v-card-text>
        <v-chip class="ma-1" color="tag" v-for="(el, index) in cluster" :key="index"> {{ filterElement(el) }}</v-chip>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>


export default {
  name: 'HierarchyChooser',
  props: {
  },
  data() {
    return {}
  },
  methods: {
  }
}
</script>

<style scoped lang="sass">
</style>
