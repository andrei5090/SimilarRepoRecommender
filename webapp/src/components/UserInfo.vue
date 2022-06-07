<template>
  <div>
    <v-row>
      <v-card>
        <v-card-text>
          <v-card-title>
            Some Information About You
          </v-card-title>
          <v-card-subtitle>
            {{ extraInfo }}
          </v-card-subtitle>

          <v-form v-model="valid" lazy-validation>

            <v-text-field v-model="areaOfExpertise" rounded outlined label="Your area of expertise or job title"
                          prepend-inner-icon="mdi-badge-account-horizontal" counter="50/" required></v-text-field>

            <v-select v-model="education" label="Current stage of education"
                      :items="educationLvls" rounded outlined prepend-inner-icon="mdi-school"></v-select>


            <v-autocomplete
                auto-select-first
                clearable
                deletable-chips
                multiple
                v-model="experienceTopics"
                :items="getAvailableTags"
                outlined
                label="Technologies you have experience with  (please select at least 3)"
                rounded
                prepend-inner-icon="mdi-label"
                no-data-text="There is no match between your search and the available topics."
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

            <v-select v-model="experience" label="Your experience in Computer Science/Software Development"
                      :items="experienceLvls" rounded outlined prepend-inner-icon="mdi-laptop"></v-select>


            <v-select v-model="age" label="Your age"
                      :items="ageList" rounded outlined prepend-inner-icon="mdi-clock-outline"></v-select>


            <v-select v-model="gender" label="Your gender"
                      :items="genderList" rounded outlined></v-select>


            <v-card-actions class="justify-end">
              <v-btn rounded color="primary" large :disabled="!isValid" @click="continuePressed"> Continue
                <v-icon large right>mdi-chevron-right</v-icon>
              </v-btn>
            </v-card-actions>

          </v-form>
        </v-card-text>
      </v-card>
    </v-row>
  </div>
</template>

<script>


import {mapGetters} from "vuex";

export default {
  name: 'UserInfo',
  props: {},
  data() {
    return {
      valid: false,
      experienceTopics: null,
      experience: null,
      areaOfExpertise: null,
      age: null,
      gender: null,
      education: null,
      genderList: ['Male', 'Female', 'Other', 'Prefer not to say'],
      ageList: ['18-22', '23-25', '25-30', '30-35','35-40', '40-50','50-60','60-70','> 70', 'Prefer not to say'],
      extraInfo: 'Before starting the evaluation process we would like to find out more about you and your experience in Computer Science or Software Development.' +
          ' Please complete the fields below. This information will be stored anonymously, no data can be traced back to you.',
      experienceLvls: ['< 1 Year', '1-2 Years', '2-4 Years', '4-6 Years', '6-8 Years', '8-10 Years', '> 10 Years'],
      educationLvls: ['Bachelor\'s or equivalent', 'Master\'s or equivalent', 'Doctorate or equivalent', 'Postdoctorate or equivalent']
    }
  },
  computed: {
    ...mapGetters(['getComputedHierarchy', 'getAvailableTags']),
    isValid() {
      return this.experience && this.education && this.education.length > 0 && this.areaOfExpertise && this.areaOfExpertise.length > 0 && this.experienceTopics && this.experienceTopics.length > 0 && this.age && this.gender
    }
  },
  methods: {
    remove(item) {
      const index = this.experienceTopics.indexOf(item.item)
      if (index >= 0) this.experienceTopics.splice(index, 1)
    },
    continuePressed() {
      let userData = {}
      userData.experienceTopics = this.experienceTopics
      userData.education = this.education
      userData.experience = this.experience
      userData.areaOfExpertise = this.areaOfExpertise
      userData.age = this.age
      userData.gender = this.gender

      this.$emit('continue', userData)
    }
  },
  watch: {}
}
</script>

<style scoped lang="sass">
</style>
