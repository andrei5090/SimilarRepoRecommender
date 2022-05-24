<template>
  <v-container>
    <v-card rounded elevation="10">
      <v-card-text>

        <v-row justify="space-around" align="center">
          <v-col cols="8" class="text-center">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
            <v-text-field label="Search" prepend-icon="mdi-magnify" outlined v-bind="attrs"
                          v-on="on"></v-text-field>
              </template>
              Your Search Query
            </v-tooltip>
          </v-col>
          <v-col cols="4" class="text-center">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
            <v-autocomplete
                auto-select-first
                clearable
                deletable-chips
                multiple
                v-model="chosenTags"
                :items="items"
                outlined
                label="Input Tags"
                v-bind="attrs"
                v-on="on"
            >

              <template v-slot:selection="data">
                <v-chip color="tag" close
                        @click:close="remove(data)">
                  {{ data.item }}
                </v-chip>
              </template>



              <template v-slot:item="data">
                <template v-if="typeof data.item !== 'object'">
                  <v-chip color="tag">
                    {{ data.item }}
                  </v-chip>
                </template>
              </template>
            </v-autocomplete>

              </template>
              The tags/topics you are interested with
            </v-tooltip>

          </v-col>


          <v-col cols="4"></v-col>
        </v-row>
      </v-card-text>

    </v-card>

  </v-container>
</template>

<script>
export default {
  name: 'SearchBar',
  props: {
    items: {
      default: null,
      required: true
    }
  },
  data() {
    return {
      chosenTags: null
    }
  },
  methods: {
    remove (item) {
      const index = this.chosenTags.indexOf(item.item)
      if (index >= 0) this.chosenTags.splice(index, 1)
    }
  }

}
</script>

<style lang="sass" scoped>
.card
  cursor: crosshair
</style>
