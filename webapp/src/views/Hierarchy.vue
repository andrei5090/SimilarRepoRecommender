<template>
  <div class="container">
    <vue-tree
        style="width: 800px; height: 600px; border: 1px solid gray;"
        :dataset="sampleData"
        :config="treeConfig"
    >
      <template v-slot:node="{ node, collapsed }">
        <span
            class="tree-node"
            :style="{ border: collapsed ? '2px solid grey' : '' }"
        >{{ node.value }}</span
        >
      </template>
    </vue-tree>
  </div>
</template>

<script>
export default {
  name: 'Hierarchy',
  data() {
    return {
      sampleData: {
        value: '1',
        children: [
          { value: 'Manele', children: [{ value: '4' }, { value: '5' }] },
          { value: '3' }
        ]
      },
      treeConfig: { nodeWidth: 120, nodeHeight: 80, levelHeight: 200 }
    }
  }
}
</script>

<style scoped lang="sass">
.container
  display: flex
  flex-direction: column
  align-items: center


.tree-node
  display: inline-block
  width: 28px
  height: 28px
  border-radius: 50%
  background-color: antiquewhite
  text-align: center
  line-height: 28px
</style>
