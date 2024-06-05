<template>
  <Header v-if="this.headerDisplay" />
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

export default {
  data() {
    return {
      headerDisplay: false,
      user: {}
    }
  },
  components: {
    Header
  },
  watch: {
      $route() {
          this.headerDisplay = window.localStorage.getItem("token")?.length > 0;
          if (this.headerDisplay)
            this.loadUser();
      },
  },  
}
</script>
