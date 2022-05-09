<template>
  <div class="">
    <v-row justify="center" align-content="center">
      <v-col cols="12" align-self="center">
        <v-card shaped class="ma-10" elevation="10">
          <v-card-title>Hierarchy</v-card-title>

          <v-card-actions class="justify-center">
            <v-btn rounded icon @click="$refs.tree.zoomOut()">
              <v-icon>mdi-magnify-minus</v-icon>
            </v-btn>
            <v-btn rounded icon @click="$refs.tree.zoomIn()">
              <v-icon>mdi-magnify-plus</v-icon>
            </v-btn>
          </v-card-actions>

          <v-card-text class="justify-center text-center">
            <v-row justify="center">
              <v-col cols="12">
                <vue-tree
                    class="tree justify-center"
                    :dataset="sampleData"
                    :config="treeConfig"
                    ref="tree"
                    :collapse-enabled="true"
                >
                  <template v-slot:node="{ node, collapsed }" @click="collapsed = true" v-show="collapsed">
                    <v-card min-width="100px" max-width="250px" min-height="100px" max-height="250px" shaped
                            elevation="15" hover v-if="!collapsed" @click="collapsed = true" :color="colours[node.value.substr(0, 5)]">
                      <v-card-title class="justify-center">{{ node.value }}</v-card-title>
                    </v-card>
                  </template>
                </vue-tree>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>

import data from '@/data/clusters.json'

export default {
  name: 'Hierarchy',
  data() {
    return {
      sampleData: data,
      treeConfig: {nodeWidth: 95, nodeHeight: 50, levelHeight: 150},
      colours: this.getColourPalette()
    }
  },
  methods: {
    getRandomColor() {
      return '#' + (Math.random() * 0xFFFFFF << 0).toString(16)
    },
    getColourPalette() {
      let dict = {}

      dict['root'] = this.getRandomColor()

      for (let i = 0; i < 50; i++)
        dict['lvl ' + i] = this.getRandomColor()

      return dict
    }
  }
}
</script>

<style scoped lang="sass">
.tree
  width: available
  height: 750px
  justify-items: center

.container
  display: flex
  flex-direction: column
  align-items: center

.tree-node
  display: inline-block
  width: 30px
  height: 35px
  border-radius: 50%
  background-color: antiquewhite
  text-align: center
  line-height: 28px
</style>
