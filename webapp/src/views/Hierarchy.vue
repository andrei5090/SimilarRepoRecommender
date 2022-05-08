<template>
  <div class="">
    <v-row justify="center" align-content="center">
      <v-col cols="12" align-self="center">
        <v-card shaped class="ma-10" elevation="10" min-height="1200px">
          <v-card-title>Hierarchy</v-card-title>
          <v-card-actions class="justify-center">
            <v-btn rounded icon @click="$refs.tree.zoomOut()"> <v-icon>mdi-magnify-minus</v-icon></v-btn>
            <v-btn rounded icon @click="$refs.tree.zoomIn()"><v-icon>mdi-magnify-plus</v-icon></v-btn>
          </v-card-actions>
          <v-card-text style="min-height: inherit">
            <vue-tree
                class="tree"
                :dataset="sampleData"
                :config="treeConfig"
                :collapse-enabled="true"
                ref="tree"
            >
              <template v-slot:node="{ node, collapsed }">
        <span
            class="tree-node"
            :style="{ border: collapsed ? '5px solid grey' : '' }"
        >{{ node.value }}

        </span>
              </template>

            </vue-tree>
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
      treeConfig: {nodeWidth: 45, nodeHeight: 45, levelHeight: 50}
    }
  }
}
</script>

<style scoped lang="sass">
.tree
  min-height: inherit

.tree-node
  display: inline-block
  width: 30px
  height: 35px
  border-radius: 50%
  background-color: antiquewhite
  text-align: center
  line-height: 28px
</style>
