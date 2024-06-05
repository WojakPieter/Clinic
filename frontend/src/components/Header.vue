<template>
    <div class="header">
        <p>Witaj {{ this.user.login }}</p>
        <router-link to="/start_page"><button>Strona główna</button></router-link>
        <button @click="this.logOut()">Wyloguj się</button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            display: false,
            user: {},
        }
    },
    methods: {
        logOut() {
            window.localStorage.removeItem("token");
            this.isLoggedOut = true;
            this.$router.push("/");
        },
        isLoggedIn() {
            return window.localStorage.getItem("token");
        }
    },
    
    mounted() {
        setTimeout(() => {
            if (this.isLoggedIn())
                this.loadUser();
        }, 800)
    },
}
</script>

<style scoped>
.header {
    height: 60px;
    background-color: black;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}

p {
    color: white;
}

button {
    height: 40px;
}
</style>