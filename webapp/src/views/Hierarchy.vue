<template>
  <div class="">
    <v-row justify="center" align-content="center">
      <v-col cols="12" align-self="center">
        <v-card shaped class="ma-10" elevation="10">
          <v-card-title>Hierarchy</v-card-title>

          <!--   File Selector     -->
          <v-row justify="space-around" class="ma-5">
            <v-col cols="6">
              <v-card elevation="10" shaped>
                <v-row justify="center">
                  <v-col cols="5">
                    <v-file-input
                        v-model="tree"
                        label="Input tree"
                        truncate-length="5"
                        prepend-icon="mdi-graph"
                    ></v-file-input>
                  </v-col>


                  <v-col cols="5">
                    <v-file-input
                        v-model="labels"
                        label="Input labels"
                        truncate-length="5"
                        prepend-icon="mdi-label"
                    ></v-file-input>
                  </v-col>
                </v-row>
              </v-card>
            </v-col>
          </v-row>


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
                <vue-tree v-if="getCluster"
                          class="tree justify-center"
                          :dataset="sampleData"
                          :config="treeConfig"
                          ref="tree"
                          :collapse-enabled="true"
                >

                  <template v-slot:node="{ node, collapsed }">


                    <div @click="showDialog(node.value.content)">
                      <v-card min-width="100px" max-width="250px" min-height="100px" max-height="250px" shaped
                              elevation="15" hover @click="displayContentList.push(node.value.content)"
                              :color="colours[node.value.id]">
                        <v-card-title class="justify-center">
                          {{ getLabels[node.value.uniqueId] ? getLabels[node.value.uniqueId] : node.value.uniqueId }}
                          {{ collapsed }}
                        </v-card-title>
                      </v-card>

                    </div>

                  </template>

                </vue-tree>
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-actions class="pt-5">
            <v-row justify="center" align-content="center">

              <v-col cols="3" class="text-center">
                <v-btn class="text-center" color="red lighten-2" @click="displayContentList = []">RESET</v-btn>
              </v-col>

              <v-col cols="3" class="text-center">
                <v-btn class="text-center" color="red lighten-2">SAVE</v-btn>
              </v-col>
            </v-row>

          </v-card-actions>

          <v-card-text class="pt-5">
            <ClusterRepresentation :padding="true" :clusters="displayContentList"></ClusterRepresentation>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="isHover">
      <ClusterEditor :clusters="hoverData"></ClusterEditor>
    </v-dialog>
  </div>
</template>

<script>

//import data from '@/data/clusters.json'
import ClusterEditor from "../components/ClusterEditor";
import ClusterRepresentation from "../components/ClusterRepresentation";
import {mapActions, mapGetters} from "vuex";

export default {
  name: 'Hierarchy',
  components: {ClusterRepresentation, ClusterEditor},
  data() {
    return {
      tree: null,
      labels: null,
      sampleData: null,
      treeConfig: {nodeWidth: 95, nodeHeight: 50, levelHeight: 150},
      colours: this.getColourPalette(),
      displayContentList: [],
      hoverData: [],
      isHover: false
    }
  },
  methods: {
    getRandomColor() {
      return '#' + (Math.random() * 0xFFFFFF << 0).toString(16)
    },
    getColourPalette() {
      let dict = {}

      dict['root'] = this.getRandomColor()

      for (let i = 0; i < 501; i++)
        dict['lvl ' + i] = this.getRandomColor()

      return dict
    },
    showDialog(content) {
      this.isHover = true
      this.hoverData = []
      this.hoverData.push(content)
    },
    ...mapActions(['storeCluster', 'storeLabels'])
  },
  computed: {
    ...mapGetters(['getCluster', 'getLabels'])
  },
  created() {
    // this.storeCluster(data)
    // this.sampleData = this.getCluster
  },
  watch: {
    tree(newValue) {
      var reader = new FileReader();
      reader.readAsText(newValue);

      reader.onload = () => {
        this.storeCluster(JSON.parse(reader.result))
        this.sampleData = this.getCluster
      }
    },
    labels(newValue) {
      var reader = new FileReader();
      reader.readAsText(newValue);

      reader.onload = () => {
        this.storeLabels(JSON.parse(reader.result))
        this.sampleData = this.getCluster
      }

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
