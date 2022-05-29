<template>
  <div>
    <v-row>
      <v-col cols="12">
        <SearchBar/>
      </v-col>
    </v-row>
  </div>
</template>

<script>


import SearchBar from "../components/SearchBar";

export default {
  name: 'Evaluation',
  components: {SearchBar},
  data() {
    return {}
  },
  methods: {},
  computed: {},
  watch: {}
}
</script>

<style scoped lang="sass">
</style>
