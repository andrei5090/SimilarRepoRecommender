<template>
  <div>
    <!--   Start Button   -->
    <div v-if="!started" class="center-align">
      <v-row align="center" justify="center">
        <v-col cols="12" md="10" class="text-center">
          <v-card>
            <v-card-title>Your task</v-card-title>
            <v-card-text>{{ task }}</v-card-text>
            <v-card-actions class="justify-center">
              <v-btn @click="started = true" color="primary" x-large>
                Start
                <v-icon right>mdi-arrow-right-bold-circle</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

    </div>
    <div v-else>
      <div v-if="progressIndex < scenarios.length">
        <div v-if="userDataCollect" class="center-align">
          <v-row justify="center" align="center">
            <v-col cols="11">
              <UserInfo @continue="saveUserData"/>
            </v-col>
          </v-row>
        </div>
        <div v-else>
          <!-- Scenario -->
          <v-row justify="center">
            <v-col cols="11" md="6">
              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                  <v-progress-linear
                      color="light-blue darken-3"
                      striped
                      height="10"
                      :value="(progressIndex + 1) * 100 / scenarios.length"
                      v-bind="attrs"
                      v-on="on"
                  >
                  </v-progress-linear>
                </template>
                <span>Your progress</span>
              </v-tooltip>
              <v-card rounded>
                <v-card-title>
                  <v-row>
                    <v-col cols="11"> Your current search scenario</v-col>
                    <v-col cols="1">
                      <v-btn icon x-large @click="helpDialog = true">
                        <v-icon class="justify-end text-right" color="primary" large> mdi-account-question</v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-card-title>
                <v-card-text>{{ scenario }}</v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-fab-transition>
            <v-row v-show="!searchCompleted">
              <v-col cols="12">
                <SearchBar :evaluation-mode="true" :loading="loading" @search="search" ref="searchBar"/>
              </v-col>
            </v-row>
          </v-fab-transition>
          <v-fab-transition>
            <v-row justify="center" align="center" v-show="searchCompleted">
              <v-col cols="12" class="text-center">
                <v-btn rounded color="primary" @click="searchCompleted = false; evalStatus=false; resetSearch()">
                  Search Again
                  <v-icon right>mdi-magnify</v-icon>
                </v-btn>
              </v-col>


              <v-col cols="11" md="6" class="text-center">
                <v-card shaped elevation="5">
                  <div v-if="evalStatus">
                    <v-card-text class="text-center success--text font-weight-bold text-h6">
                      Please check the results that you find more relevant in all the Search Results below given the
                      current
                      scenario.
                    </v-card-text>
                    <v-card-text class="text-center font-weight-bold">
                      When you are done, press the submit button.
                    </v-card-text>

                    <v-card-actions class="text-center justify-center">
                      <v-btn x-large rounded color="primary" @click="sendData" :loading="submitLoading">
                        Submit
                      </v-btn>
                    </v-card-actions>


                  </div>
                  <div v-else>
                    <v-card-text class="text-center success--text font-weight-bold text-h6">
                      Please analyze all the results and when you are finished, press the Start Evaluation button.
                    </v-card-text>

                    <v-card-actions class="text-center justify-center">
                      <v-btn x-large rounded color="primary" @click="evalStatus = true">Start Evaluation
                        <v-icon right>mdi-podium</v-icon>
                      </v-btn>
                    </v-card-actions>
                  </div>
                </v-card>
              </v-col>
            </v-row>

          </v-fab-transition>


          <v-row justify="space-around" v-if="searchCompleted">
            <v-col cols="11" md="4" class="">
              <SearchResult :evaluation-mode="evalStatus" :search-data="searchData" v-if="searchData"
                            :loading="githubLoading"
                            search-title="Search Results 1"/>
            </v-col>

            <v-col cols="11" md="4" class="">
              <SearchResult :evaluation-mode="evalStatus" :search-data="githubSearchData" v-if="githubSearchData"
                            :loading="githubClassicLoading"
                            search-title="Search Results 2"/>
            </v-col>

            <v-col cols="11" md="4" class="">
              <SearchResult :evaluation-mode="evalStatus" :search-data="googleSearchData" v-if="googleSearchData"
                            :loading="googleClassicLoading"
                            search-title="Search Results 3"/>
            </v-col>

          </v-row>
        </div>
      </div>
      <div v-else>
        <v-card class="center-align">
          <v-card-title class="text-center justify-center">
            Thank you for your answers!
          </v-card-title>

          <v-card-text class="text-center justify-center">
            <v-icon color="primary" size="100">mdi-emoticon-happy-outline</v-icon>
          </v-card-text>

          <v-card-text class="text-h5"> All of your results have been recorded.</v-card-text>

          <v-card-actions class="justify-center text-center">
            <v-btn to="/" rounded large color="primary">
              <v-icon left size="28">mdi-home</v-icon>
              HOME
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </div>


    <v-row justify="center">
      <v-col cols="10" md="6">
        <v-dialog v-model="helpDialog" max-width="750px">
          <v-card shaped>
            <v-card-title>Your Task</v-card-title>
            <v-card-text>{{ task }}</v-card-text>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>

  </div>
