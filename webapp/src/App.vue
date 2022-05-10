<template>
  <v-app>
    <v-app-bar flat app color="transparent" hide-on-scroll>
      <v-app-bar-nav-icon class="black--text" @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title class="text-uppercase black--text">
        <span class="font-weight-light">Hierarchy </span>
        <span>Visualisation</span>
      </v-toolbar-title>

      </v-app-bar>

    <v-navigation-drawer app v-model="drawer" expand-on-hover mini-variant
                         class="indigo lighten-1">
      <!--    Left Routes   -->
      <v-list class="pt-15">
        <template v-for="link in links">
          <v-list-item :to="link.route" :exact="true" :key="link.id" rel="canonical">
            <v-list-item-action>
              <v-icon class="white--text">{{ link.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title class="white--text">{{ link.text }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list>

      <v-spacer></v-spacer>
    </v-navigation-drawer>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data () {
    return {
      drawer: true,
      links: [
        {
          id: 'HOME',
          icon: 'mdi-home',
          text: 'Home',
          route: '/',

        },
        {
          id: 'LEGISLATION',
          icon: 'mdi-graph',
          text: 'Hierarchy',
          route: '/hierarchy',
        }
      ],
    }
  }
};
</script>
