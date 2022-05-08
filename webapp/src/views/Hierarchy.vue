<template>
  <div class="">
    <v-row justify="space-around" align-content="center">
      <v-col cols="12" align-self="center">
        <v-card shaped class="ma-10" elevation="10" min-height="1200px">
          <v-card-title>Hierarchy</v-card-title>
          <v-card-text style="min-height: inherit">
            <vue-tree
                class="tree"
                :dataset="sampleData"
                :config="treeConfig"
                :collapse-enabled="true"
            >
              <template v-slot:node="{ node, collapsed }">
        <span
            class="tree-node"
            :style="{ border: collapsed ? '2px solid grey' : '' }"
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
export default {
  name: 'Hierarchy',
  data() {
    return {
      sampleData: {
      },
      treeConfig: {nodeWidth: 120, nodeHeight: 80, levelHeight: 200}
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