</template>

<script>


import SearchBar from "../components/SearchBar";
import SearchResult from "../components/SearchResult";
import {mapActions, mapGetters} from "vuex";
import UserInfo from "../components/UserInfo";

const uuid = require("uuid");

export default {
  name: 'Evaluation',
  components: {UserInfo, SearchResult, SearchBar},
  data() {
    return {
      loading: false,
      started: false,
      submitLoading: false,
      userDataCollect: true,
      searchCompleted: false,
      githubLoading: false,
      githubClassicLoading: false,
      googleClassicLoading: false,
      helpDialog: false,
      userId: null,
      progressIndex: 0,
      scenarios: [
        'A car competition organizer wants to promote their business. They want to build a website about their available competitions. The website is just an informational one; the users will not be able to reserve/buy any tickets for the competitions. The website will follow a parallax scrolling style (1-page website) with information about the competitions, such as location and entry fee. The information on the website needs to be updated just once every few years when the organizers adjust the prices with the inflation. Please provide a query that may lead to an already built solution for this type of application or a stack of technologies that may help solve this task. Please focus more on the tags than on the textual search. Please keep in mind that the order of the tags is changing and provides you with recommendations when you input at least one tag.',
        'A small chair manufacturing business wants to minimize its "bookkeeping" costs. Every month, all the bills regarding materials or energy are centralized in their bookkeeping system by the business owner. The business owner thinks that he has more important things to do but doesn\'t afford to hire another person to centralize the bills. All the bills are received at the address: accounting@nicechairs.com. The business owner wants to automate this bookkeeping process. Please provide a query that may lead to an already built solution for this type of application or a stack of technologies that may help solve this task. Please focus more on the tags than on the textual search. Please keep in mind that the order of the tags is changing and provides you with recommendations when you input at least one tag.',
        'An NGO from Guatemala wants to promote their country worldwide. They plan to build a mobile application that allows users to plan their journey in Guatemala. The application should allow the users to choose their interest points and plan a trip, including transport, tickets, and accommodation. The app aims to plan the trip so that it optimizes the route to the touristic objectives and optimizes the waiting time at the interest points (e.g. a museum). Please provide a query that may lead to an already built solution for this type of application or a stack of technologies that may help solve this task. Please focus more on the tags than on the textual search. Please keep in mind that the order of the tags is changing and provides you with recommendations when you input at least one tag.',
        'Jerry just won the lottery and decided to open a bar in his hometown. \n' +
        'Last year, he went on a trip to the USA and saw live augmented reality Pool tables that can track your actions and recommend the best shots projecting a live animation on the table. Even though Jerry won the big jackpot, he doesn\'t want to invest much money in such a table; the starting price on the market is 15000 euros. He already bought the Pool table but needs somebody to build this augmentation system. Please provide a query that may lead to an already built solution for this type of application or a stack of technologies that may help solve this task. Please focus more on the tags than on the textual search. Please keep in mind that the order of the tags is changing and provides you with recommendations when you input at least one tag.',
        'The mighty food vlogger "ImiPlaceSaMananc" travels worldwide to find the best shawarma on the planet. He keeps a digital journal about the characteristics of each shawarma he tasted, the ingredients, and the restaurant\'s location that prepared the food. At the end of each tasting, he writes down the "food grade" (e.g. Above Average, Average...etc.). He wants to share his Shawarma tasting skills with the world. This is why he wants to build a recommender system that recommends the best shawarma in the user\'s area (based on his journal). Please provide a query that may lead to an already built solution for this type of application or a stack of technologies that may help solve this task. Please focus more on the tags than on the textual search. Please keep in mind that the order of the tags is changing and provides you with recommendations when you input at least one tag.',
        'The Eindhoven airport wants to create an embedded system that is able to track the RIFD chip in your passport at the self-check-in gate, so you don\'t have to take it out on your passport and scan it. They want each self-check-in gate to work independently. When you come close to the gate, it will automatically recognize your passport and start scanning your biometrics (the system will provide a video stream of the user\'s face or fingerprints). The biometric validation is not a concern at the moment since another service provider will handle this. Please provide a query that may lead to an already built solution for this type of application or a stack of technologies that may help solve this task. Please focus more on the tags than on the textual search. Please keep in mind that the order of the tags is changing and provides you with recommendations when you input at least one tag.',
        'The TU Delft Discord server admin wants to automate the filtering system. He wants to filter all the messages that contain swear words or graphic pictures that violate the TU Delft standards. This is why he wants to create a filtering system that can emit "warnings" or server "bans" according to specific criteria. The filter will act as a discord bot that scans all the messages and take action when required. Please provide a query that may lead to an already built solution for this type of application or a stack of technologies that may help solve this task. Please focus more on the tags than on the textual search. Please keep in mind that the order of the tags is changing and provides you with recommendations when you input at least one tag.',
        'A big tech company wants to provide bikes to their visitors and employees. Each bike has a card scanner attached to it. A visitor or employee card needs to be scanned to unlock a bike. The bikes can be unlocked with a card, but the administrators have no information on how many bikes are used at certain timestamps or the location of each bike. This is why they need a system to centralize the data of each bike and display information such as free bike locations in a GUI. They have no preference for how the system is implemented. Please provide a query that may lead to an already built solution for this type of application or a stack of technologies that may help solve this task. Please focus more on the tags than on the textual search. Please keep in mind that the order of the tags is changing and provides you with recommendations when you input at least one tag.',
        'WorkAholic INC. wants to implement a task prioritization system in their workflow. At the moment, the task difficulty and time needed to finish the Team Managers establish it. The CTO observed that the managers sometimes give shorter task times to please their superiors. This is why the WorkAholic INC. wants to implement an automated task "assessor" that suggests the work time needed for a task to be solved and the assignment\'s difficulty. Please provide a query that may lead to an already built solution for this type of application or a stack of technologies that may help solve this task. Please focus more on the tags than on the textual search. Please keep in mind that the order of the tags is changing and provides you with recommendations when you input at least one tag.',
      ],
      evalStatus: false,
      task: 'To evaluate how good a recommender repository system is, we decided to assess the relevance of the recommendations in a scenario-based system. First, we will require some information about you, such as your experience in Computer Science. Afterwards, you will be given several "Software Scenarios" for which you have to create a search query using textual information and Github Tags. Each query will be used in three different recommender systems, two using the Github search engine and one using the Google search engine. After you analyze the results, you have to press the "Start Evaluation" button and tick the most relevant results from all three "Search Results" (you can tick 0 or more options for each approach. If you think that one method isn\'t giving good results, you can tick 0 options).'
    }
  },
  methods: {
    ...mapActions(['searchTextAndTags', 'resetSearch', 'sendFeedback', 'searchTextGithub', 'searchRepositoryDataFromGoogle', 'retrieveAvailableTags', 'addUserFeedbackData']),
    search(searchQuery) {
      this.githubLoading = true
      this.githubClassicLoading = true
      this.googleClassicLoading = true
      this.loading = true
      this.searchTextAndTags(searchQuery)
      this.searchTextGithub(searchQuery)
      this.searchRepositoryDataFromGoogle(searchQuery)
    },
    saveUserData(data) {
      this.userDataCollect = false
      this.addUserFeedbackData(data)
    },
    sendData() {
      this.submitLoading = true
      let ownLinks = this.searchData.map(el => el.html_url)
      let ownChecked = this.searchData.filter(el => el.checked).map(el => el.html_url)

      let simpleGithubLinks = this.githubSearchData.map(el => el.html_url)
      let simpleGithubChecked = this.githubSearchData.filter(el => el.checked).map(el => el.html_url)

      let simpleGoogleLinks = this.googleSearchData.map(el => el.html_url)
      let simpleGoogleChecked = this.googleSearchData.filter(el => el.checked).map(el => el.html_url)

      this.sendFeedback({
        githubLinks: {
          github: {
            links: simpleGithubLinks
          },
          google: {
            links: simpleGoogleLinks
          }
        },
        ownLinks: {links: ownLinks},
        githubPreferences: {
          github: {
            checked: simpleGithubChecked
          },
          google: {
            checked: simpleGoogleChecked
          }
        },
        ownPreferences: {checked: ownChecked},
        extraInfo: {
          scenarioId: this.progressIndex,
          userInfo: this.getUserFeedbackData,
          userId: this.userId,
          queryData: this.$refs.searchBar.getQuery()
        }
      })
    }
  },
  computed: {
    ...mapGetters(['getSearchData', 'getFeedbackStatus', 'getGithubSearchData', 'getGoogleSearchData', 'getUserFeedbackData']),
    scenario() {
      return this.scenarios[this.progressIndex]
    },
    searchData() {
      try {
        return this.getSearchData ? this.getSearchData.data.items ? this.getSearchData.data.items.slice(0, 30) : [] : []
      } catch (e) {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        this.loading = false
        return []
      }
    },
    githubSearchData() {
      try {
        return this.getGithubSearchData ? this.getGithubSearchData.data.items ? this.getGithubSearchData.data.items.slice(0, 30) : [] : []
      } catch (e) {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        this.loading = false
        return []
      }
    },
    googleSearchData() {
      try {
        return this.getGoogleSearchData ? this.getGoogleSearchData.data.items ? this.getGoogleSearchData.data.items.slice(0, 30) : [] : []
      } catch (e) {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        this.loading = false
        return []
      }
    }
  },
  mounted() {
    this.userId = uuid.v4()
    this.resetSearch()
    this.evalStatus = false
    this.searchCompleted = false
    this.retrieveAvailableTags()
    this.$refs.searchBar.reset()
  },
  watch: {
    getSearchData(newValue) {
      if (newValue != null) {
        this.searchCompleted = true

        if (newValue.error) {
          this.searchCompleted = false
          this.evalStatus = false
        }

      }
      this.githubLoading = false
      this.loading = false
    },
    getGoogleSearchData() {
      this.googleClassicLoading = false

    },
    getGithubSearchData() {
      this.githubClassicLoading = false
    },
    getFeedbackStatus(newValue) {
      if (newValue.error)
        this.$toast.error(newValue.message, newValue.title, {position: "topCenter"});
      else {
        this.$toast.success(newValue.message, newValue.title, {position: "topCenter"});
        this.resetSearch()
        this.$refs.searchBar.reset()
        this.progressIndex++
        this.evalStatus = false
        this.searchCompleted = false
      }

      this.submitLoading = false
    }
  }
}
</script>

<style scoped lang="sass">

.center-align
  position: fixed
  top: 50%
  left: 50%
  transform: translate(-50%, -50%)

</style>
