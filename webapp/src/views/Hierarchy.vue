<template>
  <div class="">
    <v-row justify="center" align-content="center">
      <v-col cols="12" align-self="center">
        <v-card shaped class="ma-10" elevation="10">
          <v-card-title>Hierarchy</v-card-title>

          <!--   File Selector     -->
          <v-menu-transition>
            <div v-if="choice === 0">
              <v-row align="center" justify="center">
                <!--                Import From Computer button    -->
                <v-col cols="5" class="text-center">
                  <v-btn x-large color="secondary lighten-2" class="text--white" width="25vw" height="25vh" rounded
                         elevation="10"
                         @click="choice = 1">
                    <div>
                      <v-row>
                        <v-col cols="12">
                          <span>Import Hierarchy From Your Computer </span>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12">
                          <v-icon size="70">mdi-graph</v-icon>
                        </v-col>
                      </v-row>
                    </div>
                  </v-btn>
                </v-col>

                <!--   Get From Backend -->
                <v-col cols="5" class="text-center">
                  <v-btn x-large color="secondary lighten-2" class="text--white" width="25vw" height="25vh" rounded
                         elevation="10"
                         @click="choice = 2">
                    <div>
                      <v-row>
                        <v-col cols="12">
                          <span>Generate Hierarchy</span>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12">
                          <v-icon size="70">mdi-server</v-icon>
                        </v-col>
                      </v-row>
                    </div>
                  </v-btn>
                </v-col>
              </v-row>
            </div>
            <div v-else-if="choice === 1">
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
            </div>
            <div v-else-if="choice === 2">
              <HierarchyChooser @compute-hierarchy="retrieveHierarchy"/>
            </div>
          </v-menu-transition>


          <v-card-actions class="justify-center" v-if="getCluster || getComputedHierarchy">
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
                <vue-tree v-if="getCluster || getComputedHierarchy"
                          class="tree justify-center"
                          :dataset="sampleData"
                          :config="treeConfig"
                          ref="tree"
                          :collapse-enabled="true"
                >

                  <template v-slot:node="{ node, collapsed }">
                    <div @click="showDialog(node.value)">
                      <v-card min-width="150px" max-width="250px" min-height="100px" max-height="250px" shaped
                              elevation="15" hover @click="displayContentList.push(node.value.content)"
                              :color="colours[node.value.id]">
                        <div :key="isHover">
                          <v-card-title class="justify-center"
                                        v-text="getLabels ? getLabels[node.value.uniqueId] ? getLabels[node.value.uniqueId].label != null ? getLabels[node.value.uniqueId].label : node.value.uniqueId : node.value.uniqueId : node.value.uniqueId">
                            {{ collapsed }}
                          </v-card-title>
                          <v-chip color="green lighten-4">
                            {{
                              getLabels ? getLabels[node.value.uniqueId] ? getLabels[node.value.uniqueId].weight != null ? getLabels[node.value.uniqueId].weight : 'N/A' : 'N/A' : 'N/A'
                            }}
                          </v-chip>
                        </div>
                      </v-card>


                    </div>

                  </template>

                </vue-tree>
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-actions class="pt-10 justify-center" v-if="getCluster || getComputedHierarchy">
            <v-row justify="center" align-content="center">

              <v-col cols="3" class="text-center">
                <v-btn class="text-center" color="secondary" @click="displayContentList = []" rounded x-large>
                  <v-icon left> mdi-reload</v-icon>
                  Reset
                </v-btn>
              </v-col>

              <v-col cols="3" class="text-center">
                <v-btn class="text-center" color="secondary" @click="saveLabels" rounded x-large>
                  <v-icon left> mdi-download</v-icon>
                  Get Labels
                </v-btn>
              </v-col>
            </v-row>

          </v-card-actions>

          <v-card-text class="pt-5">
            <ClusterRepresentation :padding="true" :clusters="displayContentList"
                                   :id="hoverData.id"></ClusterRepresentation>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="isHover">
      <ClusterEditor :clusters="hoverData.arr" :id="hoverData.id" :key="hoverData.id"></ClusterEditor>
    </v-dialog>
  </div>
</template>

<script>

//import data from '@/data/clusters.json'
import ClusterEditor from "../components/ClusterEditor";
import ClusterRepresentation from "../components/ClusterRepresentation";
import {mapActions, mapGetters} from "vuex";
import HierarchyChooser from "../components/HierarchyChooser";

export default {
  name: 'Hierarchy',
  components: {HierarchyChooser, ClusterRepresentation, ClusterEditor},
  data() {
    return {
      tree: null,
      labels: null,
      sampleData: null,
      treeConfig: {nodeWidth: 200, nodeHeight: 50, levelHeight: 150},
      colours: this.getColourPalette(),
      displayContentList: [],
      hoverData: {
        arr: [],
        id: null
      },
      isHover: false,
      choice: 0
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
      this.hoverData.arr = []
      this.hoverData.arr.push(content.content)
      this.hoverData.id = content.uniqueId
    },
    saveLabels() {
      this.downloadBlob(JSON.stringify(this.getLabels), "labels.json", "JSON")
    },
    downloadBlob(content, filename, contentType) {
      // Create a blob
      var blob = new Blob([content], {type: contentType});
      var url = URL.createObjectURL(blob);

      // Create a link to download it
      var pom = document.createElement('a');
      pom.href = url;
      pom.setAttribute('download', filename);
      pom.click();
    },
    ...mapActions(['storeCluster', 'storeLabels', 'retrieveHierarchy', 'resetHierarchy'])
  },
  computed: {
    ...mapGetters(['getCluster', 'getLabels', 'getComputedHierarchy'])
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

    },
    getComputedHierarchy(newValue) {
      if (newValue && newValue.error)
        return
      this.sampleData = newValue.payload
    }

  },
  mounted() {
    this.resetHierarchy()
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
