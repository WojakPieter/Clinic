<template>
  <Header v-if="this.headerDisplay" />
  <v-idle
    v-if="
      this.$route.path != '/' &&
      this.$route.path != '/register_screen'
    "
    v-show="false"
    :duration="900"
    @idle="this.logout()"
  >
  </v-idle>
  <router-view></router-view>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>

<script>
import Header from './components/Header.vue';
import VIdle from "v-idle"

export default {
  data() {
    return {
      headerDisplay: false,
      user: {}
    }
  },
  components: {
    Header,
    VIdle
  },
  watch: {
      $route() {
        this.headerDisplay = window.localStorage.getItem("token")?.length > 0 && this.$route != "";
      },
  },  
}
</script>
